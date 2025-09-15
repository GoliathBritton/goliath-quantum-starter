import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  LineChart, Line, PieChart, Pie, Cell, ScatterChart, Scatter, AreaChart, Area
} from 'recharts';
import {
  Activity, TrendingUp, Zap, Database, Settings, PlayCircle,
  CheckCircle, AlertTriangle, Target, Cpu, Clock, DollarSign,
  ArrowRight, BarChart3, PieChart as PieChartIcon, LineChart as LineChartIcon,
  Workflow, GitBranch, Filter, Search, Download, Upload,
  Eye, Brain, Lightbulb, Shield, Users, Globe
} from 'lucide-react';

// FLYFOX AI Branding Colors - Centralized from brand configuration
const FLYFOX_COLORS = {
  primary: '#14B8A6', // Teal - FLYFOX AI primary
  secondary: '#0F172A', // Black - FLYFOX AI secondary
  accent: '#06B6D4', // Cyan - FLYFOX AI accent
  success: '#10B981',
  warning: '#F59E0B',
  danger: '#EF4444',
  light: '#F8FAFC',
  dark: '#1E293B'
};

// Business Unit Colors for Integration Partners
const BUSINESS_UNIT_COLORS = {
  flyfox: {
    primary: '#14B8A6', // Teal
    secondary: '#0F172A', // Black
    accent: '#06B6D4' // Cyan
  },
  goliath: {
    primary: '#F5C14C', // Gold
    secondary: '#1C1917', // Obsidian
    accent: '#D97706' // Amber
  },
  sigma: {
    primary: '#DC2626', // Crimson
    secondary: '#E5E7EB', // Platinum
    accent: '#EF4444' // Red
  }
};

// QUBO Quantum Integration Data
const QUBO_OPTIMIZATION_DATA = [
  {
    process: 'Resource Allocation',
    classical_time: 45.2,
    quantum_time: 3.8,
    improvement: 91.6,
    variables: 1024,
    constraints: 512,
    solution_quality: 98.7
  },
  {
    process: 'Route Optimization',
    classical_time: 120.5,
    quantum_time: 8.2,
    improvement: 93.2,
    variables: 2048,
    constraints: 1024,
    solution_quality: 99.1
  },
  {
    process: 'Scheduling Optimization',
    classical_time: 78.3,
    quantum_time: 5.1,
    improvement: 93.5,
    variables: 1536,
    constraints: 768,
    solution_quality: 97.9
  }
];

// Integration Partners Data
const INTEGRATION_PARTNERS = {
  n8n: {
    status: 'active',
    workflows: 47,
    automations: 156,
    success_rate: 99.2,
    quantum_enhanced: true
  },
  uipath: {
    status: 'active',
    bots: 23,
    processes: 89,
    efficiency_gain: 67.8,
    quantum_enhanced: true
  },
  nvidia: {
    status: 'active',
    gpu_acceleration: true,
    cuda_cores: 10752,
    performance_boost: 340,
    quantum_simulation: true
  },
  grok: {
    status: 'active',
    ai_insights: 234,
    pattern_recognition: 94.7,
    quantum_nlp: true
  }
};

// Quantum Workflow Templates
const QUANTUM_WORKFLOWS = [
  {
    id: 'qw_001',
    name: 'QUBO Process Optimization',
    description: 'Quantum optimization for complex process variables',
    steps: 8,
    estimated_time: '15 minutes',
    quantum_advantage: '93% faster than classical',
    integrations: ['Celonis', 'n8n', 'NVIDIA CUDA']
  },
  {
    id: 'qw_002',
    name: 'Automated Process Mining',
    description: 'AI-driven process discovery with quantum enhancement',
    steps: 12,
    estimated_time: '25 minutes',
    quantum_advantage: '87% more accurate pattern detection',
    integrations: ['Celonis', 'UiPath', 'Grok']
  },
  {
    id: 'qw_003',
    name: 'Real-time Process Monitoring',
    description: 'Continuous quantum-enhanced process surveillance',
    steps: 6,
    estimated_time: '5 minutes',
    quantum_advantage: '10x faster anomaly detection',
    integrations: ['Celonis', 'n8n', 'NVIDIA']
  }
];

// Sample Celonis Process Mining Data
const PROCESS_MINING_DATA = [
  {
    process: 'Order-to-Cash',
    efficiency: 78,
    bottlenecks: 12,
    automation_potential: 85,
    cost_savings: 2.4,
    cycle_time: 14.2,
    quantum_optimization: 92
  },
  {
    process: 'Procure-to-Pay',
    efficiency: 65,
    bottlenecks: 18,
    automation_potential: 72,
    cost_savings: 1.8,
    cycle_time: 21.5,
    quantum_optimization: 88
  },
  {
    process: 'Lead-to-Quote',
    efficiency: 82,
    bottlenecks: 8,
    automation_potential: 91,
    cost_savings: 3.1,
    cycle_time: 9.7,
    quantum_optimization: 95
  },
  {
    process: 'Issue-to-Resolution',
    efficiency: 71,
    bottlenecks: 15,
    automation_potential: 79,
    cost_savings: 1.9,
    cycle_time: 18.3,
    quantum_optimization: 86
  }
];

const PROCESS_VARIANTS = [
  { variant: 'Happy Path', frequency: 45, efficiency: 95, cost: 120 },
  { variant: 'Manual Approval', frequency: 28, efficiency: 72, cost: 180 },
  { variant: 'Exception Handling', frequency: 15, efficiency: 58, cost: 250 },
  { variant: 'Rework Required', frequency: 12, efficiency: 41, cost: 320 }
];

const OPTIMIZATION_OPPORTUNITIES = [
  {
    id: 'automation_1',
    title: 'Automated Invoice Processing',
    impact: 'High',
    effort: 'Medium',
    savings: '$2.4M',
    timeline: '3 months',
    quantum_advantage: 'Pattern recognition for invoice anomalies',
    status: 'identified'
  },
  {
    id: 'optimization_1',
    title: 'Dynamic Resource Allocation',
    impact: 'Critical',
    effort: 'High',
    savings: '$4.1M',
    timeline: '6 months',
    quantum_advantage: 'Real-time workload optimization',
    status: 'in_progress'
  },
  {
    id: 'prediction_1',
    title: 'Predictive Process Bottlenecks',
    impact: 'High',
    effort: 'Low',
    savings: '$1.8M',
    timeline: '2 months',
    quantum_advantage: 'Multi-variable process forecasting',
    status: 'completed'
  }
];

const CELONIS_METRICS = [
  { metric: 'Process Efficiency', current: 76, target: 90, trend: 'up' },
  { metric: 'Automation Rate', current: 68, target: 85, trend: 'up' },
  { metric: 'Cycle Time Reduction', current: 32, target: 50, trend: 'up' },
  { metric: 'Cost Optimization', current: 28, target: 40, trend: 'up' },
  { metric: 'Compliance Score', current: 94, target: 98, trend: 'stable' }
];

const CelonisIntegration: React.FC = () => {
  const [selectedProcess, setSelectedProcess] = useState('Order-to-Cash');
  const [activeTab, setActiveTab] = useState('overview');
  const [optimizationFilter, setOptimizationFilter] = useState('all');
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const getImpactColor = (impact: string) => {
    switch (impact) {
      case 'Critical': return 'bg-red-500';
      case 'High': return 'bg-orange-500';
      case 'Medium': return 'bg-yellow-500';
      case 'Low': return 'bg-green-500';
      default: return 'bg-gray-500';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'bg-green-500';
      case 'in_progress': return 'bg-blue-500';
      case 'identified': return 'bg-yellow-500';
      default: return 'bg-gray-500';
    }
  };

  const runQuantumAnalysis = () => {
    setIsAnalyzing(true);
    setTimeout(() => setIsAnalyzing(false), 3000);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-6">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-bold text-gray-900 mb-2">
              FLYFOX AI × Celonis Integration
            </h1>
            <p className="text-lg text-gray-600">
              Quantum-Enhanced Process Mining & Optimization Platform
            </p>
          </div>
          <div className="flex items-center space-x-4">
            <Badge className="bg-teal-500 text-white px-4 py-2">
              <Zap className="h-4 w-4 mr-2" />
              Quantum Powered
            </Badge>
            <Button 
              onClick={runQuantumAnalysis}
              disabled={isAnalyzing}
              className="bg-teal-600 hover:bg-teal-700"
            >
              {isAnalyzing ? (
                <>
                  <Activity className="h-4 w-4 mr-2 animate-spin" />
                  Analyzing...
                </>
              ) : (
                <>
                  <Brain className="h-4 w-4 mr-2" />
                  Run Quantum Analysis
                </>
              )}
            </Button>
          </div>
        </div>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
        <TabsList className="grid w-full grid-cols-8">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="processes">Process Mining</TabsTrigger>
          <TabsTrigger value="optimization">Optimization</TabsTrigger>
          <TabsTrigger value="variants">Process Variants</TabsTrigger>
          <TabsTrigger value="automation">Automation</TabsTrigger>
          <TabsTrigger value="qubo">QUBO Quantum</TabsTrigger>
          <TabsTrigger value="integrations">Integrations</TabsTrigger>
          <TabsTrigger value="insights">AI Insights</TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-6">
          {/* Key Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-6">
            {CELONIS_METRICS.map((metric, index) => (
              <Card key={index}>
                <CardContent className="p-6">
                  <div className="flex items-center justify-between mb-4">
                    <div className="text-sm font-medium text-gray-600">{metric.metric}</div>
                    <TrendingUp className={`h-4 w-4 ${
                      metric.trend === 'up' ? 'text-green-500' : 
                      metric.trend === 'down' ? 'text-red-500' : 'text-gray-500'
                    }`} />
                  </div>
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>Current</span>
                      <span className="font-bold">{metric.current}%</span>
                    </div>
                    <Progress value={metric.current} className="h-2" />
                    <div className="flex justify-between text-xs text-gray-500">
                      <span>Target: {metric.target}%</span>
                      <span className="text-teal-600 font-medium">
                        {metric.current >= metric.target ? '✓ Achieved' : `${metric.target - metric.current}% to go`}
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Process Performance Overview */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <BarChart3 className="h-5 w-5 text-teal-600" />
                  <span>Process Efficiency by Type</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={PROCESS_MINING_DATA}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="process" angle={-45} textAnchor="end" height={80} />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="efficiency" fill={FLYFOX_COLORS.primary} name="Efficiency %" />
                      <Bar dataKey="quantum_optimization" fill={FLYFOX_COLORS.accent} name="Quantum Optimized %" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <PieChartIcon className="h-5 w-5 text-teal-600" />
                  <span>Cost Savings Distribution</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={PROCESS_MINING_DATA}
                        cx="50%"
                        cy="50%"
                        outerRadius={80}
                        fill={FLYFOX_COLORS.primary}
                        dataKey="cost_savings"
                      >
                        {PROCESS_MINING_DATA.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={[
                            FLYFOX_COLORS.primary,
                            FLYFOX_COLORS.accent,
                            FLYFOX_COLORS.success,
                            FLYFOX_COLORS.warning
                          ][index % 4]} />
                        ))}
                      </Pie>
                      <Tooltip formatter={(value) => [`$${value}M`, 'Savings']} />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* FLYFOX AI Integration Status */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Zap className="h-5 w-5 text-teal-600" />
                <span>FLYFOX AI Quantum Enhancement Status</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="text-center">
                  <div className="text-3xl font-bold text-teal-600 mb-2">89%</div>
                  <div className="text-sm text-gray-600">Processes Quantum-Enhanced</div>
                  <Progress value={89} className="mt-2" />
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-600 mb-2">$12.2M</div>
                  <div className="text-sm text-gray-600">Annual Savings Identified</div>
                  <div className="text-xs text-green-600 mt-1">↗ 34% vs Classical</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-600 mb-2">47%</div>
                  <div className="text-sm text-gray-600">Cycle Time Reduction</div>
                  <div className="text-xs text-blue-600 mt-1">Quantum Advantage</div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Process Mining Tab */}
        <TabsContent value="processes" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Process Selection */}
            <Card>
              <CardHeader>
                <CardTitle>Select Process</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {PROCESS_MINING_DATA.map((process) => (
                  <Button
                    key={process.process}
                    variant={selectedProcess === process.process ? 'default' : 'outline'}
                    className="w-full justify-start"
                    onClick={() => setSelectedProcess(process.process)}
                  >
                    <Workflow className="h-4 w-4 mr-2" />
                    {process.process}
                  </Button>
                ))}
              </CardContent>
            </Card>

            {/* Process Details */}
            <Card className="lg:col-span-2">
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span>{selectedProcess} Analysis</span>
                  <Badge className="bg-teal-500 text-white">
                    Quantum Enhanced
                  </Badge>
                </CardTitle>
              </CardHeader>
              <CardContent>
                {(() => {
                  const process = PROCESS_MINING_DATA.find(p => p.process === selectedProcess);
                  if (!process) return null;
                  
                  return (
                    <div className="space-y-6">
                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <div className="text-sm text-gray-600">Efficiency Score</div>
                          <div className="text-2xl font-bold text-teal-600">{process.efficiency}%</div>
                          <Progress value={process.efficiency} className="mt-1" />
                        </div>
                        <div>
                          <div className="text-sm text-gray-600">Quantum Optimization</div>
                          <div className="text-2xl font-bold text-blue-600">{process.quantum_optimization}%</div>
                          <Progress value={process.quantum_optimization} className="mt-1" />
                        </div>
                      </div>
                      
                      <div className="grid grid-cols-3 gap-4 text-center">
                        <div>
                          <div className="text-lg font-bold text-red-500">{process.bottlenecks}</div>
                          <div className="text-xs text-gray-600">Bottlenecks</div>
                        </div>
                        <div>
                          <div className="text-lg font-bold text-green-600">${process.cost_savings}M</div>
                          <div className="text-xs text-gray-600">Savings</div>
                        </div>
                        <div>
                          <div className="text-lg font-bold text-blue-600">{process.cycle_time}d</div>
                          <div className="text-xs text-gray-600">Cycle Time</div>
                        </div>
                      </div>
                      
                      <div className="space-y-2">
                        <div className="flex justify-between text-sm">
                          <span>Automation Potential</span>
                          <span className="font-medium">{process.automation_potential}%</span>
                        </div>
                        <Progress value={process.automation_potential} className="h-2" />
                      </div>
                      
                      <div className="flex space-x-2">
                        <Button className="flex-1 bg-teal-600 hover:bg-teal-700">
                          <Eye className="h-4 w-4 mr-2" />
                          View Process Map
                        </Button>
                        <Button variant="outline" className="flex-1">
                          <Download className="h-4 w-4 mr-2" />
                          Export Analysis
                        </Button>
                      </div>
                    </div>
                  );
                })()}
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Optimization Tab */}
        <TabsContent value="optimization" className="space-y-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold">Quantum-Powered Optimization Opportunities</h2>
            <div className="flex items-center space-x-4">
              <Select value={optimizationFilter} onValueChange={setOptimizationFilter}>
                <SelectTrigger className="w-48">
                  <SelectValue placeholder="Filter by impact" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Opportunities</SelectItem>
                  <SelectItem value="Critical">Critical Impact</SelectItem>
                  <SelectItem value="High">High Impact</SelectItem>
                  <SelectItem value="Medium">Medium Impact</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
            {OPTIMIZATION_OPPORTUNITIES
              .filter(opp => optimizationFilter === 'all' || opp.impact === optimizationFilter)
              .map((opportunity) => (
              <Card key={opportunity.id} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    <span className="text-lg">{opportunity.title}</span>
                    <div className="flex items-center space-x-2">
                      <Badge className={getImpactColor(opportunity.impact)}>
                        {opportunity.impact}
                      </Badge>
                      <div className={`w-3 h-3 rounded-full ${getStatusColor(opportunity.status)}`} />
                    </div>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <div className="text-gray-600">Savings</div>
                      <div className="font-bold text-green-600">{opportunity.savings}</div>
                    </div>
                    <div>
                      <div className="text-gray-600">Timeline</div>
                      <div className="font-bold">{opportunity.timeline}</div>
                    </div>
                  </div>
                  
                  <div>
                    <div className="text-sm text-gray-600 mb-2">Quantum Advantage</div>
                    <p className="text-sm bg-teal-50 p-3 rounded-lg border-l-4 border-teal-500">
                      {opportunity.quantum_advantage}
                    </p>
                  </div>
                  
                  <div className="flex space-x-2">
                    <Button size="sm" className="flex-1 bg-teal-600 hover:bg-teal-700">
                      <PlayCircle className="h-4 w-4 mr-2" />
                      Implement
                    </Button>
                    <Button size="sm" variant="outline">
                      <Eye className="h-4 w-4 mr-2" />
                      Details
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* Process Variants Tab */}
        <TabsContent value="variants" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <GitBranch className="h-5 w-5 text-teal-600" />
                <span>Process Variant Analysis</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <ScatterChart>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="frequency" name="Frequency" unit="%" />
                      <YAxis dataKey="efficiency" name="Efficiency" unit="%" />
                      <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                      <Scatter name="Process Variants" data={PROCESS_VARIANTS} fill={FLYFOX_COLORS.primary} />
                    </ScatterChart>
                  </ResponsiveContainer>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  {PROCESS_VARIANTS.map((variant, index) => (
                    <Card key={index} className="border-l-4 border-teal-500">
                      <CardContent className="p-4">
                        <h3 className="font-semibold mb-2">{variant.variant}</h3>
                        <div className="space-y-2 text-sm">
                          <div className="flex justify-between">
                            <span>Frequency:</span>
                            <span className="font-medium">{variant.frequency}%</span>
                          </div>
                          <div className="flex justify-between">
                            <span>Efficiency:</span>
                            <span className="font-medium">{variant.efficiency}%</span>
                          </div>
                          <div className="flex justify-between">
                            <span>Cost:</span>
                            <span className="font-medium">${variant.cost}</span>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Automation Tab */}
        <TabsContent value="automation" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Settings className="h-5 w-5 text-teal-600" />
                  <span>Automation Readiness</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {PROCESS_MINING_DATA.map((process, index) => (
                    <div key={index} className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span>{process.process}</span>
                        <span className="font-medium">{process.automation_potential}%</span>
                      </div>
                      <Progress value={process.automation_potential} className="h-2" />
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Cpu className="h-5 w-5 text-teal-600" />
                  <span>Quantum Automation Benefits</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="bg-teal-50 p-4 rounded-lg border-l-4 border-teal-500">
                  <h3 className="font-semibold text-teal-800 mb-2">Pattern Recognition</h3>
                  <p className="text-sm text-teal-700">
                    Quantum algorithms identify complex process patterns 10x faster than classical methods
                  </p>
                </div>
                
                <div className="bg-blue-50 p-4 rounded-lg border-l-4 border-blue-500">
                  <h3 className="font-semibold text-blue-800 mb-2">Optimization</h3>
                  <p className="text-sm text-blue-700">
                    Real-time process optimization considering thousands of variables simultaneously
                  </p>
                </div>
                
                <div className="bg-green-50 p-4 rounded-lg border-l-4 border-green-500">
                  <h3 className="font-semibold text-green-800 mb-2">Predictive Analytics</h3>
                  <p className="text-sm text-green-700">
                    Quantum-enhanced forecasting prevents bottlenecks before they occur
                  </p>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* QUBO Quantum Tab */}
        <TabsContent value="qubo" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Cpu className="h-5 w-5 text-teal-600" />
                  <span>QUBO Optimization Performance</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={QUBO_OPTIMIZATION_DATA}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="process" angle={-45} textAnchor="end" height={80} />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="classical_time" fill="#EF4444" name="Classical Time (min)" />
                      <Bar dataKey="quantum_time" fill={FLYFOX_COLORS.primary} name="Quantum Time (min)" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Zap className="h-5 w-5 text-teal-600" />
                  <span>Quantum Advantage Metrics</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {QUBO_OPTIMIZATION_DATA.map((item, index) => (
                  <div key={index} className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>{item.process}</span>
                      <span className="font-bold text-green-600">{item.improvement}% faster</span>
                    </div>
                    <Progress value={item.improvement} className="h-2" />
                    <div className="grid grid-cols-3 gap-2 text-xs text-gray-600">
                      <div>Variables: {item.variables}</div>
                      <div>Constraints: {item.constraints}</div>
                      <div>Quality: {item.solution_quality}%</div>
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Workflow className="h-5 w-5 text-teal-600" />
                <span>Quantum Workflow Templates</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {QUANTUM_WORKFLOWS.map((workflow) => (
                  <Card key={workflow.id} className="border-l-4 border-teal-500 hover:shadow-lg transition-shadow">
                    <CardContent className="p-4">
                      <h3 className="font-semibold mb-2">{workflow.name}</h3>
                      <p className="text-sm text-gray-600 mb-3">{workflow.description}</p>
                      
                      <div className="space-y-2 text-sm">
                        <div className="flex justify-between">
                          <span>Steps:</span>
                          <span className="font-medium">{workflow.steps}</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Time:</span>
                          <span className="font-medium">{workflow.estimated_time}</span>
                        </div>
                      </div>
                      
                      <div className="mt-3 p-2 bg-teal-50 rounded text-xs text-teal-700">
                        <strong>Quantum Advantage:</strong> {workflow.quantum_advantage}
                      </div>
                      
                      <div className="mt-3">
                        <div className="text-xs text-gray-600 mb-1">Integrations:</div>
                        <div className="flex flex-wrap gap-1">
                          {workflow.integrations.map((integration, idx) => (
                            <Badge key={idx} variant="outline" className="text-xs">
                              {integration}
                            </Badge>
                          ))}
                        </div>
                      </div>
                      
                      <Button className="w-full mt-4 bg-teal-600 hover:bg-teal-700" size="sm">
                        <PlayCircle className="h-4 w-4 mr-2" />
                        Deploy Workflow
                      </Button>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Integrations Tab */}
        <TabsContent value="integrations" className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {/* n8n Integration */}
            <Card className="border-l-4 border-purple-500">
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span className="flex items-center space-x-2">
                    <Workflow className="h-5 w-5 text-purple-600" />
                    <span>n8n</span>
                  </span>
                  <Badge className="bg-green-500 text-white">Active</Badge>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <div className="text-gray-600">Workflows</div>
                    <div className="font-bold text-purple-600">{INTEGRATION_PARTNERS.n8n.workflows}</div>
                  </div>
                  <div>
                    <div className="text-gray-600">Automations</div>
                    <div className="font-bold text-purple-600">{INTEGRATION_PARTNERS.n8n.automations}</div>
                  </div>
                </div>
                
                <div>
                  <div className="text-sm text-gray-600 mb-1">Success Rate</div>
                  <Progress value={INTEGRATION_PARTNERS.n8n.success_rate} className="h-2" />
                  <div className="text-xs text-right mt-1">{INTEGRATION_PARTNERS.n8n.success_rate}%</div>
                </div>
                
                <div className="flex items-center space-x-2 text-sm">
                  <Zap className="h-4 w-4 text-teal-500" />
                  <span className="text-teal-600 font-medium">Quantum Enhanced</span>
                </div>
                
                <Button className="w-full" variant="outline">
                  <Settings className="h-4 w-4 mr-2" />
                  Configure
                </Button>
              </CardContent>
            </Card>

            {/* UiPath Integration */}
            <Card className="border-l-4 border-blue-500">
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span className="flex items-center space-x-2">
                    <Settings className="h-5 w-5 text-blue-600" />
                    <span>UiPath</span>
                  </span>
                  <Badge className="bg-green-500 text-white">Active</Badge>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <div className="text-gray-600">Bots</div>
                    <div className="font-bold text-blue-600">{INTEGRATION_PARTNERS.uipath.bots}</div>
                  </div>
                  <div>
                    <div className="text-gray-600">Processes</div>
                    <div className="font-bold text-blue-600">{INTEGRATION_PARTNERS.uipath.processes}</div>
                  </div>
                </div>
                
                <div>
                  <div className="text-sm text-gray-600 mb-1">Efficiency Gain</div>
                  <Progress value={INTEGRATION_PARTNERS.uipath.efficiency_gain} className="h-2" />
                  <div className="text-xs text-right mt-1">{INTEGRATION_PARTNERS.uipath.efficiency_gain}%</div>
                </div>
                
                <div className="flex items-center space-x-2 text-sm">
                  <Zap className="h-4 w-4 text-teal-500" />
                  <span className="text-teal-600 font-medium">Quantum Enhanced</span>
                </div>
                
                <Button className="w-full" variant="outline">
                  <Settings className="h-4 w-4 mr-2" />
                  Configure
                </Button>
              </CardContent>
            </Card>

            {/* NVIDIA Integration */}
            <Card className="border-l-4 border-green-500">
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span className="flex items-center space-x-2">
                    <Cpu className="h-5 w-5 text-green-600" />
                    <span>NVIDIA CUDA</span>
                  </span>
                  <Badge className="bg-green-500 text-white">Active</Badge>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 gap-4 text-sm">
                  <div>
                    <div className="text-gray-600">CUDA Cores</div>
                    <div className="font-bold text-green-600">{INTEGRATION_PARTNERS.nvidia.cuda_cores.toLocaleString()}</div>
                  </div>
                  <div>
                    <div className="text-gray-600">Performance Boost</div>
                    <div className="font-bold text-green-600">{INTEGRATION_PARTNERS.nvidia.performance_boost}x</div>
                  </div>
                </div>
                
                <div className="space-y-2">
                  <div className="flex items-center space-x-2 text-sm">
                    <CheckCircle className="h-4 w-4 text-green-500" />
                    <span>GPU Acceleration</span>
                  </div>
                  <div className="flex items-center space-x-2 text-sm">
                    <Zap className="h-4 w-4 text-teal-500" />
                    <span className="text-teal-600 font-medium">Quantum Simulation</span>
                  </div>
                </div>
                
                <Button className="w-full" variant="outline">
                  <Settings className="h-4 w-4 mr-2" />
                  Configure
                </Button>
              </CardContent>
            </Card>

            {/* Grok Integration */}
            <Card className="border-l-4 border-orange-500">
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span className="flex items-center space-x-2">
                    <Brain className="h-5 w-5 text-orange-600" />
                    <span>Grok AI</span>
                  </span>
                  <Badge className="bg-green-500 text-white">Active</Badge>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 gap-4 text-sm">
                  <div>
                    <div className="text-gray-600">AI Insights</div>
                    <div className="font-bold text-orange-600">{INTEGRATION_PARTNERS.grok.ai_insights}</div>
                  </div>
                  <div>
                    <div className="text-gray-600">Pattern Recognition</div>
                    <div className="font-bold text-orange-600">{INTEGRATION_PARTNERS.grok.pattern_recognition}%</div>
                  </div>
                </div>
                
                <div>
                  <div className="text-sm text-gray-600 mb-1">Recognition Accuracy</div>
                  <Progress value={INTEGRATION_PARTNERS.grok.pattern_recognition} className="h-2" />
                  <div className="text-xs text-right mt-1">{INTEGRATION_PARTNERS.grok.pattern_recognition}%</div>
                </div>
                
                <div className="flex items-center space-x-2 text-sm">
                  <Zap className="h-4 w-4 text-teal-500" />
                  <span className="text-teal-600 font-medium">Quantum NLP</span>
                </div>
                
                <Button className="w-full" variant="outline">
                  <Settings className="h-4 w-4 mr-2" />
                  Configure
                </Button>
              </CardContent>
            </Card>
          </div>

          {/* Integration Value Proposition */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Globe className="h-5 w-5 text-teal-600" />
                <span>Integration Value Proposition</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg">Unified Quantum-Enhanced Ecosystem</h3>
                  <div className="space-y-3">
                    <div className="bg-purple-50 p-4 rounded-lg border-l-4 border-purple-500">
                      <h4 className="font-medium text-purple-800">n8n Workflow Automation</h4>
                      <p className="text-sm text-purple-700 mt-1">
                        Quantum-enhanced workflow orchestration with 99.2% success rate and intelligent process routing
                      </p>
                    </div>
                    <div className="bg-blue-50 p-4 rounded-lg border-l-4 border-blue-500">
                      <h4 className="font-medium text-blue-800">UiPath RPA Integration</h4>
                      <p className="text-sm text-blue-700 mt-1">
                        Quantum-optimized robotic process automation delivering 67.8% efficiency improvements
                      </p>
                    </div>
                  </div>
                </div>
                
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg">Advanced Computing & AI</h3>
                  <div className="space-y-3">
                    <div className="bg-green-50 p-4 rounded-lg border-l-4 border-green-500">
                      <h4 className="font-medium text-green-800">NVIDIA CUDA Acceleration</h4>
                      <p className="text-sm text-green-700 mt-1">
                        340x performance boost with 10,752 CUDA cores enabling real-time quantum simulations
                      </p>
                    </div>
                    <div className="bg-orange-50 p-4 rounded-lg border-l-4 border-orange-500">
                      <h4 className="font-medium text-orange-800">Grok AI Intelligence</h4>
                      <p className="text-sm text-orange-700 mt-1">
                        Quantum NLP with 94.7% pattern recognition accuracy for advanced process insights
                      </p>
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="mt-6 p-4 bg-teal-50 rounded-lg border border-teal-200">
                <h3 className="font-semibold text-teal-800 mb-2">Combined Platform Value</h3>
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-center">
                  <div>
                    <div className="text-2xl font-bold text-teal-600">$47.3M</div>
                    <div className="text-sm text-gray-600">Annual Value Creation</div>
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-blue-600">89%</div>
                    <div className="text-sm text-gray-600">Process Optimization</div>
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-green-600">340x</div>
                    <div className="text-sm text-gray-600">Performance Acceleration</div>
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-purple-600">99.2%</div>
                    <div className="text-sm text-gray-600">Automation Success</div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* AI Insights Tab */}
        <TabsContent value="insights" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Brain className="h-5 w-5 text-teal-600" />
                <span>FLYFOX AI Quantum Insights</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <h3 className="font-semibold flex items-center space-x-2">
                    <Lightbulb className="h-4 w-4 text-yellow-500" />
                    <span>Key Insights</span>
                  </h3>
                  <div className="space-y-3">
                    <div className="bg-yellow-50 p-4 rounded-lg border-l-4 border-yellow-500">
                      <p className="text-sm">
                        <strong>Order-to-Cash optimization:</strong> Quantum routing algorithms can reduce processing time by 47% while maintaining 99.8% accuracy.
                      </p>
                    </div>
                    <div className="bg-blue-50 p-4 rounded-lg border-l-4 border-blue-500">
                      <p className="text-sm">
                        <strong>Anomaly Detection:</strong> FLYFOX AI identified 23 previously unknown process deviations, saving $1.2M annually.
                      </p>
                    </div>
                    <div className="bg-green-50 p-4 rounded-lg border-l-4 border-green-500">
                      <p className="text-sm">
                        <strong>Resource Optimization:</strong> Dynamic allocation using quantum algorithms improved resource utilization by 34%.
                      </p>
                    </div>
                  </div>
                </div>
                
                <div className="space-y-4">
                  <h3 className="font-semibold flex items-center space-x-2">
                    <Target className="h-4 w-4 text-red-500" />
                    <span>Recommendations</span>
                  </h3>
                  <div className="space-y-3">
                    <div className="bg-red-50 p-4 rounded-lg border-l-4 border-red-500">
                      <p className="text-sm">
                        <strong>Priority 1:</strong> Implement quantum-enhanced invoice processing to eliminate 89% of manual reviews.
                      </p>
                    </div>
                    <div className="bg-orange-50 p-4 rounded-lg border-l-4 border-orange-500">
                      <p className="text-sm">
                        <strong>Priority 2:</strong> Deploy predictive bottleneck detection for Procure-to-Pay process.
                      </p>
                    </div>
                    <div className="bg-purple-50 p-4 rounded-lg border-l-4 border-purple-500">
                      <p className="text-sm">
                        <strong>Priority 3:</strong> Integrate quantum optimization for cross-process resource allocation.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="border-t pt-6">
                <h3 className="font-semibold mb-4 flex items-center space-x-2">
                  <Shield className="h-4 w-4 text-green-500" />
                  <span>Quantum Advantage Summary</span>
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="text-center p-4 bg-teal-50 rounded-lg">
                    <div className="text-2xl font-bold text-teal-600">10x</div>
                    <div className="text-sm text-gray-600">Faster Pattern Recognition</div>
                  </div>
                  <div className="text-center p-4 bg-blue-50 rounded-lg">
                    <div className="text-2xl font-bold text-blue-600">47%</div>
                    <div className="text-sm text-gray-600">Cycle Time Reduction</div>
                  </div>
                  <div className="text-center p-4 bg-green-50 rounded-lg">
                    <div className="text-2xl font-bold text-green-600">$12.2M</div>
                    <div className="text-sm text-gray-600">Annual Savings</div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default CelonisIntegration;