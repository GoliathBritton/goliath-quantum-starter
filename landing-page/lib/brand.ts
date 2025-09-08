/**
 * FLYFOX AI Brand Configuration
 * Centralized brand, partners, and business unit definitions
 * Maintains NQBA quantum MCP foundation while supporting new architecture
 */

export interface BusinessUnit {
  name: string
  description: string
  focus: string
  quantumAdvantage: string
  color: string
  icon: string
}

export interface Partner {
  name: string
  type: 'quantum' | 'workflow' | 'ai' | 'infrastructure'
  description: string
  integration: string
  tier: 'core' | 'strategic' | 'ecosystem'
  logo?: string
}

export interface PricingTier {
  name: string
  description: string
  features: string[]
  quantumAccess: boolean
  whiteLabel: boolean
  price?: string
}

export interface AdvancedRole {
  name: string
  title: string
  description: string
  capabilities: string[]
  quantumPrinciples: string[]
  brandEntity: 'FLYFOX AI' | 'Goliath of All Trade' | 'Sigma Select'
  layer: 'governance' | 'core' | 'agents' | 'marketplace'
  icon: string
}

export interface QuantumCouncilMember {
  role: string
  title: string
  focus: string
  quantumAdvantage: string
  advancedIntegration: string
}

// Core Brand Colors - Strict palette for high contrast
export const brandColors = {
  primary: {
    cyan: '#27E5FF',
    gold: '#F5C14C',
    navy: '#111827'
  },
  base: {
    white: '#FFFFFF',
    black: '#000000',
    gray: {
      50: '#F9FAFB',
      100: '#F3F4F6',
      900: '#111827'
    }
  },
  quantum: {
    blue: '#3B82F6',
    purple: '#8B5CF6',
    emerald: '#10B981'
  }
} as const

// Intelligence Economy Business Units
export const businessUnits: BusinessUnit[] = [
  {
    name: 'FLYFOX AI',
    description: 'Quantum-native AI platform powering the intelligence economy',
    focus: 'AI Agents & Business Intelligence',
    quantumAdvantage: '3.2x execution efficiency with NQBA Core',
    color: brandColors.primary.cyan,
    icon: '🧠'
  },
  {
    name: 'Goliath of All Trade',
    description: 'Capital • Energy • Insurance optimization through quantum computing',
    focus: 'Financial & Energy Markets',
    quantumAdvantage: '4.1x portfolio performance optimization',
    color: brandColors.primary.gold,
    icon: '⚡'
  },
  {
    name: 'Sigma Select',
    description: 'Elite training and lead optimization with quantum-powered insights',
    focus: 'Training & Lead Conversion',
    quantumAdvantage: '2.8x lead conversion improvement',
    color: brandColors.primary.navy,
    icon: '🎯'
  }
]

// Strategic Partners - Quantum-first ecosystem
export const partners: Partner[] = [
  {
    name: 'Dynex',
    type: 'quantum',
    description: 'Primary quantum computing platform for NQBA Core execution',
    integration: 'Native QUBO optimization and neuromorphic computing',
    tier: 'core'
  },
  {
    name: 'NVIDIA',
    type: 'quantum',
    description: 'GPU acceleration and quantum simulation capabilities',
    integration: 'CUDA-accelerated quantum algorithms and AI model training',
    tier: 'strategic'
  },
  {
    name: 'OpenAI',
    type: 'ai',
    description: 'Large language model integration for AI agents',
    integration: 'GPT models with NQBA governance and audit trails',
    tier: 'strategic'
  },
  {
    name: 'UiPath',
    type: 'workflow',
    description: 'Robotic process automation and workflow orchestration',
    integration: 'RPA bots governed by NQBA decision engine',
    tier: 'ecosystem'
  },
  {
    name: 'n8n',
    type: 'workflow',
    description: 'Lightweight workflow automation and integration platform',
    integration: 'Visual workflow builder with quantum-enhanced decision nodes',
    tier: 'ecosystem'
  },
  {
    name: 'Mendix',
    type: 'workflow',
    description: 'Low-code application development platform',
    integration: 'Rapid app development with NQBA-powered business logic',
    tier: 'ecosystem'
  },
  {
    name: 'Prismatic',
    type: 'workflow',
    description: 'SaaS integration hub for enterprise connectivity',
    integration: 'Pre-built connectors with quantum-optimized data flows',
    tier: 'ecosystem'
  }
]

// Pricing Tiers - White-label ready
export const pricingTiers: PricingTier[] = [
  {
    name: 'Standard',
    description: 'Essential NQBA Core features for small businesses',
    features: [
      'Basic AI agents',
      'Standard quantum access',
      'Community support',
      'Basic audit trails'
    ],
    quantumAccess: true,
    whiteLabel: false,
    price: '$99/month'
  },
  {
    name: 'Pro',
    description: 'Advanced features for growing enterprises',
    features: [
      'Advanced AI agents',
      'Priority quantum access',
      'Premium support',
      'Full LTC audit trails',
      'Custom integrations'
    ],
    quantumAccess: true,
    whiteLabel: false,
    price: '$499/month'
  },
  {
    name: 'Partner',
    description: 'White-label platform for strategic partners',
    features: [
      'Full platform access',
      'Dedicated quantum resources',
      'White-label branding',
      'Custom business logic',
      'Dedicated support',
      'Revenue sharing'
    ],
    quantumAccess: true,
    whiteLabel: true,
    price: 'Custom'
  }
]

// Quantum High Council - Expanded with Advanced Advisors
export const quantumHighCouncil: QuantumCouncilMember[] = [
  {
    role: 'Chief Executive Officer',
    title: 'Quantum Visionary & Strategic Leader',
    focus: 'Ecosystem orchestration and quantum business transformation',
    quantumAdvantage: 'Superposition-based strategic planning across multiple scenarios',
    advancedIntegration: 'Dynamic Entrepreneur + Market Strategist fusion'
  },
  {
    role: 'Senior Legal Counsel',
    title: 'Quantum Compliance & Risk Architect',
    focus: 'Ethical AI governance, quantum-safe legal frameworks',
    quantumAdvantage: 'Entangled risk assessment across regulatory dimensions',
    advancedIntegration: 'Legal expertise with quantum uncertainty modeling'
  },
  {
    role: 'Chief Financial Officer',
    title: 'Quantum Financial Strategist',
    focus: 'Capital optimization, quantum portfolio management',
    quantumAdvantage: 'Tunneling through financial barriers and market inefficiencies',
    advancedIntegration: 'Financial modeling with quantum superposition scenarios'
  },
  {
    role: 'Chief Psychology Officer',
    title: 'Quantum Behavioral Architect',
    focus: 'Culture development, bias detection, engagement optimization',
    quantumAdvantage: 'Quantum entanglement of team dynamics and customer psychology',
    advancedIntegration: 'SigmaEQ leadership principles with quantum behavioral modeling'
  }
]

// Advanced Roles - Integrated Across Ecosystem
export const advancedRoles: AdvancedRole[] = [
  // FLYFOX AI - Technology & Innovation
  {
    name: 'Chief Technology Officer',
    title: 'Quantum Technology Visionary',
    description: 'Multi-tech roadmaps and quantum adoption strategies',
    capabilities: ['Quantum architecture design', 'Technology stack optimization', 'Innovation pipeline management'],
    quantumPrinciples: ['Superposition: Multiple tech scenarios', 'Entanglement: Cross-platform integration'],
    brandEntity: 'FLYFOX AI',
    layer: 'core',
    icon: '🔬'
  },
  {
    name: 'Senior Software Engineer',
    title: 'Quantum Code Architect',
    description: 'Secure infrastructure and microservices translation',
    capabilities: ['Quantum-safe coding', 'Microservices architecture', 'API security'],
    quantumPrinciples: ['Tunneling: Breaking technical barriers', 'Superposition: Multi-environment deployment'],
    brandEntity: 'FLYFOX AI',
    layer: 'core',
    icon: '💻'
  },
  {
    name: 'Senior Data Scientist',
    title: 'Quantum ML Innovator',
    description: 'Quantum ML and predictive engines',
    capabilities: ['Quantum machine learning', 'Predictive modeling', 'Algorithm optimization'],
    quantumPrinciples: ['Superposition: Multiple model states', 'Entanglement: Data correlation discovery'],
    brandEntity: 'FLYFOX AI',
    layer: 'core',
    icon: '📊'
  },
  {
    name: 'Senior Data Analyst',
    title: 'Quantum Insights Engine',
    description: 'Real-time insights for agents and clients',
    capabilities: ['Real-time analytics', 'Business intelligence', 'Performance optimization'],
    quantumPrinciples: ['Tunneling: Instant insight delivery', 'Entanglement: Connected data streams'],
    brandEntity: 'FLYFOX AI',
    layer: 'core',
    icon: '📈'
  },
  {
    name: 'Senior Cybersecurity Specialist',
    title: 'Quantum Security Guardian',
    description: 'Real-time anomaly detection and post-quantum crypto',
    capabilities: ['Quantum cryptography', 'Threat detection', 'Security architecture'],
    quantumPrinciples: ['Superposition: Multi-layer security', 'Tunneling: Rapid threat response'],
    brandEntity: 'FLYFOX AI',
    layer: 'core',
    icon: '🛡️'
  },
  {
    name: 'Senior Programmer',
    title: 'Quantum Logic Optimizer',
    description: 'Optimized agent logic and reusable QUBO workflows',
    capabilities: ['QUBO optimization', 'Agent programming', 'Workflow automation'],
    quantumPrinciples: ['Superposition: Multiple code paths', 'Entanglement: Interconnected systems'],
    brandEntity: 'FLYFOX AI',
    layer: 'agents',
    icon: '⚡'
  },
  {
    name: 'Senior Product Engineer',
    title: 'Quantum Experience Designer',
    description: 'Multi-modal features and digital twin presence',
    capabilities: ['Product design', 'User experience', 'Feature development'],
    quantumPrinciples: ['Superposition: Multiple user journeys', 'Entanglement: Seamless integration'],
    brandEntity: 'FLYFOX AI',
    layer: 'agents',
    icon: '🎨'
  },
  // Goliath of All Trade - Finance & Operations
  {
    name: 'Senior Operations Manager',
    title: 'Quantum Operations Orchestrator',
    description: 'Seamless provisioning and supply chain alignment',
    capabilities: ['Operations optimization', 'Supply chain management', 'SLA adherence'],
    quantumPrinciples: ['Tunneling: Operational efficiency', 'Entanglement: Connected processes'],
    brandEntity: 'Goliath of All Trade',
    layer: 'marketplace',
    icon: '⚙️'
  },
  {
    name: 'Senior Business Development',
    title: 'Quantum Business Catalyst',
    description: 'New agent businesses and SaaS pod creation',
    capabilities: ['Business model innovation', 'Market expansion', 'Revenue optimization'],
    quantumPrinciples: ['Superposition: Multiple business models', 'Tunneling: Market penetration'],
    brandEntity: 'Goliath of All Trade',
    layer: 'agents',
    icon: '🚀'
  },
  // Sigma Select - Sales & Leadership
  {
    name: 'Senior Project Manager',
    title: 'Quantum Delivery Orchestrator',
    description: 'Agile delivery and version control with KPIs',
    capabilities: ['Project orchestration', 'Agile methodology', 'Performance tracking'],
    quantumPrinciples: ['Superposition: Multiple project states', 'Entanglement: Team synchronization'],
    brandEntity: 'Sigma Select',
    layer: 'agents',
    icon: '📋'
  },
  {
    name: 'Senior Market Strategist',
    title: 'Quantum Growth Architect',
    description: 'Growth hacks and funnel intelligence',
    capabilities: ['Market analysis', 'Growth strategy', 'Competitive intelligence'],
    quantumPrinciples: ['Superposition: Multiple market scenarios', 'Tunneling: Competitive advantages'],
    brandEntity: 'Sigma Select',
    layer: 'agents',
    icon: '🎯'
  },
  {
    name: 'Chief Marketing Officer',
    title: 'Quantum Brand Amplifier',
    description: 'Campaigns and co-brand strategies for partners',
    capabilities: ['Brand strategy', 'Campaign management', 'Partner marketing'],
    quantumPrinciples: ['Entanglement: Brand synergy', 'Superposition: Multi-channel campaigns'],
    brandEntity: 'Sigma Select',
    layer: 'marketplace',
    icon: '📢'
  },
  {
    name: 'Senior HR Director',
    title: 'Quantum Talent Orchestrator',
    description: 'Partner team scaling with DEI and retention',
    capabilities: ['Talent acquisition', 'Team development', 'Culture building'],
    quantumPrinciples: ['Entanglement: Team dynamics', 'Superposition: Multiple talent paths'],
    brandEntity: 'Sigma Select',
    layer: 'marketplace',
    icon: '👥'
  }
]

// NQBA Core Architecture Layers - Enhanced with Advanced Integration
export const nqbaLayers = [
  {
    name: 'Quantum High Council',
    description: 'Strategic directives with advanced advisors (Legal, CFO, Psychology)',
    icon: '👑',
    color: brandColors.quantum.purple,
    advancedRoles: ['Senior Legal Counsel', 'Chief Financial Officer', 'Chief Psychology Officer']
  },
  {
    name: 'NQBA Orchestrator',
    description: 'CTO and Software Engineer embedded for secure infrastructure',
    icon: '🧠',
    color: brandColors.quantum.blue,
    advancedRoles: ['Chief Technology Officer', 'Senior Software Engineer']
  },
  {
    name: 'QSAI Learner',
    description: 'Self-healing intelligence with Data Scientists and Cybersecurity',
    icon: '⚛️',
    color: brandColors.quantum.emerald,
    advancedRoles: ['Senior Data Scientist', 'Senior Data Analyst', 'Senior Cybersecurity Specialist']
  },
  {
    name: 'Agent Factory',
    description: 'Enhanced agents with Programmers, Product Engineers, and Entrepreneurs',
    icon: '🤖',
    color: brandColors.primary.gold,
    advancedRoles: ['Senior Programmer', 'Senior Product Engineer', 'Senior Project Manager', 'Senior Business Development']
  },
  {
    name: 'Q-Sales Division™',
    description: 'Growth-optimized agents with Market Strategy and Lead Generation',
    icon: '💼',
    color: brandColors.primary.cyan,
    advancedRoles: ['Senior Market Strategist']
  },
  {
    name: 'Marketplace Pods',
    description: 'Partner ecosystem with CMO, Operations, and HR capabilities',
    icon: '🌐',
    color: brandColors.primary.navy,
    advancedRoles: ['Chief Marketing Officer', 'Senior Operations Manager', 'Senior HR Director']
  }
]

// Navigation Structure
export const navigation = {
  main: [
    { label: 'About', path: '/about' },
    { label: 'Products', path: '/products' },
    { label: 'Industries', path: '/industries' },
    { label: 'Resources', path: '/resources' },
    { label: 'Advanced AI', path: '/advanced' },
    { label: 'Case Studies', path: '/case-studies' },
    { label: 'Investor Relations', path: '/investor-relations' },
    { label: 'Contact', path: '/contact' }
  ],
  auth: [
    { label: 'Sign In', path: '/flyfox-ai/sign-in' },
    { label: 'Pipeline Builder', path: '/pipeline' }
  ]
}

// Compliance & Trust Metrics
export const trustMetrics = [
  { label: 'API Response Time', value: '< 100ms', icon: '⚡' },
  { label: 'Quantum Success Rate', value: '85%', icon: '⭐' },
  { label: 'Test Coverage', value: '92%', icon: '✅' },
  { label: 'Uptime', value: '99.9%', icon: '📈' }
]

// Export default brand configuration
export const brand = {
  name: 'FLYFOX AI',
  tagline: 'The Intelligence Economy. Powered by NQBA.',
  description: 'Quantum-native execution layer powering adaptive, intelligent business operations with advanced AI integration',
  colors: brandColors,
  businessUnits,
  partners,
  pricingTiers,
  nqbaLayers,
  quantumHighCouncil,
  advancedRoles,
  navigation,
  trustMetrics
} as const

export default brand