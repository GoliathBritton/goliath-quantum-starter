// Business Pod Types for Goliath Quantum Starter

export interface BusinessPod {
  id: string;
  name: string;
  description: string;
  type: BusinessPodType;
  status: BusinessPodStatus;
  owner: string;
  createdAt: Date;
  updatedAt: Date;
  configuration: BusinessPodConfig;
  metrics: BusinessPodMetrics;
  integrations: Integration[];
}

export type BusinessPodType = 
  | 'flyfox_ai'
  | 'ghost_neuroq'
  | 'goliath_trade'
  | 'sigma_select'
  | 'sfg_symmetry'
  | 'quantum_lead_generator'
  | 'custom';

export type BusinessPodStatus = 
  | 'active'
  | 'inactive'
  | 'pending'
  | 'error'
  | 'maintenance';

export interface BusinessPodConfig {
  autoScale: boolean;
  maxInstances: number;
  minInstances: number;
  resourceLimits: ResourceLimits;
  environment: Record<string, string>;
  secrets: string[];
}

export interface ResourceLimits {
  cpu: string;
  memory: string;
  storage: string;
  network: string;
}

export interface BusinessPodMetrics {
  uptime: number;
  requests: number;
  errors: number;
  responseTime: number;
  throughput: number;
  resourceUsage: ResourceUsage;
  lastUpdated: Date;
}

export interface ResourceUsage {
  cpu: number;
  memory: number;
  storage: number;
  network: number;
}

export interface Integration {
  id: string;
  name: string;
  type: IntegrationType;
  endpoint: string;
  credentials: string;
  status: 'connected' | 'disconnected' | 'error';
  lastSync: Date;
}

export type IntegrationType = 
  | 'api'
  | 'webhook'
  | 'database'
  | 'message_queue'
  | 'file_system'
  | 'quantum_backend';

export interface BusinessPodTemplate {
  id: string;
  name: string;
  description: string;
  type: BusinessPodType;
  defaultConfig: BusinessPodConfig;
  requiredIntegrations: IntegrationType[];
  documentation: string;
}

export interface BusinessPodDeployment {
  id: string;
  podId: string;
  version: string;
  environment: 'development' | 'staging' | 'production';
  status: 'deploying' | 'deployed' | 'failed' | 'rollback';
  deployedAt: Date;
  rollbackVersion?: string;
}