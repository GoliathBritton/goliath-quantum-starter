'use client';

import React, { useState, useMemo } from 'react';
import {
  Search,
  Filter,
  Download,
  Users,
  Building,
  Zap,
  Globe,
  Star,
  TrendingUp,
  Award,
  CheckCircle,
  X,
  Mail,
  Phone,
  MapPin,
  Calendar,
  Mountain
} from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';

interface Certification {
  id: string;
  name: string;
  level: string;
  status: 'active' | 'expired' | 'pending';
  score: number;
  expiryDate: string;
  vertical?: string;
}

interface Partner {
  id: string;
  name: string;
  type: 'technology' | 'channel' | 'strategic' | 'implementation';
  tier: 'Platinum' | 'Gold' | 'Silver' | 'Bronze';
  status: 'active' | 'inactive' | 'pending';
  logo: string;
  description: string;
  verticals: string[];
  capabilities: string[];
  certifications: Certification[];
  performance: {
    revenue: number;
    deals: number;
    satisfaction: number;
    enablementScore: number;
  };
  contact: {
    primaryContact: string;
    email: string;
    phone: string;
    region: string;
    timezone: string;
  };
  joinDate: string;
}

const mockPartners: Partner[] = [
  {
    id: '1',
    name: 'TechFlow Solutions',
    type: 'technology',
    tier: 'Platinum',
    status: 'active',
    logo: '/api/placeholder/60/60',
    description: 'Leading AI and quantum computing integration specialist',
    verticals: ['Financial Services', 'Healthcare', 'Manufacturing'],
    capabilities: ['AI Integration', 'Quantum Computing', 'Cloud Migration', 'Data Analytics'],
    certifications: [
      {
        id: 'cert1',
        name: 'Quantum AI Specialist',
        level: 'Expert',
        status: 'active',
        score: 95,
        expiryDate: '2025-06-15',
        vertical: 'Technology'
      },
      {
        id: 'cert2',
        name: 'Cloud Architecture',
        level: 'Advanced',
        status: 'active',
        score: 88,
        expiryDate: '2024-12-20'
      }
    ],
    performance: {
      revenue: 2500000,
      deals: 45,
      satisfaction: 4.8,
      enablementScore: 92
    },
    contact: {
      primaryContact: 'Sarah Chen',
      email: 'sarah.chen@techflow.com',
      phone: '+1-555-0123',
      region: 'North America',
      timezone: 'PST'
    },
    joinDate: '2023-01-15'
  },
  {
    id: '2',
    name: 'Global Systems Inc',
    type: 'channel',
    tier: 'Gold',
    status: 'active',
    logo: '/api/placeholder/60/60',
    description: 'Worldwide distribution and implementation partner',
    verticals: ['Retail', 'Logistics', 'Energy'],
    capabilities: ['Implementation', 'Training', 'Support', 'Consulting'],
    certifications: [
      {
        id: 'cert3',
        name: 'Implementation Specialist',
        level: 'Advanced',
        status: 'active',
        score: 85,
        expiryDate: '2024-09-30'
      }
    ],
    performance: {
      revenue: 1800000,
      deals: 32,
      satisfaction: 4.6,
      enablementScore: 87
    },
    contact: {
      primaryContact: 'Michael Rodriguez',
      email: 'michael.r@globalsystems.com',
      phone: '+1-555-0456',
      region: 'Global',
      timezone: 'EST'
    },
    joinDate: '2022-08-20'
  }
];

const AlliancePartnerStrategy: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState<string>('all');
  const [filterTier, setFilterTier] = useState<string>('all');
  const [filterStatus, setFilterStatus] = useState<string>('all');
  const [selectedPartner, setSelectedPartner] = useState<Partner | null>(null);

  const filteredPartners = useMemo(() => {
    return mockPartners.filter(partner => {
      const matchesSearch = partner.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          partner.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          partner.verticals.some(v => v.toLowerCase().includes(searchTerm.toLowerCase()));
      
      const matchesType = filterType === 'all' || partner.type === filterType;
      const matchesTier = filterTier === 'all' || partner.tier === filterTier;
      const matchesStatus = filterStatus === 'all' || partner.status === filterStatus;
      
      return matchesSearch && matchesType && matchesTier && matchesStatus;
    });
  }, [searchTerm, filterType, filterTier, filterStatus]);

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'technology': return <Zap className="h-5 w-5" />;
      case 'channel': return <Users className="h-5 w-5" />;
      case 'strategic': return <Building className="h-5 w-5" />;
      case 'implementation': return <Mountain className="h-5 w-5" />;
      default: return <Globe className="h-5 w-5" />;
    }
  };

  const getTierColor = (tier: string) => {
    switch (tier) {
      case 'Platinum': return '#E5E7EB';
      case 'Gold': return '#FCD34D';
      case 'Silver': return '#D1D5DB';
      case 'Bronze': return '#F59E0B';
      default: return '#6B7280';
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);
  };

  const totalRevenue = mockPartners.reduce((sum, partner) => sum + partner.performance.revenue, 0);
  const totalDeals = mockPartners.reduce((sum, partner) => sum + partner.performance.deals, 0);
  const avgSatisfaction = mockPartners.reduce((sum, partner) => sum + partner.performance.satisfaction, 0) / mockPartners.length;
  const avgEnablement = mockPartners.reduce((sum, partner) => sum + partner.performance.enablementScore, 0) / mockPartners.length;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Alliance Partner Strategy</h1>
          <p className="text-gray-600 mt-2">Manage and optimize strategic partnerships</p>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="outline" className="flex items-center gap-2">
            <Download className="h-4 w-4" />
            Export Report
          </Button>
          <Button className="flex items-center gap-2">
            <Users className="h-4 w-4" />
            Add Partner
          </Button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-lg border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Revenue</p>
              <p className="text-2xl font-bold text-gray-900">{formatCurrency(totalRevenue)}</p>
            </div>
            <div className="h-12 w-12 bg-green-100 rounded-lg flex items-center justify-center">
              <TrendingUp className="h-6 w-6 text-green-600" />
            </div>
          </div>
          <div className="mt-4">
            <span className="text-sm text-green-600">+12.5% from last quarter</span>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Deals</p>
              <p className="text-2xl font-bold text-gray-900">{totalDeals}</p>
            </div>
            <div className="h-12 w-12 bg-blue-100 rounded-lg flex items-center justify-center">
              <Users className="h-6 w-6 text-blue-600" />
            </div>
          </div>
          <div className="mt-4">
            <span className="text-sm text-blue-600">+8.3% from last quarter</span>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Avg Satisfaction</p>
              <p className="text-2xl font-bold text-gray-900">{avgSatisfaction.toFixed(1)}</p>
            </div>
            <div className="h-12 w-12 bg-yellow-100 rounded-lg flex items-center justify-center">
              <Star className="h-6 w-6 text-yellow-600" />
            </div>
          </div>
          <div className="mt-4">
            <span className="text-sm text-yellow-600">+0.2 from last quarter</span>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Avg Enablement</p>
              <p className="text-2xl font-bold text-gray-900">{avgEnablement.toFixed(0)}%</p>
            </div>
            <div className="h-12 w-12 bg-purple-100 rounded-lg flex items-center justify-center">
              <Award className="h-6 w-6 text-purple-600" />
            </div>
          </div>
          <div className="mt-4">
            <span className="text-sm text-purple-600">+5.2% from last quarter</span>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white p-6 rounded-lg border">
        <div className="flex flex-col lg:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
              <Input
                placeholder="Search partners..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
          </div>
          
          <div className="flex gap-3">
            <Select value={filterType} onValueChange={setFilterType}>
              <SelectTrigger className="w-[150px]">
                <SelectValue placeholder="Type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Types</SelectItem>
                <SelectItem value="technology">Technology</SelectItem>
                <SelectItem value="channel">Channel</SelectItem>
                <SelectItem value="strategic">Strategic</SelectItem>
                <SelectItem value="implementation">Implementation</SelectItem>
              </SelectContent>
            </Select>

            <Select value={filterTier} onValueChange={setFilterTier}>
              <SelectTrigger className="w-[150px]">
                <SelectValue placeholder="Tier" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Tiers</SelectItem>
                <SelectItem value="Platinum">Platinum</SelectItem>
                <SelectItem value="Gold">Gold</SelectItem>
                <SelectItem value="Silver">Silver</SelectItem>
                <SelectItem value="Bronze">Bronze</SelectItem>
              </SelectContent>
            </Select>

            <Select value={filterStatus} onValueChange={setFilterStatus}>
              <SelectTrigger className="w-[150px]">
                <SelectValue placeholder="Status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Status</SelectItem>
                <SelectItem value="active">Active</SelectItem>
                <SelectItem value="inactive">Inactive</SelectItem>
                <SelectItem value="pending">Pending</SelectItem>
              </SelectContent>
            </Select>

            <Button variant="outline" size="icon">
              <Filter className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>

      {/* Partners Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
        {filteredPartners.map((partner) => (
          <div key={partner.id} className="bg-white rounded-lg border hover:shadow-lg transition-shadow cursor-pointer"
               onClick={() => setSelectedPartner(partner)}>
            <div className="p-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <img src={partner.logo} alt={partner.name} className="w-12 h-12 rounded-lg" />
                  <div>
                    <h3 className="font-semibold text-gray-900">{partner.name}</h3>
                    <div className="flex items-center gap-2 mt-1">
                      {getTypeIcon(partner.type)}
                      <span className="text-sm text-gray-600 capitalize">{partner.type.replace('_', ' ')}</span>
                    </div>
                  </div>
                </div>
                <div className="flex flex-col items-end gap-2">
                  <Badge 
                    style={{ backgroundColor: getTierColor(partner.tier) }}
                    className="text-white"
                  >
                    {partner.tier}
                  </Badge>
                  <Badge variant={partner.status === 'active' ? 'default' : 'secondary'}>
                    {partner.status}
                  </Badge>
                </div>
              </div>
              
              <p className="text-sm text-gray-600 mb-4">{partner.description}</p>
              
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium text-gray-700">Revenue</span>
                  <span className="text-sm font-bold text-green-600">
                    {formatCurrency(partner.performance.revenue)}
                  </span>
                </div>
                
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium text-gray-700">Deals</span>
                  <span className="text-sm font-bold text-blue-600">
                    {partner.performance.deals}
                  </span>
                </div>
                
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium text-gray-700">Satisfaction</span>
                  <div className="flex items-center gap-1">
                    <Star className="h-4 w-4 text-yellow-500 fill-current" />
                    <span className="text-sm font-bold text-yellow-600">
                      {partner.performance.satisfaction}
                    </span>
                  </div>
                </div>
                
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium text-gray-700">Enablement</span>
                  <span className="text-sm font-bold text-purple-600">
                    {partner.performance.enablementScore}%
                  </span>
                </div>
              </div>
              
              <div className="mt-4 pt-4 border-t">
                <div className="flex flex-wrap gap-1">
                  {partner.verticals.slice(0, 2).map((vertical) => (
                    <Badge key={vertical} variant="outline" className="text-xs">
                      {vertical}
                    </Badge>
                  ))}
                  {partner.verticals.length > 2 && (
                    <Badge variant="outline" className="text-xs">
                      +{partner.verticals.length - 2} more
                    </Badge>
                  )}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Partner Detail Modal */}
      {selectedPartner && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6 border-b">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <img src={selectedPartner.logo} alt={selectedPartner.name} className="w-16 h-16 rounded-lg" />
                  <div>
                    <h2 className="text-2xl font-bold text-gray-900">{selectedPartner.name}</h2>
                    <p className="text-gray-600">{selectedPartner.description}</p>
                  </div>
                </div>
                <Button variant="ghost" size="icon" onClick={() => setSelectedPartner(null)}>
                  <X className="h-6 w-6" />
                </Button>
              </div>
            </div>
            
            <div className="p-6 space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div className="space-y-2">
                  <h3 className="font-semibold text-gray-900">Partner Type</h3>
                  <div className="flex items-center gap-2">
                    {getTypeIcon(selectedPartner.type)}
                    <span className="capitalize">{selectedPartner.type.replace('_', ' ')}</span>
                  </div>
                </div>
                
                <div className="space-y-2">
                  <h3 className="font-semibold text-gray-900">Tier</h3>
                  <Badge 
                    style={{ backgroundColor: getTierColor(selectedPartner.tier) }}
                    className="text-white"
                  >
                    {selectedPartner.tier}
                  </Badge>
                </div>
                
                <div className="space-y-2">
                  <h3 className="font-semibold text-gray-900">Status</h3>
                  <Badge variant={selectedPartner.status === 'active' ? 'default' : 'secondary'}>
                    {selectedPartner.status}
                  </Badge>
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="space-y-2">
                  <h3 className="font-semibold text-gray-900">Revenue</h3>
                  <p className="text-2xl font-bold text-green-600">
                    {formatCurrency(selectedPartner.performance.revenue)}
                  </p>
                </div>
                
                <div className="space-y-2">
                  <h3 className="font-semibold text-gray-900">Deals</h3>
                  <p className="text-2xl font-bold text-blue-600">
                    {selectedPartner.performance.deals}
                  </p>
                </div>
                
                <div className="space-y-2">
                  <h3 className="font-semibold text-gray-900">Satisfaction</h3>
                  <div className="flex items-center gap-2">
                    <Star className="h-5 w-5 text-yellow-500 fill-current" />
                    <span className="text-2xl font-bold text-yellow-600">
                      {selectedPartner.performance.satisfaction}
                    </span>
                  </div>
                </div>
                
                <div className="space-y-2">
                  <h3 className="font-semibold text-gray-900">Enablement</h3>
                  <p className="text-2xl font-bold text-purple-600">
                    {selectedPartner.performance.enablementScore}%
                  </p>
                </div>
              </div>
              
              <div className="space-y-4">
                <h3 className="font-semibold text-gray-900">Verticals</h3>
                <div className="flex flex-wrap gap-2">
                  {selectedPartner.verticals.map((vertical) => (
                    <Badge key={vertical} variant="outline">
                      {vertical}
                    </Badge>
                  ))}
                </div>
              </div>
              
              <div className="space-y-4">
                <h3 className="font-semibold text-gray-900">Capabilities</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                  {selectedPartner.capabilities.map((capability) => (
                    <div key={capability} className="flex items-center gap-2">
                      <CheckCircle className="h-4 w-4 text-green-500" />
                      <span className="text-sm">{capability}</span>
                    </div>
                  ))}
                </div>
              </div>
              
              <div className="space-y-4">
                <h3 className="font-semibold text-gray-900">Certifications</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {selectedPartner.certifications.map((cert) => (
                    <div key={cert.id} className="p-4 border rounded-lg">
                      <div className="flex items-center justify-between mb-2">
                        <h4 className="font-medium">{cert.name}</h4>
                        <Badge variant={cert.status === 'active' ? 'default' : 'secondary'}>
                          {cert.status}
                        </Badge>
                      </div>
                      <div className="space-y-1 text-sm text-gray-600">
                        <div className="flex justify-between">
                          <span>Level:</span>
                          <span className="font-medium">{cert.level}</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Score:</span>
                          <span className="font-medium">{cert.score}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Expires:</span>
                          <span className="font-medium">{cert.expiryDate}</span>
                        </div>
                        {cert.vertical && (
                          <div className="flex justify-between">
                            <span>Vertical:</span>
                            <span className="font-medium">{cert.vertical}</span>
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
              
              <div className="space-y-4">
                <h3 className="font-semibold text-gray-900">Contact Information</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <div className="flex items-center gap-2">
                      <Users className="h-4 w-4 text-gray-500" />
                      <span className="text-sm font-medium">Primary Contact:</span>
                      <span className="text-sm">{selectedPartner.contact.primaryContact}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Mail className="h-4 w-4 text-gray-500" />
                      <span className="text-sm font-medium">Email:</span>
                      <span className="text-sm">{selectedPartner.contact.email}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Phone className="h-4 w-4 text-gray-500" />
                      <span className="text-sm font-medium">Phone:</span>
                      <span className="text-sm">{selectedPartner.contact.phone}</span>
                    </div>
                  </div>
                  <div className="space-y-2">
                    <div className="flex items-center gap-2">
                      <MapPin className="h-4 w-4 text-gray-500" />
                      <span className="text-sm font-medium">Region:</span>
                      <span className="text-sm">{selectedPartner.contact.region}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Globe className="h-4 w-4 text-gray-500" />
                      <span className="text-sm font-medium">Timezone:</span>
                      <span className="text-sm">{selectedPartner.contact.timezone}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Calendar className="h-4 w-4 text-gray-500" />
                      <span className="text-sm font-medium">Join Date:</span>
                      <span className="text-sm">{selectedPartner.joinDate}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AlliancePartnerStrategy;