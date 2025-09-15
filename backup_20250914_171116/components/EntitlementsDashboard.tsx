import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface FeatureAccess {
  has_access: boolean;
  description: string;
  upgrade_info?: {
    upgrade_needed: boolean;
    current_tier: string;
    recommended_tier: string;
    benefits: Record<string, string>;
  };
}

interface UsageStats {
  quantum_jobs_used: number;
  quantum_jobs_limit: number;
  storage_used_gb: number;
  storage_limit_gb: number;
  api_requests_today: number;
  api_rate_limit: number;
}

interface EntitlementConfig {
  tier: string;
  features: string[];
  quantum_job_limit: number;
  api_rate_limit: number;
  storage_limit_gb: number;
  support_level: string;
}

interface TierComparison {
  [tier: string]: {
    features: string[];
    quantum_job_limit: number;
    api_rate_limit: number;
    storage_limit_gb: number;
    support_level: string;
    pricing: {
      monthly: number | string;
      annual: number | string;
      currency: string;
    };
  };
}

interface EntitlementsDashboardProps {
  userTier: string;
  onUpgrade?: (tier: string) => void;
}

const EntitlementsDashboard: React.FC<EntitlementsDashboardProps> = ({ userTier, onUpgrade }) => {
  const [entitlements, setEntitlements] = useState<EntitlementConfig | null>(null);
  const [usageStats, setUsageStats] = useState<UsageStats | null>(null);
  const [featuresStatus, setFeaturesStatus] = useState<Record<string, FeatureAccess>>({});
  const [tierComparison, setTierComparison] = useState<TierComparison>({});
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'overview' | 'features' | 'usage' | 'upgrade'>('overview');

  useEffect(() => {
    fetchEntitlementsData();
  }, []);

  const fetchEntitlementsData = async () => {
    try {
      setLoading(true);
      const [entitlementsRes, usageRes, featuresRes, comparisonRes] = await Promise.all([
        axios.get('/api/entitlements/my-entitlements'),
        axios.get('/api/entitlements/usage-stats'),
        axios.get('/api/entitlements/available-features'),
        axios.get('/api/entitlements/tier-comparison')
      ]);

      setEntitlements(entitlementsRes.data);
      setUsageStats(usageRes.data);
      setFeaturesStatus(featuresRes.data.features);
      setTierComparison(comparisonRes.data);
    } catch (error) {
      console.error('Failed to fetch entitlements data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getUsagePercentage = (used: number, limit: number) => {
    if (limit === -1) return 0; // Unlimited
    return Math.min((used / limit) * 100, 100);
  };

  const getUsageColor = (percentage: number) => {
    if (percentage < 50) return 'text-green-400';
    if (percentage < 80) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getTierColor = (tier: string) => {
    const colors = {
      basic: 'from-gray-600 to-gray-700',
      premium: 'from-flyfox-600 to-quantum-600',
      elite: 'from-quantum-600 to-purple-600',
      enterprise: 'from-purple-600 to-pink-600'
    };
    return colors[tier.toLowerCase() as keyof typeof colors] || colors.basic;
  };

  const formatLimit = (limit: number) => {
    return limit === -1 ? 'Unlimited' : limit.toLocaleString();
  };

  if (loading) {
    return (
      <div className="max-w-6xl mx-auto p-6">
        <div className="animate-pulse">
          <div className="h-8 bg-space-700 rounded mb-6"></div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[1, 2, 3].map(i => (
              <div key={i} className="h-32 bg-space-700 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto p-6">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-white mb-2">Subscription Dashboard</h1>
        <p className="text-gray-400">Manage your features, usage, and subscription tier</p>
      </div>

      {/* Current Tier Badge */}
      <div className="text-center mb-8">
        <div className={`inline-flex items-center px-6 py-3 rounded-full bg-gradient-to-r ${getTierColor(userTier)} text-white font-bold text-lg shadow-lg`}>
          <span className="mr-2">🎯</span>
          {userTier.toUpperCase()} TIER
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex justify-center mb-8">
        <div className="bg-space-800 rounded-lg p-1 flex">
          {[
            { id: 'overview', label: 'Overview', icon: '📊' },
            { id: 'features', label: 'Features', icon: '⚡' },
            { id: 'usage', label: 'Usage', icon: '📈' },
            { id: 'upgrade', label: 'Upgrade', icon: '🚀' }
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`px-6 py-3 rounded-md font-medium transition-all ${
                activeTab === tab.id
                  ? 'bg-gradient-to-r from-flyfox-600 to-quantum-600 text-white'
                  : 'text-gray-400 hover:text-white'
              }`}
            >
              <span className="mr-2">{tab.icon}</span>
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* Overview Tab */}
      {activeTab === 'overview' && entitlements && usageStats && (
        <div className="space-y-6">
          {/* Usage Overview Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Quantum Jobs */}
            <div className="bg-space-800/50 rounded-xl p-6 border border-quantum-500/30">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-white">Quantum Jobs</h3>
                <span className="text-2xl">⚛️</span>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-400">Used</span>
                  <span className="text-white">{usageStats.quantum_jobs_used} / {formatLimit(usageStats.quantum_jobs_limit)}</span>
                </div>
                {usageStats.quantum_jobs_limit !== -1 && (
                  <div className="w-full bg-space-600 rounded-full h-2">
                    <div 
                      className="bg-gradient-to-r from-flyfox-500 to-quantum-500 h-2 rounded-full transition-all"
                      style={{ width: `${getUsagePercentage(usageStats.quantum_jobs_used, usageStats.quantum_jobs_limit)}%` }}
                    ></div>
                  </div>
                )}
              </div>
            </div>

            {/* API Usage */}
            <div className="bg-space-800/50 rounded-xl p-6 border border-quantum-500/30">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-white">API Requests</h3>
                <span className="text-2xl">🔌</span>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-400">Today</span>
                  <span className="text-white">{usageStats.api_requests_today} / {usageStats.api_rate_limit}/min</span>
                </div>
                <div className="w-full bg-space-600 rounded-full h-2">
                  <div 
                    className="bg-gradient-to-r from-green-500 to-blue-500 h-2 rounded-full transition-all"
                    style={{ width: `${Math.min((usageStats.api_requests_today / usageStats.api_rate_limit) * 100, 100)}%` }}
                  ></div>
                </div>
              </div>
            </div>

            {/* Storage */}
            <div className="bg-space-800/50 rounded-xl p-6 border border-quantum-500/30">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-white">Storage</h3>
                <span className="text-2xl">💾</span>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-400">Used</span>
                  <span className="text-white">{usageStats.storage_used_gb.toFixed(2)} / {usageStats.storage_limit_gb} GB</span>
                </div>
                <div className="w-full bg-space-600 rounded-full h-2">
                  <div 
                    className="bg-gradient-to-r from-purple-500 to-pink-500 h-2 rounded-full transition-all"
                    style={{ width: `${getUsagePercentage(usageStats.storage_used_gb, usageStats.storage_limit_gb)}%` }}
                  ></div>
                </div>
              </div>
            </div>
          </div>

          {/* Current Plan Details */}
          <div className="bg-space-800/50 rounded-xl p-6 border border-quantum-500/30">
            <h3 className="text-xl font-semibold text-white mb-4">Current Plan Details</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-quantum-400">{formatLimit(entitlements.quantum_job_limit)}</div>
                <div className="text-sm text-gray-400">Quantum Jobs</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-flyfox-400">{entitlements.api_rate_limit}/min</div>
                <div className="text-sm text-gray-400">API Rate Limit</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-purple-400">{entitlements.storage_limit_gb} GB</div>
                <div className="text-sm text-gray-400">Storage</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-green-400 capitalize">{entitlements.support_level}</div>
                <div className="text-sm text-gray-400">Support Level</div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Features Tab */}
      {activeTab === 'features' && (
        <div className="space-y-4">
          <h3 className="text-xl font-semibold text-white mb-6">Feature Access</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {Object.entries(featuresStatus).map(([feature, access]) => (
              <div key={feature} className="bg-space-800/50 rounded-lg p-4 border border-quantum-500/30">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-medium text-white capitalize">{feature.replace(/_/g, ' ')}</h4>
                  <span className={`px-2 py-1 rounded text-xs font-medium ${
                    access.has_access 
                      ? 'bg-green-500/20 text-green-400 border border-green-500/30'
                      : 'bg-red-500/20 text-red-400 border border-red-500/30'
                  }`}>
                    {access.has_access ? 'Enabled' : 'Locked'}
                  </span>
                </div>
                <p className="text-sm text-gray-400 mb-3">{access.description}</p>
                {!access.has_access && access.upgrade_info && (
                  <button
                    onClick={() => onUpgrade?.(access.upgrade_info!.recommended_tier)}
                    className="text-xs px-3 py-1 bg-gradient-to-r from-flyfox-600 to-quantum-600 hover:from-flyfox-700 hover:to-quantum-700 text-white rounded transition-all"
                  >
                    Upgrade to {access.upgrade_info.recommended_tier}
                  </button>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Usage Tab */}
      {activeTab === 'usage' && usageStats && (
        <div className="space-y-6">
          <h3 className="text-xl font-semibold text-white mb-6">Detailed Usage Statistics</h3>
          
          {/* Usage Charts */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-space-800/50 rounded-xl p-6 border border-quantum-500/30">
              <h4 className="text-lg font-semibold text-white mb-4">Quantum Jobs Usage</h4>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-gray-400">Jobs Completed</span>
                  <span className={`font-bold ${getUsageColor(getUsagePercentage(usageStats.quantum_jobs_used, usageStats.quantum_jobs_limit))}`}>
                    {usageStats.quantum_jobs_used}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-400">Jobs Remaining</span>
                  <span className="text-white font-bold">
                    {usageStats.quantum_jobs_limit === -1 ? 'Unlimited' : usageStats.quantum_jobs_limit - usageStats.quantum_jobs_used}
                  </span>
                </div>
                {usageStats.quantum_jobs_limit !== -1 && (
                  <div className="w-full bg-space-600 rounded-full h-4">
                    <div 
                      className={`h-4 rounded-full transition-all bg-gradient-to-r ${
                        getUsagePercentage(usageStats.quantum_jobs_used, usageStats.quantum_jobs_limit) < 80
                          ? 'from-green-500 to-blue-500'
                          : 'from-yellow-500 to-red-500'
                      }`}
                      style={{ width: `${getUsagePercentage(usageStats.quantum_jobs_used, usageStats.quantum_jobs_limit)}%` }}
                    ></div>
                  </div>
                )}
              </div>
            </div>

            <div className="bg-space-800/50 rounded-xl p-6 border border-quantum-500/30">
              <h4 className="text-lg font-semibold text-white mb-4">Storage Usage</h4>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-gray-400">Used Storage</span>
                  <span className={`font-bold ${getUsageColor(getUsagePercentage(usageStats.storage_used_gb, usageStats.storage_limit_gb))}`}>
                    {usageStats.storage_used_gb.toFixed(2)} GB
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-400">Available Storage</span>
                  <span className="text-white font-bold">
                    {(usageStats.storage_limit_gb - usageStats.storage_used_gb).toFixed(2)} GB
                  </span>
                </div>
                <div className="w-full bg-space-600 rounded-full h-4">
                  <div 
                    className={`h-4 rounded-full transition-all bg-gradient-to-r ${
                      getUsagePercentage(usageStats.storage_used_gb, usageStats.storage_limit_gb) < 80
                        ? 'from-purple-500 to-pink-500'
                        : 'from-yellow-500 to-red-500'
                    }`}
                    style={{ width: `${getUsagePercentage(usageStats.storage_used_gb, usageStats.storage_limit_gb)}%` }}
                  ></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Upgrade Tab */}
      {activeTab === 'upgrade' && (
        <div className="space-y-6">
          <h3 className="text-xl font-semibold text-white mb-6">Upgrade Your Plan</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {Object.entries(tierComparison).map(([tier, details]) => (
              <div key={tier} className={`rounded-xl p-6 border-2 transition-all ${
                tier.toLowerCase() === userTier.toLowerCase()
                  ? 'border-quantum-500 bg-quantum-500/10'
                  : 'border-space-600 bg-space-800/50 hover:border-quantum-500/50'
              }`}>
                <div className="text-center mb-4">
                  <h4 className="text-xl font-bold text-white capitalize mb-2">{tier}</h4>
                  <div className="text-2xl font-bold text-quantum-400">
                    {typeof details.pricing.monthly === 'number' 
                      ? `$${details.pricing.monthly}/mo`
                      : details.pricing.monthly
                    }
                  </div>
                </div>
                
                <div className="space-y-3 mb-6">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-400">Quantum Jobs</span>
                    <span className="text-white">{formatLimit(details.quantum_job_limit)}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-400">API Rate</span>
                    <span className="text-white">{details.api_rate_limit}/min</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-400">Storage</span>
                    <span className="text-white">{details.storage_limit_gb} GB</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-400">Support</span>
                    <span className="text-white capitalize">{details.support_level}</span>
                  </div>
                </div>

                {tier.toLowerCase() === userTier.toLowerCase() ? (
                  <div className="text-center py-2 px-4 bg-quantum-500/20 text-quantum-400 rounded-lg font-medium">
                    Current Plan
                  </div>
                ) : (
                  <button
                    onClick={() => onUpgrade?.(tier)}
                    className="w-full py-2 px-4 bg-gradient-to-r from-flyfox-600 to-quantum-600 hover:from-flyfox-700 hover:to-quantum-700 text-white font-medium rounded-lg transition-all transform hover:scale-105"
                  >
                    Upgrade to {tier}
                  </button>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default EntitlementsDashboard;