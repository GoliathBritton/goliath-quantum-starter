# Branding
<div align="center">
  <img src="../docs/goliath_logo.png" width="180" alt="Goliath Logo" style="margin:1em;"/>
  <img src="../docs/flyfox_logo.png" width="120" alt="Fly Fox Logo" style="margin:1em;"/>
  <img src="../docs/sigma_select_logo.png" width="120" alt="Sigma Select Logo" style="margin:1em;"/>
  <h1>Goliath of All Trade | Fly Fox AI | Sigma Select</h1>
  <p><em>Unifying Quantum, AI, and Automation for the Next Era of Business</em></p>
  <p><strong>Goliath:</strong> The Quantum Operating System for Business<br>
     <strong>Fly Fox:</strong> AI-Driven Automation for Every Workflow<br>
     <strong>Sigma Select:</strong> Quantum-Enhanced Decision Intelligence
  </p>
</div>
# 🏗️ GitHub Organization Setup Guide
## FLYFOX AI, Goliath of All Trade, Sigma Select

This guide will walk you through setting up the three GitHub organizations and transferring the NQBA-Core repository to establish the foundation for your quantum business architecture.

---

## 🎯 **Overview**

**Target Structure:**
- **`flyfoxai`** (Primary): NQBA-Core platform, quantum AI agents
- **`goliath-trade`** (Finance): Trading algorithms, portfolio optimization
- **`sigma-select`** (Sales): Lead scoring, business intelligence

**Repository Flow:**
```
goliath-quantum-starter → flyfoxai/nqba-core → Business Unit Repos
```

---

## 🚀 **Step 1: Create GitHub Organizations**

### **1.1 FLYFOX AI Organization**
1. **Navigate to GitHub**: https://github.com/settings/organizations
2. **Click "New organization"**
3. **Fill in details**:
   - **Organization name**: `flyfoxai`
   - **Email**: `admin@flyfox.ai`
   - **Plan**: Free (upgrade later as needed)
4. **Complete setup**:
   - **Owner**: Your GitHub username
   - **Repository creation**: Allow members to create repositories
   - **Member privileges**: Standard

### **1.2 Goliath of All Trade Organization**
1. **Repeat organization creation**
2. **Organization name**: `goliath-trade`
3. **Email**: `admin@goliath-trade.com`
4. **Settings**:
   - **Repository creation**: Owner only (controlled access)
   - **Member privileges**: Read (consumers of NQBA-Core)

### **1.3 Sigma Select Organization**
1. **Create organization**
2. **Organization name**: `sigma-select`
3. **Email**: `admin@sigma-select.com`
4. **Settings**:
   - **Repository creation**: Owner only
   - **Member privileges**: Read (consumers of NQBA-Core)

---

## 🔄 **Step 2: Repository Transfer to flyfoxai/nqba-core**

### **2.1 Prepare Current Repository**
```bash
# Ensure you're in the goliath-quantum-starter directory
cd /c/Users/johnb/goliath-quantum-starter

# Check current remote
git remote -v

# Create backup branch from commit 6656698 (as specified in roadmap)
git checkout -b backup-6656698 6656698

# Push backup branch
git push origin backup-6656698
```

### **2.2 Transfer Repository**
1. **Go to repository settings**: https://github.com/[your-username]/goliath-quantum-starter/settings
2. **Scroll to "Danger Zone"**
3. **Click "Transfer ownership"**
4. **Enter**: `flyfoxai`
5. **Confirm transfer**

### **2.3 Rename Repository**
1. **In flyfoxai organization**: Go to transferred repository
2. **Settings → General**
3. **Repository name**: `nqba-core`
4. **Click "Rename"**

**New URL**: `https://github.com/flyfoxai/nqba-core`

---

## 📁 **Step 3: Repository Structure Setup**

### **3.1 Enable GitHub Pages**
1. **Settings → Pages**
2. **Source**: Deploy from a branch
3. **Branch**: `main` → `/docs`
4. **Save**

### **3.2 Set Repository Topics**
Add these topics to `flyfoxai/nqba-core`:
```
quantum-computing
neuromorphic-computing
business-architecture
nqba
flyfox-ai
goliath-trade
sigma-select
ai-agents
quantum-optimization
```

### **3.3 Repository Description**
```
🚀 NQBA-Core: Neuromorphic Quantum Business Architecture

The quantum-native execution layer powering FLYFOX AI, Goliath of All Trade, and Sigma Select. Built for adaptive, intelligent quantum execution with business alignment.

🔗 Live Demo: https://flyfoxai.github.io/nqba-core/
📚 Docs: https://flyfoxai.github.io/nqba-core/docs/
```

---

## 🔐 **Step 4: Security & Access Control**

### **4.1 Organization Security Settings**
For each organization (`flyfoxai`, `goliath-trade`, `sigma-select`):

1. **Settings → Security**
   - **Two-factor authentication**: Required for all members
   - **SSH certificate authorities**: Configure if needed
   - **Security advisories**: Enable

2. **Settings → Code security and analysis**
   - **Dependabot alerts**: Enable
   - **Dependabot security updates**: Enable
   - **Secret scanning**: Enable
   - **Code scanning**: Enable (GitHub Advanced Security)

### **4.2 Repository Secrets**
In `flyfoxai/nqba-core` → Settings → Secrets and variables → Actions:

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `DYNEX_API_KEY` | DynexSolve API key | `dnx_...` |
| `WEB3_PROVIDER_URL` | Blockchain testnet URL | `https://testnet.dynexcoin.org` |
| `IPFS_PROJECT_ID` | IPFS credentials | `Qm...` |
| `IPFS_PROJECT_SECRET` | IPFS project secret | `...` |
| `LLM_API_KEY` | qdLLM fallback | `sk-...` |
| `DEPLOY_KEY` | GitHub Pages deploy key | `ssh-rsa...` |

### **4.3 Branch Protection Rules**
1. **Settings → Branches**
2. **Add rule for `main` branch**:
   - ✅ **Require a pull request before merging**
   - ✅ **Require status checks to pass before merging**
   - ✅ **Require branches to be up to date before merging**
   - ✅ **Require signed commits**
   - ✅ **Require linear history**
   - ✅ **Include administrators**

---

## 👥 **Step 5: Team Structure & Permissions**

### **5.1 FLYFOX AI Teams**
Create these teams in `flyfoxai` organization:

| Team | Permission | Purpose |
|------|------------|---------|
| `nqba-core-maintainers` | Admin | Core platform development |
| `quantum-integration` | Write | Dynex, quantum backends |
| `business-logic` | Write | Decision engine, rules |
| `ai-agents` | Write | Chatbot, voice, digital human |
| `documentation` | Write | Docs, onboarding, guides |
| `security` | Admin | Security reviews, audits |

### **5.2 Cross-Organization Access**
1. **Invite organizations** to collaborate:
   - `goliath-trade` → Read access to `nqba-core`
   - `sigma-select` → Read access to `nqba-core`

2. **Create integration teams**:
   - `goliath-trade/nqba-consumers` → Read access
   - `sigma-select/nqba-consumers` → Read access

---

## 🚀 **Step 6: CI/CD Pipeline Setup**

### **6.1 GitHub Actions Workflow**
The `.github/workflows/ci.yml` should already be in place. Verify:

```yaml
name: NQBA Core CI/CD

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov ruff black mypy
      - name: Run tests
        run: pytest --cov=src --cov-report=xml
      - name: Code quality
        run: |
          black --check src/ tests/
          ruff check src/ tests/
          mypy src/
```

### **6.2 Automated Deployment**
Add deployment workflow to `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs
```

---

## 📊 **Step 7: Project Management Setup**

### **7.1 Create Project Board**
1. **Go to**: `flyfoxai/nqba-core` → Projects
2. **Click "New project"**
3. **Template**: Board
4. **Name**: "NQBA Sprint-1 Roadmap"
5. **Description**: "6-week Sprint-1 execution for NQBA-Core MVP"

### **7.2 Project Columns**
Set up these columns:
- **📋 Backlog**: Planned tasks
- **🔄 In Progress**: Active development
- **🧪 Testing**: Code review & testing
- **✅ Done**: Completed tasks
- **🚀 Deployed**: Production ready

### **7.3 Sprint Milestones**
Create these milestones:
- **Sprint 1.1** (Week 1-2): Foundation & Org Setup
- **Sprint 1.2** (Week 3-4): Core Engine & Demo Agent
- **Sprint 1.3** (Week 5-6): Multi-Agent + SaaS Hook

---

## 🔍 **Step 8: Verification Checklist**

### **8.1 Organization Setup**
- [ ] `flyfoxai` organization created
- [ ] `goliath-trade` organization created
- [ ] `sigma-select` organization created
- [ ] Repository transferred to `flyfoxai/nqba-core`
- [ ] Repository renamed from `goliath-quantum-starter`

### **8.2 Repository Configuration**
- [ ] GitHub Pages enabled (`main/docs`)
- [ ] Branch protection rules configured
- [ ] Repository topics added
- [ ] Description updated
- [ ] Secrets configured

### **8.3 Access Control**
- [ ] Teams created with appropriate permissions
- [ ] Cross-organization access configured
- [ ] Two-factor authentication required
- [ ] Security features enabled

### **8.4 CI/CD Pipeline**
- [ ] GitHub Actions workflows configured
- [ ] Automated testing enabled
- [ ] Code quality gates active
- [ ] Deployment automation ready

---

## 🎯 **Step 9: Next Actions**

### **Immediate (Today)**
1. **Execute repository transfer**
2. **Configure basic security settings**
3. **Set up GitHub Pages**

### **This Week**
1. **Create project board**
2. **Set up CI/CD pipeline**
3. **Configure team permissions**
4. **Add repository secrets**

### **Next Week**
1. **Begin Sprint-1 execution**
2. **Onboard development team**
3. **Start first development tasks**

---

## 📞 **Support & Troubleshooting**

### **Common Issues**
- **Transfer failed**: Ensure you have admin access to both repositories
- **Pages not working**: Check branch and folder configuration
- **Secrets not available**: Verify organization permissions

### **Getting Help**
- **GitHub Support**: For technical issues
- **Organization Settings**: For permission problems
- **Team Management**: For access control issues

---

## 🎉 **Success Criteria**

You'll know the setup is complete when:
1. ✅ `https://github.com/flyfoxai/nqba-core` is accessible
2. ✅ `https://flyfoxai.github.io/nqba-core/` shows your documentation
3. ✅ CI/CD pipeline runs automatically on commits
4. ✅ Teams can access repositories with appropriate permissions
5. ✅ Security features are active and monitoring

---

*This guide ensures your NQBA-Core platform has a solid foundation for Sprint-1 execution and future growth.* 🚀
