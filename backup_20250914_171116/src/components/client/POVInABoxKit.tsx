import React, { useState, useEffect, useMemo } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Textarea } from '@/components/ui/textarea';
import { Checkbox } from '@/components/ui/checkbox';
import { LineChart, Line, AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';
import { 
  Package, 
  Rocket, 
  Target, 
  TrendingUp, 
  DollarSign, 
  Users, 
  Clock, 
  Award, 
  Sparkles, 
  Activity, 
  BarChart3, 
  PieChart as PieChartIcon,
  Settings,
  Bell,
  RefreshCw,
  CheckCircle,
  XCircle,
  AlertTriangle,
  ArrowUp,
  ArrowDown,
  Minus,
  Play,
  Pause,
  Calendar,
  Mail,
  Phone,
  MapPin,
  ExternalLink,
  ChevronRight,
  Plus,
  Edit,
  Search,
  Filter,
  Download,
  Upload,
  FileText,
  Database,
  Cpu,
  Network,
  Globe,
  Shield,
  Lightbulb,
  Factory,
  Banknote,
  Truck,
  Building2,
  Briefcase,
  Calculator,
  Microscope,
  Layers,
  GitBranch,
  Workflow,
  Gauge,
  TrendingDown,
  Eye,
  EyeOff,
  Lock,
  Unlock,
  Star,
  Heart,
  ThumbsUp,
  MessageSquare,
  Share2,
  Bookmark,
  Code,
  Terminal,
  Zap,
  Brain,
  Cog,
  FlaskConical,
  LineChart as LineChartIcon,
  Presentation,
  FileSpreadsheet,
  Clipboard,
  Timer,
  CheckSquare,
  AlertCircle,
  Info,
  HelpCircle,
  BookOpen,
  GraduationCap,
  Wrench,
  Hammer
} from 'lucide-react';

interface POVTemplate {
  id: string;
  name: string;
  vertical: string;
  useCase: string;
  description: string;
  duration: string;
  complexity: 'beginner' | 'intermediate' | 'advanced';
  expectedROI: string;
  dataRequirements: string[];
  deliverables: string[];
  successMetrics: string[];
  quantumAdvantage: string;
  classicalComparison: string;
  estimatedValue: number;
  confidence: number;
}

interface POVStep {
  id: string;
  title: string;
  description: string;
  duration: string;
  status: 'pending' | 'in_progress' | 'completed' | 'blocked';
  dependencies: string[];
  deliverables: string[];
  resources: string[];
  automationLevel: number;
}

interface DataIngestionConfig {
  format: string;
  source: string;
  schema: any;
  validation: string[];
  preprocessing: string[];
  sampleSize: number;
  qualityScore: number;
}

const POV_TEMPLATES: POVTemplate[] = [
  {
    id: 'manufacturing-quality',
    name: 'Predictive Quality Control',
    vertical: 'Manufacturing',
    useCase: 'Real-time defect prediction and quality optimization',
    description: 'Quantum-enhanced machine learning for predicting product defects before they occur, reducing scrap rates and improving overall equipment effectiveness.',
    duration: '4-6 weeks',
    complexity: 'intermediate',
    expectedROI: '300-500%',
    dataRequirements: [
      'Production line sensor data (temperature, pressure, vibration)',
      'Historical quality control records',
      'Material composition and batch information',
      'Environmental conditions data',
      'Maintenance logs and equipment status'
    ],
    deliverables: [
      'Quantum-enhanced prediction model',
      'Real-time quality dashboard',
      'ROI analysis and business case',
      'Implementation roadmap',
      'Training materials for operators'
    ],
    successMetrics: [
      'Defect prediction accuracy >95%',
      'Scrap rate reduction >20%',
      'OEE improvement >15%',
      'Cost savings >$500K annually',
      'Implementation time <8 weeks'
    ],
    quantumAdvantage: 'Quantum algorithms excel at finding non-obvious patterns in high-dimensional sensor data, achieving 34% better accuracy than classical ML',
    classicalComparison: 'Traditional ML models plateau at ~78% accuracy due to feature interaction complexity',
    estimatedValue: 2400000,
    confidence: 94.2
  },
  {
    id: 'finance-portfolio',
    name: 'Portfolio Risk Optimization',
    vertical: 'Finance',
    useCase: 'Dynamic portfolio rebalancing with quantum risk modeling',
    description: 'Quantum-powered portfolio optimization that considers complex market correlations and tail risk scenarios for superior risk-adjusted returns.',
    duration: '3-5 weeks',
    complexity: 'advanced',
    expectedROI: '200-400%',
    dataRequirements: [
      'Historical price and volume data',
      'Market volatility indices',
      'Economic indicators and news sentiment',
      'Correlation matrices across asset classes',
      'Risk factor exposures and stress test scenarios'
    ],
    deliverables: [
      'Quantum portfolio optimization engine',
      'Risk analytics dashboard',
      'Backtesting results and performance attribution',
      'Regulatory compliance documentation',
      'Integration with existing trading systems'
    ],
    successMetrics: [
      'Sharpe ratio improvement >25%',
      'Maximum drawdown reduction >30%',
      'Alpha generation >2% annually',
      'Risk model accuracy >90%',
      'Execution time <5 minutes'
    ],
    quantumAdvantage: 'Quantum annealing solves complex portfolio constraints 100x faster while finding globally optimal solutions',
    classicalComparison: 'Classical optimizers often get trapped in local minima, missing 15-20% of potential alpha',
    estimatedValue: 1800000,
    confidence: 91.7
  },
  {
    id: 'logistics-routing',
    name: 'Dynamic Route Optimization',
    vertical: 'Logistics',
    useCase: 'Real-time fleet routing with quantum optimization',
    description: 'Quantum-enhanced vehicle routing that adapts to real-time traffic, weather, and demand changes for maximum efficiency.',
    duration: '5-7 weeks',
    complexity: 'intermediate',
    expectedROI: '250-450%',
    dataRequirements: [
      'GPS tracking and telematics data',
      'Real-time traffic and road condition feeds',
      'Customer delivery windows and priorities',
      'Vehicle capacity and fuel consumption data',
      'Driver schedules and regulatory constraints'
    ],
    deliverables: [
      'Quantum routing optimization engine',
      'Real-time fleet management dashboard',
      'Mobile driver applications',
      'Performance analytics and reporting',
      'Integration with existing logistics systems'
    ],
    successMetrics: [
      'Route efficiency improvement >25%',
      'Fuel cost reduction >20%',
      'On-time delivery rate >98%',
      'Driver satisfaction score >4.5/5',
      'Customer complaints reduction >40%'
    ],
    quantumAdvantage: 'Quantum algorithms handle exponential route combinations, finding optimal solutions 50x faster than classical methods',
    classicalComparison: 'Classical heuristics achieve only 70-80% of optimal efficiency due to computational limitations',
    estimatedValue: 3200000,
    confidence: 89.3
  },
  {
    id: 'energy-grid',
    name: 'Smart Grid Optimization',
    vertical: 'Energy',
    useCase: 'Real-time energy distribution and demand forecasting',
    description: 'Quantum-powered smart grid management that optimizes energy distribution, predicts demand, and integrates renewable sources efficiently.',
    duration: '6-8 weeks',
    complexity: 'advanced',
    expectedROI: '400-600%',
    dataRequirements: [
      'Smart meter consumption data',
      'Weather forecasts and renewable generation',
      'Grid topology and transmission constraints',
      'Energy market prices and demand forecasts',
      'Equipment status and maintenance schedules'
    ],
    deliverables: [
      'Quantum grid optimization platform',
      'Demand forecasting models',
      'Real-time monitoring dashboard',
      'Renewable integration optimizer',
      'Regulatory compliance reporting'
    ],
    successMetrics: [
      'Grid efficiency improvement >20%',
      'Renewable integration >35%',
      'Demand forecast accuracy >95%',
      'Outage reduction >50%',
      'Cost savings >$1M annually'
    ],
    quantumAdvantage: 'Quantum computing handles complex grid constraints and renewable variability with 60% better optimization',
    classicalComparison: 'Classical methods struggle with real-time optimization of large-scale grid networks',
    estimatedValue: 4500000,
    confidence: 87.8
  }
];

const POV_STEPS: POVStep[] = [
  {
    id: 'discovery',
    title: 'Business Discovery & Data Assessment',
    description: 'Understand business objectives, identify key pain points, and assess data quality and availability',
    duration: '3-5 days',
    status: 'pending',
    dependencies: [],
    deliverables: [
      'Business requirements document',
      'Data quality assessment report',
      'Technical feasibility analysis',
      'Success criteria definition'
    ],
    resources: [
      'Business analyst',
      'Data scientist',
      'Solution architect'
    ],
    automationLevel: 40
  },
  {
    id: 'data-preparation',
    title: 'Data Ingestion & Preprocessing',
    description: 'Automated data collection, cleaning, and preparation using standardized pipelines',
    duration: '5-7 days',
    status: 'pending',
    dependencies: ['discovery'],
    deliverables: [
      'Clean, validated dataset',
      'Data pipeline documentation',
      'Quality metrics dashboard',
      'Feature engineering results'
    ],
    resources: [
      'Data engineer',
      'Automated preprocessing tools',
      'Data validation framework'
    ],
    automationLevel: 85
  },
  {
    id: 'model-development',
    title: 'Quantum Model Development',
    description: 'Build and train quantum-enhanced models using NQBA platform and Dynex QaaS',
    duration: '7-10 days',
    status: 'pending',
    dependencies: ['data-preparation'],
    deliverables: [
      'Trained quantum models',
      'Model performance metrics',
      'Hyperparameter optimization results',
      'Model interpretability analysis'
    ],
    resources: [
      'Quantum ML engineer',
      'NQBA platform access',
      'Dynex QaaS compute resources'
    ],
    automationLevel: 70
  },
  {
    id: 'classical-baseline',
    title: 'Classical Baseline Development',
    description: 'Develop classical ML models for direct performance comparison',
    duration: '3-5 days',
    status: 'pending',
    dependencies: ['data-preparation'],
    deliverables: [
      'Classical baseline models',
      'Performance comparison metrics',
      'Computational efficiency analysis',
      'Cost-benefit comparison'
    ],
    resources: [
      'ML engineer',
      'Classical ML frameworks',
      'Performance benchmarking tools'
    ],
    automationLevel: 90
  },
  {
    id: 'validation',
    title: 'Model Validation & Testing',
    description: 'Comprehensive testing of quantum models against business requirements and classical baselines',
    duration: '5-7 days',
    status: 'pending',
    dependencies: ['model-development', 'classical-baseline'],
    deliverables: [
      'Validation test results',
      'A/B testing framework',
      'Statistical significance analysis',
      'Risk assessment report'
    ],
    resources: [
      'QA engineer',
      'Statistical analyst',
      'Validation framework'
    ],
    automationLevel: 75
  },
  {
    id: 'integration',
    title: 'System Integration & Deployment',
    description: 'Integrate quantum models with existing business systems and deploy to production environment',
    duration: '7-10 days',
    status: 'pending',
    dependencies: ['validation'],
    deliverables: [
      'Production deployment',
      'API documentation',
      'Monitoring and alerting setup',
      'User training materials'
    ],
    resources: [
      'DevOps engineer',
      'System administrator',
      'Integration specialist'
    ],
    automationLevel: 60
  },
  {
    id: 'results',
    title: 'Results Analysis & Reporting',
    description: 'Generate comprehensive POV results, ROI analysis, and business case for full implementation',
    duration: '3-5 days',
    status: 'pending',
    dependencies: ['integration'],
    deliverables: [
      'Executive summary report',
      'Detailed technical analysis',
      'ROI calculation and business case',
      'Implementation roadmap'
    ],
    resources: [
      'Business analyst',
      'Technical writer',
      'Executive presentation specialist'
    ],
    automationLevel: 50
  }
];

const DATA_FORMATS = [
  { id: 'csv', name: 'CSV Files', icon: FileSpreadsheet, automation: 95 },
  { id: 'json', name: 'JSON Data', icon: Code, automation: 90 },
  { id: 'sql', name: 'SQL Database', icon: Database, automation: 85 },
  { id: 'api', name: 'REST API', icon: Network, automation: 80 },
  { id: 'streaming', name: 'Real-time Streams', icon: Activity, automation: 70 },
  { id: 'files', name: 'File Systems', icon: FileText, automation: 75 }
];

const COLORS = {
  primary: '#3b82f6',
  secondary: '#10b981',
  accent: '#8b5cf6',
  warning: '#f59e0b',
  error: '#ef4444',
  success: '#10b981',
  quantum: '#6366f1',
  classical: '#6b7280'
};

export const POVInABoxKit: React.FC = () => {
  const [activeTab, setActiveTab] = useState('templates');
  const [selectedTemplate, setSelectedTemplate] = useState<POVTemplate | null>(null);
  const [povSteps, setPovSteps] = useState<POVStep[]>(POV_STEPS);
  const [selectedVertical, setSelectedVertical] = useState('all');
  const [dataConfig, setDataConfig] = useState<DataIngestionConfig | null>(null);
  const [isGeneratingPOV, setIsGeneratingPOV] = useState(false);
  const [povProgress, setPovProgress] = useState(0);

  // Filter templates by vertical
  const filteredTemplates = useMemo(() => {
    if (selectedVertical === 'all') return POV_TEMPLATES;
    return POV_TEMPLATES.filter(template => 
      template.vertical.toLowerCase() === selectedVertical.toLowerCase()
    );
  }, [selectedVertical]);

  // Calculate overall POV progress
  const overallProgress = useMemo(() => {
    const completedSteps = povSteps.filter(step => step.status === 'completed').length;
    return (completedSteps / povSteps.length) * 100;
  }, [povSteps]);

  // Simulate POV generation
  const generatePOV = async (template: POVTemplate) => {
    setIsGeneratingPOV(true);
    setPovProgress(0);
    
    // Simulate step-by-step POV generation
    for (let i = 0; i <= 100; i += 10) {
      await new Promise(resolve => setTimeout(resolve, 200));
      setPovProgress(i);
    }
    
    setIsGeneratingPOV(false);
    setSelectedTemplate(template);
    setActiveTab('execution');
  };

  // Update step status
  const updateStepStatus = (stepId: string, status: POVStep['status']) => {
    setPovSteps(prev => prev.map(step => 
      step.id === stepId ? { ...step, status } : step
    ));
  };

  return (
    <div className="w-full max-w-7xl mx-auto p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="space-y-2">
          <div className="flex items-center space-x-3">
            <div className="relative">
              <Package className="h-8 w-8 text-blue-600" />
              <Sparkles className="h-4 w-4 text-yellow-500 absolute -top-1 -right-1 animate-pulse" />
            </div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              POV in a Box Kit
            </h1>
          </div>
          <p className="text-gray-600">Streamlined, repeatable quantum advantage demonstrations for enterprise sales</p>
        </div>
        
        <div className="flex items-center space-x-3">
          <Badge variant="outline" className="flex items-center space-x-2">
            <Rocket className="h-4 w-4" />
            <span>Ready to Deploy</span>
          </Badge>
          <Button className="bg-gradient-to-r from-blue-600 to-purple-600 text-white">
            <Plus className="h-4 w-4 mr-2" />
            Create Custom POV
          </Button>
        </div>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="templates" className="flex items-center space-x-2">
            <Package className="h-4 w-4" />
            <span>Templates</span>
          </TabsTrigger>
          <TabsTrigger value="execution" className="flex items-center space-x-2">
            <Play className="h-4 w-4" />
            <span>Execution</span>
          </TabsTrigger>
          <TabsTrigger value="data" className="flex items-center space-x-2">
            <Database className="h-4 w-4" />
            <span>Data Setup</span>
          </TabsTrigger>
          <TabsTrigger value="automation" className="flex items-center space-x-2">
            <Cog className="h-4 w-4" />
            <span>Automation</span>
          </TabsTrigger>
          <TabsTrigger value="results" className="flex items-center space-x-2">
            <Presentation className="h-4 w-4" />
            <span>Results</span>
          </TabsTrigger>
        </TabsList>

        {/* Templates Tab */}
        <TabsContent value="templates" className="space-y-6">
          {/* Vertical Filter */}
          <div className="flex items-center space-x-4">
            <Label htmlFor="vertical-filter">Filter by Vertical:</Label>
            <Select value={selectedVertical} onValueChange={setSelectedVertical}>
              <SelectTrigger className="w-48">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Verticals</SelectItem>
                <SelectItem value="manufacturing">Manufacturing</SelectItem>
                <SelectItem value="finance">Finance</SelectItem>
                <SelectItem value="logistics">Logistics</SelectItem>
                <SelectItem value="energy">Energy</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* Template Cards */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {filteredTemplates.map((template) => {
              const complexityColors = {
                beginner: 'bg-green-100 text-green-800',
                intermediate: 'bg-yellow-100 text-yellow-800',
                advanced: 'bg-red-100 text-red-800'
              };
              
              const verticalIcons = {
                Manufacturing: Factory,
                Finance: Banknote,
                Logistics: Truck,
                Energy: Zap
              };
              
              const VerticalIcon = verticalIcons[template.vertical as keyof typeof verticalIcons] || Building2;
              
              return (
                <Card key={template.id} className="hover:shadow-lg transition-shadow cursor-pointer">
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <VerticalIcon className="h-6 w-6 text-blue-600" />
                        <div>
                          <CardTitle className="text-lg">{template.name}</CardTitle>
                          <div className="text-sm text-gray-600">{template.vertical}</div>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Badge className={complexityColors[template.complexity]}>
                          {template.complexity}
                        </Badge>
                        <Badge variant="outline">
                          {template.duration}
                        </Badge>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <p className="text-sm text-gray-700">{template.description}</p>
                    
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <div className="text-sm font-medium text-gray-600">Expected ROI</div>
                        <div className="text-lg font-bold text-green-600">{template.expectedROI}</div>
                      </div>
                      <div>
                        <div className="text-sm font-medium text-gray-600">Confidence</div>
                        <div className="text-lg font-bold text-blue-600">{template.confidence.toFixed(1)}%</div>
                      </div>
                    </div>
                    
                    <div className="space-y-2">
                      <div className="text-sm font-medium text-gray-600">Quantum Advantage:</div>
                      <p className="text-xs text-gray-700 bg-purple-50 p-2 rounded">
                        {template.quantumAdvantage}
                      </p>
                    </div>
                    
                    <div className="space-y-2">
                      <div className="text-sm font-medium text-gray-600">Success Metrics:</div>
                      <div className="space-y-1">
                        {template.successMetrics.slice(0, 3).map((metric, index) => (
                          <div key={index} className="flex items-center space-x-2">
                            <CheckCircle className="h-3 w-3 text-green-600" />
                            <span className="text-xs text-gray-700">{metric}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                    
                    <div className="flex items-center justify-between pt-4 border-t">
                      <div className="text-sm text-gray-600">
                        Est. Value: <span className="font-bold text-green-600">
                          ${template.estimatedValue.toLocaleString()}
                        </span>
                      </div>
                      <Button 
                        onClick={() => generatePOV(template)}
                        className="bg-gradient-to-r from-blue-600 to-purple-600 text-white"
                        disabled={isGeneratingPOV}
                      >
                        {isGeneratingPOV ? (
                          <>
                            <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                            Generating...
                          </>
                        ) : (
                          <>
                            <Rocket className="h-4 w-4 mr-2" />
                            Start POV
                          </>
                        )}
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>

          {/* POV Generation Progress */}
          {isGeneratingPOV && (
            <Card className="bg-blue-50 border-blue-200">
              <CardContent className="p-6">
                <div className="space-y-4">
                  <div className="flex items-center space-x-3">
                    <RefreshCw className="h-6 w-6 text-blue-600 animate-spin" />
                    <div>
                      <div className="font-semibold text-blue-800">Generating POV Package</div>
                      <div className="text-sm text-blue-600">Setting up automated workflows and templates...</div>
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>Progress</span>
                      <span>{povProgress}%</span>
                    </div>
                    <Progress value={povProgress} className="h-3" />
                  </div>
                  
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                    <div className="flex items-center space-x-2">
                      <CheckCircle className="h-4 w-4 text-green-600" />
                      <span>Templates loaded</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <CheckCircle className="h-4 w-4 text-green-600" />
                      <span>Data pipelines ready</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <RefreshCw className="h-4 w-4 text-blue-600 animate-spin" />
                      <span>Models configuring</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Clock className="h-4 w-4 text-gray-400" />
                      <span>Reports pending</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        {/* Execution Tab */}
        <TabsContent value="execution" className="space-y-6">
          {selectedTemplate ? (
            <>
              {/* POV Overview */}
              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div>
                      <CardTitle className="flex items-center space-x-2">
                        <Target className="h-5 w-5 text-blue-600" />
                        <span>{selectedTemplate.name} POV</span>
                      </CardTitle>
                      <div className="text-sm text-gray-600 mt-1">
                        {selectedTemplate.vertical} • {selectedTemplate.duration} • {selectedTemplate.complexity}
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-2xl font-bold text-green-600">
                        {overallProgress.toFixed(0)}%
                      </div>
                      <div className="text-sm text-gray-600">Complete</div>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <Progress value={overallProgress} className="h-3" />
                </CardContent>
              </Card>

              {/* Execution Steps */}
              <div className="space-y-4">
                {povSteps.map((step, index) => {
                  const statusColors = {
                    pending: 'bg-gray-100 text-gray-800 border-gray-200',
                    in_progress: 'bg-blue-100 text-blue-800 border-blue-200',
                    completed: 'bg-green-100 text-green-800 border-green-200',
                    blocked: 'bg-red-100 text-red-800 border-red-200'
                  };
                  
                  const statusIcons = {
                    pending: Clock,
                    in_progress: RefreshCw,
                    completed: CheckCircle,
                    blocked: XCircle
                  };
                  
                  const StatusIcon = statusIcons[step.status];
                  
                  return (
                    <Card key={step.id} className={`${statusColors[step.status]} transition-all hover:shadow-md`}>
                      <CardContent className="p-6">
                        <div className="flex items-start justify-between">
                          <div className="flex items-start space-x-4 flex-1">
                            <div className="flex items-center justify-center w-8 h-8 rounded-full bg-white">
                              <StatusIcon className={`h-4 w-4 ${
                                step.status === 'in_progress' ? 'animate-spin' : ''
                              }`} />
                            </div>
                            
                            <div className="flex-1 space-y-3">
                              <div>
                                <div className="font-semibold text-lg">
                                  Step {index + 1}: {step.title}
                                </div>
                                <div className="text-sm opacity-80">{step.description}</div>
                              </div>
                              
                              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                                <div>
                                  <div className="font-medium mb-1">Duration:</div>
                                  <div className="opacity-80">{step.duration}</div>
                                </div>
                                <div>
                                  <div className="font-medium mb-1">Automation Level:</div>
                                  <div className="flex items-center space-x-2">
                                    <Progress value={step.automationLevel} className="h-2 flex-1" />
                                    <span className="opacity-80">{step.automationLevel}%</span>
                                  </div>
                                </div>
                                <div>
                                  <div className="font-medium mb-1">Resources:</div>
                                  <div className="opacity-80">{step.resources.length} assigned</div>
                                </div>
                              </div>
                              
                              <div className="space-y-2">
                                <div className="font-medium">Deliverables:</div>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-1">
                                  {step.deliverables.map((deliverable, idx) => (
                                    <div key={idx} className="flex items-center space-x-2">
                                      <CheckSquare className="h-3 w-3" />
                                      <span className="text-sm opacity-80">{deliverable}</span>
                                    </div>
                                  ))}
                                </div>
                              </div>
                            </div>
                          </div>
                          
                          <div className="flex flex-col space-y-2">
                            <Button 
                              size="sm" 
                              variant="outline"
                              onClick={() => updateStepStatus(step.id, 
                                step.status === 'completed' ? 'pending' : 
                                step.status === 'pending' ? 'in_progress' : 'completed'
                              )}
                            >
                              {step.status === 'completed' ? 'Reset' : 
                               step.status === 'pending' ? 'Start' : 'Complete'}
                            </Button>
                            
                            {step.status === 'in_progress' && (
                              <Button size="sm" variant="outline" className="text-red-600">
                                <Pause className="h-3 w-3 mr-1" />
                                Pause
                              </Button>
                            )}
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  );
                })}
              </div>
            </>
          ) : (
            <Card>
              <CardContent className="p-12 text-center">
                <Package className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                <div className="text-xl font-semibold text-gray-600 mb-2">
                  No POV Selected
                </div>
                <p className="text-gray-500 mb-6">
                  Choose a POV template from the Templates tab to begin execution
                </p>
                <Button onClick={() => setActiveTab('templates')}>
                  <ChevronRight className="h-4 w-4 mr-2" />
                  Browse Templates
                </Button>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        {/* Data Setup Tab */}
        <TabsContent value="data" className="space-y-6">
          {/* Data Format Selection */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Database className="h-5 w-5 text-blue-600" />
                <span>Automated Data Ingestion</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                {DATA_FORMATS.map((format) => {
                  const FormatIcon = format.icon;
                  return (
                    <Card key={format.id} className="hover:shadow-md transition-shadow cursor-pointer">
                      <CardContent className="p-4 text-center">
                        <FormatIcon className="h-8 w-8 text-blue-600 mx-auto mb-2" />
                        <div className="font-medium mb-1">{format.name}</div>
                        <div className="text-sm text-gray-600 mb-2">
                          {format.automation}% Automated
                        </div>
                        <Progress value={format.automation} className="h-2" />
                      </CardContent>
                    </Card>
                  );
                })}
              </div>
            </CardContent>
          </Card>

          {/* Data Quality Assessment */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <FlaskConical className="h-5 w-5 text-green-600" />
                  <span>Data Quality Metrics</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Completeness</span>
                    <span className="text-sm font-bold">94.2%</span>
                  </div>
                  <Progress value={94.2} className="h-2" />
                  
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Accuracy</span>
                    <span className="text-sm font-bold">97.8%</span>
                  </div>
                  <Progress value={97.8} className="h-2" />
                  
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Consistency</span>
                    <span className="text-sm font-bold">91.5%</span>
                  </div>
                  <Progress value={91.5} className="h-2" />
                  
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Timeliness</span>
                    <span className="text-sm font-bold">89.3%</span>
                  </div>
                  <Progress value={89.3} className="h-2" />
                </div>
                
                <div className="pt-4 border-t">
                  <div className="flex justify-between items-center">
                    <span className="font-medium">Overall Quality Score</span>
                    <span className="text-xl font-bold text-green-600">93.2%</span>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Wrench className="h-5 w-5 text-orange-600" />
                  <span>Preprocessing Pipeline</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-3">
                  <div className="flex items-center space-x-3">
                    <CheckCircle className="h-4 w-4 text-green-600" />
                    <span className="text-sm">Data validation rules applied</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <CheckCircle className="h-4 w-4 text-green-600" />
                    <span className="text-sm">Missing value imputation</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <CheckCircle className="h-4 w-4 text-green-600" />
                    <span className="text-sm">Outlier detection and handling</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <CheckCircle className="h-4 w-4 text-green-600" />
                    <span className="text-sm">Feature scaling and normalization</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <RefreshCw className="h-4 w-4 text-blue-600 animate-spin" />
                    <span className="text-sm">Automated feature engineering</span>
                  </div>
                </div>
                
                <div className="pt-4 border-t">
                  <Button className="w-full">
                    <Play className="h-4 w-4 mr-2" />
                    Run Preprocessing Pipeline
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Sample Data Preview */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Eye className="h-5 w-5 text-purple-600" />
                <span>Sample Data Preview</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="bg-gray-50 p-4 rounded-lg font-mono text-sm overflow-x-auto">
                <div className="grid grid-cols-5 gap-4 mb-2 font-bold">
                  <div>timestamp</div>
                  <div>sensor_temp</div>
                  <div>pressure</div>
                  <div>vibration</div>
                  <div>quality_score</div>
                </div>
                <div className="space-y-1 text-gray-700">
                  <div className="grid grid-cols-5 gap-4">
                    <div>2024-01-15 10:30:00</div>
                    <div>72.3</div>
                    <div>145.2</div>
                    <div>0.023</div>
                    <div>0.94</div>
                  </div>
                  <div className="grid grid-cols-5 gap-4">
                    <div>2024-01-15 10:31:00</div>
                    <div>72.8</div>
                    <div>146.1</div>
                    <div>0.025</div>
                    <div>0.92</div>
                  </div>
                  <div className="grid grid-cols-5 gap-4">
                    <div>2024-01-15 10:32:00</div>
                    <div>73.1</div>
                    <div>144.8</div>
                    <div>0.021</div>
                    <div>0.96</div>
                  </div>
                  <div className="text-center text-gray-500 py-2">... 10,000+ more rows</div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Automation Tab */}
        <TabsContent value="automation" className="space-y-6">
          {/* Automation Overview */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Cog className="h-5 w-5 text-blue-600" />
                <span>POV Automation Level</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="text-center p-6 bg-green-50 rounded-lg">
                  <div className="text-3xl font-bold text-green-600 mb-2">78%</div>
                  <div className="text-sm text-gray-600">Overall Automation</div>
                  <Progress value={78} className="mt-2" />
                </div>
                
                <div className="text-center p-6 bg-blue-50 rounded-lg">
                  <div className="text-3xl font-bold text-blue-600 mb-2">5.2x</div>
                  <div className="text-sm text-gray-600">Faster Deployment</div>
                  <div className="text-xs text-blue-600 mt-1">vs Manual Process</div>
                </div>
                
                <div className="text-center p-6 bg-purple-50 rounded-lg">
                  <div className="text-3xl font-bold text-purple-600 mb-2">92%</div>
                  <div className="text-sm text-gray-600">Consistency Rate</div>
                  <div className="text-xs text-purple-600 mt-1">Across POVs</div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Automation by Step */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <BarChart3 className="h-5 w-5 text-green-600" />
                <span>Automation Breakdown by Step</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {povSteps.map((step, index) => (
                  <div key={step.id} className="flex items-center space-x-4">
                    <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center text-sm font-bold text-blue-600">
                      {index + 1}
                    </div>
                    <div className="flex-1">
                      <div className="font-medium">{step.title}</div>
                      <div className="text-sm text-gray-600">{step.duration}</div>
                    </div>
                    <div className="w-32">
                      <div className="flex justify-between text-sm mb-1">
                        <span>Automation</span>
                        <span>{step.automationLevel}%</span>
                      </div>
                      <Progress value={step.automationLevel} className="h-2" />
                    </div>
                    <div className="w-20 text-right">
                      <Badge variant={step.automationLevel > 80 ? 'default' : step.automationLevel > 60 ? 'secondary' : 'outline'}>
                        {step.automationLevel > 80 ? 'High' : step.automationLevel > 60 ? 'Medium' : 'Low'}
                      </Badge>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Automation Benefits */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Timer className="h-5 w-5 text-orange-600" />
                  <span>Time Savings</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={250}>
                  <BarChart data={[
                    { step: 'Discovery', manual: 5, automated: 2 },
                    { step: 'Data Prep', manual: 10, automated: 2 },
                    { step: 'Modeling', manual: 12, automated: 4 },
                    { step: 'Validation', manual: 8, automated: 2 },
                    { step: 'Integration', manual: 15, automated: 6 },
                    { step: 'Reporting', manual: 6, automated: 3 }
                  ]}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="step" />
                    <YAxis label={{ value: 'Days', angle: -90, position: 'insideLeft' }} />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="manual" fill={COLORS.classical} name="Manual Process" />
                    <Bar dataKey="automated" fill={COLORS.quantum} name="Automated Process" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Award className="h-5 w-5 text-purple-600" />
                  <span>Quality Improvements</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-3">
                  <div className="flex items-center space-x-3">
                    <CheckCircle className="h-5 w-5 text-green-600" />
                    <div className="flex-1">
                      <div className="font-medium">Standardized Templates</div>
                      <div className="text-sm text-gray-600">Consistent POV structure across all verticals</div>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-3">
                    <CheckCircle className="h-5 w-5 text-green-600" />
                    <div className="flex-1">
                      <div className="font-medium">Automated Validation</div>
                      <div className="text-sm text-gray-600">Built-in quality checks and error detection</div>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-3">
                    <CheckCircle className="h-5 w-5 text-green-600" />
                    <div className="flex-1">
                      <div className="font-medium">Reproducible Results</div>
                      <div className="text-sm text-gray-600">Consistent outcomes across different teams</div>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-3">
                    <CheckCircle className="h-5 w-5 text-green-600" />
                    <div className="flex-1">
                      <div className="font-medium">Real-time Monitoring</div>
                      <div className="text-sm text-gray-600">Continuous tracking of POV progress and health</div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Results Tab */}
        <TabsContent value="results" className="space-y-6">
          {/* Results Overview */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Presentation className="h-5 w-5 text-blue-600" />
                <span>POV Results Dashboard</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="text-center p-4 bg-green-50 rounded-lg">
                  <div className="text-2xl font-bold text-green-600">94.7%</div>
                  <div className="text-sm text-gray-600">Success Rate</div>
                </div>
                <div className="text-center p-4 bg-blue-50 rounded-lg">
                  <div className="text-2xl font-bold text-blue-600">3.2x</div>
                  <div className="text-sm text-gray-600">Avg ROI</div>
                </div>
                <div className="text-center p-4 bg-purple-50 rounded-lg">
                  <div className="text-2xl font-bold text-purple-600">18 days</div>
                  <div className="text-sm text-gray-600">Avg Duration</div>
                </div>
                <div className="text-center p-4 bg-orange-50 rounded-lg">
                  <div className="text-2xl font-bold text-orange-600">$2.4M</div>
                  <div className="text-sm text-gray-600">Avg Value</div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Executive Report Generator */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <FileText className="h-5 w-5 text-green-600" />
                <span>Automated Report Generation</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Card className="bg-blue-50 border-blue-200">
                  <CardContent className="p-4 text-center">
                    <Briefcase className="h-8 w-8 text-blue-600 mx-auto mb-2" />
                    <div className="font-medium">Executive Summary</div>
                    <div className="text-sm text-gray-600 mb-3">C-level focused business case</div>
                    <Button size="sm" className="w-full">
                      <Download className="h-3 w-3 mr-2" />
                      Generate PDF
                    </Button>
                  </CardContent>
                </Card>
                
                <Card className="bg-green-50 border-green-200">
                  <CardContent className="p-4 text-center">
                    <LineChartIcon className="h-8 w-8 text-green-600 mx-auto mb-2" />
                    <div className="font-medium">Technical Analysis</div>
                    <div className="text-sm text-gray-600 mb-3">Detailed performance metrics</div>
                    <Button size="sm" className="w-full">
                      <Download className="h-3 w-3 mr-2" />
                      Generate Report
                    </Button>
                  </CardContent>
                </Card>
                
                <Card className="bg-purple-50 border-purple-200">
                  <CardContent className="p-4 text-center">
                    <Calculator className="h-8 w-8 text-purple-600 mx-auto mb-2" />
                    <div className="font-medium">ROI Calculator</div>
                    <div className="text-sm text-gray-600 mb-3">Interactive business case</div>
                    <Button size="sm" className="w-full">
                      <ExternalLink className="h-3 w-3 mr-2" />
                      Open Tool
                    </Button>
                  </CardContent>
                </Card>
              </div>
              
              <div className="bg-gray-50 p-4 rounded-lg">
                <div className="flex items-center space-x-3 mb-3">
                  <Info className="h-5 w-5 text-blue-600" />
                  <div className="font-medium">Automated Report Features</div>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm">
                  <div className="flex items-center space-x-2">
                    <CheckCircle className="h-3 w-3 text-green-600" />
                    <span>Executive summary with key findings</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <CheckCircle className="h-3 w-3 text-green-600" />
                    <span>Quantum vs classical performance comparison</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <CheckCircle className="h-3 w-3 text-green-600" />
                    <span>ROI analysis and business justification</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <CheckCircle className="h-3 w-3 text-green-600" />
                    <span>Implementation roadmap and next steps</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <CheckCircle className="h-3 w-3 text-green-600" />
                    <span>Risk assessment and mitigation strategies</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <CheckCircle className="h-3 w-3 text-green-600" />
                    <span>Customized recommendations by vertical</span>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Success Stories */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Star className="h-5 w-5 text-yellow-500" />
                <span>POV Success Stories</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="p-4 bg-green-50 rounded-lg border-l-4 border-green-500">
                  <div className="flex items-center space-x-3 mb-2">
                    <Factory className="h-5 w-5 text-green-600" />
                    <div className="font-semibold">Global Manufacturing Corp</div>
                    <Badge className="bg-green-100 text-green-800">Manufacturing</Badge>
                  </div>
                  <p className="text-sm text-gray-700 mb-2">
                    "The POV demonstrated 34% improvement in defect prediction accuracy, leading to $2.4M in annual savings. 
                    We signed a 3-year enterprise contract within 6 weeks of POV completion."
                  </p>
                  <div className="flex items-center space-x-4 text-sm">
                    <div className="flex items-center space-x-1">
                      <TrendingUp className="h-3 w-3 text-green-600" />
                      <span>ROI: 420%</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <Clock className="h-3 w-3 text-blue-600" />
                      <span>Duration: 4 weeks</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <DollarSign className="h-3 w-3 text-purple-600" />
                      <span>Contract: $2.4M</span>
                    </div>
                  </div>
                </div>
                
                <div className="p-4 bg-blue-50 rounded-lg border-l-4 border-blue-500">
                  <div className="flex items-center space-x-3 mb-2">
                    <Banknote className="h-5 w-5 text-blue-600" />
                    <div className="font-semibold">FinTech Innovations</div>
                    <Badge className="bg-blue-100 text-blue-800">Finance</Badge>
                  </div>
                  <p className="text-sm text-gray-700 mb-2">
                    "Quantum portfolio optimization delivered 28% better Sharpe ratio and reduced max drawdown by 35%. 
                    The POV convinced our board to approve a $1.8M quantum computing initiative."
                  </p>
                  <div className="flex items-center space-x-4 text-sm">
                    <div className="flex items-center space-x-1">
                      <TrendingUp className="h-3 w-3 text-blue-600" />
                      <span>ROI: 340%</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <Clock className="h-3 w-3 text-blue-600" />
                      <span>Duration: 5 weeks</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <DollarSign className="h-3 w-3 text-purple-600" />
                      <span>Contract: $1.8M</span>
                    </div>
                  </div>
                </div>
                
                <div className="p-4 bg-purple-50 rounded-lg border-l-4 border-purple-500">
                  <div className="flex items-center space-x-3 mb-2">
                    <Truck className="h-5 w-5 text-purple-600" />
                    <div className="font-semibold">LogiFlow Solutions</div>
                    <Badge className="bg-purple-100 text-purple-800">Logistics</Badge>
                  </div>
                  <p className="text-sm text-gray-700 mb-2">
                    "Real-time route optimization reduced fuel costs by 22% and improved delivery times by 18%. 
                    The quantum advantage was undeniable - we expanded to a multi-year partnership."
                  </p>
                  <div className="flex items-center space-x-4 text-sm">
                    <div className="flex items-center space-x-1">
                      <TrendingUp className="h-3 w-3 text-purple-600" />
                      <span>ROI: 380%</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <Clock className="h-3 w-3 text-blue-600" />
                      <span>Duration: 6 weeks</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <DollarSign className="h-3 w-3 text-purple-600" />
                      <span>Contract: $3.2M</span>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Performance Comparison */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <BarChart3 className="h-5 w-5 text-blue-600" />
                  <span>Quantum vs Classical Performance</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={[
                    { metric: 'Accuracy', quantum: 94.7, classical: 78.2 },
                    { metric: 'Speed', quantum: 89.3, classical: 45.6 },
                    { metric: 'Efficiency', quantum: 92.1, classical: 67.8 },
                    { metric: 'Scalability', quantum: 96.4, classical: 52.3 }
                  ]}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="metric" />
                    <YAxis domain={[0, 100]} />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="quantum" fill={COLORS.quantum} name="Quantum Enhanced" />
                    <Bar dataKey="classical" fill={COLORS.classical} name="Classical Methods" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <PieChartIcon className="h-5 w-5 text-green-600" />
                  <span>POV Outcomes Distribution</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={[
                        { name: 'Full Implementation', value: 68, fill: COLORS.success },
                        { name: 'Pilot Extension', value: 22, fill: COLORS.primary },
                        { name: 'Further Evaluation', value: 8, fill: COLORS.warning },
                        { name: 'No Action', value: 2, fill: COLORS.error }
                      ]}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name }) => name}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default POVInABoxKit;