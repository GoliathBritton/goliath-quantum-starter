#!/usr/bin/env python3
"""
🔐 NQBA Authentication Client Example

Simple Python client for testing the NQBA authentication system.
This example demonstrates how to interact with the authentication API.
"""

import requests
import json
from typing import Dict, Optional

class NQBAAuthClient:
    """Simple client for NQBA authentication API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for authenticated requests"""
        headers = {"Content-Type": "application/json"}
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        return headers
    
    def login(self, username: str, password: str, remember_me: bool = False) -> bool:
        """
        Login to the NQBA system
        
        Args:
            username: Username
            password: Password
            remember_me: Whether to remember the session
            
        Returns:
            True if login successful, False otherwise
        """
        url = f"{self.base_url}/api/v1/auth/login"
        data = {
            "username": username,
            "password": password,
            "remember_me": remember_me
        }
        
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            
            result = response.json()
            self.access_token = result["access_token"]
            self.refresh_token = result["refresh_token"]
            
            print(f"✅ Login successful for user: {result['user']['username']}")
            print(f"   User ID: {result['user']['id']}")
            print(f"   Roles: {result['user']['roles']}")
            print(f"   Status: {result['user']['status']}")
            
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Login failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    print(f"   Error: {error_detail.get('error', 'Unknown error')}")
                except:
                    print(f"   Status Code: {e.response.status_code}")
            return False
    
    def logout(self) -> bool:
        """
        Logout from the NQBA system
        
        Returns:
            True if logout successful, False otherwise
        """
        if not self.access_token:
            print("⚠️  No active session to logout")
            return False
        
        url = f"{self.base_url}/api/v1/auth/logout"
        
        try:
            response = requests.post(url, headers=self._get_headers())
            response.raise_for_status()
            
            result = response.json()
            print(f"✅ Logout successful: {result['message']}")
            
            # Clear tokens
            self.access_token = None
            self.refresh_token = None
            
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Logout failed: {e}")
            return False
    
    def get_current_user(self) -> Optional[Dict]:
        """
        Get current user information
        
        Returns:
            User information or None if failed
        """
        if not self.access_token:
            print("⚠️  No active session")
            return None
        
        url = f"{self.base_url}/api/v1/auth/me"
        
        try:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            
            user_info = response.json()
            print(f"✅ Current user: {user_info['username']}")
            print(f"   Email: {user_info['email']}")
            print(f"   Name: {user_info['first_name']} {user_info['last_name']}")
            print(f"   Status: {user_info['status']}")
            print(f"   Roles: {user_info['roles']}")
            
            return user_info
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to get current user: {e}")
            return None
    
    def get_permissions(self) -> Optional[Dict]:
        """
        Get current user's permissions
        
        Returns:
            User permissions or None if failed
        """
        if not self.access_token:
            print("⚠️  No active session")
            return None
        
        url = f"{self.base_url}/api/v1/auth/permissions"
        
        try:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            
            permissions = response.json()
            print(f"✅ User permissions retrieved")
            print(f"   User ID: {permissions['user_id']}")
            print(f"   Username: {permissions['username']}")
            print(f"   Roles: {permissions['roles']}")
            print(f"   Permissions: {permissions['permissions']}")
            
            return permissions
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to get permissions: {e}")
            return None
    
    def get_auth_status(self) -> Optional[Dict]:
        """
        Get authentication system status
        
        Returns:
            System status or None if failed
        """
        url = f"{self.base_url}/api/v1/auth/status"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            status = response.json()
            print(f"✅ Authentication system status:")
            print(f"   Total Users: {status['total_users']}")
            print(f"   Active Users: {status['active_users']}")
            print(f"   Total Sessions: {status['total_sessions']}")
            print(f"   Total Roles: {status['total_roles']}")
            print(f"   Total Permissions: {status['total_permissions']}")
            print(f"   System Roles: {', '.join(status['system_roles'])}")
            
            return status
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to get system status: {e}")
            return None
    
    def create_user(self, user_data: Dict) -> Optional[Dict]:
        """
        Create a new user (requires appropriate permissions)
        
        Args:
            user_data: User creation data
            
        Returns:
            Created user or None if failed
        """
        if not self.access_token:
            print("⚠️  No active session")
            return None
        
        url = f"{self.base_url}/api/v1/auth/users"
        
        try:
            response = requests.post(url, json=user_data, headers=self._get_headers())
            response.raise_for_status()
            
            user = response.json()
            print(f"✅ User created successfully: {user['username']}")
            print(f"   User ID: {user['id']}")
            print(f"   Email: {user['email']}")
            print(f"   Status: {user['status']}")
            
            return user
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to create user: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    print(f"   Error: {error_detail.get('error', 'Unknown error')}")
                except:
                    print(f"   Status Code: {e.response.status_code}")
            return None
    
    def get_users(self) -> Optional[list]:
        """
        Get all users (requires appropriate permissions)
        
        Returns:
            List of users or None if failed
        """
        if not self.access_token:
            print("⚠️  No active session")
            return None
        
        url = f"{self.base_url}/api/v1/auth/users"
        
        try:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            
            users = response.json()
            print(f"✅ Retrieved {len(users)} users:")
            
            for user in users:
                print(f"   - {user['username']} ({user['email']}) - {user['status']}")
            
            return users
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to get users: {e}")
            return None
    
    def change_password(self, user_id: str, current_password: str, new_password: str) -> bool:
        """
        Change user password
        
        Args:
            user_id: User ID to change password for
            current_password: Current password
            new_password: New password
            
        Returns:
            True if successful, False otherwise
        """
        if not self.access_token:
            print("⚠️  No active session")
            return False
        
        url = f"{self.base_url}/api/v1/auth/users/{user_id}/change-password"
        data = {
            "current_password": current_password,
            "new_password": new_password
        }
        
        try:
            response = requests.post(url, json=data, headers=self._get_headers())
            response.raise_for_status()
            
            result = response.json()
            print(f"✅ Password changed successfully: {result['message']}")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to change password: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    print(f"   Error: {error_detail.get('error', 'Unknown error')}")
                except:
                    print(f"   Status Code: {e.response.status_code}")
            return False

def main():
    """Main example function"""
    print("🚀 NQBA Authentication Client Example")
    print("=" * 50)
    
    # Create client
    client = NQBAAuthClient()
    
    # Check system status
    print("\n📊 Checking authentication system status...")
    client.get_auth_status()
    
    # Example: Login as founder
    print("\n🔐 Attempting to login as founder...")
    success = client.login("founder", "Founder@2024!")
    
    if success:
        # Get current user info
        print("\n👤 Getting current user information...")
        client.get_current_user()
        
        # Get user permissions
        print("\n🔑 Getting user permissions...")
        client.get_permissions()
        
        # Get all users
        print("\n👥 Getting all users...")
        client.get_users()
        
        # Example: Create a new user
        print("\n➕ Creating a new user...")
        new_user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "TestPass123!",
            "roles": [],
            "metadata": {
                "department": "engineering",
                "created_by": "founder"
            }
        }
        client.create_user(new_user_data)
        
        # Logout
        print("\n🚪 Logging out...")
        client.logout()
    
    print("\n✅ Example completed!")

if __name__ == "__main__":
    main()
