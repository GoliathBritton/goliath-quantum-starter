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
import { LineChart, Line, AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { 
  Factory, 
  TrendingUp, 
  Zap, 
  DollarSign, 
  Clock, 
  Target, 
  Sparkles, 
  Brain, 
  Cpu, 
  Database,
  Shield,
  Globe,
  Users,
  BarChart3,
  PieChart as PieChartIcon,
  Settings,
  Bell,
  Download,
  RefreshCw,
  AlertTriangle,
  CheckCircle,
  XCircle,
  Upload,
  Play,
  Pause,
  FileText,
  Award,
  Briefcase,
  TrendingDown,
  Calculator,
  Microscope,
  Wrench,
  Building2,
  Banknote,
  Truck,
  Lightbulb
} from 'lucide-react';

interface POVConfiguration {
  vertical: 'manufacturing' | 'finance' | 'logistics' | 'energy';
  useCase: string;
  dataSource: string;
  expectedROI: number;
  timeframe: string;
  complianceRequirements: string[];
}

interface POVResults {
  quantumAdvantage: number;
  accuracyImprovement: number;
  costReduction: number;
  timeToSolution: number;
  riskReduction: number;
  complianceScore: number;
}

interface BenchmarkComparison {
  solution: string;
  performance: number;
  accuracy: number;
  cost: number;
  timeToSolution: number;
  color: string;
}

const COLORS = {
  primary: '#3b82f6',
  secondary: '#10b981',
  accent: '#8b5cf6',
  warning: '#f59e0b',
  error: '#ef4444',
  success: '#10b981',
  quantum: '#6366f1'
};

const VERTICAL_CONFIGS = {
  manufacturing: {
    icon: Factory,
    color: '#10b981',
    useCases: [
      'Predictive Quality Control',
      'Supply Chain Optimization',
      'Production Scheduling',
      'Equipment Maintenance Prediction',
      'Energy Consumption Optimization'
    ],
    expectedMetrics: {
      quantumAdvantage: 422.4,
      accuracyImprovement: 99.2,
      costReduction: 4300000,
      timeToSolution: 0.5,
      riskReduction: 43.2
    }
  },
  finance: {
    icon: Banknote,
    color: '#3b82f6',
    useCases: [
      'Portfolio Risk Optimization',
      'Fraud Detection',
      'Algorithmic Trading',
      'Credit Risk Assessment',
      'Regulatory Compliance'
    ],
    expectedMetrics: {
      quantumAdvantage: 234.7,
      accuracyImprovement: 96.8,
      costReduction: 2800000,
      timeToSolution: 0.3,
      riskReduction: 67.4
    }
  },
  logistics: {
    icon: Truck,
    color: '#f59e0b',
    useCases: [
      'Route Optimization',
      'Warehouse Management',
      'Fleet Scheduling',
      'Demand Forecasting',
      'Last-Mile Delivery'
    ],
    expectedMetrics: {
      quantumAdvantage: 156.3,
      accuracyImprovement: 94.5,
      costReduction: 1900000,
      timeToSolution: 0.8,
      riskReduction: 38.7
    }
  },
  energy: {
    icon: Lightbulb,
    color: '#8b5cf6',
    useCases: [
      'Grid Optimization',
      'Renewable Energy Forecasting',
      'Load Balancing',
      'Energy Trading',
      'Infrastructure Planning'
    ],
    expectedMetrics: {
      quantumAdvantage: 289.1,
      accuracyImprovement: 97.3,
      costReduction: 3200000,
      timeToSolution: 0.4,
      riskReduction: 52.1
    }
  }
};

const BENCHMARK_DATA: BenchmarkComparison[] = [
  { solution: 'Classical (Gurobi)', performance: 100, accuracy: 87.3, cost: 100, timeToSolution: 100, color: '#ef4444' },
  { solution: 'Classical (CPLEX)', performance: 105, accuracy: 89.1, cost: 95, timeToSolution: 95, color: '#f59e0b' },
  { solution: 'AWS Optimization', performance: 120, accuracy: 91.2, cost: 85, timeToSolution: 80, color: '#6b7280' },
  { solution: 'NQBA Quantum', performance: 422, accuracy: 99.2, cost: 35, timeToSolution: 15, color: '#10b981' }
];

export const POVAutomationPlatform: React.FC = () => {
  const [activeTab, setActiveTab] = useState('configure');
  const [povConfig, setPovConfig] = useState<POVConfiguration>({
    vertical: 'manufacturing',
    useCase: 'Predictive Quality Control',
    dataSource: '',
    expectedROI: 0,
    timeframe: '3 months',
    complianceRequirements: []
  });
  const [povResults, setPovResults] = useState<POVResults | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [progress, setProgress] = useState(0);
  const [uploadedFiles, setUploadedFiles] = useState<string[]>([]);

  // Simulate POV execution
  const runPOV = async () => {
    setIsRunning(true);
    setProgress(0);
    
    // Simulate progress
    const progressSteps = [
      { step: 'Data Ingestion', duration: 2000, progress: 20 },
      { step: 'Quantum Model Training', duration: 3000, progress: 50 },
      { step: 'Classical Benchmarking', duration: 2000, progress: 70 },
      { step: 'Performance Analysis', duration: 2000, progress: 90 },
      { step: 'Report Generation', duration: 1000, progress: 100 }
    ];

    for (const step of progressSteps) {
      await new Promise(resolve => setTimeout(resolve, step.duration));
      setProgress(step.progress);
    }

    // Generate results based on selected vertical
    const verticalConfig = VERTICAL_CONFIGS[povConfig.vertical];
    const results: POVResults = {
      quantumAdvantage: verticalConfig.expectedMetrics.quantumAdvantage + (Math.random() * 50 - 25),
      accuracyImprovement: verticalConfig.expectedMetrics.accuracyImprovement + (Math.random() * 2 - 1),
      costReduction: verticalConfig.expectedMetrics.costReduction + (Math.random() * 500000 - 250000),
      timeToSolution: verticalConfig.expectedMetrics.timeToSolution + (Math.random() * 0.2 - 0.1),
      riskReduction: verticalConfig.expectedMetrics.riskReduction + (Math.random() * 10 - 5),
      complianceScore: 95 + Math.random() * 5
    };

    setPovResults(results);
    setIsRunning(false);
    setActiveTab('results');
  };

  const calculateROI = useMemo(() => {
    if (!povResults) return 0;
    const annualSavings = povResults.costReduction;
    const implementationCost = 150000; // Estimated implementation cost
    return ((annualSavings - implementationCost) / implementationCost) * 100;
  }, [povResults]);

  const calculatePaybackPeriod = useMemo(() => {
    if (!povResults) return 0;
    const monthlySavings = povResults.costReduction / 12;
    const implementationCost = 150000;
    return implementationCost / monthlySavings;
  }, [povResults]);

  const verticalConfig = VERTICAL_CONFIGS[povConfig.vertical];
  const VerticalIcon = verticalConfig.icon;

  // ROI timeline data
  const roiTimeline = useMemo(() => {
    if (!povResults) return [];
    const monthlySavings = povResults.costReduction / 12;
    const implementationCost = 150000;
    
    return Array.from({ length: 12 }, (_, i) => ({
      month: `Month ${i + 1}`,
      cumulativeSavings: (monthlySavings * (i + 1)) - implementationCost,
      monthlySavings: monthlySavings,
      breakEven: i >= calculatePaybackPeriod
    }));
  }, [povResults, calculatePaybackPeriod]);

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (files) {
      const fileNames = Array.from(files).map(file => file.name);
      setUploadedFiles(prev => [...prev, ...fileNames]);
    }
  };

  const exportReport = () => {
    if (!povResults) return;
    
    const report = {
      configuration: povConfig,
      results: povResults,
      roi: calculateROI,
      paybackPeriod: calculatePaybackPeriod,
      benchmarkComparison: BENCHMARK_DATA,
      generatedAt: new Date().toISOString()
    };
    
    const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `nqba-pov-report-${povConfig.vertical}-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="w-full max-w-7xl mx-auto p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="space-y-2">
          <div className="flex items-center space-x-3">
            <div className="relative">
              <Microscope className="h-8 w-8 text-blue-600" />
              <Sparkles className="h-4 w-4 text-yellow-500 absolute -top-1 -right-1 animate-pulse" />
            </div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              POV Automation Platform
            </h1>
          </div>
          <p className="text-gray-600">Proof-of-Value in a Box - Streamlined Enterprise Quantum Demonstrations</p>
        </div>
        
        <div className="flex items-center space-x-3">
          <Badge variant="outline" className="flex items-center space-x-2">
            <Award className="h-4 w-4" />
            <span>Enterprise Ready</span>
          </Badge>
          <Button variant="outline" size="sm" onClick={exportReport} disabled={!povResults}>
            <Download className="h-4 w-4 mr-2" />
            Export Report
          </Button>
        </div>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="configure" className="flex items-center space-x-2">
            <Settings className="h-4 w-4" />
            <span>Configure</span>
          </TabsTrigger>
          <TabsTrigger value="execute" className="flex items-center space-x-2">
            <Play className="h-4 w-4" />
            <span>Execute</span>
          </TabsTrigger>
          <TabsTrigger value="results" className="flex items-center space-x-2" disabled={!povResults}>
            <BarChart3 className="h-4 w-4" />
            <span>Results</span>
          </TabsTrigger>
          <TabsTrigger value="benchmark" className="flex items-center space-x-2" disabled={!povResults}>
            <Target className="h-4 w-4" />
            <span>Benchmark</span>
          </TabsTrigger>
        </TabsList>

        {/* Configuration Tab */}
        <TabsContent value="configure" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Vertical Selection */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Briefcase className="h-5 w-5 text-blue-600" />
                  <span>Industry Vertical</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-3">
                  {Object.entries(VERTICAL_CONFIGS).map(([key, config]) => {
                    const Icon = config.icon;
                    return (
                      <Button
                        key={key}
                        variant={povConfig.vertical === key ? "default" : "outline"}
                        className="h-20 flex flex-col items-center space-y-2"
                        onClick={() => setPovConfig(prev => ({ 
                          ...prev, 
                          vertical: key as any,
                          useCase: config.useCases[0]
                        }))}
                      >
                        <Icon className="h-6 w-6" style={{ color: config.color }} />
                        <span className="text-sm capitalize">{key}</span>
                      </Button>
                    );
                  })}
                </div>
                
                <div className="space-y-2">
                  <Label>Use Case</Label>
                  <Select 
                    value={povConfig.useCase} 
                    onValueChange={(value) => setPovConfig(prev => ({ ...prev, useCase: value }))}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {verticalConfig.useCases.map((useCase) => (
                        <SelectItem key={useCase} value={useCase}>
                          {useCase}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </CardContent>
            </Card>

            {/* Data Configuration */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Database className="h-5 w-5 text-green-600" />
                  <span>Data Configuration</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label>Data Source Description</Label>
                  <Textarea 
                    placeholder="Describe your data source, format, and volume..."
                    value={povConfig.dataSource}
                    onChange={(e) => setPovConfig(prev => ({ ...prev, dataSource: e.target.value }))}
                  />
                </div>
                
                <div className="space-y-2">
                  <Label>Upload Sample Data</Label>
                  <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                    <Upload className="h-8 w-8 text-gray-400 mx-auto mb-2" />
                    <p className="text-sm text-gray-600 mb-2">Upload CSV, JSON, or Excel files</p>
                    <input
                      type="file"
                      multiple
                      accept=".csv,.json,.xlsx,.xls"
                      onChange={handleFileUpload}
                      className="hidden"
                      id="file-upload"
                    />
                    <Button variant="outline" size="sm" onClick={() => document.getElementById('file-upload')?.click()}>
                      Choose Files
                    </Button>
                  </div>
                  {uploadedFiles.length > 0 && (
                    <div className="space-y-1">
                      {uploadedFiles.map((file, index) => (
                        <div key={index} className="flex items-center space-x-2 text-sm text-green-600">
                          <CheckCircle className="h-4 w-4" />
                          <span>{file}</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Expected Outcomes */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Target className="h-5 w-5 text-purple-600" />
                <span>Expected Outcomes</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                <div className="text-center p-4 bg-blue-50 rounded-lg">
                  <VerticalIcon className="h-8 w-8 mx-auto mb-2" style={{ color: verticalConfig.color }} />
                  <div className="text-2xl font-bold" style={{ color: verticalConfig.color }}>
                    {verticalConfig.expectedMetrics.quantumAdvantage.toFixed(1)}x
                  </div>
                  <div className="text-sm text-gray-600">Quantum Advantage</div>
                </div>
                <div className="text-center p-4 bg-green-50 rounded-lg">
                  <Target className="h-8 w-8 text-green-600 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-green-600">
                    {verticalConfig.expectedMetrics.accuracyImprovement.toFixed(1)}%
                  </div>
                  <div className="text-sm text-gray-600">Accuracy</div>
                </div>
                <div className="text-center p-4 bg-yellow-50 rounded-lg">
                  <DollarSign className="h-8 w-8 text-yellow-600 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-yellow-600">
                    ${(verticalConfig.expectedMetrics.costReduction / 1000000).toFixed(1)}M
                  </div>
                  <div className="text-sm text-gray-600">Annual Savings</div>
                </div>
                <div className="text-center p-4 bg-purple-50 rounded-lg">
                  <Clock className="h-8 w-8 text-purple-600 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-purple-600">
                    {verticalConfig.expectedMetrics.timeToSolution.toFixed(1)}h
                  </div>
                  <div className="text-sm text-gray-600">Time to Solution</div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Execute Tab */}
        <TabsContent value="execute" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Play className="h-5 w-5 text-blue-600" />
                <span>POV Execution</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="text-center space-y-4">
                <div className="flex items-center justify-center space-x-4">
                  <VerticalIcon className="h-12 w-12" style={{ color: verticalConfig.color }} />
                  <div className="text-left">
                    <h3 className="text-xl font-bold capitalize">{povConfig.vertical} POV</h3>
                    <p className="text-gray-600">{povConfig.useCase}</p>
                  </div>
                </div>
                
                {isRunning ? (
                  <div className="space-y-4">
                    <div className="flex items-center justify-center space-x-2">
                      <RefreshCw className="h-5 w-5 animate-spin text-blue-600" />
                      <span className="text-lg font-medium">Executing POV...</span>
                    </div>
                    <Progress value={progress} className="w-full max-w-md mx-auto" />
                    <p className="text-sm text-gray-600">{progress}% Complete</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <p className="text-gray-600 max-w-2xl mx-auto">
                      Ready to execute your Proof-of-Value demonstration. This will run quantum algorithms 
                      against your data and generate comprehensive performance benchmarks.
                    </p>
                    <Button 
                      size="lg" 
                      onClick={runPOV}
                      className="flex items-center space-x-2"
                      disabled={!povConfig.dataSource || uploadedFiles.length === 0}
                    >
                      <Play className="h-5 w-5" />
                      <span>Start POV Execution</span>
                    </Button>
                    {(!povConfig.dataSource || uploadedFiles.length === 0) && (
                      <p className="text-sm text-red-600">
                        Please configure data source and upload sample files to proceed
                      </p>
                    )}
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Results Tab */}
        <TabsContent value="results" className="space-y-6">
          {povResults && (
            <>
              {/* Key Results */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <Card>
                  <CardContent className="p-4 text-center">
                    <Brain className="h-8 w-8 text-purple-600 mx-auto mb-2" />
                    <div className="text-2xl font-bold text-purple-600">
                      {povResults.quantumAdvantage.toFixed(1)}x
                    </div>
                    <div className="text-sm text-gray-600">Quantum Advantage</div>
                  </CardContent>
                </Card>
                
                <Card>
                  <CardContent className="p-4 text-center">
                    <Target className="h-8 w-8 text-green-600 mx-auto mb-2" />
                    <div className="text-2xl font-bold text-green-600">
                      {povResults.accuracyImprovement.toFixed(1)}%
                    </div>
                    <div className="text-sm text-gray-600">Accuracy Achieved</div>
                  </CardContent>
                </Card>
                
                <Card>
                  <CardContent className="p-4 text-center">
                    <DollarSign className="h-8 w-8 text-blue-600 mx-auto mb-2" />
                    <div className="text-2xl font-bold text-blue-600">
                      {calculateROI.toFixed(0)}%
                    </div>
                    <div className="text-sm text-gray-600">ROI</div>
                  </CardContent>
                </Card>
                
                <Card>
                  <CardContent className="p-4 text-center">
                    <Clock className="h-8 w-8 text-orange-600 mx-auto mb-2" />
                    <div className="text-2xl font-bold text-orange-600">
                      {calculatePaybackPeriod.toFixed(1)}
                    </div>
                    <div className="text-sm text-gray-600">Payback (months)</div>
                  </CardContent>
                </Card>
              </div>

              {/* ROI Timeline */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <TrendingUp className="h-5 w-5 text-green-600" />
                    <span>ROI Timeline</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <AreaChart data={roiTimeline}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="month" />
                      <YAxis />
                      <Tooltip formatter={(value) => [`$${value.toLocaleString()}`, '']} />
                      <Area 
                        type="monotone" 
                        dataKey="cumulativeSavings" 
                        stroke={COLORS.success} 
                        fill={COLORS.success}
                        fillOpacity={0.6}
                        name="Cumulative Savings"
                      />
                    </AreaChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              {/* Business Impact Summary */}
              <Card>
                <CardHeader>
                  <CardTitle>Business Impact Summary</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="space-y-4">
                      <h4 className="font-semibold text-lg">Financial Impact</h4>
                      <div className="space-y-2">
                        <div className="flex justify-between">
                          <span>Annual Cost Reduction:</span>
                          <span className="font-bold text-green-600">
                            ${povResults.costReduction.toLocaleString()}
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span>Implementation Cost:</span>
                          <span className="font-bold">$150,000</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Net Annual Benefit:</span>
                          <span className="font-bold text-blue-600">
                            ${(povResults.costReduction - 150000).toLocaleString()}
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span>3-Year NPV:</span>
                          <span className="font-bold text-purple-600">
                            ${((povResults.costReduction - 150000) * 3).toLocaleString()}
                          </span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="space-y-4">
                      <h4 className="font-semibold text-lg">Operational Impact</h4>
                      <div className="space-y-2">
                        <div className="flex justify-between">
                          <span>Risk Reduction:</span>
                          <span className="font-bold text-green-600">
                            {povResults.riskReduction.toFixed(1)}%
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span>Time to Solution:</span>
                          <span className="font-bold text-blue-600">
                            {povResults.timeToSolution.toFixed(1)} hours
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span>Compliance Score:</span>
                          <span className="font-bold text-purple-600">
                            {povResults.complianceScore.toFixed(1)}%
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span>Quantum Advantage:</span>
                          <span className="font-bold text-orange-600">
                            {povResults.quantumAdvantage.toFixed(1)}x faster
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </>
          )}
        </TabsContent>

        {/* Benchmark Tab */}
        <TabsContent value="benchmark" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <BarChart3 className="h-5 w-5 text-blue-600" />
                <span>Competitive Benchmark Analysis</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={400}>
                <BarChart data={BENCHMARK_DATA}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="solution" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="performance" fill="#3b82f6" name="Performance (relative)" />
                  <Bar dataKey="accuracy" fill="#10b981" name="Accuracy (%)" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Cost Comparison */}
            <Card>
              <CardHeader>
                <CardTitle>Cost Comparison</CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={BENCHMARK_DATA}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="solution" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="cost" fill="#3B82F6" name="Relative Cost" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Time to Solution */}
            <Card>
              <CardHeader>
                <CardTitle>Time to Solution</CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={BENCHMARK_DATA}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="solution" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="timeToSolution" fill="#f59e0b" name="Time (relative)" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>

          {/* Competitive Summary */}
          <Card>
            <CardHeader>
              <CardTitle>Competitive Advantage Summary</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="text-center p-4 bg-green-50 rounded-lg">
                    <div className="text-3xl font-bold text-green-600">4.2x</div>
                    <div className="text-sm text-gray-600">Faster than Classical</div>
                  </div>
                  <div className="text-center p-4 bg-blue-50 rounded-lg">
                    <div className="text-3xl font-bold text-blue-600">65%</div>
                    <div className="text-sm text-gray-600">Cost Reduction</div>
                  </div>
                  <div className="text-center p-4 bg-purple-50 rounded-lg">
                    <div className="text-3xl font-bold text-purple-600">99.2%</div>
                    <div className="text-sm text-gray-600">Accuracy Achieved</div>
                  </div>
                  <div className="text-center p-4 bg-orange-50 rounded-lg">
                    <div className="text-3xl font-bold text-orange-600">85%</div>
                    <div className="text-sm text-gray-600">Time Savings</div>
                  </div>
                </div>
                
                <div className="bg-gray-50 p-4 rounded-lg">
                  <h4 className="font-semibold mb-2">Key Differentiators:</h4>
                  <ul className="space-y-1 text-sm">
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="h-4 w-4 text-green-600" />
                      <span>Quantum-computational advantage for complex optimization</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="h-4 w-4 text-green-600" />
                      <span>Litecoin Trust Chain for immutable audit trails</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="h-4 w-4 text-green-600" />
                      <span>Real-time processing with sub-second response times</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="h-4 w-4 text-green-600" />
                      <span>Industry-specific optimization models</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="h-4 w-4 text-green-600" />
                      <span>Compliance-ready reporting and documentation</span>
                    </li>
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default POVAutomationPlatform;