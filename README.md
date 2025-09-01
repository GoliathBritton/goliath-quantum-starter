# Q-Sales Division™ Partner Portal

## 🚀 Overview

The **Q-Sales Division™ Partner Portal** is a quantum-powered CRM and sales division factory that enables businesses to deploy autonomous sales agents powered by Dynex quantum computing and NVIDIA acceleration. This portal serves as the "showroom floor" for the Goliath family of businesses, offering three distinct service tiers with comprehensive pricing and deployment options.

## 🏗️ Architecture

### Three-Pillar Business Empire

1. **GOLIATH** - Financial & CRM
   - Lending, insurance, and CRM operations
   - Quantum-enhanced risk assessment
   - Financial services integration

2. **FLYFOX AI** - Transformational Tech & Energy
   - Cutting-edge AI and energy solutions
   - Dynex quantum computing (410x performance)
   - NVIDIA acceleration overlay

3. **SIGMA SELECT** - Sales & Revenue
   - Revenue generation powerhouse
   - Autonomous sales agents
   - Lead optimization and conversion maximization

### Technology Stack

- **Frontend**: Next.js 14, React 18, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python 3.11+
- **Quantum Computing**: Dynex (preferred resource, 410x performance)
- **AI Acceleration**: NVIDIA cuQuantum, TensorRT, Energy SDK
- **Authentication**: NextAuth.js
- **Payments**: Stripe Connect
- **Deployment**: Docker, Kubernetes (EKS), GitHub Actions CI/CD

## 🎯 Core Features

### Q-Sales Division™ Packages

#### DIY (Do-It-Yourself)
- **Monthly**: $2,500
- **Setup**: $0
- **Features**: Full CRM access, QHC consultation, contact enrichment, basic automation
- **Best For**: Tech-savvy teams who want full control

#### DFY (Done-For-You)
- **Monthly**: $10,000
- **Setup**: $25,000
- **Features**: Everything in DIY + full setup, Quantum Architect deployment, custom campaigns
- **Best For**: Growing companies wanting rapid deployment
- **Badge**: Most Popular

#### Enterprise "Division in a Box"
- **Monthly**: $50,000
- **Setup**: $250,000
- **Features**: Everything in DFY + 500+ agents, white-label options, 24/7 support
- **Best For**: Large enterprises and category leaders

### Contact Management & Campaigns

- **CSV Import**: Drag & drop contact import with AI validation
- **AI Enrichment**: Quantum-powered contact scoring and data enhancement
- **Multi-Channel Campaigns**: Email, SMS, voice calls, social media
- **Real-time Analytics**: Performance tracking and optimization

### Sales Pod Management

- **Pod Types**: Starter (5 agents), Growth (25 agents), Scale (100 agents), Enterprise (500+)
- **Autonomous Agents**: 24/7 availability, continuous learning, performance optimization
- **Real-time Monitoring**: Health status, performance metrics, revenue tracking
- **Instant Deployment**: Deploy new pods in minutes with quantum optimization

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.11+
- Docker and Docker Compose
- Stripe account for payments
- Dynex quantum computing access

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/goliath-family/qsales-portal.git
   cd qsales-portal
   ```

2. **Install dependencies**
   ```bash
   # Frontend
   npm install
   
   # Backend (if applicable)
   pip install -r requirements.txt
   ```

3. **Environment setup**
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your configuration
   ```

4. **Run the development server**
   ```bash
   npm run dev
   ```

5. **Open your browser**
   Navigate to [http://localhost:3000](http://localhost:3000)

### Environment Variables

```env
# Stripe Configuration
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_your_key
STRIPE_SECRET_KEY=sk_test_your_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# NextAuth Configuration
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your_nextauth_secret

# NQBA MCP Integration
NQBA_MCP_ENDPOINT=http://localhost:8000/mcp
NQBA_API_KEY=your_nqba_api_key

# Goliath Business Configuration
GOLIATH_PORTAL_URL=https://portal.goliath.com
FLYFOX_AI_URL=https://app.flyfoxai.io
SIGMA_SELECT_URL=https://sigma-select.com
```

## 🎨 UI Components

### Core Components

- **Sidebar**: Collapsible navigation with business pillar sections
- **Navbar**: Responsive header with user menu and notifications
- **PackageSelector**: Interactive pricing tier selection with comparison
- **ContactWizard**: Step-by-step contact import and campaign setup
- **SalesPodDashboard**: Real-time pod management and monitoring

### Design System

- **Colors**: Goliath (blue), FLYFOX AI (purple), Sigma Select (green)
- **Typography**: Inter font family
- **Components**: Consistent button styles, cards, inputs, and animations
- **Responsive**: Mobile-first design with Tailwind CSS

## 🔧 Development

### Project Structure

```
src/
├── app/                    # Next.js app directory
│   ├── auth/              # Authentication pages
│   ├── packages/          # Package selection
│   ├── contacts/          # Contact management
│   ├── pods/              # Sales pod dashboard
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/            # Reusable UI components
│   ├── Navbar.tsx         # Navigation bar
│   ├── Sidebar.tsx        # Sidebar navigation
│   ├── PackageSelector.tsx # Package selection
│   ├── ContactWizard.tsx  # Contact import wizard
│   └── SalesPodDashboard.tsx # Pod management
└── lib/                   # Utility functions and types
```

### Available Scripts

```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint
```

### Code Quality

- **TypeScript**: Strict type checking enabled
- **ESLint**: Code quality and consistency
- **Prettier**: Code formatting
- **Tailwind CSS**: Utility-first CSS framework

## 🚀 Deployment

### Production Build

```bash
npm run build
npm run start
```

### Docker Deployment

```bash
# Build the image
docker build -t qsales-portal .

# Run the container
docker run -p 3000:3000 qsales-portal
```

### Kubernetes Deployment

```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -n qsales-portal
```

## 🔐 Security

- **Authentication**: NextAuth.js with multiple providers
- **API Security**: Rate limiting, CORS, input validation
- **Data Protection**: Encryption at rest and in transit
- **Access Control**: Role-based permissions and API key management

## 📊 Performance

### Quantum Computing Benefits

- **Dynex Integration**: 410x performance improvement
- **NVIDIA Acceleration**: GPU-accelerated AI inference
- **Real-time Optimization**: Continuous performance tuning
- **Scalability**: Handle millions of contacts and agents

### Frontend Performance

- **Next.js 14**: App Router and Server Components
- **Image Optimization**: Automatic WebP conversion
- **Code Splitting**: Dynamic imports and lazy loading
- **Caching**: Static generation and ISR

## 🔌 Integrations

### Current Integrations

- **Stripe**: Payment processing and subscription management
- **NextAuth**: Authentication and user management
- **Dynex**: Quantum computing platform
- **NVIDIA**: AI acceleration and GPU optimization

### Planned Integrations

- **GoHighLevel**: CRM features and automation
- **OpenAI**: Advanced AI capabilities
- **UiPath/n8n**: Workflow automation
- **Mendix/OutSystems**: Low-code development

## 📈 Analytics & Monitoring

### Real-time Metrics

- **Pod Performance**: Conversion rates, ROI, revenue
- **Agent Activity**: Calls, emails, responses
- **System Health**: Dynex status, NVIDIA acceleration
- **Business Metrics**: Contact counts, campaign performance

### Dashboard Features

- **Live Updates**: Real-time data refresh
- **Interactive Charts**: Performance visualization
- **Export Capabilities**: Data export for reporting
- **Alert System**: Performance and health notifications

## 🆘 Support & Troubleshooting

### Common Issues

1. **Build Errors**: Ensure Node.js version compatibility
2. **Styling Issues**: Check Tailwind CSS configuration
3. **API Errors**: Verify environment variables
4. **Performance Issues**: Check Dynex connection status

### Getting Help

- **Documentation**: This README and inline code comments
- **Issues**: GitHub Issues for bug reports
- **Discussions**: GitHub Discussions for questions
- **Support**: Contact the Goliath family support team

## 🚀 Roadmap

### Phase 1 (Current)
- ✅ Core portal functionality
- ✅ Package selection and pricing
- ✅ Contact import wizard
- ✅ Sales pod dashboard
- ✅ Basic authentication

### Phase 2 (Next)
- 🔄 Stripe Connect integration
- 🔄 Advanced analytics
- 🔄 Multi-tenant support
- 🔄 API documentation

### Phase 3 (Future)
- 📋 GoHighLevel integration
- 📋 Advanced AI features
- 📋 Mobile applications
- 📋 White-label solutions

## 📄 License

This project is proprietary software owned by the Goliath family of businesses. All rights reserved.

## 🤝 Contributing

This is a private, enterprise-grade system. For contributions or access, please contact the Goliath family development team.

## 📞 Contact

- **Website**: [https://portal.goliath.com](https://portal.goliath.com)
- **FLYFOX AI**: [https://app.flyfoxai.io](https://app.flyfoxai.io)
- **Support**: support@goliath.com

---

**Powered by Dynex Quantum Computing (410x Performance) + NVIDIA Acceleration**

*The future of autonomous sales is here.*