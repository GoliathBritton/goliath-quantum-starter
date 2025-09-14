import React, { useState, useEffect, useMemo } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { LineChart, Line, AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell, RadialBarChart, RadialBar } from 'recharts';
import { 
  Activity, 
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
  Minus
} from 'lucide-react';

interface QuantumMetrics {
  timestamp: string;
  computationsPerSecond: number;
  averageLatency: number;
  successRate: number;
  costPerComputation: number;
  quantumAdvantage: number;
}

interface BusinessImpact {
  totalSavings: number;
  revenueIncrease: number;
  efficiencyGain: number;
  riskReduction: number;
  timeToDecision: number;
  customerSatisfaction: number;
}

interface SystemHealth {
  apiStatus: 'healthy' | 'warning' | 'error';
  quantumNodes: number;
  activeConnections: number;
  queueLength: number;
  systemLoad: number;
  uptime: number;
}

interface AlertItem {
  id: string;
  type: 'info' | 'warning' | 'error' | 'success';
  message: string;
  timestamp: string;
  resolved: boolean;
}

const COLORS = {
  primary: '#3b82f6',
  secondary: '#10b981',
  accent: '#8b5cf6',
  warning: '#f59e0b',
  error: '#ef4444',
  success: '#10b981'
};

const PIE_COLORS = ['#3b82f6', '#10b981', '#8b5cf6', '#f59e0b', '#ef4444', '#06b6d4'];

export const ClientDashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [isRealTime, setIsRealTime] = useState(true);
  const [lastUpdate, setLastUpdate] = useState(new Date());

  // Mock real-time data - in production, this would come from WebSocket or API
  const [quantumMetrics, setQuantumMetrics] = useState<QuantumMetrics[]>([
    { timestamp: '09:00', computationsPerSecond: 1250, averageLatency: 45, successRate: 99.8, costPerComputation: 0.12, quantumAdvantage: 422.4 },
    { timestamp: '09:15', computationsPerSecond: 1380, averageLatency: 42, successRate: 99.9, costPerComputation: 0.11, quantumAdvantage: 445.2 },
    { timestamp: '09:30', computationsPerSecond: 1420, averageLatency: 38, successRate: 99.7, costPerComputation: 0.10, quantumAdvantage: 467.8 },
    { timestamp: '09:45', computationsPerSecond: 1560, averageLatency: 35, successRate: 99.9, costPerComputation: 0.09, quantumAdvantage: 489.3 },
    { timestamp: '10:00', computationsPerSecond: 1680, averageLatency: 32, successRate: 99.8, costPerComputation: 0.08, quantumAdvantage: 512.7 },
    { timestamp: '10:15', computationsPerSecond: 1750, averageLatency: 30, successRate: 99.9, costPerComputation: 0.08, quantumAdvantage: 534.1 }
  ]);

  const [businessImpact, setBusinessImpact] = useState<BusinessImpact>({
    totalSavings: 2847000,
    revenueIncrease: 1650000,
    efficiencyGain: 67.8,
    riskReduction: 43.2,
    timeToDecision: 0.8,
    customerSatisfaction: 94.5
  });

  const [systemHealth, setSystemHealth] = useState<SystemHealth>({
    apiStatus: 'healthy',
    quantumNodes: 1247,
    activeConnections: 89,
    queueLength: 12,
    systemLoad: 67,
    uptime: 99.97
  });

  const [alerts, setAlerts] = useState<AlertItem[]>([
    {
      id: '1',
      type: 'success',
      message: 'Portfolio optimization completed with 534.1x quantum advantage',
      timestamp: '10:15 AM',
      resolved: false
    },
    {
      id: '2',
      type: 'info',
      message: 'New quantum node cluster deployed in US-East region',
      timestamp: '09:45 AM',
      resolved: false
    },
    {
      id: '3',
      type: 'warning',
      message: 'High computation volume detected - auto-scaling initiated',
      timestamp: '09:30 AM',
      resolved: true
    }
  ]);

  // Simulate real-time updates
  useEffect(() => {
    if (!isRealTime) return;

    const interval = setInterval(() => {
      const now = new Date();
      const timeString = now.toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit' });
      
      // Update quantum metrics
      setQuantumMetrics(prev => {
        const newMetric: QuantumMetrics = {
          timestamp: timeString,
          computationsPerSecond: 1200 + Math.random() * 800,
          averageLatency: 25 + Math.random() * 20,
          successRate: 99.5 + Math.random() * 0.5,
          costPerComputation: 0.05 + Math.random() * 0.10,
          quantumAdvantage: 400 + Math.random() * 200
        };
        
        const updated = [...prev.slice(-5), newMetric];
        return updated;
      });

      // Update business impact
      setBusinessImpact(prev => ({
        ...prev,
        totalSavings: prev.totalSavings + Math.random() * 1000,
        revenueIncrease: prev.revenueIncrease + Math.random() * 500,
        efficiencyGain: Math.min(100, prev.efficiencyGain + Math.random() * 0.5),
        customerSatisfaction: Math.min(100, prev.customerSatisfaction + Math.random() * 0.2)
      }));

      // Update system health
      setSystemHealth(prev => ({
        ...prev,
        activeConnections: Math.max(50, prev.activeConnections + Math.floor(Math.random() * 10 - 5)),
        queueLength: Math.max(0, prev.queueLength + Math.floor(Math.random() * 6 - 3)),
        systemLoad: Math.max(30, Math.min(90, prev.systemLoad + Math.random() * 10 - 5))
      }));

      setLastUpdate(now);
    }, 5000); // Update every 5 seconds

    return () => clearInterval(interval);
  }, [isRealTime]);

  // Calculate current performance metrics
  const currentMetrics = useMemo(() => {
    const latest = quantumMetrics[quantumMetrics.length - 1];
    if (!latest) return null;

    const previous = quantumMetrics[quantumMetrics.length - 2];
    if (!previous) return { ...latest, trends: {} };

    return {
      ...latest,
      trends: {
        computationsPerSecond: ((latest.computationsPerSecond - previous.computationsPerSecond) / previous.computationsPerSecond) * 100,
        averageLatency: ((latest.averageLatency - previous.averageLatency) / previous.averageLatency) * 100,
        successRate: ((latest.successRate - previous.successRate) / previous.successRate) * 100,
        quantumAdvantage: ((latest.quantumAdvantage - previous.quantumAdvantage) / previous.quantumAdvantage) * 100
      }
    };
  }, [quantumMetrics]);

  // Portfolio optimization data
  const portfolioData = [
    { name: 'Traditional', value: 8.2, color: '#ef4444' },
    { name: 'Classical AI', value: 12.7, color: '#f59e0b' },
    { name: 'NQBA Quantum', value: 24.8, color: '#10b981' }
  ];

  // Industry performance comparison
  const industryComparison = [
    { industry: 'Financial Services', traditional: 100, quantum: 422, improvement: 322 },
    { industry: 'Energy', traditional: 100, quantum: 234, improvement: 134 },
    { industry: 'Healthcare', traditional: 100, quantum: 189, improvement: 89 },
    { industry: 'Manufacturing', traditional: 100, quantum: 156, improvement: 56 },
    { industry: 'Logistics', traditional: 100, quantum: 145, improvement: 45 }
  ];

  // Cost analysis data
  const costAnalysis = [
    { month: 'Jan', traditional: 125000, quantum: 45000, savings: 80000 },
    { month: 'Feb', traditional: 132000, quantum: 42000, savings: 90000 },
    { month: 'Mar', traditional: 128000, quantum: 38000, savings: 90000 },
    { month: 'Apr', traditional: 135000, quantum: 35000, savings: 100000 },
    { month: 'May', traditional: 142000, quantum: 32000, savings: 110000 },
    { month: 'Jun', traditional: 148000, quantum: 30000, savings: 118000 }
  ];

  const toggleRealTime = () => {
    setIsRealTime(!isRealTime);
  };

  const exportData = () => {
    const data = {
      quantumMetrics,
      businessImpact,
      systemHealth,
      exportTime: new Date().toISOString()
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `nqba-dashboard-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'healthy': return <CheckCircle className="h-4 w-4 text-green-600" />;
      case 'warning': return <AlertTriangle className="h-4 w-4 text-yellow-600" />;
      case 'error': return <XCircle className="h-4 w-4 text-red-600" />;
      default: return <Minus className="h-4 w-4 text-gray-600" />;
    }
  };

  const getAlertIcon = (type: string) => {
    switch (type) {
      case 'success': return <CheckCircle className="h-4 w-4 text-green-600" />;
      case 'warning': return <AlertTriangle className="h-4 w-4 text-yellow-600" />;
      case 'error': return <XCircle className="h-4 w-4 text-red-600" />;
      default: return <Bell className="h-4 w-4 text-blue-600" />;
    }
  };

  const getTrendIcon = (trend: number) => {
    if (trend > 0) return <TrendingUp className="h-3 w-3 text-green-600" />;
    if (trend < 0) return <TrendingUp className="h-3 w-3 text-red-600 rotate-180" />;
    return <Minus className="h-3 w-3 text-gray-600" />;
  };

  return (
    <div className="w-full max-w-7xl mx-auto p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="space-y-2">
          <div className="flex items-center space-x-3">
            <div className="relative">
              <Activity className="h-8 w-8 text-blue-600" />
              <Sparkles className="h-4 w-4 text-yellow-500 absolute -top-1 -right-1 animate-pulse" />
            </div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Quantum Performance Dashboard
            </h1>
          </div>
          <div className="flex items-center space-x-4 text-sm text-gray-600">
            <div className="flex items-center space-x-2">
              {getStatusIcon(systemHealth.apiStatus)}
              <span>System Status: {systemHealth.apiStatus}</span>
            </div>
            <div className="flex items-center space-x-2">
              <Clock className="h-4 w-4" />
              <span>Last Update: {lastUpdate.toLocaleTimeString()}</span>
            </div>
            <div className="flex items-center space-x-2">
              <Globe className="h-4 w-4" />
              <span>{systemHealth.quantumNodes} Quantum Nodes</span>
            </div>
          </div>
        </div>
        
        <div className="flex items-center space-x-3">
          <Button
            variant={isRealTime ? "default" : "outline"}
            size="sm"
            onClick={toggleRealTime}
            className="flex items-center space-x-2"
          >
            <RefreshCw className={`h-4 w-4 ${isRealTime ? 'animate-spin' : ''}`} />
            <span>{isRealTime ? 'Live' : 'Paused'}</span>
          </Button>
          <Button variant="outline" size="sm" onClick={exportData}>
            <Download className="h-4 w-4 mr-2" />
            Export
          </Button>
          <Button variant="outline" size="sm">
            <Settings className="h-4 w-4" />
          </Button>
        </div>
      </div>

      {/* Key Metrics Overview */}
      {currentMetrics && (
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Computations/sec</p>
                  <p className="text-2xl font-bold">{Math.round(currentMetrics.computationsPerSecond).toLocaleString()}</p>
                </div>
                <div className="flex items-center space-x-1">
                  {getTrendIcon(currentMetrics.trends?.computationsPerSecond || 0)}
                  <Cpu className="h-8 w-8 text-blue-600" />
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Latency (ms)</p>
                  <p className="text-2xl font-bold">{Math.round(currentMetrics.averageLatency)}</p>
                </div>
                <div className="flex items-center space-x-1">
                  {getTrendIcon(-(currentMetrics.trends?.averageLatency || 0))}
                  <Zap className="h-8 w-8 text-yellow-600" />
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Success Rate</p>
                  <p className="text-2xl font-bold">{currentMetrics.successRate.toFixed(1)}%</p>
                </div>
                <div className="flex items-center space-x-1">
                  {getTrendIcon(currentMetrics.trends?.successRate || 0)}
                  <Target className="h-8 w-8 text-green-600" />
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Quantum Advantage</p>
                  <p className="text-2xl font-bold">{Math.round(currentMetrics.quantumAdvantage)}x</p>
                </div>
                <div className="flex items-center space-x-1">
                  {getTrendIcon(currentMetrics.trends?.quantumAdvantage || 0)}
                  <Brain className="h-8 w-8 text-purple-600" />
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Total Savings</p>
                  <p className="text-2xl font-bold">${(businessImpact.totalSavings / 1000000).toFixed(1)}M</p>
                </div>
                <div className="flex items-center space-x-1">
                  <TrendingUp className="h-3 w-3 text-green-600" />
                  <DollarSign className="h-8 w-8 text-green-600" />
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">System Load</p>
                  <p className="text-2xl font-bold">{systemHealth.systemLoad}%</p>
                </div>
                <div className="flex items-center space-x-1">
                  <Progress value={systemHealth.systemLoad} className="w-8" />
                  <Database className="h-8 w-8 text-blue-600" />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="overview" className="flex items-center space-x-2">
            <BarChart3 className="h-4 w-4" />
            <span>Overview</span>
          </TabsTrigger>
          <TabsTrigger value="performance" className="flex items-center space-x-2">
            <Activity className="h-4 w-4" />
            <span>Performance</span>
          </TabsTrigger>
          <TabsTrigger value="business" className="flex items-center space-x-2">
            <DollarSign className="h-4 w-4" />
            <span>Business Impact</span>
          </TabsTrigger>
          <TabsTrigger value="system" className="flex items-center space-x-2">
            <Shield className="h-4 w-4" />
            <span>System Health</span>
          </TabsTrigger>
          <TabsTrigger value="alerts" className="flex items-center space-x-2">
            <Bell className="h-4 w-4" />
            <span>Alerts</span>
            {alerts.filter(a => !a.resolved).length > 0 && (
              <Badge variant="destructive" className="ml-1 h-5 w-5 p-0 text-xs">
                {alerts.filter(a => !a.resolved).length}
              </Badge>
            )}
          </TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Real-time Performance */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Activity className="h-5 w-5 text-blue-600" />
                  <span>Real-time Performance</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={quantumMetrics}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="timestamp" />
                    <YAxis />
                    <Tooltip />
                    <Line 
                      type="monotone" 
                      dataKey="quantumAdvantage" 
                      stroke={COLORS.primary} 
                      strokeWidth={3}
                      dot={{ fill: COLORS.primary, strokeWidth: 2, r: 4 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Portfolio Performance */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <PieChartIcon className="h-5 w-5 text-green-600" />
                  <span>Portfolio Performance</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={portfolioData}
                      cx="50%"
                      cy="50%"
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                      label={({ name, value }) => `${name}: ${value}%`}
                    >
                      {portfolioData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>

          {/* Industry Comparison */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <BarChart3 className="h-5 w-5 text-purple-600" />
                <span>Industry Performance Comparison</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={400}>
                <BarChart data={industryComparison}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="industry" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="traditional" fill="#ef4444" name="Traditional" />
                  <Bar dataKey="quantum" fill="#10b981" name="NQBA Quantum" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Performance Tab */}
        <TabsContent value="performance" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Computation Metrics */}
            <Card>
              <CardHeader>
                <CardTitle>Computation Metrics</CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <AreaChart data={quantumMetrics}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="timestamp" />
                    <YAxis />
                    <Tooltip />
                    <Area 
                      type="monotone" 
                      dataKey="computationsPerSecond" 
                      stroke={COLORS.primary} 
                      fill={COLORS.primary}
                      fillOpacity={0.6}
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Latency & Success Rate */}
            <Card>
              <CardHeader>
                <CardTitle>Latency & Success Rate</CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={quantumMetrics}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="timestamp" />
                    <YAxis yAxisId="left" />
                    <YAxis yAxisId="right" orientation="right" />
                    <Tooltip />
                    <Legend />
                    <Line 
                      yAxisId="left"
                      type="monotone" 
                      dataKey="averageLatency" 
                      stroke={COLORS.warning} 
                      name="Latency (ms)"
                    />
                    <Line 
                      yAxisId="right"
                      type="monotone" 
                      dataKey="successRate" 
                      stroke={COLORS.success} 
                      name="Success Rate (%)"
                    />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>

          {/* Performance Benchmarks */}
          <Card>
            <CardHeader>
              <CardTitle>Performance Benchmarks</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="text-center p-4 bg-blue-50 rounded-lg">
                  <div className="text-3xl font-bold text-blue-600">422.4x</div>
                  <div className="text-sm text-gray-600">Portfolio Optimization</div>
                  <Progress value={95} className="mt-2" />
                </div>
                <div className="text-center p-4 bg-green-50 rounded-lg">
                  <div className="text-3xl font-bold text-green-600">156.7x</div>
                  <div className="text-sm text-gray-600">Risk Analysis</div>
                  <Progress value={87} className="mt-2" />
                </div>
                <div className="text-center p-4 bg-purple-50 rounded-lg">
                  <div className="text-3xl font-bold text-purple-600">234.1x</div>
                  <div className="text-sm text-gray-600">Energy Optimization</div>
                  <Progress value={92} className="mt-2" />
                </div>
                <div className="text-center p-4 bg-orange-50 rounded-lg">
                  <div className="text-3xl font-bold text-orange-600">89.3x</div>
                  <div className="text-sm text-gray-600">Supply Chain</div>
                  <Progress value={78} className="mt-2" />
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Business Impact Tab */}
        <TabsContent value="business" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Cost Analysis */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <DollarSign className="h-5 w-5 text-green-600" />
                  <span>Cost Analysis</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <AreaChart data={costAnalysis}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis />
                    <Tooltip formatter={(value) => [`$${value.toLocaleString()}`, '']} />
                    <Legend />
                    <Area 
                      type="monotone" 
                      dataKey="traditional" 
                      stackId="1" 
                      stroke="#ef4444" 
                      fill="#ef4444" 
                      fillOpacity={0.6}
                      name="Traditional Costs"
                    />
                    <Area 
                      type="monotone" 
                      dataKey="quantum" 
                      stackId="2" 
                      stroke="#10b981" 
                      fill="#10b981" 
                      fillOpacity={0.6}
                      name="Quantum Costs"
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Business KPIs */}
            <Card>
              <CardHeader>
                <CardTitle>Business KPIs</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Efficiency Gain</span>
                    <div className="flex items-center space-x-2">
                      <Progress value={businessImpact.efficiencyGain} className="w-24" />
                      <span className="text-sm font-bold">{businessImpact.efficiencyGain.toFixed(1)}%</span>
                    </div>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Risk Reduction</span>
                    <div className="flex items-center space-x-2">
                      <Progress value={businessImpact.riskReduction} className="w-24" />
                      <span className="text-sm font-bold">{businessImpact.riskReduction.toFixed(1)}%</span>
                    </div>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Customer Satisfaction</span>
                    <div className="flex items-center space-x-2">
                      <Progress value={businessImpact.customerSatisfaction} className="w-24" />
                      <span className="text-sm font-bold">{businessImpact.customerSatisfaction.toFixed(1)}%</span>
                    </div>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Decision Time</span>
                    <div className="flex items-center space-x-2">
                      <Clock className="h-4 w-4 text-blue-600" />
                      <span className="text-sm font-bold">{businessImpact.timeToDecision} hours</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Financial Summary */}
          <Card>
            <CardHeader>
              <CardTitle>Financial Impact Summary</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-600">
                    ${(businessImpact.totalSavings / 1000000).toFixed(1)}M
                  </div>
                  <div className="text-sm text-gray-600">Total Savings</div>
                  <div className="text-xs text-green-600 mt-1">↗ +12.3% this month</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-600">
                    ${(businessImpact.revenueIncrease / 1000000).toFixed(1)}M
                  </div>
                  <div className="text-sm text-gray-600">Revenue Increase</div>
                  <div className="text-xs text-blue-600 mt-1">↗ +8.7% this month</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-purple-600">6,009%</div>
                  <div className="text-sm text-gray-600">Average ROI</div>
                  <div className="text-xs text-purple-600 mt-1">Industry leading</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-orange-600">2.8</div>
                  <div className="text-sm text-gray-600">Payback (months)</div>
                  <div className="text-xs text-orange-600 mt-1">Best in class</div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* System Health Tab */}
        <TabsContent value="system" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* System Status */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Shield className="h-5 w-5 text-green-600" />
                  <span>System Status</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm">API Status</span>
                    <div className="flex items-center space-x-2">
                      {getStatusIcon(systemHealth.apiStatus)}
                      <Badge variant={systemHealth.apiStatus === 'healthy' ? 'default' : 'destructive'}>
                        {systemHealth.apiStatus}
                      </Badge>
                    </div>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Uptime</span>
                    <span className="font-bold text-green-600">{systemHealth.uptime}%</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Active Connections</span>
                    <span className="font-bold">{systemHealth.activeConnections}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Queue Length</span>
                    <span className="font-bold">{systemHealth.queueLength}</span>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Resource Usage */}
            <Card>
              <CardHeader>
                <CardTitle>Resource Usage</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <div className="flex justify-between text-sm mb-2">
                      <span>System Load</span>
                      <span>{systemHealth.systemLoad}%</span>
                    </div>
                    <Progress value={systemHealth.systemLoad} />
                  </div>
                  <div>
                    <div className="flex justify-between text-sm mb-2">
                      <span>Memory Usage</span>
                      <span>67%</span>
                    </div>
                    <Progress value={67} />
                  </div>
                  <div>
                    <div className="flex justify-between text-sm mb-2">
                      <span>Network I/O</span>
                      <span>43%</span>
                    </div>
                    <Progress value={43} />
                  </div>
                  <div>
                    <div className="flex justify-between text-sm mb-2">
                      <span>Storage</span>
                      <span>28%</span>
                    </div>
                    <Progress value={28} />
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Quantum Network */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Globe className="h-5 w-5 text-blue-600" />
                  <span>Quantum Network</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="text-center">
                    <div className="text-3xl font-bold text-blue-600">{systemHealth.quantumNodes}</div>
                    <div className="text-sm text-gray-600">Active Nodes</div>
                  </div>
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>US-East</span>
                      <Badge variant="outline">423 nodes</Badge>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span>US-West</span>
                      <Badge variant="outline">387 nodes</Badge>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span>Europe</span>
                      <Badge variant="outline">289 nodes</Badge>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span>Asia-Pacific</span>
                      <Badge variant="outline">148 nodes</Badge>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Alerts Tab */}
        <TabsContent value="alerts" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Bell className="h-5 w-5 text-blue-600" />
                  <span>System Alerts</span>
                </div>
                <Badge variant="outline">
                  {alerts.filter(a => !a.resolved).length} active
                </Badge>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {alerts.map((alert) => (
                  <div 
                    key={alert.id} 
                    className={`flex items-center space-x-3 p-3 rounded-lg border ${
                      alert.resolved ? 'bg-gray-50 opacity-60' : 'bg-white'
                    }`}
                  >
                    {getAlertIcon(alert.type)}
                    <div className="flex-1">
                      <p className={`text-sm ${alert.resolved ? 'line-through text-gray-500' : ''}`}>
                        {alert.message}
                      </p>
                      <p className="text-xs text-gray-500">{alert.timestamp}</p>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Badge 
                        variant={alert.type === 'error' ? 'destructive' : 
                                alert.type === 'warning' ? 'secondary' : 'default'}
                      >
                        {alert.type}
                      </Badge>
                      {alert.resolved && (
                        <Badge variant="outline" className="text-green-600">
                          Resolved
                        </Badge>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default ClientDashboard;