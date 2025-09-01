import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  Users, 
  DollarSign, 
  TrendingUp, 
  Award, 
  Settings, 
  BarChart3,
  Plus,
  Search,
  Filter
} from 'lucide-react';

const PartnerDashboard = () => {
  const [partners, setPartners] = useState([]);
  const [analytics, setAnalytics] = useState({});
  const [loading, setLoading] = useState(true);
  const [selectedTier, setSelectedTier] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');

  const API_BASE = 'http://localhost:8080';

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [partnersRes, analyticsRes] = await Promise.all([
        axios.get(`${API_BASE}/api/partners`),
        axios.get(`${API_BASE}/api/analytics/overview`)
      ]);
      
      setPartners(partnersRes.data.partners);
      setAnalytics(analyticsRes.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      setLoading(false);
    }
  };

  const filteredPartners = partners.filter(partner => {
    const matchesTier = selectedTier === 'all' || partner.tier === selectedTier;
    const matchesSearch = partner.company.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesTier && matchesSearch;
  });

  const getTierColor = (tier) => {
    const colors = {
      bronze: 'bg-amber-600',
      silver: 'bg-gray-500',
      gold: 'bg-yellow-500',
      platinum: 'bg-slate-400'
    };
    return colors[tier] || 'bg-gray-400';
  };

  const getTierIcon = (tier) => {
    const icons = {
      bronze: '🥉',
      silver: '🥈',
      gold: '🥇',
      platinum: '💎'
    };
    return icons[tier] || '👤';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-xl text-gray-600">Loading Goliath Partner Portal...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <h1 className="text-3xl font-bold text-gray-900">
                  🚀 Goliath Omniedge
                </h1>
                <p className="text-sm text-gray-500">Partner Portal</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center">
                <Plus className="w-4 h-4 mr-2" />
                Add Partner
              </button>
              <button className="text-gray-400 hover:text-gray-600">
                <Settings className="w-6 h-6" />
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {/* Analytics Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <Users className="h-6 w-6 text-gray-400" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">Total Partners</dt>
                    <dd className="text-lg font-medium text-gray-900">{analytics.total_partners || 0}</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <DollarSign className="h-6 w-6 text-green-400" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">Monthly Revenue</dt>
                    <dd className="text-lg font-medium text-gray-900">
                      ${(analytics.total_monthly_revenue || 0).toLocaleString()}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <TrendingUp className="h-6 w-6 text-blue-400" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">Commission Paid</dt>
                    <dd className="text-lg font-medium text-gray-900">
                      ${(analytics.total_commission_paid || 0).toLocaleString()}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <Award className="h-6 w-6 text-yellow-400" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">Top Tier</dt>
                    <dd className="text-lg font-medium text-gray-900 capitalize">
                      {analytics.top_performing_tier || 'N/A'}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Filters and Search */}
        <div className="bg-white shadow rounded-lg mb-6">
          <div className="px-6 py-4 border-b border-gray-200">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0">
              <div className="flex-1 max-w-lg">
                <label htmlFor="search" className="sr-only">Search partners</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Search className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    id="search"
                    name="search"
                    className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                    placeholder="Search partners..."
                    type="search"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                  />
                </div>
              </div>
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2">
                  <Filter className="h-5 w-5 text-gray-400" />
                  <select
                    value={selectedTier}
                    onChange={(e) => setSelectedTier(e.target.value)}
                    className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
                  >
                    <option value="all">All Tiers</option>
                    <option value="bronze">Bronze</option>
                    <option value="silver">Silver</option>
                    <option value="gold">Gold</option>
                    <option value="platinum">Platinum</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Partners Table */}
        <div className="bg-white shadow overflow-hidden sm:rounded-md">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg leading-6 font-medium text-gray-900">
              Partner Network ({filteredPartners.length})
            </h3>
          </div>
          <ul className="divide-y divide-gray-200">
            {filteredPartners.map((partner) => (
              <li key={partner.partner_id} className="px-6 py-4 hover:bg-gray-50">
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div className="flex-shrink-0 h-10 w-10">
                      <div className={`h-10 w-10 rounded-full flex items-center justify-center text-white text-lg ${getTierColor(partner.tier)}`}>
                        {getTierIcon(partner.tier)}
                      </div>
                    </div>
                    <div className="ml-4">
                      <div className="text-sm font-medium text-gray-900">
                        {partner.company}
                      </div>
                      <div className="text-sm text-gray-500">
                        {partner.contact?.name || 'Contact N/A'} • {partner.contact?.email || 'Email N/A'}
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center space-x-6">
                    <div className="text-right">
                      <div className="text-sm font-medium text-gray-900">
                        ${partner.monthly_revenue?.toLocaleString() || '0'}
                      </div>
                      <div className="text-sm text-gray-500">Monthly Revenue</div>
                    </div>
                    <div className="text-right">
                      <div className="text-sm font-medium text-gray-900">
                        ${partner.commission_earned?.toLocaleString() || '0'}
                      </div>
                      <div className="text-sm text-gray-500">Commission</div>
                    </div>
                    <div className="text-right">
                      <div className="text-sm font-medium text-gray-900 capitalize">
                        {partner.tier}
                      </div>
                      <div className="text-sm text-gray-500">
                        {partner.tier === 'bronze' && '15%'}
                        {partner.tier === 'silver' && '20%'}
                        {partner.tier === 'gold' && '25%'}
                        {partner.tier === 'platinum' && '30%'}
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-sm font-medium text-gray-900">
                        {partner.solutions?.length || 0}
                      </div>
                      <div className="text-sm text-gray-500">Solutions</div>
                    </div>
                    <button className="text-blue-600 hover:text-blue-900 text-sm font-medium">
                      View Details
                    </button>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>

        {/* Tier Distribution Chart */}
        <div className="mt-8 bg-white shadow rounded-lg">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg leading-6 font-medium text-gray-900">
              Partner Tier Distribution
            </h3>
          </div>
          <div className="p-6">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {Object.entries(analytics.tier_distribution || {}).map(([tier, count]) => (
                <div key={tier} className="text-center">
                  <div className={`inline-flex items-center justify-center w-16 h-16 rounded-full text-white text-2xl ${getTierColor(tier)}`}>
                    {getTierIcon(tier)}
                  </div>
                  <div className="mt-2 text-sm font-medium text-gray-900 capitalize">{tier}</div>
                  <div className="text-2xl font-bold text-gray-900">{count}</div>
                  <div className="text-sm text-gray-500">partners</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default PartnerDashboard;
