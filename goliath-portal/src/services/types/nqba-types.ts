/**
 * NQBA Types
 * ==========
 * 
 * TypeScript type definitions for the Neuromorphic Quantum Business Architecture
 * Ensures type safety across all NQBA systems and integrations
 */

// Dynex Quantum Computing Types
export interface DynexConfig {
  preferred_quantum_resource: string
  performance_multiplier: string
  nvidia_acceleration: boolean
  combined_performance: string
  quantum_backend: string
  neuromorphic_computing: boolean
  qubo_optimization: boolean
  qdllm_integration: boolean
}

export interface OptimizationResult {
  job_id: string
  status: 'pending' | 'processing' | 'completed' | 'failed'
  result?: any
  performance_boost: string
  processing_time: number
  energy_consumption: number
}

// Q-Sales Division Types
export interface QSalesAgent {
  agent_id: string
  name: string
  role: 'vp_sales' | 'sales_manager' | 'senior_rep' | 'junior_rep' | 'sdr' | 'closer'
  specialization: string
  experience_level: number
  communication_channels: string[]
  performance_metrics: Record<string, number>
  is_active: boolean
  created_at: Date
  last_activity: Date
}

export interface QSalesPod {
  pod_id: string
  name: string
  industry: string
  target_market: string
  agents: QSalesAgent[]
  playbook_id: string
  performance_targets: {
    conversion_rate: number
    roi: number
    revenue_target: number
  }
  status: 'active' | 'training' | 'optimizing' | 'paused' | 'scaling'
  revenue_generated: number
  leads_processed: number
  conversion_rate: number
}

export interface QSalesPlaybook {
  playbook_id: string
  name: string
  industry: string
  target_audience: string
  scripts: Record<string, string>
  cadences: Record<string, any[]>
  objection_handlers: Record<string, string>
  success_patterns: any[]
  version: number
  created_at: Date
  last_updated: Date
}

// FLYFOX AI Platform Types
export interface FlyfoxConfig {
  platform_url: string
  api_endpoint: string
  energy_optimization: boolean
  ai_platform: boolean
}

export interface FlyfoxEnergyOptimization {
  optimization_id: string
  target_system: string
  current_consumption: number
  optimized_consumption: number
  savings_percentage: number
  quantum_enhancement: boolean
}

// Goliath Financial Types
export interface GoliathConfig {
  crm_endpoint: string
  lending_portal: string
  insurance_hub: string
}

export interface GoliathCRMContact {
  contact_id: string
  company_name: string
  contact_name: string
  title?: string
  phone?: string
  email: string
  industry?: string
  company_size?: string
  annual_revenue?: string
  lead_score: number
  status: 'new' | 'qualified' | 'proposal' | 'negotiation' | 'closed'
  created_at: Date
  last_activity: Date
}

export interface GoliathLendingApplication {
  application_id: string
  company_name: string
  requested_amount: number
  purpose: string
  risk_score: number
  quantum_risk_assessment: boolean
  status: 'pending' | 'approved' | 'rejected' | 'funded'
  created_at: Date
}

// Sigma Select Types
export interface SigmaConfig {
  sales_dashboard: string
  lead_generation: string
  revenue_analytics: string
}

export interface SigmaLead {
  lead_id: string
  source: string
  company_name: string
  contact_name: string
  email: string
  phone?: string
  industry: string
  lead_score: number
  qualification_status: 'unqualified' | 'qualified' | 'disqualified'
  assigned_agent?: string
  created_at: Date
  last_activity: Date
}

export interface SigmaRevenueMetrics {
  period: string
  total_revenue: number
  new_customers: number
  customer_lifetime_value: number
  conversion_rate: number
  average_deal_size: number
  sales_cycle_length: number
  quantum_optimization_applied: boolean
}

// NQBA Core Types
export interface NQBAConfig {
  dynex: DynexConfig
  qsales: QSalesConfig
  flyfox: FlyfoxConfig
  goliath: GoliathConfig
  sigma: SigmaConfig
}

export interface QSalesConfig {
  agent_count: number
  pod_configuration: string
  campaign_channels: string[]
  performance_targets: {
    conversion_rate: number
    roi: number
    revenue_target: number
  }
}

export interface NQBAStatus {
  dynex_quantum: 'ready' | 'initializing' | 'error'
  qsales_division: 'ready' | 'deploying' | 'error'
  flyfox_ai: 'ready' | 'connecting' | 'error'
  goliath_financial: 'ready' | 'connecting' | 'error'
  sigma_select: 'ready' | 'connecting' | 'error'
  overall_status: 'operational' | 'degraded' | 'down'
}

// Quantum Optimization Types
export interface QuantumOptimizationRequest {
  problem_type: 'lead_scoring' | 'campaign_optimization' | 'revenue_prediction' | 'agent_allocation'
  data: any
  constraints?: any
  target_metric: string
}

export interface QuantumOptimizationResult {
  job_id: string
  status: 'pending' | 'processing' | 'completed' | 'failed'
  result?: any
  performance_boost: string
  processing_time: number
  energy_consumption: number
}

// Business Pod Types
export interface BusinessPod {
  pod_id: string
  name: string
  type: 'goliath' | 'flyfox' | 'sigma'
  status: 'active' | 'inactive' | 'maintenance'
  quantum_enhancement: boolean
  performance_metrics: Record<string, number>
  created_at: Date
  last_updated: Date
}

// NQBA Orchestrator Types
export interface NQBAOrchestratorTask {
  task_id: string
  task_type: string
  priority: 'low' | 'medium' | 'high' | 'critical'
  status: 'pending' | 'running' | 'completed' | 'failed'
  assigned_pod?: string
  quantum_optimization_required: boolean
  created_at: Date
  started_at?: Date
  completed_at?: Date
  result?: any
}

// LTC Logger Types
export interface LTCOperation {
  operation_id: string
  operation_type: string
  system: string
  user_id?: string
  timestamp: Date
  details: any
  quantum_enhancement: boolean
  performance_metrics?: Record<string, number>
}

// QSAI Engine Types
export interface QSAIContext {
  context_id: string
  business_pod: string
  current_state: any
  available_actions: string[]
  constraints: any
  quantum_optimization_applied: boolean
}

export interface QSAIAction {
  action_id: string
  action_type: string
  context_id: string
  parameters: any
  confidence_score: number
  quantum_enhancement: boolean
  created_at: Date
}

// QEA-DO Types
export interface QEAAlgorithmBlueprint {
  blueprint_id: string
  algorithm_type: string
  complexity_level: 'basic' | 'standard' | 'enterprise'
  quantum_enhancement: boolean
  target_performance: Record<string, number>
  created_at: Date
}

export interface QEAAlgorithmArtifact {
  artifact_id: string
  blueprint_id: string
  artifact_type: 'code' | 'configuration' | 'documentation'
  content: any
  version: string
  created_at: Date
}

// Marketplace Types
export interface NQBAMarketplaceSolution {
  solution_id: string
  name: string
  description: string
  category: string
  type: string
  pricing_model: 'subscription' | 'one_time' | 'usage_based'
  price: number
  quantum_enhancement: boolean
  business_pod: string
  created_at: Date
  updated_at: Date
}

// API Response Types
export interface NQBAAPIResponse<T = any> {
  success: boolean
  data?: T
  error?: string
  message?: string
  timestamp: Date
  quantum_optimization_applied: boolean
  performance_metrics?: Record<string, number>
}

// Event Types
export interface NQBAEvent {
  event_id: string
  event_type: string
  system: string
  severity: 'info' | 'warning' | 'error' | 'critical'
  message: string
  data?: any
  quantum_enhancement: boolean
  timestamp: Date
}

// Monitoring Types
export interface NQBAMetrics {
  system: string
  timestamp: Date
  metrics: {
    performance: Record<string, number>
    quantum_optimization: Record<string, boolean>
    business_metrics: Record<string, number>
  }
}

// Configuration Types
export interface NQBAEnvironmentConfig {
  environment: 'development' | 'staging' | 'production'
  quantum_backend: 'dynex' | 'simulator' | 'hybrid'
  nvidia_acceleration: boolean
  monitoring_enabled: boolean
  quantum_optimization_enabled: boolean
}

// Security Types
export interface NQBASecurityContext {
  user_id: string
  permissions: string[]
  business_pod_access: string[]
  quantum_access_level: 'basic' | 'advanced' | 'enterprise'
  session_token: string
  expires_at: Date
}
