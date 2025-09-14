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
  Users, 
  Handshake, 
  GraduationCap, 
  Award, 
  Target, 
  TrendingUp, 
  DollarSign, 
  Globe, 
  Building2, 
  Briefcase, 
  BookOpen, 
  Video, 
  FileText, 
  Download, 
  Upload, 
  CheckCircle, 
  Clock, 
  Star, 
  Zap, 
  Shield, 
  Brain, 
  Cpu, 
  Database,
  Settings,
  Bell,
  RefreshCw,
  AlertTriangle,
  XCircle,
  Play,
  Pause,
  Calendar,
  Mail,
  Phone,
  MapPin,
  ExternalLink,
  ChevronRight,
  Plus,
  Minus,
  Edit,
  Trash2,
  Search,
  Filter,
  BarChart3,
  PieChart as PieChartIcon,
  Activity,
  Layers,
  Network,
  Rocket,
  Lightbulb,
  Factory,
  Banknote,
  Truck
} from 'lucide-react';

interface Partner {
  id: string;
  name: string;
  type: 'si' | 'consulting' | 'technology' | 'reseller';
  tier: 'platinum' | 'gold' | 'silver' | 'bronze';
  verticals: string[];
  certificationLevel: number;
  revenue: number;
  deals: number;
  status: 'active' | 'onboarding' | 'inactive';
  lastActivity: string;
  contact: {
    name: string;
    email: string;
    phone: string;
  };
}

interface TrainingModule {
  id: string;
  title: string;
  category: 'technical' | 'sales' | 'business' | 'certification';
  duration: number;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  completionRate: number;
  prerequisites: string[];
  description: string;
}

interface CertificationTrack {
  id: string;
  name: string;
  level: 'associate' | 'professional' | 'expert';
  modules: string[];
  duration: number;
  passingScore: number;
  benefits: string[];
}

const PARTNER_TYPES = {
  si: { label: 'System Integrator', icon: Building2, color: '#3b82f6' },
  consulting: { label: 'Consulting Partner', icon: Users, color: '#10b981' },
  technology: { label: 'Technology Partner', icon: Cpu, color: '#8b5cf6' },
  reseller: { label: 'Reseller Partner', icon: Handshake, color: '#f59e0b' }
};

const PARTNER_TIERS = {
  platinum: { label: 'Platinum', color: '#e5e7eb', benefits: ['Priority Support', 'Co-marketing', 'Executive Access'] },
  gold: { label: 'Gold', color: '#fbbf24', benefits: ['Technical Support', 'Marketing Materials', 'Training Credits'] },
  silver: { label: 'Silver', color: '#9ca3af', benefits: ['Standard Support', 'Basic Training', 'Portal Access'] },
  bronze: { label: 'Bronze', color: '#92400e', benefits: ['Self-Service Portal', 'Basic Documentation'] }
};

const SAMPLE_PARTNERS: Partner[] = [
  {
    id: '1',
    name: 'Accenture Quantum Practice',
    type: 'si',
    tier: 'platinum',
    verticals: ['Manufacturing', 'Finance', 'Energy'],
    certificationLevel: 95,
    revenue: 2400000,
    deals: 12,
    status: 'active',
    lastActivity: '2024-01-15',
    contact: {
      name: 'Sarah Chen',
      email: 'sarah.chen@accenture.com',
      phone: '+1-555-0123'
    }
  },
  {
    id: '2',
    name: 'Deloitte Digital',
    type: 'consulting',
    tier: 'gold',
    verticals: ['Finance', 'Healthcare'],
    certificationLevel: 87,
    revenue: 1800000,
    deals: 8,
    status: 'active',
    lastActivity: '2024-01-12',
    contact: {
      name: 'Michael Rodriguez',
      email: 'm.rodriguez@deloitte.com',
      phone: '+1-555-0124'
    }
  },
  {
    id: '3',
    name: 'IBM Quantum Network',
    type: 'technology',
    tier: 'platinum',
    verticals: ['Manufacturing', 'Logistics', 'Energy'],
    certificationLevel: 92,
    revenue: 3200000,
    deals: 15,
    status: 'active',
    lastActivity: '2024-01-14',
    contact: {
      name: 'Dr. James Wilson',
      email: 'j.wilson@ibm.com',
      phone: '+1-555-0125'
    }
  },
  {
    id: '4',
    name: 'QuantumTech Solutions',
    type: 'reseller',
    tier: 'silver',
    verticals: ['Manufacturing'],
    certificationLevel: 73,
    revenue: 650000,
    deals: 4,
    status: 'onboarding',
    lastActivity: '2024-01-10',
    contact: {
      name: 'Lisa Park',
      email: 'lisa.park@quantumtech.com',
      phone: '+1-555-0126'
    }
  }
];

const TRAINING_MODULES: TrainingModule[] = [
  {
    id: 'nqba-101',
    title: 'NQBA Platform Fundamentals',
    category: 'technical',
    duration: 120,
    difficulty: 'beginner',
    completionRate: 94,
    prerequisites: [],
    description: 'Introduction to NQBA architecture, core components, and basic quantum concepts'
  },
  {
    id: 'dynex-deep-dive',
    title: 'Dynex QaaS Integration',
    category: 'technical',
    duration: 180,
    difficulty: 'intermediate',
    completionRate: 87,
    prerequisites: ['nqba-101'],
    description: 'Advanced training on Dynex quantum computing integration and optimization'
  },
  {
    id: 'sales-methodology',
    title: 'Quantum Sales Methodology',
    category: 'sales',
    duration: 90,
    difficulty: 'beginner',
    completionRate: 91,
    prerequisites: [],
    description: 'Proven sales techniques for quantum computing solutions'
  },
  {
    id: 'vertical-manufacturing',
    title: 'Manufacturing Use Cases',
    category: 'business',
    duration: 150,
    difficulty: 'intermediate',
    completionRate: 89,
    prerequisites: ['nqba-101'],
    description: 'Deep dive into manufacturing optimization use cases and ROI models'
  },
  {
    id: 'certification-prep',
    title: 'NQBA Certification Preparation',
    category: 'certification',
    duration: 240,
    difficulty: 'advanced',
    completionRate: 76,
    prerequisites: ['nqba-101', 'dynex-deep-dive'],
    description: 'Comprehensive preparation for NQBA professional certification'
  }
];

const CERTIFICATION_TRACKS: CertificationTrack[] = [
  {
    id: 'associate',
    name: 'NQBA Associate',
    level: 'associate',
    modules: ['nqba-101', 'sales-methodology'],
    duration: 210,
    passingScore: 80,
    benefits: ['Partner Portal Access', 'Basic Marketing Materials', 'Community Forum']
  },
  {
    id: 'professional',
    name: 'NQBA Professional',
    level: 'professional',
    modules: ['nqba-101', 'dynex-deep-dive', 'vertical-manufacturing', 'sales-methodology'],
    duration: 540,
    passingScore: 85,
    benefits: ['Technical Support', 'Advanced Materials', 'Co-marketing Opportunities']
  },
  {
    id: 'expert',
    name: 'NQBA Expert',
    level: 'expert',
    modules: ['nqba-101', 'dynex-deep-dive', 'vertical-manufacturing', 'sales-methodology', 'certification-prep'],
    duration: 780,
    passingScore: 90,
    benefits: ['Priority Support', 'Executive Access', 'Revenue Sharing', 'Co-development Rights']
  }
];

const COLORS = {
  primary: '#3b82f6',
  secondary: '#10b981',
  accent: '#8b5cf6',
  warning: '#f59e0b',
  error: '#ef4444',
  success: '#10b981',
  quantum: '#6366f1'
};

export const PartnerEnablementPlatform: React.FC = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [partners, setPartners] = useState<Partner[]>(SAMPLE_PARTNERS);
  const [selectedPartner, setSelectedPartner] = useState<Partner | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState<string>('all');
  const [filterTier, setFilterTier] = useState<string>('all');

  // Filter partners based on search and filters
  const filteredPartners = useMemo(() => {
    return partners.filter(partner => {
      const matchesSearch = partner.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           partner.contact.name.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesType = filterType === 'all' || partner.type === filterType;
      const matchesTier = filterTier === 'all' || partner.tier === filterTier;
      return matchesSearch && matchesType && matchesTier;
    });
  }, [partners, searchTerm, filterType, filterTier]);

  // Calculate partner metrics
  const partnerMetrics = useMemo(() => {
    const totalRevenue = partners.reduce((sum, p) => sum + p.revenue, 0);
    const totalDeals = partners.reduce((sum, p) => sum + p.deals, 0);
    const avgCertification = partners.reduce((sum, p) => sum + p.certificationLevel, 0) / partners.length;
    const activePartners = partners.filter(p => p.status === 'active').length;
    
    return {
      totalRevenue,
      totalDeals,
      avgCertification,
      activePartners,
      totalPartners: partners.length
    };
  }, [partners]);

  // Partner distribution by type
  const partnerTypeDistribution = useMemo(() => {
    const distribution = Object.keys(PARTNER_TYPES).map(type => ({
      name: PARTNER_TYPES[type as keyof typeof PARTNER_TYPES].label,
      value: partners.filter(p => p.type === type).length,
      color: PARTNER_TYPES[type as keyof typeof PARTNER_TYPES].color
    }));
    return distribution;
  }, [partners]);

  // Revenue by tier
  const revenueByTier = useMemo(() => {
    return Object.keys(PARTNER_TIERS).map(tier => ({
      tier: PARTNER_TIERS[tier as keyof typeof PARTNER_TIERS].label,
      revenue: partners.filter(p => p.tier === tier).reduce((sum, p) => sum + p.revenue, 0),
      count: partners.filter(p => p.tier === tier).length,
      color: PARTNER_TIERS[tier as keyof typeof PARTNER_TIERS].color
    }));
  }, [partners]);

  // Training completion rates
  const trainingMetrics = useMemo(() => {
    return TRAINING_MODULES.map(module => ({
      name: module.title,
      completion: module.completionRate,
      category: module.category,
      difficulty: module.difficulty
    }));
  }, []);

  return (
    <div className="w-full max-w-7xl mx-auto p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="space-y-2">
          <div className="flex items-center space-x-3">
            <div className="relative">
              <Network className="h-8 w-8 text-blue-600" />
              <Handshake className="h-4 w-4 text-green-500 absolute -top-1 -right-1" />
            </div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Partner Enablement Platform
            </h1>
          </div>
          <p className="text-gray-600">Comprehensive partner training, certification, and enablement ecosystem</p>
        </div>
        
        <div className="flex items-center space-x-3">
          <Badge variant="outline" className="flex items-center space-x-2">
            <Users className="h-4 w-4" />
            <span>{partnerMetrics.activePartners} Active Partners</span>
          </Badge>
          <Button variant="outline" size="sm">
            <Plus className="h-4 w-4 mr-2" />
            Add Partner
          </Button>
        </div>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-6">
          <TabsTrigger value="overview" className="flex items-center space-x-2">
            <BarChart3 className="h-4 w-4" />
            <span>Overview</span>
          </TabsTrigger>
          <TabsTrigger value="partners" className="flex items-center space-x-2">
            <Users className="h-4 w-4" />
            <span>Partners</span>
          </TabsTrigger>
          <TabsTrigger value="training" className="flex items-center space-x-2">
            <GraduationCap className="h-4 w-4" />
            <span>Training</span>
          </TabsTrigger>
          <TabsTrigger value="certification" className="flex items-center space-x-2">
            <Award className="h-4 w-4" />
            <span>Certification</span>
          </TabsTrigger>
          <TabsTrigger value="resources" className="flex items-center space-x-2">
            <BookOpen className="h-4 w-4" />
            <span>Resources</span>
          </TabsTrigger>
          <TabsTrigger value="analytics" className="flex items-center space-x-2">
            <Activity className="h-4 w-4" />
            <span>Analytics</span>
          </TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-6">
          {/* Key Metrics */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <Card>
              <CardContent className="p-4 text-center">
                <Users className="h-8 w-8 text-blue-600 mx-auto mb-2" />
                <div className="text-2xl font-bold text-blue-600">
                  {partnerMetrics.totalPartners}
                </div>
                <div className="text-sm text-gray-600">Total Partners</div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-4 text-center">
                <DollarSign className="h-8 w-8 text-green-600 mx-auto mb-2" />
                <div className="text-2xl font-bold text-green-600">
                  ${(partnerMetrics.totalRevenue / 1000000).toFixed(1)}M
                </div>
                <div className="text-sm text-gray-600">Partner Revenue</div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-4 text-center">
                <Target className="h-8 w-8 text-purple-600 mx-auto mb-2" />
                <div className="text-2xl font-bold text-purple-600">
                  {partnerMetrics.totalDeals}
                </div>
                <div className="text-sm text-gray-600">Active Deals</div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-4 text-center">
                <Award className="h-8 w-8 text-orange-600 mx-auto mb-2" />
                <div className="text-2xl font-bold text-orange-600">
                  {partnerMetrics.avgCertification.toFixed(0)}%
                </div>
                <div className="text-sm text-gray-600">Avg Certification</div>
              </CardContent>
            </Card>
          </div>

          {/* Partner Distribution */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <PieChartIcon className="h-5 w-5 text-blue-600" />
                  <span>Partner Type Distribution</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={partnerTypeDistribution}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, value }) => `${name}: ${value}`}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {partnerTypeDistribution.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <BarChart3 className="h-5 w-5 text-green-600" />
                  <span>Revenue by Partner Tier</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={revenueByTier}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="tier" />
                    <YAxis />
                    <Tooltip formatter={(value) => [`$${value.toLocaleString()}`, 'Revenue']} />
                    <Bar dataKey="revenue" fill={COLORS.success} />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>

          {/* Recent Activity */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Activity className="h-5 w-5 text-purple-600" />
                <span>Recent Partner Activity</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {partners.slice(0, 5).map((partner) => {
                  const PartnerIcon = PARTNER_TYPES[partner.type].icon;
                  return (
                    <div key={partner.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                      <div className="flex items-center space-x-3">
                        <PartnerIcon className="h-6 w-6" style={{ color: PARTNER_TYPES[partner.type].color }} />
                        <div>
                          <div className="font-medium">{partner.name}</div>
                          <div className="text-sm text-gray-600">{partner.contact.name}</div>
                        </div>
                      </div>
                      <div className="text-right">
                        <Badge variant={partner.status === 'active' ? 'default' : 'secondary'}>
                          {partner.status}
                        </Badge>
                        <div className="text-sm text-gray-600 mt-1">{partner.lastActivity}</div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Partners Tab */}
        <TabsContent value="partners" className="space-y-6">
          {/* Search and Filters */}
          <Card>
            <CardContent className="p-4">
              <div className="flex flex-wrap items-center gap-4">
                <div className="flex-1 min-w-64">
                  <div className="relative">
                    <Search className="h-4 w-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                    <Input
                      placeholder="Search partners..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="pl-10"
                    />
                  </div>
                </div>
                
                <Select value={filterType} onValueChange={setFilterType}>
                  <SelectTrigger className="w-48">
                    <SelectValue placeholder="Filter by type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Types</SelectItem>
                    {Object.entries(PARTNER_TYPES).map(([key, type]) => (
                      <SelectItem key={key} value={key}>{type.label}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                
                <Select value={filterTier} onValueChange={setFilterTier}>
                  <SelectTrigger className="w-48">
                    <SelectValue placeholder="Filter by tier" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Tiers</SelectItem>
                    {Object.entries(PARTNER_TIERS).map(([key, tier]) => (
                      <SelectItem key={key} value={key}>{tier.label}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
          </Card>

          {/* Partners List */}
          <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
            {filteredPartners.map((partner) => {
              const PartnerIcon = PARTNER_TYPES[partner.type].icon;
              const tierColor = PARTNER_TIERS[partner.tier].color;
              
              return (
                <Card key={partner.id} className="hover:shadow-lg transition-shadow cursor-pointer"
                      onClick={() => setSelectedPartner(partner)}>
                  <CardHeader className="pb-3">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <PartnerIcon className="h-6 w-6" style={{ color: PARTNER_TYPES[partner.type].color }} />
                        <div>
                          <CardTitle className="text-lg">{partner.name}</CardTitle>
                          <p className="text-sm text-gray-600">{PARTNER_TYPES[partner.type].label}</p>
                        </div>
                      </div>
                      <Badge style={{ backgroundColor: tierColor, color: 'white' }}>
                        {PARTNER_TIERS[partner.tier].label}
                      </Badge>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <div className="text-gray-600">Revenue</div>
                        <div className="font-bold">${(partner.revenue / 1000000).toFixed(1)}M</div>
                      </div>
                      <div>
                        <div className="text-gray-600">Deals</div>
                        <div className="font-bold">{partner.deals}</div>
                      </div>
                    </div>
                    
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span>Certification</span>
                        <span>{partner.certificationLevel}%</span>
                      </div>
                      <Progress value={partner.certificationLevel} className="h-2" />
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <div className="flex flex-wrap gap-1">
                        {partner.verticals.slice(0, 2).map((vertical) => (
                          <Badge key={vertical} variant="outline" className="text-xs">
                            {vertical}
                          </Badge>
                        ))}
                        {partner.verticals.length > 2 && (
                          <Badge variant="outline" className="text-xs">
                            +{partner.verticals.length - 2}
                          </Badge>
                        )}
                      </div>
                      <Badge variant={partner.status === 'active' ? 'default' : 'secondary'}>
                        {partner.status}
                      </Badge>
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </TabsContent>

        {/* Training Tab */}
        <TabsContent value="training" className="space-y-6">
          {/* Training Overview */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <GraduationCap className="h-5 w-5 text-blue-600" />
                <span>Training Module Completion Rates</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={trainingMetrics}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="completion" fill={COLORS.primary} />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Training Modules */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {TRAINING_MODULES.map((module) => {
              const categoryColors = {
                technical: 'bg-blue-100 text-blue-800',
                sales: 'bg-green-100 text-green-800',
                business: 'bg-purple-100 text-purple-800',
                certification: 'bg-orange-100 text-orange-800'
              };
              
              const difficultyColors = {
                beginner: 'bg-green-100 text-green-800',
                intermediate: 'bg-yellow-100 text-yellow-800',
                advanced: 'bg-red-100 text-red-800'
              };
              
              return (
                <Card key={module.id}>
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <CardTitle className="text-lg">{module.title}</CardTitle>
                      <div className="flex space-x-2">
                        <Badge className={categoryColors[module.category]}>
                          {module.category}
                        </Badge>
                        <Badge className={difficultyColors[module.difficulty]}>
                          {module.difficulty}
                        </Badge>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <p className="text-sm text-gray-600">{module.description}</p>
                    
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <div className="text-gray-600">Duration</div>
                        <div className="font-bold">{module.duration} minutes</div>
                      </div>
                      <div>
                        <div className="text-gray-600">Completion Rate</div>
                        <div className="font-bold">{module.completionRate}%</div>
                      </div>
                    </div>
                    
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span>Progress</span>
                        <span>{module.completionRate}%</span>
                      </div>
                      <Progress value={module.completionRate} className="h-2" />
                    </div>
                    
                    {module.prerequisites.length > 0 && (
                      <div>
                        <div className="text-sm text-gray-600 mb-1">Prerequisites:</div>
                        <div className="flex flex-wrap gap-1">
                          {module.prerequisites.map((prereq) => (
                            <Badge key={prereq} variant="outline" className="text-xs">
                              {prereq}
                            </Badge>
                          ))}
                        </div>
                      </div>
                    )}
                    
                    <Button className="w-full">
                      <Play className="h-4 w-4 mr-2" />
                      Start Module
                    </Button>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </TabsContent>

        {/* Certification Tab */}
        <TabsContent value="certification" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {CERTIFICATION_TRACKS.map((track) => {
              const levelColors = {
                associate: 'bg-green-100 text-green-800 border-green-200',
                professional: 'bg-blue-100 text-blue-800 border-blue-200',
                expert: 'bg-purple-100 text-purple-800 border-purple-200'
              };
              
              return (
                <Card key={track.id} className={`border-2 ${levelColors[track.level]}`}>
                  <CardHeader>
                    <div className="text-center">
                      <Award className="h-12 w-12 mx-auto mb-3" />
                      <CardTitle className="text-xl">{track.name}</CardTitle>
                      <Badge className={levelColors[track.level]}>
                        {track.level.toUpperCase()}
                      </Badge>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <div className="text-gray-600">Duration</div>
                        <div className="font-bold">{track.duration} minutes</div>
                      </div>
                      <div>
                        <div className="text-gray-600">Passing Score</div>
                        <div className="font-bold">{track.passingScore}%</div>
                      </div>
                    </div>
                    
                    <div>
                      <div className="text-sm text-gray-600 mb-2">Required Modules:</div>
                      <div className="space-y-1">
                        {track.modules.map((moduleId) => {
                          const module = TRAINING_MODULES.find(m => m.id === moduleId);
                          return (
                            <div key={moduleId} className="flex items-center space-x-2 text-sm">
                              <CheckCircle className="h-4 w-4 text-green-600" />
                              <span>{module?.title || moduleId}</span>
                            </div>
                          );
                        })}
                      </div>
                    </div>
                    
                    <div>
                      <div className="text-sm text-gray-600 mb-2">Benefits:</div>
                      <div className="space-y-1">
                        {track.benefits.map((benefit, index) => (
                          <div key={index} className="flex items-center space-x-2 text-sm">
                            <Star className="h-4 w-4 text-yellow-500" />
                            <span>{benefit}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                    
                    <Button className="w-full">
                      <Rocket className="h-4 w-4 mr-2" />
                      Start Certification
                    </Button>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </TabsContent>

        {/* Resources Tab */}
        <TabsContent value="resources" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Sales Materials */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Briefcase className="h-5 w-5 text-blue-600" />
                  <span>Sales Materials</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="space-y-2">
                  <Button variant="outline" className="w-full justify-start">
                    <FileText className="h-4 w-4 mr-2" />
                    NQBA Sales Deck (Manufacturing)
                    <Download className="h-4 w-4 ml-auto" />
                  </Button>
                  <Button variant="outline" className="w-full justify-start">
                    <FileText className="h-4 w-4 mr-2" />
                    ROI Calculator Template
                    <Download className="h-4 w-4 ml-auto" />
                  </Button>
                  <Button variant="outline" className="w-full justify-start">
                    <FileText className="h-4 w-4 mr-2" />
                    Competitive Battlecards
                    <Download className="h-4 w-4 ml-auto" />
                  </Button>
                  <Button variant="outline" className="w-full justify-start">
                    <Video className="h-4 w-4 mr-2" />
                    Demo Video Library
                    <ExternalLink className="h-4 w-4 ml-auto" />
                  </Button>
                </div>
              </CardContent>
            </Card>

            {/* Technical Resources */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Cpu className="h-5 w-5 text-purple-600" />
                  <span>Technical Resources</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="space-y-2">
                  <Button variant="outline" className="w-full justify-start">
                    <BookOpen className="h-4 w-4 mr-2" />
                    API Documentation
                    <ExternalLink className="h-4 w-4 ml-auto" />
                  </Button>
                  <Button variant="outline" className="w-full justify-start">
                    <FileText className="h-4 w-4 mr-2" />
                    Architecture Whitepaper
                    <Download className="h-4 w-4 ml-auto" />
                  </Button>
                  <Button variant="outline" className="w-full justify-start">
                    <Cpu className="h-4 w-4 mr-2" />
                    Integration Guides
                    <Download className="h-4 w-4 ml-auto" />
                  </Button>
                  <Button variant="outline" className="w-full justify-start">
                    <Database className="h-4 w-4 mr-2" />
                    Sample Datasets
                    <Download className="h-4 w-4 ml-auto" />
                  </Button>
                </div>
              </CardContent>
            </Card>

            {/* Marketing Materials */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Globe className="h-5 w-5 text-green-600" />
                  <span>Marketing Materials</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="space-y-2">
                  <Button variant="outline" className="w-full justify-start">
                    <FileText className="h-4 w-4 mr-2" />
                    Brand Guidelines
                    <Download className="h-4 w-4 ml-auto" />
                  </Button>
                  <Button variant="outline" className="w-full justify-start">
                    <FileText className="h-4 w-4 mr-2" />
                    Case Study Templates
                    <Download className="h-4 w-4 ml-auto" />
                  </Button>
                  <Button variant="outline" className="w-full justify-start">
                    <Globe className="h-4 w-4 mr-2" />
                    Web Assets & Logos
                    <Download className="h-4 w-4 ml-auto" />
                  </Button>
                  <Button variant="outline" className="w-full justify-start">
                    <Video className="h-4 w-4 mr-2" />
                    Customer Testimonials
                    <ExternalLink className="h-4 w-4 ml-auto" />
                  </Button>
                </div>
              </CardContent>
            </Card>

            {/* Support Resources */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Shield className="h-5 w-5 text-orange-600" />
                  <span>Support Resources</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="space-y-2">
                  <Button variant="outline" className="w-full justify-start">
                    <BookOpen className="h-4 w-4 mr-2" />
                    Knowledge Base
                    <ExternalLink className="h-4 w-4 ml-auto" />
                  </Button>
                  <Button variant="outline" className="w-full justify-start">
                    <Users className="h-4 w-4 mr-2" />
                    Partner Community Forum
                    <ExternalLink className="h-4 w-4 ml-auto" />
                  </Button>
                  <Button variant="outline" className="w-full justify-start">
                    <Phone className="h-4 w-4 mr-2" />
                    Technical Support Portal
                    <ExternalLink className="h-4 w-4 ml-auto" />
                  </Button>
                  <Button variant="outline" className="w-full justify-start">
                    <Calendar className="h-4 w-4 mr-2" />
                    Office Hours Schedule
                    <ExternalLink className="h-4 w-4 ml-auto" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Analytics Tab */}
        <TabsContent value="analytics" className="space-y-6">
          {/* Partner Performance */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <TrendingUp className="h-5 w-5 text-green-600" />
                <span>Partner Performance Trends</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={[
                  { month: 'Jan', revenue: 1200000, deals: 8, partners: 12 },
                  { month: 'Feb', revenue: 1450000, deals: 11, partners: 14 },
                  { month: 'Mar', revenue: 1680000, deals: 13, partners: 15 },
                  { month: 'Apr', revenue: 1920000, deals: 16, partners: 17 },
                  { month: 'May', revenue: 2150000, deals: 19, partners: 18 },
                  { month: 'Jun', revenue: 2380000, deals: 22, partners: 20 }
                ]}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis yAxisId="left" />
                  <YAxis yAxisId="right" orientation="right" />
                  <Tooltip />
                  <Legend />
                  <Line yAxisId="left" type="monotone" dataKey="revenue" stroke={COLORS.primary} name="Revenue" />
                  <Line yAxisId="right" type="monotone" dataKey="deals" stroke={COLORS.success} name="Deals" />
                  <Line yAxisId="right" type="monotone" dataKey="partners" stroke={COLORS.accent} name="Active Partners" />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Certification Progress */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Award className="h-5 w-5 text-purple-600" />
                  <span>Certification Distribution</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={250}>
                  <PieChart>
                    <Pie
                      data={[
                        { name: 'Associate', value: 45, color: '#10b981' },
                        { name: 'Professional', value: 32, color: '#3b82f6' },
                        { name: 'Expert', value: 18, color: '#8b5cf6' },
                        { name: 'Not Certified', value: 5, color: '#6b7280' }
                      ]}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, value }) => `${name}: ${value}%`}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {[
                        { name: 'Associate', value: 45, color: '#10b981' },
                        { name: 'Professional', value: 32, color: '#3b82f6' },
                        { name: 'Expert', value: 18, color: '#8b5cf6' },
                        { name: 'Not Certified', value: 5, color: '#6b7280' }
                      ].map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Activity className="h-5 w-5 text-blue-600" />
                  <span>Training Engagement</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Active Learners</span>
                    <span className="font-bold">127</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Modules Completed</span>
                    <span className="font-bold">1,234</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Avg. Completion Time</span>
                    <span className="font-bold">4.2 days</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Satisfaction Score</span>
                    <span className="font-bold">4.7/5</span>
                  </div>
                  
                  <div className="pt-4">
                    <h4 className="font-semibold mb-2">Top Performing Modules</h4>
                    <div className="space-y-2">
                      {TRAINING_MODULES.slice(0, 3).map((module) => (
                        <div key={module.id} className="flex justify-between items-center text-sm">
                          <span>{module.title}</span>
                          <span className="font-bold">{module.completionRate}%</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default PartnerEnablementPlatform;