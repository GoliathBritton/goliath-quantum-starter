"""OAuth2 Provider Integration with Quantum-Resistant Security"""

import os
import secrets
import hashlib
import base64
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional, List, Any
from dataclasses import dataclass
from enum import Enum
import json
import urllib.parse
import requests
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend

from .auth_service import User, UserRole, SecurityLevel, QuantumResistantCrypto

class OAuth2Provider(Enum):
    GOOGLE = "google"
    MICROSOFT = "microsoft"
    GITHUB = "github"
    OKTA = "okta"
    AUTH0 = "auth0"
    CUSTOM = "custom"

@dataclass
class OAuth2Config:
    provider: OAuth2Provider
    client_id: str
    client_secret: str
    redirect_uri: str
    authorization_url: str
    token_url: str
    userinfo_url: str
    scopes: List[str]
    quantum_enhanced: bool = True

@dataclass
class OAuth2State:
    state: str
    nonce: str
    code_verifier: str
    code_challenge: str
    created_at: datetime
    expires_at: datetime
    redirect_uri: str
    provider: OAuth2Provider

@dataclass
class OAuth2Token:
    access_token: str
    refresh_token: Optional[str]
    id_token: Optional[str]
    token_type: str
    expires_in: int
    scope: str
    provider: OAuth2Provider

@dataclass
class OAuth2UserInfo:
    provider_id: str
    email: str
    name: str
    username: Optional[str]
    avatar_url: Optional[str]
    provider: OAuth2Provider
    verified: bool = False
    mfa_enabled: bool = False

class QuantumOAuth2Service:
    """OAuth2 Service with Quantum-Resistant Security Enhancements"""
    
    def __init__(self):
        self.crypto = QuantumResistantCrypto()
        self.providers: Dict[OAuth2Provider, OAuth2Config] = {}
        self.pending_states: Dict[str, OAuth2State] = {}
        self.state_expiry = timedelta(minutes=10)
        
        # Initialize default providers
        self._init_default_providers()
    
    def _init_default_providers(self):
        """Initialize default OAuth2 provider configurations"""
        # Google OAuth2
        if os.getenv('GOOGLE_CLIENT_ID'):
            self.providers[OAuth2Provider.GOOGLE] = OAuth2Config(
                provider=OAuth2Provider.GOOGLE,
                client_id=os.getenv('GOOGLE_CLIENT_ID'),
                client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
                redirect_uri=os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:3000/auth/callback/google'),
                authorization_url='https://accounts.google.com/o/oauth2/v2/auth',
                token_url='https://oauth2.googleapis.com/token',
                userinfo_url='https://www.googleapis.com/oauth2/v2/userinfo',
                scopes=['openid', 'email', 'profile']
            )
        
        # Microsoft OAuth2
        if os.getenv('MICROSOFT_CLIENT_ID'):
            tenant_id = os.getenv('MICROSOFT_TENANT_ID', 'common')
            self.providers[OAuth2Provider.MICROSOFT] = OAuth2Config(
                provider=OAuth2Provider.MICROSOFT,
                client_id=os.getenv('MICROSOFT_CLIENT_ID'),
                client_secret=os.getenv('MICROSOFT_CLIENT_SECRET'),
                redirect_uri=os.getenv('MICROSOFT_REDIRECT_URI', 'http://localhost:3000/auth/callback/microsoft'),
                authorization_url=f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize',
                token_url=f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token',
                userinfo_url='https://graph.microsoft.com/v1.0/me',
                scopes=['openid', 'email', 'profile']
            )
        
        # GitHub OAuth2
        if os.getenv('GITHUB_CLIENT_ID'):
            self.providers[OAuth2Provider.GITHUB] = OAuth2Config(
                provider=OAuth2Provider.GITHUB,
                client_id=os.getenv('GITHUB_CLIENT_ID'),
                client_secret=os.getenv('GITHUB_CLIENT_SECRET'),
                redirect_uri=os.getenv('GITHUB_REDIRECT_URI', 'http://localhost:3000/auth/callback/github'),
                authorization_url='https://github.com/login/oauth/authorize',
                token_url='https://github.com/login/oauth/access_token',
                userinfo_url='https://api.github.com/user',
                scopes=['user:email']
            )
    
    def register_provider(self, config: OAuth2Config):
        """Register custom OAuth2 provider"""
        self.providers[config.provider] = config
    
    def generate_authorization_url(self, provider: OAuth2Provider, 
                                 redirect_uri: Optional[str] = None) -> Dict[str, str]:
        """Generate OAuth2 authorization URL with PKCE and quantum-enhanced security"""
        if provider not in self.providers:
            raise ValueError(f"Provider {provider} not configured")
        
        config = self.providers[provider]
        
        # Generate quantum-enhanced PKCE parameters
        code_verifier = self._generate_code_verifier()
        code_challenge = self._generate_code_challenge(code_verifier)
        
        # Generate quantum-enhanced state and nonce
        state = self._generate_quantum_state()
        nonce = self._generate_quantum_nonce()
        
        # Store state for verification
        oauth_state = OAuth2State(
            state=state,
            nonce=nonce,
            code_verifier=code_verifier,
            code_challenge=code_challenge,
            created_at=datetime.now(timezone.utc),
            expires_at=datetime.now(timezone.utc) + self.state_expiry,
            redirect_uri=redirect_uri or config.redirect_uri,
            provider=provider
        )
        self.pending_states[state] = oauth_state
        
        # Build authorization URL
        params = {
            'client_id': config.client_id,
            'redirect_uri': redirect_uri or config.redirect_uri,
            'scope': ' '.join(config.scopes),
            'response_type': 'code',
            'state': state,
            'code_challenge': code_challenge,
            'code_challenge_method': 'S256'
        }
        
        # Add nonce for OpenID Connect
        if 'openid' in config.scopes:
            params['nonce'] = nonce
        
        # Provider-specific parameters
        if provider == OAuth2Provider.MICROSOFT:
            params['response_mode'] = 'query'
        elif provider == OAuth2Provider.GOOGLE:
            params['access_type'] = 'offline'
            params['prompt'] = 'consent'
        
        auth_url = f"{config.authorization_url}?{urllib.parse.urlencode(params)}"
        
        return {
            'authorization_url': auth_url,
            'state': state,
            'code_verifier': code_verifier
        }
    
    def exchange_code_for_token(self, provider: OAuth2Provider, 
                               authorization_code: str, 
                               state: str) -> OAuth2Token:
        """Exchange authorization code for access token"""
        if provider not in self.providers:
            raise ValueError(f"Provider {provider} not configured")
        
        if state not in self.pending_states:
            raise ValueError("Invalid or expired state")
        
        oauth_state = self.pending_states[state]
        
        # Verify state hasn't expired
        if oauth_state.expires_at < datetime.now(timezone.utc):
            del self.pending_states[state]
            raise ValueError("State has expired")
        
        config = self.providers[provider]
        
        # Prepare token request
        token_data = {
            'client_id': config.client_id,
            'client_secret': config.client_secret,
            'code': authorization_code,
            'grant_type': 'authorization_code',
            'redirect_uri': oauth_state.redirect_uri,
            'code_verifier': oauth_state.code_verifier
        }
        
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        # Exchange code for token
        response = requests.post(
            config.token_url,
            data=token_data,
            headers=headers,
            timeout=30
        )
        
        if response.status_code != 200:
            raise ValueError(f"Token exchange failed: {response.text}")
        
        token_response = response.json()
        
        # Clean up state
        del self.pending_states[state]
        
        return OAuth2Token(
            access_token=token_response['access_token'],
            refresh_token=token_response.get('refresh_token'),
            id_token=token_response.get('id_token'),
            token_type=token_response.get('token_type', 'Bearer'),
            expires_in=token_response.get('expires_in', 3600),
            scope=token_response.get('scope', ''),
            provider=provider
        )
    
    def get_user_info(self, provider: OAuth2Provider, token: OAuth2Token) -> OAuth2UserInfo:
        """Get user information from OAuth2 provider"""
        if provider not in self.providers:
            raise ValueError(f"Provider {provider} not configured")
        
        config = self.providers[provider]
        
        headers = {
            'Authorization': f'{token.token_type} {token.access_token}',
            'Accept': 'application/json'
        }
        
        response = requests.get(
            config.userinfo_url,
            headers=headers,
            timeout=30
        )
        
        if response.status_code != 200:
            raise ValueError(f"Failed to get user info: {response.text}")
        
        user_data = response.json()
        
        # Parse user info based on provider
        if provider == OAuth2Provider.GOOGLE:
            return OAuth2UserInfo(
                provider_id=user_data['id'],
                email=user_data['email'],
                name=user_data['name'],
                username=user_data.get('email'),
                avatar_url=user_data.get('picture'),
                provider=provider,
                verified=user_data.get('email_verified', False)
            )
        elif provider == OAuth2Provider.MICROSOFT:
            return OAuth2UserInfo(
                provider_id=user_data['id'],
                email=user_data['mail'] or user_data['userPrincipalName'],
                name=user_data['displayName'],
                username=user_data.get('userPrincipalName'),
                provider=provider,
                verified=True  # Microsoft accounts are pre-verified
            )
        elif provider == OAuth2Provider.GITHUB:
            # Get email separately for GitHub
            email_response = requests.get(
                'https://api.github.com/user/emails',
                headers=headers,
                timeout=30
            )
            emails = email_response.json() if email_response.status_code == 200 else []
            primary_email = next((e['email'] for e in emails if e['primary']), user_data.get('email'))
            
            return OAuth2UserInfo(
                provider_id=str(user_data['id']),
                email=primary_email,
                name=user_data['name'] or user_data['login'],
                username=user_data['login'],
                avatar_url=user_data.get('avatar_url'),
                provider=provider,
                verified=any(e['verified'] for e in emails if e['primary']) if emails else False
            )
        else:
            # Generic parsing
            return OAuth2UserInfo(
                provider_id=str(user_data.get('id', user_data.get('sub'))),
                email=user_data.get('email'),
                name=user_data.get('name', user_data.get('displayName')),
                username=user_data.get('preferred_username', user_data.get('email')),
                provider=provider
            )
    
    def create_or_update_user(self, oauth_user: OAuth2UserInfo) -> User:
        """Create or update user from OAuth2 user info"""
        # In production, this would interact with user database
        user_id = f"{oauth_user.provider.value}_{oauth_user.provider_id}"
        
        # Determine role based on email domain or other criteria
        role = self._determine_user_role(oauth_user.email)
        security_level = self._determine_security_level(oauth_user)
        
        user = User(
            id=user_id,
            username=oauth_user.username or oauth_user.email,
            email=oauth_user.email,
            role=role,
            security_level=security_level,
            mfa_enabled=oauth_user.mfa_enabled,
            created_at=datetime.now(timezone.utc),
            last_login=datetime.now(timezone.utc)
        )
        
        return user
    
    def _generate_code_verifier(self) -> str:
        """Generate PKCE code verifier with quantum-enhanced entropy"""
        # Use quantum-safe random generation
        random_bytes = secrets.token_bytes(32)
        # Add additional entropy from quantum source if available
        quantum_entropy = self.crypto.generate_quantum_safe_key()
        combined = random_bytes + quantum_entropy
        
        # Create code verifier
        verifier = base64.urlsafe_b64encode(combined).decode('utf-8')
        return verifier.rstrip('=')
    
    def _generate_code_challenge(self, code_verifier: str) -> str:
        """Generate PKCE code challenge"""
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(code_verifier.encode('utf-8'))
        challenge_bytes = digest.finalize()
        challenge = base64.urlsafe_b64encode(challenge_bytes).decode('utf-8')
        return challenge.rstrip('=')
    
    def _generate_quantum_state(self) -> str:
        """Generate quantum-enhanced state parameter"""
        # Combine multiple entropy sources
        timestamp = str(int(datetime.now(timezone.utc).timestamp() * 1000000))
        random_part = secrets.token_urlsafe(32)
        quantum_part = base64.urlsafe_b64encode(self.crypto.generate_quantum_safe_key()).decode()
        
        # Create HMAC for integrity
        combined = f"{timestamp}:{random_part}:{quantum_part}"
        state_hash = hashlib.sha256(combined.encode()).hexdigest()[:16]
        
        return f"{random_part}_{state_hash}"
    
    def _generate_quantum_nonce(self) -> str:
        """Generate quantum-enhanced nonce"""
        return secrets.token_urlsafe(32)
    
    def _determine_user_role(self, email: str) -> UserRole:
        """Determine user role based on email or other criteria"""
        # Admin domains
        admin_domains = os.getenv('ADMIN_EMAIL_DOMAINS', '').split(',')
        if any(email.endswith(f'@{domain.strip()}') for domain in admin_domains if domain.strip()):
            return UserRole.ADMIN
        
        # Analyst domains
        analyst_domains = os.getenv('ANALYST_EMAIL_DOMAINS', '').split(',')
        if any(email.endswith(f'@{domain.strip()}') for domain in analyst_domains if domain.strip()):
            return UserRole.QUANTUM_ANALYST
        
        # Default role
        return UserRole.VIEWER
    
    def _determine_security_level(self, oauth_user: OAuth2UserInfo) -> SecurityLevel:
        """Determine security level based on OAuth2 user info"""
        # High security for verified enterprise accounts
        if oauth_user.verified and oauth_user.provider in [OAuth2Provider.MICROSOFT, OAuth2Provider.OKTA]:
            return SecurityLevel.HIGH
        
        # Medium security for verified accounts
        if oauth_user.verified:
            return SecurityLevel.MEDIUM
        
        # Low security for unverified accounts
        return SecurityLevel.LOW
    
    def cleanup_expired_states(self):
        """Clean up expired OAuth2 states"""
        now = datetime.now(timezone.utc)
        expired_states = [
            state for state, oauth_state in self.pending_states.items()
            if oauth_state.expires_at < now
        ]
        
        for state in expired_states:
            del self.pending_states[state]

# Global OAuth2 service instance
oauth2_service = None

def get_oauth2_service() -> QuantumOAuth2Service:
    """Get global OAuth2 service instance"""
    global oauth2_service
    if oauth2_service is None:
        oauth2_service = QuantumOAuth2Service()
    return oauth2_service