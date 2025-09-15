import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Alert, AlertDescription } from '@/components/ui/alert';
import {
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar
} from 'recharts';
import {
  Target, TrendingUp, Users, Award, Rocket, CheckCircle,
  AlertTriangle, Clock, DollarSign, Building, Zap, Star,
  ArrowRight, PlayCircle, FileText, BarChart3, Shield,
  Lightbulb, Globe, Handshake, Brain, Cpu, Database
} from 'lucide-react';

const COLORS = {
  primary: '#3B82F6',
  secondary: '#10B981',
  accent: '#F59E0B',
  danger: '#EF4444',
  purple: '#8B5CF6',
  teal: '#14B8A6'
};

// Strategic Framework Data
const STRATEGIC_STRENGTHS = [
  {
    id: 'icp_targeting',
    title: 'Precise ICP Targeting',
    description: 'Focus on data-rich, process-heavy enterprises with costly problems',
    impact: 'High',
    status: 'validated',
    score: 95
  },
  {
    id: 'vertical_messaging',
    title: 'Verticalized Problem-Led Messaging',
    description: 'Technology-to-value shift with C-level priority alignment',
    impact: 'High',
    status: 'validated',
    score: 92
  },
  {
    id: 'unfair_advantage',
    title: 'Unfair Advantage Trifecta',
    description: 'Dynex + LTC + SigmaEQ creates defensible moat',
    impact: 'Critical',
    status: 'validated',
    score: 98
  },
  {
    id: 'consultative_sales',
    title: 'Consultative Sales Motion',
    description: 'Workshop → POV → Pilot → Enterprise deal cycle',
    impact: 'High',
    status: 'validated',
    score: 88
  }
];

const STRATEGIC_CONSIDERATIONS = [
  {
    id: 'quantum_hurdle',
    title: 'Quantum Skepticism',
    risk: 'Medium',
    mitigation: 'Lead with business problem, use quantum-inspired terminology',
    progress: 75
  },
  {
    id: 'champion_building',
    title: 'Internal Champion Building',
    risk: 'Medium',
    mitigation: 'Dual-purpose collateral for data scientists and executives',
    progress: 68
  },
  {
    id: 'classical_competition',
    title: 'Classical Optimization Competition',
    risk: 'High',
    mitigation: 'Focus on non-convex problems with combinatorial explosion',
    progress: 82
  },
  {
    id: 'sales_scalability',
    title: 'Sales Motion Scalability',
    risk: 'High',
    mitigation: 'Develop POV-in-a-Box and standardized assessment tools',
    progress: 45
  }
];

const IMPLEMENTATION_PHASES = [
  {
    id: 'pov_in_box',
    title: 'POV in a Box Development',
    priority: 'Critical',
    timeline: '4-6 weeks',
    status: 'in_progress',
    progress: 75,
    deliverables: [
      'Jupyter notebook templates for each vertical',
      'Data ingestion scripts for common formats',
      'Automated ROI analysis and LTC audit trail',
      'Standardized report templates'
    ],
    impact: '$2.5M ARR potential'
  },
  {
    id: 'vertical_domination',
    title: 'Vertical Market Domination',
    priority: 'High',
    timeline: '8-12 weeks',
    status: 'planning',
    progress: 35,
    deliverables: [
      'Manufacturing case study with hard ROI numbers',
      'Video testimonials from technical and business leads',
      'Industry-specific white papers and benchmarks',
      'Competitive analysis against classical solvers'
    ],
    impact: '$5M ARR potential'
  },
  {
    id: 'sigmaeq_showcase',
    title: 'SigmaEQ Internal Showcase',
    priority: 'High',
    timeline: '6-8 weeks',
    status: 'active',
    progress: 60,
    deliverables: [
      'Internal sales optimization metrics',
      'Quantum vs classical performance comparison',
      'Customer-facing demonstration platform',
      'Investor presentation materials'
    ],
    impact: 'Proof-of-concept validation'
  },
  {
    id: 'partner_channels',
    title: 'Partner Channel Development',
    priority: 'Medium',
    timeline: '12-16 weeks',
    status: 'planning',
    progress: 20,
    deliverables: [
      'System integrator partnership agreements',
      'Partner training and certification programs',
      'Co-marketing materials and case studies',
      'Revenue sharing and incentive structures'
    ],
    impact: '3x GTM acceleration'
  }
];

const MARKET_POSITIONING_DATA = [
  { vertical: 'Manufacturing', market_size: 45, penetration: 12, opportunity: 38.5 },
  { vertical: 'Financial Services', market_size: 62, penetration: 8, opportunity: 57.0 },
  { vertical: 'Logistics', market_size: 28, penetration: 15, opportunity: 23.8 },
  { vertical: 'Energy', market_size: 35, penetration: 5, opportunity: 33.3 }
];

const ROI_PROJECTIONS = [
  { quarter: 'Q1 2024', revenue: 2.5, costs: 1.8, profit: 0.7 },
  { quarter: 'Q2 2024', revenue: 4.2, costs: 2.1, profit: 2.1 },
  { quarter: 'Q3 2024', revenue: 7.8, costs: 2.8, profit: 5.0 },
  { quarter: 'Q4 2024', revenue: 12.5, costs: 3.5, profit: 9.0 }
];

const COMPETITIVE_ANALYSIS = [
  {
    competitor: 'Classical Solvers',
    strength: 85,
    weakness: 'Non-convex optimization',
    our_advantage: 'Quantum advantage for complex problems'
  },
  {
    competitor: 'IBM Quantum',
    strength: 70,
    weakness: 'Limited business applications',
    our_advantage: 'Vertical-specific solutions'
  },
  {
    competitor: 'Google Quantum AI',
    strength: 75,
    weakness: 'Research-focused',
    our_advantage: 'Enterprise-ready platform'
  },
  {
    competitor: 'Microsoft Azure Quantum',
    strength: 80,
    weakness: 'Generic platform',
    our_advantage: 'Industry-specific optimization'
  }
];

const SUCCESS_METRICS = [
  { metric: 'POV Conversion Rate', current: 68, target: 85, trend: 'up' },
  { metric: 'Average Deal Size', current: 450000, target: 750000, trend: 'up' },
  { metric: 'Sales Cycle Length', current: 180, target: 120, trend: 'down' },
  { metric: 'Partner Revenue %', current: 15, target: 40, trend: 'up' },
  { metric: 'Customer Satisfaction', current: 4.2, target: 4.7, trend: 'up' }
];

export const StrategicImplementationDashboard: React.FC = () => {
  const [activePhase, setActivePhase] = useState<string>('pov_in_box');
  const [selectedVertical, setSelectedVertical] = useState<string>('Manufacturing');

  const calculateOverallProgress = () => {
    const totalProgress = IMPLEMENTATION_PHASES.reduce((sum, phase) => sum + phase.progress, 0);
    return Math.round(totalProgress / IMPLEMENTATION_PHASES.length);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'bg-green-500';
      case 'in_progress': return 'bg-blue-500';
      case 'active': return 'bg-purple-500';
      case 'planning': return 'bg-yellow-500';
      default: return 'bg-gray-500';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'Critical': return 'bg-red-500';
      case 'High': return 'bg-orange-500';
      case 'Medium': return 'bg-yellow-500';
      case 'Low': return 'bg-green-500';
      default: return 'bg-gray-500';
    }
  };

  return (
    <div className="p-6 space-y-6 bg-gradient-to-br from-slate-50 to-blue-50 min-h-screen">
      {/* Header */}
      <div className="text-center space-y-4">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
          NQBA Strategic Implementation Dashboard
        </h1>
        <p className="text-lg text-gray-600 max-w-4xl mx-auto">
          Comprehensive roadmap for enterprise quantum business advantage implementation,
          integrating strategic feedback and actionable next steps
        </p>
        
        {/* Overall Progress */}
        <Card className="max-w-2xl mx-auto">
          <CardContent className="pt-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-2">
                <Target className="h-5 w-5 text-blue-600" />
                <span className="font-semibold">Overall Implementation Progress</span>
              </div>
              <Badge className="bg-blue-100 text-blue-800">
                {calculateOverallProgress()}% Complete
              </Badge>
            </div>
            <Progress value={calculateOverallProgress()} className="h-3" />
          </CardContent>
        </Card>
      </div>

      <Tabs defaultValue="overview" className="space-y-6">
        <TabsList className="grid w-full grid-cols-6">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="strengths">Strengths</TabsTrigger>
          <TabsTrigger value="implementation">Implementation</TabsTrigger>
          <TabsTrigger value="market">Market Position</TabsTrigger>
          <TabsTrigger value="metrics">Success Metrics</TabsTrigger>
          <TabsTrigger value="roadmap">Roadmap</TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Strategic Framework Summary */}
            <Card className="lg:col-span-2">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Lightbulb className="h-5 w-5 text-yellow-500" />
                  <span>Strategic Framework Excellence</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <Alert className="border-green-200 bg-green-50">
                  <CheckCircle className="h-4 w-4 text-green-600" />
                  <AlertDescription className="text-green-800">
                    <strong>Exceptional Framework:</strong> You've moved beyond generic "quantum for business" 
                    and crafted a compelling, enterprise-grade value proposition that is both credible and highly defensible.
                  </AlertDescription>
                </Alert>
                
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <div className="flex items-center space-x-2">
                      <Target className="h-4 w-4 text-blue-600" />
                      <span className="font-medium">Precise ICP Targeting</span>
                    </div>
                    <p className="text-sm text-gray-600">
                      Focus on data-rich, process-heavy enterprises with specific, costly problems
                    </p>
                  </div>
                  
                  <div className="space-y-2">
                    <div className="flex items-center space-x-2">
                      <Shield className="h-4 w-4 text-purple-600" />
                      <span className="font-medium">Unfair Advantage Trifecta</span>
                    </div>
                    <p className="text-sm text-gray-600">
                      Dynex + LTC + SigmaEQ creates a defensible competitive moat
                    </p>
                  </div>
                  
                  <div className="space-y-2">
                    <div className="flex items-center space-x-2">
                      <Users className="h-4 w-4 text-green-600" />
                      <span className="font-medium">Consultative Sales Motion</span>
                    </div>
                    <p className="text-sm text-gray-600">
                      Workshop → POV → Pilot → Enterprise deal builds trust and de-risks purchase
                    </p>
                  </div>
                  
                  <div className="space-y-2">
                    <div className="flex items-center space-x-2">
                      <Building className="h-4 w-4 text-orange-600" />
                      <span className="font-medium">Vertical Specialization</span>
                    </div>
                    <p className="text-sm text-gray-600">
                      Problem-led messaging that speaks directly to C-level priorities
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Key Metrics Summary */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <BarChart3 className="h-5 w-5 text-blue-600" />
                  <span>Key Metrics</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">POV Conversion</span>
                    <span className="font-semibold text-green-600">68%</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Avg Deal Size</span>
                    <span className="font-semibold text-blue-600">$450K</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Sales Cycle</span>
                    <span className="font-semibold text-purple-600">180 days</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Market Penetration</span>
                    <span className="font-semibold text-orange-600">12%</span>
                  </div>
                </div>
                
                <Button className="w-full mt-4">
                  <ArrowRight className="h-4 w-4 mr-2" />
                  View Detailed Metrics
                </Button>
              </CardContent>
            </Card>
          </div>

          {/* Implementation Phases Overview */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Rocket className="h-5 w-5 text-purple-600" />
                <span>Implementation Phases Overview</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {IMPLEMENTATION_PHASES.map((phase) => (
                  <Card key={phase.id} className="hover:shadow-lg transition-shadow cursor-pointer"
                        onClick={() => setActivePhase(phase.id)}>
                    <CardContent className="pt-4">
                      <div className="space-y-3">
                        <div className="flex items-center justify-between">
                          <Badge className={getPriorityColor(phase.priority)}>
                            {phase.priority}
                          </Badge>
                          <Badge variant="outline" className={getStatusColor(phase.status)}>
                            {phase.status.replace('_', ' ')}
                          </Badge>
                        </div>
                        
                        <h3 className="font-semibold text-sm">{phase.title}</h3>
                        
                        <div className="space-y-2">
                          <div className="flex justify-between text-xs">
                            <span>Progress</span>
                            <span className="font-medium">{phase.progress}%</span>
                          </div>
                          <Progress value={phase.progress} className="h-2" />
                        </div>
                        
                        <div className="text-xs text-gray-600">
                          <div className="flex items-center space-x-1">
                            <Clock className="h-3 w-3" />
                            <span>{phase.timeline}</span>
                          </div>
                          <div className="flex items-center space-x-1 mt-1">
                            <DollarSign className="h-3 w-3" />
                            <span>{phase.impact}</span>
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Strengths Tab */}
        <TabsContent value="strengths" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Validated Strengths */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Star className="h-5 w-5 text-yellow-500" />
                  <span>Validated Strategic Strengths</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {STRATEGIC_STRENGTHS.map((strength) => (
                  <div key={strength.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                    <div className="flex items-start justify-between mb-2">
                      <h3 className="font-semibold text-sm">{strength.title}</h3>
                      <div className="flex items-center space-x-2">
                        <Badge variant={strength.impact === 'Critical' ? 'destructive' : strength.impact === 'High' ? 'default' : 'secondary'}>
                          {strength.impact}
                        </Badge>
                        <div className="text-right">
                          <div className="text-lg font-bold text-green-600">{strength.score}</div>
                          <div className="text-xs text-gray-500">Score</div>
                        </div>
                      </div>
                    </div>
                    <p className="text-sm text-gray-600 mb-3">{strength.description}</p>
                    <div className="flex items-center space-x-2">
                      <CheckCircle className="h-4 w-4 text-green-500" />
                      <span className="text-xs font-medium text-green-700">Validated</span>
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>

            {/* Strategic Considerations */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <AlertTriangle className="h-5 w-5 text-orange-500" />
                  <span>Strategic Considerations & Mitigations</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {STRATEGIC_CONSIDERATIONS.map((consideration) => (
                  <div key={consideration.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                    <div className="flex items-start justify-between mb-2">
                      <h3 className="font-semibold text-sm">{consideration.title}</h3>
                      <Badge variant={consideration.risk === 'High' ? 'destructive' : consideration.risk === 'Medium' ? 'default' : 'secondary'}>
                        {consideration.risk} Risk
                      </Badge>
                    </div>
                    <p className="text-sm text-gray-600 mb-3">{consideration.mitigation}</p>
                    <div className="space-y-2">
                      <div className="flex justify-between text-xs">
                        <span>Mitigation Progress</span>
                        <span className="font-medium">{consideration.progress}%</span>
                      </div>
                      <Progress value={consideration.progress} className="h-2" />
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>

          {/* Competitive Analysis */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Shield className="h-5 w-5 text-blue-600" />
                <span>Competitive Analysis & Positioning</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {COMPETITIVE_ANALYSIS.map((competitor, index) => (
                  <div key={index} className="flex items-center justify-between p-4 border rounded-lg hover:shadow-md transition-shadow">
                    <div className="flex-1">
                      <h3 className="font-semibold">{competitor.competitor}</h3>
                      <p className="text-sm text-gray-600">Weakness: {competitor.weakness}</p>
                      <p className="text-sm text-blue-600 font-medium">Our Advantage: {competitor.our_advantage}</p>
                    </div>
                    <div className="text-right">
                      <div className="text-lg font-bold">{competitor.strength}%</div>
                      <div className="text-xs text-gray-500">Market Strength</div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Implementation Tab */}
        <TabsContent value="implementation" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Phase Selection */}
            <Card>
              <CardHeader>
                <CardTitle>Implementation Phases</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                {IMPLEMENTATION_PHASES.map((phase) => (
                  <Button
                    key={phase.id}
                    variant={activePhase === phase.id ? 'default' : 'outline'}
                    className="w-full justify-start"
                    onClick={() => setActivePhase(phase.id)}
                  >
                    <div className="flex items-center space-x-2">
                      <div className={`w-2 h-2 rounded-full ${getStatusColor(phase.status)}`} />
                      <span className="text-sm">{phase.title}</span>
                    </div>
                  </Button>
                ))}
              </CardContent>
            </Card>

            {/* Phase Details */}
            <Card className="lg:col-span-2">
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span>{IMPLEMENTATION_PHASES.find(p => p.id === activePhase)?.title}</span>
                  <Badge className={getPriorityColor(IMPLEMENTATION_PHASES.find(p => p.id === activePhase)?.priority || '')}>
                    {IMPLEMENTATION_PHASES.find(p => p.id === activePhase)?.priority}
                  </Badge>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {(() => {
                  const phase = IMPLEMENTATION_PHASES.find(p => p.id === activePhase);
                  if (!phase) return null;
                  
                  return (
                    <>
                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <div className="text-sm text-gray-600">Timeline</div>
                          <div className="font-semibold">{phase.timeline}</div>
                        </div>
                        <div>
                          <div className="text-sm text-gray-600">Expected Impact</div>
                          <div className="font-semibold text-green-600">{phase.impact}</div>
                        </div>
                      </div>
                      
                      <div className="space-y-2">
                        <div className="flex justify-between text-sm">
                          <span>Progress</span>
                          <span className="font-medium">{phase.progress}%</span>
                        </div>
                        <Progress value={phase.progress} className="h-3" />
                      </div>
                      
                      <div>
                        <h4 className="font-semibold mb-2">Key Deliverables</h4>
                        <ul className="space-y-2">
                          {phase.deliverables.map((deliverable, index) => (
                            <li key={index} className="flex items-start space-x-2">
                              <CheckCircle className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                              <span className="text-sm">{deliverable}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                      
                      <div className="flex space-x-2">
                        <Button className="flex-1">
                          <PlayCircle className="h-4 w-4 mr-2" />
                          Start Phase
                        </Button>
                        <Button variant="outline">
                          <FileText className="h-4 w-4 mr-2" />
                          View Details
                        </Button>
                      </div>
                    </>
                  );
                })()}
              </CardContent>
            </Card>
          </div>

          {/* ROI Projections */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <TrendingUp className="h-5 w-5 text-green-600" />
                <span>ROI Projections & Financial Impact</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={ROI_PROJECTIONS}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="quarter" />
                    <YAxis />
                    <Tooltip formatter={(value) => [`$${value}M`, '']} />
                    <Bar dataKey="revenue" fill={COLORS.primary} name="Revenue" />
                    <Bar dataKey="costs" fill={COLORS.danger} name="Costs" />
                    <Bar dataKey="profit" fill={COLORS.secondary} name="Profit" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Market Position Tab */}
        <TabsContent value="market" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Market Opportunity */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Globe className="h-5 w-5 text-blue-600" />
                  <span>Market Opportunity by Vertical</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={MARKET_POSITIONING_DATA}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="vertical" />
                      <YAxis />
                      <Tooltip formatter={(value) => [`$${value}B`, '']} />
                      <Bar dataKey="market_size" fill={COLORS.primary} name="Market Size" />
                      <Bar dataKey="opportunity" fill={COLORS.secondary} name="Opportunity" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>

            {/* Vertical Focus */}
            <Card>
              <CardHeader>
                <CardTitle>Vertical Market Analysis</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {MARKET_POSITIONING_DATA.map((vertical) => (
                  <div key={vertical.vertical} className="border rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer"
                       onClick={() => setSelectedVertical(vertical.vertical)}>
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="font-semibold">{vertical.vertical}</h3>
                      <Badge variant={selectedVertical === vertical.vertical ? 'default' : 'outline'}>
                        ${vertical.opportunity}B Opportunity
                      </Badge>
                    </div>
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span>Market Size</span>
                        <span className="font-medium">${vertical.market_size}B</span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span>Current Penetration</span>
                        <span className="font-medium">{vertical.penetration}%</span>
                      </div>
                      <Progress value={vertical.penetration} className="h-2" />
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>

          {/* Strategic Recommendations */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Lightbulb className="h-5 w-5 text-yellow-500" />
                <span>Strategic Market Recommendations</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h3 className="font-semibold mb-3 flex items-center space-x-2">
                    <Target className="h-4 w-4 text-blue-600" />
                    <span>Primary Focus Areas</span>
                  </h3>
                  <ul className="space-y-2">
                    <li className="flex items-start space-x-2">
                      <CheckCircle className="h-4 w-4 text-green-500 mt-0.5" />
                      <span className="text-sm">Manufacturing: Predictive Quality & Process Optimization</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <CheckCircle className="h-4 w-4 text-green-500 mt-0.5" />
                      <span className="text-sm">Financial Services: Portfolio Risk & Fraud Detection</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <CheckCircle className="h-4 w-4 text-green-500 mt-0.5" />
                      <span className="text-sm">Logistics: Route Optimization & Supply Chain</span>
                    </li>
                  </ul>
                </div>
                
                <div>
                  <h3 className="font-semibold mb-3 flex items-center space-x-2">
                    <Handshake className="h-4 w-4 text-purple-600" />
                    <span>Partnership Strategy</span>
                  </h3>
                  <ul className="space-y-2">
                    <li className="flex items-start space-x-2">
                      <ArrowRight className="h-4 w-4 text-blue-500 mt-0.5" />
                      <span className="text-sm">System Integrators: Accenture, Deloitte, IBM</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <ArrowRight className="h-4 w-4 text-blue-500 mt-0.5" />
                      <span className="text-sm">Technology Partners: Cloud providers & AI platforms</span>
                    </li>
                    <li className="flex items-start space-x-2">
                      <ArrowRight className="h-4 w-4 text-blue-500 mt-0.5" />
                      <span className="text-sm">Industry Specialists: Vertical-specific consultancies</span>
                    </li>
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Success Metrics Tab */}
        <TabsContent value="metrics" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Key Performance Indicators */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <BarChart3 className="h-5 w-5 text-blue-600" />
                  <span>Key Performance Indicators</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {SUCCESS_METRICS.map((metric, index) => (
                  <div key={index} className="border rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="font-semibold text-sm">{metric.metric}</h3>
                      <div className="flex items-center space-x-1">
                        <TrendingUp className={`h-4 w-4 ${metric.trend === 'up' ? 'text-green-500' : 'text-red-500'}`} />
                        <span className={`text-sm font-medium ${metric.trend === 'up' ? 'text-green-600' : 'text-red-600'}`}>
                          {metric.trend === 'up' ? '↗' : '↘'}
                        </span>
                      </div>
                    </div>
                    <div className="flex justify-between text-sm mb-2">
                      <span>Current: <span className="font-medium">
                        {metric.metric.includes('Deal Size') ? `$${metric.current.toLocaleString()}` : 
                         metric.metric.includes('Satisfaction') ? `${metric.current}/5.0` :
                         metric.metric.includes('Length') ? `${metric.current} days` :
                         `${metric.current}%`}
                      </span></span>
                      <span>Target: <span className="font-medium text-blue-600">
                        {metric.metric.includes('Deal Size') ? `$${metric.target.toLocaleString()}` : 
                         metric.metric.includes('Satisfaction') ? `${metric.target}/5.0` :
                         metric.metric.includes('Length') ? `${metric.target} days` :
                         `${metric.target}%`}
                      </span></span>
                    </div>
                    <Progress 
                      value={metric.metric.includes('Length') ? 
                        ((metric.current - metric.target) / metric.current) * 100 :
                        (metric.current / metric.target) * 100
                      } 
                      className="h-2" 
                    />
                  </div>
                ))}
              </CardContent>
            </Card>

            {/* Success Framework */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Award className="h-5 w-5 text-purple-600" />
                  <span>Success Framework</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-4">
                  <div>
                    <h3 className="font-semibold mb-2 flex items-center space-x-2">
                      <Cpu className="h-4 w-4 text-blue-600" />
                      <span>Technical Excellence</span>
                    </h3>
                    <ul className="text-sm space-y-1">
                      <li>• Quantum advantage demonstration on client data</li>
                      <li>• LTC audit trail for compliance and explainability</li>
                      <li>• Head-to-head benchmarks vs classical solvers</li>
                    </ul>
                  </div>
                  
                  <div>
                    <h3 className="font-semibold mb-2 flex items-center space-x-2">
                      <DollarSign className="h-4 w-4 text-green-600" />
                      <span>Business Impact</span>
                    </h3>
                    <ul className="text-sm space-y-1">
                      <li>• Measurable ROI within 6 months</li>
                      <li>• Cost reduction or revenue increase</li>
                      <li>• Competitive advantage demonstration</li>
                    </ul>
                  </div>
                  
                  <div>
                    <h3 className="font-semibold mb-2 flex items-center space-x-2">
                      <Users className="h-4 w-4 text-purple-600" />
                      <span>Customer Success</span>
                    </h3>
                    <ul className="text-sm space-y-1">
                      <li>• Executive and technical stakeholder satisfaction</li>
                      <li>• Successful pilot to production transition</li>
                      <li>• Reference customer and case study development</li>
                    </ul>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Roadmap Tab */}
        <TabsContent value="roadmap" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Rocket className="h-5 w-5 text-purple-600" />
                <span>Strategic Implementation Roadmap</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                {IMPLEMENTATION_PHASES.map((phase, index) => (
                  <div key={phase.id} className="relative">
                    {index < IMPLEMENTATION_PHASES.length - 1 && (
                      <div className="absolute left-4 top-8 w-0.5 h-16 bg-gray-300" />
                    )}
                    <div className="flex items-start space-x-4">
                      <div className={`w-8 h-8 rounded-full flex items-center justify-center text-white text-sm font-bold ${getStatusColor(phase.status)}`}>
                        {index + 1}
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center justify-between mb-2">
                          <h3 className="font-semibold">{phase.title}</h3>
                          <div className="flex items-center space-x-2">
                            <Badge className={getPriorityColor(phase.priority)}>
                              {phase.priority}
                            </Badge>
                            <Badge variant="outline">
                              {phase.timeline}
                            </Badge>
                          </div>
                        </div>
                        <div className="space-y-2">
                          <Progress value={phase.progress} className="h-2" />
                          <div className="flex justify-between text-sm text-gray-600">
                            <span>{phase.progress}% Complete</span>
                            <span>{phase.impact}</span>
                          </div>
                        </div>
                      </div>
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

export default StrategicImplementationDashboard;