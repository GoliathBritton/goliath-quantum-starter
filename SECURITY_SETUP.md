# 🔒 NQBA Stack Security Setup Guide

**CRITICAL: This document contains security protocols that must be followed immediately.**

## 🚨 IMMEDIATE SECURITY ACTIONS REQUIRED

### 1. **CREDENTIAL ROTATION (NEXT 2 HOURS)**

The following credentials have been exposed in our development history and MUST be rotated immediately:

#### **Dynex API Key**
- **Current Status**: Exposed in chat history
- **Action**: Revoke current key, generate new one
- **Format**: Should start with `dnx_` and be at least 20 characters
- **Storage**: Store in GitHub Secrets, NOT in code

#### **IPFS Project Credentials**
- **Current Status**: Exposed in chat history
- **Action**: Rotate both Project ID and Secret
- **Format**: Project ID should start with `Qm` or `bafy`
- **Storage**: Store in GitHub Secrets, NOT in code

#### **LLM API Keys**
- **Current Status**: Exposed in chat history
- **Action**: Rotate OpenAI and any other LLM keys
- **Format**: OpenAI keys should start with `sk-`
- **Storage**: Store in GitHub Secrets, NOT in code

### 2. **GITHUB SECRETS CONFIGURATION**

#### **Required Secrets**
```bash
# Add these to GitHub Repository Secrets (Settings > Secrets and variables > Actions)
DYNEX_API_KEY=dnx_new_rotated_key_here
IPFS_PROJECT_ID=QmNewProjectID
IPFS_PROJECT_SECRET=new_project_secret
LLM_API_KEY=new_llm_key
OPENAI_API_KEY=sk-new_openai_key
WEB3_PROVIDER_URL=https://new_web3_provider
```

#### **How to Add Secrets**
1. Go to your GitHub repository
2. Click `Settings` > `Secrets and variables` > `Actions`
3. Click `New repository secret`
4. Add each credential with the exact name above
5. **NEVER** commit these values to code

### 3. **ENVIRONMENT VARIABLE SECURITY**

#### **Create .env file (DO NOT COMMIT)**
```bash
# Copy this template to .env file (add to .gitignore)
NQBA_ENVIRONMENT=development
NQBA_DEBUG=false

# Company Information
NQBA_COMPANY_NAME=FLYFOX AI
NQBA_BUSINESS_UNIT=NQBA Core

# API Credentials (SECURE - Rotate these regularly)
DYNEX_API_KEY=dnx_your_new_dynex_api_key
IPFS_PROJECT_ID=QmYourNewIPFSProjectID
IPFS_PROJECT_SECRET=your_new_ipfs_project_secret
LLM_API_KEY=your_new_llm_api_key
OPENAI_API_KEY=sk-your_new_openai_api_key

# Web3 Configuration
WEB3_PROVIDER_URL=https://your_web3_provider_url

# Data and Storage
NQBA_DATA_DIR=./data
NQBA_LOG_DIR=./logs
NQBA_CACHE_DIR=./cache

# API Configuration
NQBA_API_HOST=0.0.0.0
NQBA_API_PORT=8000
NQBA_API_WORKERS=1

# Quantum Configuration
NQBA_QUANTUM_TIMEOUT=300
NQBA_QUANTUM_MAX_QUBITS=64
NQBA_QUANTUM_BACKEND=dynex

# LTC Configuration
NQBA_LTC_BACKUP_INTERVAL=3600
NQBA_LTC_MAX_ENTRIES=10000
NQBA_LTC_ENABLE_IPFS=true

# Security Configuration
NQBA_ENABLE_CORS=true
NQBA_CORS_ORIGINS=["*"]
NQBA_ENABLE_RATE_LIMITING=true
NQBA_RATE_LIMIT_REQUESTS=100
NQBA_RATE_LIMIT_WINDOW=60
```

#### **Update .gitignore**
```bash
# Add these lines to .gitignore
.env
.env.local
.env.production
.env.staging
*.key
*.pem
*.p12
secrets/
credentials/
```

## 🔐 **SECURITY VALIDATION CHECKLIST**

### **Before Running Any Code**
- [ ] All API keys rotated and new ones generated
- [ ] GitHub Secrets configured with new credentials
- [ ] .env file created with new credentials
- [ ] .gitignore updated to exclude sensitive files
- [ ] No hardcoded credentials in codebase
- [ ] Environment variables properly loaded

### **Security Testing**
- [ ] Run `python -c "from src.nqba_stack.core.settings import get_settings; s = get_settings(); print(s.get_credential_status())"`
- [ ] Verify no credentials are logged to console
- [ ] Check that all services show "configured" status
- [ ] Validate no secrets in git history

## 🚀 **IMMEDIATE NEXT STEPS**

### **Phase 1: Security Lockdown (Next 2 Hours)**
1. **Rotate all exposed credentials**
2. **Configure GitHub Secrets**
3. **Create secure .env file**
4. **Update .gitignore**

### **Phase 2: Validation (Next 4 Hours)**
1. **Test credential loading**
2. **Verify no secrets in logs**
3. **Run security audit**
4. **Test API endpoints**

### **Phase 3: Team Onboarding (Next 24 Hours)**
1. **Grant repository access to key team members**
2. **Share security protocols**
3. **Schedule technical kickoff**
4. **Assign security responsibilities**

## 🛡️ **ONGOING SECURITY PROTOCOLS**

### **Daily Security Checks**
- [ ] Verify no credentials in logs
- [ ] Check GitHub Secrets are accessible
- [ ] Monitor for unauthorized access
- [ ] Review security audit logs

### **Weekly Security Reviews**
- [ ] Rotate non-critical credentials
- [ ] Review access permissions
- [ ] Update security documentation
- [ ] Conduct security training

### **Monthly Security Audits**
- [ ] Full credential rotation
- [ ] Security penetration testing
- [ ] Compliance review
- [ ] Incident response drills

## 📞 **SECURITY CONTACTS**

- **Security Lead**: [Assign Security Lead]
- **Incident Response**: [Assign Incident Response Lead]
- **Compliance Officer**: [Assign Compliance Officer]

## ⚠️ **SECURITY INCIDENT RESPONSE**

### **If Credentials are Compromised**
1. **IMMEDIATELY** revoke all compromised credentials
2. **Generate new credentials** for all services
3. **Update GitHub Secrets** with new values
4. **Update .env files** with new values
5. **Notify security team** immediately
6. **Document incident** for compliance

### **Emergency Contacts**
- **24/7 Security Hotline**: [Emergency Number]
- **Security Email**: [Emergency Email]
- **Slack Channel**: #nqba-security-emergency

---

**Remember: Security is everyone's responsibility. When in doubt, ask the security team before proceeding.**

**Last Updated**: [Current Date]
**Next Review**: [Next Review Date]
**Security Level**: CONFIDENTIAL
