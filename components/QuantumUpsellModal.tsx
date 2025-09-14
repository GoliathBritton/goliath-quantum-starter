import React, { useState, useEffect } from "react";
import Modal from "react-modal";
import axios from "axios";

interface QuantumPremiumData {
  enabled: boolean;
  name: string;
  description: string;
  priceMonthlyUSD: number;
  payPerJobUSD: number;
  features: string[];
  benefits: string[];
}

interface CurrentUsage {
  quantumJobsThisMonth: number;
  totalComputeHours: number;
  estimatedSavings: string;
  efficiencyGain: string;
}

interface QuantumUpsellModalProps {
  isOpen: boolean;
  onClose: () => void;
  onUpgrade: (plan: string) => void;
  triggerContext?: string; // e.g., "workflow_builder", "premium_node"
}

interface PricingPlan {
  id: string;
  name: string;
  description: string;
  features: string[];
  pricing: {
    monthly: number;
    yearly: number;
    payPerJob: number;
  };
  popular: boolean;
  mystical?: boolean;
}

const QuantumUpsellModal: React.FC<QuantumUpsellModalProps> = ({
  isOpen,
  onClose,
  onUpgrade,
  triggerContext = "general"
}) => {
  const [premiumData, setPremiumData] = useState<QuantumPremiumData | null>(null);
  const [usageData, setUsageData] = useState<CurrentUsage | null>(null);
  const [loading, setLoading] = useState(false);
  const [selectedPlan, setSelectedPlan] = useState<string>("quantum");
  const [billingCycle, setBillingCycle] = useState<"monthly" | "payPerJob">("monthly");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const pricingPlans: PricingPlan[] = [
    {
      id: 'starter',
      name: 'FLYFOX AI Starter',
      description: 'Chatbots + drag-drop automations for SMBs',
      features: [
        'AI Chatbots & Voice Agents',
        'Drag-drop workflow builder',
        'Basic CRM integration',
        'Email support',
        'Up to 5 workflows'
      ],
      pricing: {
        monthly: 599,
        yearly: 5990,
        payPerJob: 99
      },
      popular: false
    },
    {
      id: 'pro',
      name: 'FLYFOX AI Pro',
      description: 'Voice agents + Digital Humans + CRM-lite',
      features: [
        'Voice agents & Digital Humans',
        'Advanced CRM-lite features',
        'Multi-agent coordination',
        'Priority support',
        'Up to 25 workflows'
      ],
      pricing: {
        monthly: 2999,
        yearly: 29990,
        payPerJob: 499
      },
      popular: true
    },
    {
      id: 'enterprise',
      name: 'FLYFOX Enterprise',
      description: 'Multi-agent systems + QSAI-lite + 25 workflows',
      features: [
        'Multi-agent AI systems',
        'QSAI-lite quantum processing',
        'Unlimited workflows',
        'Dedicated account manager',
        'Custom integrations'
      ],
      pricing: {
        monthly: 14999,
        yearly: 149990,
        payPerJob: 2499
      },
      popular: false
    },
    {
      id: 'omniscient',
      name: 'Omniscient Basic™',
      description: 'The All-Seeing Decision Engine with quantum forecasting',
      features: [
        '🔮 Quantum Omniscient™ Access',
        'Dynex-powered forecasting reports',
        'Decision confidence analytics',
        'Quantum scenario modeling',
        'Invite-only mystical insights'
      ],
      pricing: {
        monthly: 29999,
        yearly: 299990,
        payPerJob: 4999
      },
      popular: false,
      mystical: true
    },
    {
      id: 'echelon',
      name: 'Echelon Pro™',
      description: 'Government-grade black-box intelligence with QHC governance',
      features: [
        '🏛️ Echelon Quantum™ Access',
        'Black-box decision engine',
        'QHC governance layer',
        'Advanced integrations',
        'Military-grade security'
      ],
      pricing: {
        monthly: 149999,
        yearly: 1499990,
        payPerJob: 24999
      },
      popular: false,
      mystical: true
    },
    {
      id: 'aeon',
      name: 'Aeon Enterprise™',
      description: 'Auto-execution with AGI foresight substrate',
      features: [
        '⚡ Aeon Core™ Auto-Execution',
        'AGI foresight substrate',
        'Autonomous decision making',
        'Timeless prophetic insights',
        'White-glove implementation'
      ],
      pricing: {
        monthly: 599999,
        yearly: 5999990,
        payPerJob: 99999
      },
      popular: false,
      mystical: true
    }
  ];

  useEffect(() => {
    if (isOpen) {
      fetchPricingData();
    }
  }, [isOpen]);

  const fetchPricingData = async () => {
    setLoading(true);
    try {
      const response = await fetch("/api/quantum/price");
      const data = await response.json();
      setPremiumData(data.quantumPremium);
      setUsageData(data.currentUsage);
    } catch (error) {
      console.error("Failed to fetch pricing data:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleUpgrade = async () => {
    try {
      setIsLoading(true);
      
      const response = await axios.post('/api/checkout', {
        productId: selectedPlan,
        planType: billingCycle,
        userId: 'user_' + Date.now(), // Replace with actual user ID
        metadata: {
          context: triggerContext || 'upsell_modal',
          timestamp: new Date().toISOString()
        }
      });
      
      // Redirect to Stripe checkout
      window.location.href = response.data.url;
      
    } catch (error) {
      console.error('Error creating checkout session:', error);
      setError('Failed to create checkout session. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const getContextualMessage = () => {
    switch (triggerContext) {
      case "workflow_builder":
        return "Unlock quantum-enhanced workflow nodes for superior optimization and performance.";
      case "premium_node":
        return "This premium node requires Dynex QUBO processing for optimal results.";
      case "entanglement_map":
        return "Access advanced quantum visualization and real-time neuromorphic insights.";
      default:
        return "Experience the power of quantum-enhanced business automation.";
    }
  };

  if (!premiumData || loading) {
    return (
      <Modal
        isOpen={isOpen}
        onRequestClose={onClose}
        className="fixed inset-0 flex items-center justify-center p-4 z-50"
        overlayClassName="fixed inset-0 bg-black bg-opacity-75"
      >
        <div className="bg-gray-900 rounded-xl p-8 max-w-md w-full">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-flyfox mx-auto mb-4"></div>
            <p className="text-white">Loading quantum pricing...</p>
          </div>
        </div>
      </Modal>
    );
  }

  return (
    <Modal
      isOpen={isOpen}
      onRequestClose={onClose}
      className="fixed inset-0 flex items-center justify-center p-4 z-50"
      overlayClassName="fixed inset-0 bg-black bg-opacity-75 backdrop-blur-sm"
    >
      <div className="bg-gradient-to-br from-space-900 via-quantum-900 to-space-900 rounded-2xl p-8 max-w-2xl w-full max-h-[90vh] overflow-y-auto border border-flyfox-500/30 shadow-2xl">
        <div className="flex justify-between items-start mb-6">
          <div>
            <h2 className="text-3xl font-bold text-white mb-2 bg-gradient-to-r from-flyfox-400 to-quantum-400 bg-clip-text text-transparent">
              Unlock Quantum Premium
            </h2>
            <p className="text-gray-300">
              {getContextualMessage()}
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors p-2"
          >
            ✕
          </button>
        </div>

        <div className="space-y-6">
          {/* Billing Cycle Toggle */}
          <div className="flex justify-center mb-6">
            <div className="bg-space-800/50 p-1 rounded-lg flex">
              <button
                onClick={() => setBillingCycle("monthly")}
                className={`px-4 py-2 rounded-md transition-all ${
                  billingCycle === "monthly"
                    ? "bg-flyfox-500 text-white"
                    : "text-gray-400 hover:text-white"
                }`}
              >
                Monthly
              </button>
              <button
                onClick={() => setBillingCycle("payPerJob")}
                className={`px-4 py-2 rounded-md transition-all ${
                  billingCycle === "payPerJob"
                    ? "bg-quantum-500 text-white"
                    : "text-gray-400 hover:text-white"
                }`}
              >
                Pay-per-Job
              </button>
            </div>
          </div>

          {/* Pricing Plans Grid */}
           <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {pricingPlans.map((plan) => {
              const selectedPlanData = pricingPlans.find(p => p.id === selectedPlan);
              return (
                <div
                  key={plan.id}
                  onClick={() => setSelectedPlan(plan.id)}
                  className={`relative p-6 rounded-xl border-2 cursor-pointer transition-all transform hover:scale-105 ${
                    selectedPlan === plan.id
                      ? 'border-quantum-500 bg-quantum-500/10 shadow-lg'
                      : 'border-gray-600 bg-space-700/50 hover:border-quantum-400'
                  } ${
                    plan.popular ? 'ring-2 ring-flyfox-500' : ''
                  } ${
                    plan.mystical ? 'bg-gradient-to-br from-flyfox-900/30 to-quantum-900/30 quantum-glow' : ''
                  }`}
                >
                  {plan.popular && (
                    <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                      <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                        plan.mystical 
                          ? 'bg-gradient-to-r from-flyfox-500 to-quantum-500 text-white quantum-glow'
                          : 'bg-flyfox-500 text-white'
                      }`}>
                        {plan.mystical ? '✨ Mystical' : 'Most Popular'}
                      </span>
                    </div>
                  )}

                  <div className="text-center mb-4">
                    <h3 className={`text-xl font-bold mb-2 ${
                      plan.mystical 
                        ? 'bg-gradient-to-r from-flyfox-400 to-quantum-400 bg-clip-text text-transparent'
                        : 'text-white'
                    }`}>
                      {plan.name}
                    </h3>
                    <p className="text-gray-300 text-sm mb-4">{plan.description}</p>
                    
                    <div className="text-3xl font-bold text-white mb-1">
                       ${plan.pricing[billingCycle].toLocaleString()}
                     </div>
                     <div className="text-sm text-gray-400">
                       {billingCycle === 'monthly' ? 'per month' : 'per job'}
                     </div>
                     {plan.mystical && (
                       <div className="text-xs text-flyfox-400 italic mt-1">
                         Invite-only access
                       </div>
                     )}
                  </div>

                  <ul className="space-y-2 mb-6">
                    {plan.features.map((feature, index) => (
                      <li key={index} className="flex items-center gap-2">
                        <span className={plan.mystical ? 'text-flyfox-400' : 'text-quantum-400'}>
                          {plan.mystical && feature.includes('🔮') ? '🔮' : '✓'}
                        </span>
                        <span className="text-gray-300 text-sm">{feature}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              );
            })}
          </div>

          {/* Current Usage Stats */}
          {usageData && (
            <div className="bg-white/5 rounded-lg p-6 mb-6">
              <h4 className="text-lg font-semibold text-white mb-4">Your Quantum Impact</h4>
              <div className="grid grid-cols-2 gap-4 text-center">
                <div>
                  <div className="text-2xl font-bold text-flyfox">{usageData.quantumJobsThisMonth}</div>
                  <div className="text-sm text-gray-400">Jobs This Month</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-green-400">{usageData.efficiencyGain}</div>
                  <div className="text-sm text-gray-400">Efficiency Gain</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-blue-400">{usageData.totalComputeHours}h</div>
                  <div className="text-sm text-gray-400">Compute Hours</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-purple-400">{usageData.estimatedSavings}</div>
                  <div className="text-sm text-gray-400">Est. Savings</div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-4 p-4 bg-red-500/20 border border-red-500 rounded-lg text-red-300 text-center">
            {error}
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex gap-4 justify-center mt-8">
          <button
            onClick={onClose}
            disabled={isLoading}
            className="px-6 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors disabled:opacity-50"
          >
            Maybe Later
          </button>
          <button
            onClick={handleUpgrade}
            disabled={isLoading}
            className="px-8 py-3 bg-gradient-to-r from-flyfox-600 to-quantum-600 hover:from-flyfox-700 hover:to-quantum-700 text-white font-bold rounded-lg transition-all transform hover:scale-105 shadow-lg quantum-glow flex items-center gap-2 disabled:opacity-50 disabled:transform-none"
          >
            {isLoading ? (
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
            ) : (
              <span>⚡</span>
            )}
            {isLoading ? 'Processing...' : 'Upgrade to Quantum Premium'}
            {!isLoading && (
              <span className="text-sm opacity-75">
                (${pricingPlans.find(p => p.id === selectedPlan)?.pricing[billingCycle].toLocaleString()}{billingCycle === 'monthly' ? '/mo' : '/job'})
              </span>
            )}
          </button>
        </div>

        {/* Security Notice */}
        <div className="mt-6 text-center">
          <p className="text-xs text-gray-400">
            🔒 Secure payment processing • 30-day money-back guarantee • Cancel anytime
          </p>
        </div>
      </div>
    </Modal>
  );
};

export default QuantumUpsellModal;