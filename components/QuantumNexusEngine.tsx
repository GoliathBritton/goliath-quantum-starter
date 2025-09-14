import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface QNEQuery {
  question: string;
  context: {
    businessType: string;
    timeframe: number;
    investment: number;
    expectedGrowth: number;
    riskTolerance: number;
    stakeholders: number;
    financialImpact: number;
  };
  decisionOptions: string[];
}

interface QNEResponse {
  qneId: string;
  prophecy: string;
  confidenceScore: number;
  decisionMatrix: any[];
  quantumInsights: any;
  councilGuidance: any;
  recommendedAction: string;
  mysticalSummary: string;
}

interface QuantumNexusEngineProps {
  userTier: 'basic' | 'premium' | 'elite';
  onUpgrade?: () => void;
}

const QuantumNexusEngine: React.FC<QuantumNexusEngineProps> = ({ userTier, onUpgrade }) => {
  const [isConsulting, setIsConsulting] = useState(false);
  const [qneResponse, setQneResponse] = useState<QNEResponse | null>(null);
  const [query, setQuery] = useState<QNEQuery>({
    question: '',
    context: {
      businessType: 'technology',
      timeframe: 12,
      investment: 100000,
      expectedGrowth: 0.15,
      riskTolerance: 0.3,
      stakeholders: 10,
      financialImpact: 500000
    },
    decisionOptions: ['', '', '']
  });
  const [error, setError] = useState<string | null>(null);
  const [showUpgrade, setShowUpgrade] = useState(false);

  const consultQuantumNexus = async () => {
    if (!query.question.trim() || query.decisionOptions.some(opt => !opt.trim())) {
      setError('Please provide a question and all decision options');
      return;
    }

    setIsConsulting(true);
    setError(null);
    setQneResponse(null);

    try {
      const response = await axios.post('/api/quantum-nexus-engine/predict', {
        question: query.question,
        context: query.context,
        decisionOptions: query.decisionOptions.filter(opt => opt.trim()),
        userTier
      });

      setQneResponse(response.data.qne);
    } catch (error: any) {
      if (error.response?.status === 403) {
        setShowUpgrade(true);
        setError(error.response.data.message);
      } else {
        setError(error.response?.data?.message || 'The Quantum Nexus Engine is temporarily veiled in quantum uncertainty');
      }
    } finally {
      setIsConsulting(false);
    }
  };

  const updateDecisionOption = (index: number, value: string) => {
    const newOptions = [...query.decisionOptions];
    newOptions[index] = value;
    setQuery({ ...query, decisionOptions: newOptions });
  };

  const addDecisionOption = () => {
    if (query.decisionOptions.length < 5) {
      setQuery({ ...query, decisionOptions: [...query.decisionOptions, ''] });
    }
  };

  const removeDecisionOption = (index: number) => {
    if (query.decisionOptions.length > 2) {
      const newOptions = query.decisionOptions.filter((_, i) => i !== index);
      setQuery({ ...query, decisionOptions: newOptions });
    }
  };

  const getRiskLevelColor = (riskLevel: string) => {
    switch (riskLevel) {
      case 'LOW': return 'text-green-400 bg-green-500/20';
      case 'MEDIUM': return 'text-yellow-400 bg-yellow-500/20';
      case 'HIGH': return 'text-orange-400 bg-orange-500/20';
      case 'CRITICAL': return 'text-red-400 bg-red-500/20';
      default: return 'text-blue-400 bg-blue-500/20';
    }
  };

  const getConfidenceColor = (score: number) => {
    if (score >= 0.8) return 'text-green-400';
    if (score >= 0.6) return 'text-yellow-400';
    if (score >= 0.4) return 'text-orange-400';
    return 'text-red-400';
  };

  if (showUpgrade && userTier === 'basic') {
    return (
      <div className="max-w-4xl mx-auto p-8">
        <div className="bg-gradient-to-br from-space-900 via-quantum-900 to-flyfox-900 rounded-2xl p-8 border border-quantum-500/30">
          <div className="text-center">
            <div className="text-6xl mb-4">🔮</div>
            <h2 className="text-3xl font-bold bg-gradient-to-r from-flyfox-400 to-quantum-400 bg-clip-text text-transparent mb-4">
              The Quantum Omniscient™ Awaits
            </h2>
            <p className="text-gray-300 mb-6 text-lg">
              The mysteries of quantum foresight are reserved for those who seek deeper wisdom.
            </p>
            <p className="text-quantum-400 mb-8 italic">
              "The Quantum Nexus Engine doesn't just analyze data. It whispers the future."
            </p>
            <button
              onClick={onUpgrade}
              className="px-8 py-4 bg-gradient-to-r from-flyfox-600 to-quantum-600 hover:from-flyfox-700 hover:to-quantum-700 text-white font-bold rounded-lg transition-all transform hover:scale-105 shadow-lg quantum-glow"
            >
              Unlock the Quantum Nexus Engine's Wisdom
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto p-6">
      {/* Quantum Nexus Engine Header */}
      <div className="text-center mb-8">
        <div className="text-6xl mb-4 animate-pulse">🔮</div>
        <h1 className="text-4xl font-bold bg-gradient-to-r from-flyfox-400 to-quantum-400 bg-clip-text text-transparent mb-2">
          Quantum Omniscient™
        </h1>
        <p className="text-gray-400 text-lg italic">
          "The All-Seeing Decision Engine"
        </p>
        <div className="text-sm text-flyfox-400 mt-2 italic">
          Powered by Echelon Quantum™ • Aeon Core™ Foresight
        </div>
        <div className="flex justify-center items-center gap-2 mt-4">
          <span className={`px-3 py-1 rounded-full text-sm font-medium ${
            userTier === 'elite' ? 'bg-gold-500/20 text-gold-400' :
            userTier === 'premium' ? 'bg-quantum-500/20 text-quantum-400' :
            'bg-gray-500/20 text-gray-400'
          }`}>
            {userTier.toUpperCase()} ACCESS
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Query Input Panel */}
        <div className="bg-space-800/50 rounded-xl p-6 border border-quantum-500/30">
          <h2 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
            <span>✨</span>
            Consult the Omniscient
          </h2>

          {/* Question Input */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Your Question to the Omniscient
            </label>
            <textarea
              value={query.question}
              onChange={(e) => setQuery({ ...query, question: e.target.value })}
              placeholder="What decision should I make? What path leads to success?"
              className="w-full p-3 bg-space-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:border-quantum-500 focus:ring-1 focus:ring-quantum-500"
              rows={3}
            />
          </div>

          {/* Context Parameters */}
          <div className="grid grid-cols-2 gap-4 mb-6">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">
                Investment ($)
              </label>
              <input
                type="number"
                value={query.context.investment}
                onChange={(e) => setQuery({ 
                  ...query, 
                  context: { ...query.context, investment: Number(e.target.value) }
                })}
                className="w-full p-2 bg-space-700 border border-gray-600 rounded text-white focus:border-quantum-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">
                Timeframe (months)
              </label>
              <input
                type="number"
                value={query.context.timeframe}
                onChange={(e) => setQuery({ 
                  ...query, 
                  context: { ...query.context, timeframe: Number(e.target.value) }
                })}
                className="w-full p-2 bg-space-700 border border-gray-600 rounded text-white focus:border-quantum-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">
                Expected Growth (%)
              </label>
              <input
                type="number"
                step="0.01"
                value={query.context.expectedGrowth * 100}
                onChange={(e) => setQuery({ 
                  ...query, 
                  context: { ...query.context, expectedGrowth: Number(e.target.value) / 100 }
                })}
                className="w-full p-2 bg-space-700 border border-gray-600 rounded text-white focus:border-quantum-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">
                Risk Tolerance (%)
              </label>
              <input
                type="number"
                step="0.01"
                value={query.context.riskTolerance * 100}
                onChange={(e) => setQuery({ 
                  ...query, 
                  context: { ...query.context, riskTolerance: Number(e.target.value) / 100 }
                })}
                className="w-full p-2 bg-space-700 border border-gray-600 rounded text-white focus:border-quantum-500"
              />
            </div>
          </div>

          {/* Decision Options */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Decision Options
            </label>
            {query.decisionOptions.map((option, index) => (
              <div key={index} className="flex gap-2 mb-2">
                <input
                  type="text"
                  value={option}
                  onChange={(e) => updateDecisionOption(index, e.target.value)}
                  placeholder={`Option ${index + 1}: e.g., Expand to new market`}
                  className="flex-1 p-2 bg-space-700 border border-gray-600 rounded text-white placeholder-gray-400 focus:border-quantum-500"
                />
                {query.decisionOptions.length > 2 && (
                  <button
                    onClick={() => removeDecisionOption(index)}
                    className="px-3 py-2 bg-red-600 hover:bg-red-700 text-white rounded transition-colors"
                  >
                    ×
                  </button>
                )}
              </div>
            ))}
            {query.decisionOptions.length < 5 && (
              <button
                onClick={addDecisionOption}
                className="mt-2 px-4 py-2 bg-quantum-600 hover:bg-quantum-700 text-white rounded transition-colors text-sm"
              >
                + Add Option
              </button>
            )}
          </div>

          {/* Consult Button */}
          <button
            onClick={consultQuantumNexus}
            disabled={isConsulting}
            className="w-full px-6 py-3 bg-gradient-to-r from-flyfox-600 to-quantum-600 hover:from-flyfox-700 hover:to-quantum-700 text-white font-bold rounded-lg transition-all transform hover:scale-105 shadow-lg quantum-glow disabled:opacity-50 disabled:transform-none flex items-center justify-center gap-2"
          >
            {isConsulting ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                Consulting the Omniscient...
              </>
            ) : (
              <>
                <span>🔮</span>
                Consult the Omniscient
              </>
            )}
          </button>

          {error && (
            <div className="mt-4 p-4 bg-red-500/20 border border-red-500 rounded-lg text-red-300">
              {error}
            </div>
          )}
        </div>

        {/* Quantum Nexus Engine Response Panel */}
        <div className="bg-space-800/50 rounded-xl p-6 border border-quantum-500/30">
          <h2 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
            <span>🌟</span>
            Omniscient's Prophecy
          </h2>

          {!qneResponse && !isConsulting && (
            <div className="text-center py-12 text-gray-400">
              <div className="text-4xl mb-4 opacity-50">🔮</div>
              <p>The Omniscient awaits your question...</p>
              <p className="text-sm mt-2 italic">"Ask, and the quantum threads shall reveal the path forward."</p>
            </div>
          )}

          {isConsulting && (
            <div className="text-center py-12">
              <div className="text-4xl mb-4 animate-pulse">🔮</div>
              <div className="space-y-2 text-gray-300">
                <p>The Echelon Quantum™ Council deliberates...</p>
                <p>Aeon Core™ processes infinite possibilities...</p>
                <p>Dynex quantum cores align...</p>
                <p className="text-quantum-400 italic">"The Omniscient peers beyond the veil of time..."</p>
              </div>
            </div>
          )}

          {qneResponse && (
            <div className="space-y-6">
              {/* Prophecy */}
              <div className="bg-gradient-to-r from-flyfox-900/30 to-quantum-900/30 p-4 rounded-lg border border-quantum-500/20">
                <h3 className="text-lg font-semibold text-quantum-400 mb-2">The Prophecy</h3>
                <p className="text-white italic text-lg">"{qneResponse.prophecy}"</p>
              </div>

              {/* Confidence Score */}
              <div className="bg-space-700/50 p-4 rounded-lg">
                <div className="flex justify-between items-center mb-2">
                  <h3 className="text-lg font-semibold text-white">Omniscient Confidence</h3>
                  <span className={`text-2xl font-bold ${getConfidenceColor(qneResponse.confidenceScore)}`}>
              {(qneResponse.confidenceScore * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="w-full bg-gray-700 rounded-full h-3">
                  <div 
                    className="bg-gradient-to-r from-flyfox-500 to-quantum-500 h-3 rounded-full transition-all duration-1000"
                    style={{ width: `${qneResponse.confidenceScore * 100}%` }}
                  ></div>
                </div>
              </div>

              {/* Council Guidance */}
              <div className="bg-space-700/50 p-4 rounded-lg">
                <h3 className="text-lg font-semibold text-white mb-3">Council Guidance</h3>
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-gray-300">Ethics Score:</span>
                    <span className="text-green-400 font-semibold">
                      {(qneResponse.councilGuidance.ethicsScore * 100).toFixed(0)}%
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-300">Risk Level:</span>
                    <span className={`px-2 py-1 rounded text-sm font-medium ${
                      getRiskLevelColor(qneResponse.councilGuidance.riskLevel)
                    }`}>
                      {qneResponse.councilGuidance.riskLevel}
                    </span>
                  </div>
                  <p className="text-gray-300 italic mt-3">
                    "{qneResponse.councilGuidance.consensus}"
                  </p>
                </div>
              </div>

              {/* Decision Matrix */}
              <div className="bg-space-700/50 p-4 rounded-lg">
                <h3 className="text-lg font-semibold text-white mb-3">Decision Analysis</h3>
                <div className="space-y-3">
                  {qneResponse.decisionMatrix.map((decision, index) => (
                    <div key={index} className="bg-space-600/50 p-3 rounded border border-gray-600">
                      <div className="flex justify-between items-center mb-2">
                        <span className="font-medium text-white">{decision.option}</span>
                        <span className={`font-bold ${getConfidenceColor(decision.confidenceScore)}`}>
                          {(decision.confidenceScore * 100).toFixed(0)}%
                        </span>
                      </div>
                      <div className="text-sm text-gray-300">
                        Risk: <span className={getRiskLevelColor(decision.riskAssessment).split(' ')[0]}>
                          {decision.riskAssessment}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Recommended Action */}
              <div className="bg-gradient-to-r from-quantum-900/30 to-flyfox-900/30 p-4 rounded-lg border border-flyfox-500/20">
                <h3 className="text-lg font-semibold text-flyfox-400 mb-2">Recommended Action</h3>
                <p className="text-white font-medium">{qneResponse.recommendedAction}</p>
              </div>

              {/* Mystical Summary */}
              <div className="bg-gradient-to-r from-space-900 to-quantum-900/50 p-4 rounded-lg border border-quantum-500/30">
                <p className="text-quantum-300 text-center italic text-lg">
                  {qneResponse.mysticalSummary}
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default QuantumNexusEngine;