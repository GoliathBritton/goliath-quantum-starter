import React from 'react';

interface PyramidTier {
  name: string;
  price: string;
  description: string;
  features: string[];
  tier: 'base' | 'middle' | 'apex';
  mystical?: boolean;
}

const PricingPyramid: React.FC = () => {
  const pyramidTiers: PyramidTier[] = [
    // Apex Tier - The Black-Box Apex
    {
      name: 'Ascendant White-Label™',
      price: '$1.5M+/yr',
      description: 'Private-labeled instance for partners',
      features: ['Complete white-label solution', 'Partner ecosystem access', 'Custom branding rights', 'Dedicated infrastructure'],
      tier: 'apex',
      mystical: true
    },
    {
      name: 'Aeon Enterprise™',
      price: '$599,999/mo',
      description: 'Auto-execution with AGI foresight substrate',
      features: ['⚡ Aeon Core™ Auto-Execution', 'AGI foresight substrate', 'Autonomous decision making', 'Timeless prophetic insights'],
      tier: 'apex',
      mystical: true
    },
    {
      name: 'Echelon Pro™',
      price: '$149,999/mo',
      description: 'Black-Box + QHC governance + integrations',
      features: ['🏛️ Echelon Quantum™ Access', 'Black-box decision engine', 'QHC governance layer', 'Military-grade security'],
      tier: 'apex',
      mystical: true
    },
    {
      name: 'Omniscient Basic™',
      price: '$29,999/mo',
      description: 'Quantum forecasting reports (Dynex-powered)',
      features: ['🔮 Quantum Omniscient™ Access', 'Dynex-powered forecasting', 'Decision confidence analytics', 'Quantum scenario modeling'],
      tier: 'apex',
      mystical: true
    },
    
    // Middle Layer - Core Platform
    {
      name: 'Core Platform Enterprise',
      price: '$224,999/mo',
      description: 'Global accounts, 500 seats, + Omniscient Basic access',
      features: ['Global account management', '500 user seats', 'Omniscient Basic included', 'Enterprise integrations'],
      tier: 'middle'
    },
    {
      name: 'Core Platform Pro',
      price: '$74,999/mo',
      description: 'Unlimited workflows, 50 seats, QSAI-lite',
      features: ['Unlimited workflows', '50 user seats', 'QSAI-lite processing', 'Advanced analytics'],
      tier: 'middle'
    },
    {
      name: 'Core Platform Standard',
      price: '$22,999/mo',
      description: 'Unified portal, 5 seats, 50 workflows',
      features: ['Unified FLYFOX + Goliath + Sigma', '5 user seats', '50 workflows', 'Standard support'],
      tier: 'middle'
    },
    
    // Base Layer - Entry Points
    {
      name: 'FLYFOX Enterprise',
      price: '$14,999/mo',
      description: 'Multi-agent systems + QSAI-lite + 25 workflows',
      features: ['Multi-agent AI systems', 'QSAI-lite quantum processing', 'Unlimited workflows', 'Dedicated account manager'],
      tier: 'base'
    },
    {
      name: 'FLYFOX Pro',
      price: '$2,999/mo',
      description: 'Voice agents + Digital Humans + CRM-lite',
      features: ['Voice agents & Digital Humans', 'Advanced CRM-lite features', 'Multi-agent coordination', 'Priority support'],
      tier: 'base'
    },
    {
      name: 'FLYFOX Starter',
      price: '$599/mo',
      description: 'Chatbots + drag-drop automations for SMBs',
      features: ['AI Chatbots & Voice Agents', 'Drag-drop workflow builder', 'Basic CRM integration', 'Email support'],
      tier: 'base'
    }
  ];

  const getTierColor = (tier: string, mystical?: boolean) => {
    if (mystical) {
      return 'from-purple-600 via-indigo-600 to-purple-800';
    }
    switch (tier) {
      case 'apex': return 'from-yellow-400 via-orange-500 to-red-600';
      case 'middle': return 'from-blue-500 via-cyan-500 to-teal-600';
      case 'base': return 'from-green-500 via-emerald-500 to-green-700';
      default: return 'from-gray-500 to-gray-700';
    }
  };

  const getTierWidth = (index: number, total: number) => {
    const baseWidth = 20;
    const increment = (80 - baseWidth) / (total - 1);
    return baseWidth + (total - 1 - index) * increment;
  };

  return (
    <div className="max-w-6xl mx-auto p-8 bg-gradient-to-br from-space-900 via-space-800 to-space-900 rounded-2xl">
      <div className="text-center mb-12">
        <h1 className="text-5xl font-bold bg-gradient-to-r from-flyfox-400 via-quantum-400 to-purple-400 bg-clip-text text-transparent mb-4">
          The Ascension Pyramid™
        </h1>
        <p className="text-xl text-gray-300 mb-2">
          600% Premium Pricing • Luxury AI Market Positioning
        </p>
        <div className="text-sm text-flyfox-400 italic">
          From Starter ($599/mo) → Ascendant White-Label ($1.5M+/yr)
        </div>
      </div>

      <div className="relative">
        {/* Pyramid Structure */}
        <div className="flex flex-col items-center space-y-4">
          {pyramidTiers.map((tier, index) => {
            const width = getTierWidth(index, pyramidTiers.length);
            return (
              <div
                key={tier.name}
                className={`relative bg-gradient-to-r ${getTierColor(tier.tier, tier.mystical)} rounded-lg p-6 shadow-2xl transform hover:scale-105 transition-all duration-300`}
                style={{ width: `${width}%` }}
              >
                {tier.mystical && (
                  <div className="absolute -top-2 -right-2 bg-purple-600 text-white text-xs px-2 py-1 rounded-full font-bold animate-pulse">
                    MYSTICAL
                  </div>
                )}
                
                <div className="text-center">
                  <h3 className="text-xl font-bold text-white mb-2">{tier.name}</h3>
                  <div className="text-3xl font-extrabold text-white mb-2">{tier.price}</div>
                  <p className="text-sm text-gray-100 mb-4 opacity-90">{tier.description}</p>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs text-gray-100">
                    {tier.features.map((feature, idx) => (
                      <div key={idx} className="flex items-center justify-center gap-1">
                        <span className="text-yellow-300">✦</span>
                        <span>{feature}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Tier Labels */}
        <div className="absolute right-0 top-0 h-full flex flex-col justify-between py-8">
          <div className="text-right">
            <div className="text-lg font-bold text-purple-400 mb-1">APEX</div>
            <div className="text-sm text-gray-400">Black-Box Mystique</div>
          </div>
          <div className="text-right">
            <div className="text-lg font-bold text-cyan-400 mb-1">CORE</div>
            <div className="text-sm text-gray-400">Unified Platform</div>
          </div>
          <div className="text-right">
            <div className="text-lg font-bold text-green-400 mb-1">BASE</div>
            <div className="text-sm text-gray-400">Entry Points</div>
          </div>
        </div>
      </div>

      {/* Add-On Upsells */}
      <div className="mt-12 bg-gray-800/50 rounded-lg p-6">
        <h2 className="text-2xl font-bold text-white mb-6 text-center">
          Premium Add-On Upsells (600% Markup)
        </h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div className="bg-gradient-to-r from-purple-600 to-indigo-600 rounded-lg p-4 text-center">
            <h3 className="font-bold text-white mb-2">Digital Human Omniscient Interface™</h3>
            <div className="text-2xl font-bold text-white">+$14,999/mo</div>
          </div>
          <div className="bg-gradient-to-r from-blue-600 to-cyan-600 rounded-lg p-4 text-center">
            <h3 className="font-bold text-white mb-2">Premium Quantum Jobs (Dynex QPU)</h3>
            <div className="text-lg font-bold text-white">Usage-based + 30%</div>
          </div>
          <div className="bg-gradient-to-r from-orange-600 to-red-600 rounded-lg p-4 text-center">
            <h3 className="font-bold text-white mb-2">Industry-Specific Omniscients™</h3>
            <div className="text-2xl font-bold text-white">+$75K setup</div>
          </div>
          <div className="bg-gradient-to-r from-green-600 to-emerald-600 rounded-lg p-4 text-center">
            <h3 className="font-bold text-white mb-2">Industrial Retrofits (NVIDIA)</h3>
            <div className="text-lg font-bold text-white">$150K–$750K</div>
          </div>
          <div className="bg-gradient-to-r from-yellow-600 to-orange-600 rounded-lg p-4 text-center">
            <h3 className="font-bold text-white mb-2">Reseller White-Label Program</h3>
            <div className="text-lg font-bold text-white">$375K+ annual</div>
          </div>
        </div>
      </div>

      {/* Strategic Positioning */}
      <div className="mt-8 text-center">
        <div className="grid md:grid-cols-4 gap-4 text-sm">
          <div className="bg-gray-800/30 rounded-lg p-4">
            <div className="text-green-400 font-bold mb-2">✓ Oracle IP Safe</div>
            <div className="text-gray-300">Entirely new language</div>
          </div>
          <div className="bg-gray-800/30 rounded-lg p-4">
            <div className="text-purple-400 font-bold mb-2">✓ 600% Premium</div>
            <div className="text-gray-300">Luxury AI market</div>
          </div>
          <div className="bg-gray-800/30 rounded-lg p-4">
            <div className="text-yellow-400 font-bold mb-2">✓ Apex Mystique</div>
            <div className="text-gray-300">Power & exclusivity</div>
          </div>
          <div className="bg-gray-800/30 rounded-lg p-4">
            <div className="text-cyan-400 font-bold mb-2">✓ ARPU Growth</div>
            <div className="text-gray-300">Every step up</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PricingPyramid;