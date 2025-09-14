import Head from 'next/head'
import { useState } from 'react'
import { motion } from 'framer-motion'
import QuantumParticles from '@/components/QuantumParticles'
import GlassCard, { GlassButton, GlassInput, GlassSelect } from '@/components/GlassCard'
import { formatQuantumNumber, getQuantumColor, generateQuantumId } from '@/lib/utils'

interface MarketData {
  symbol: string
  price: number
  change: number
  volume: number
  prediction?: {
    direction: 'up' | 'down'
    confidence: number
    target_price: number
  }
}

interface QuantumResult {
  job_id: string
  status: 'pending' | 'running' | 'completed' | 'failed'
  result?: {
    optimal_solution: number[]
    energy: number
    execution_time: number
    quantum_advantage: number
  }
  error?: string
}

export default function Home() {
  const [selectedAssets, setSelectedAssets] = useState<string[]>(['AAPL', 'GOOGL'])
  const [riskTolerance, setRiskTolerance] = useState<number>(0.5)
  const [timeHorizon, setTimeHorizon] = useState<string>('1M')
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [result, setResult] = useState<QuantumResult | null>(null)
  const [marketData] = useState<MarketData[]>([
    { symbol: 'AAPL', price: 175.43, change: 2.34, volume: 45234567, prediction: { direction: 'up', confidence: 0.87, target_price: 185.20 } },
    { symbol: 'GOOGL', price: 142.56, change: -1.23, volume: 23456789, prediction: { direction: 'down', confidence: 0.72, target_price: 138.90 } },
    { symbol: 'MSFT', price: 378.91, change: 5.67, volume: 34567890, prediction: { direction: 'up', confidence: 0.91, target_price: 395.50 } },
    { symbol: 'TSLA', price: 248.73, change: -8.45, volume: 56789012, prediction: { direction: 'up', confidence: 0.65, target_price: 265.80 } },
  ])

  const handleOptimize = async () => {
    setIsLoading(true)
    setResult(null)
    
    try {
      // Simulate quantum optimization with realistic timing
      await new Promise(resolve => setTimeout(resolve, 3000))
      
      setResult({
        job_id: generateQuantumId(),
        status: 'completed',
        result: {
          optimal_solution: selectedAssets.map(() => Math.random()),
          energy: -Math.random() * 100,
          execution_time: Math.random() * 5000,
          quantum_advantage: 1 + Math.random() * 3
        }
      })
    } catch (error) {
      setResult({
        job_id: 'qne_error',
        status: 'failed',
        error: 'Quantum optimization failed'
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <>
      <Head>
        <title>Quantum Nexus Engine - Portfolio Optimization</title>
        <meta name="description" content="Advanced quantum-powered portfolio optimization" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 relative overflow-hidden">
        <QuantumParticles />
        
        <div className="relative z-10 container mx-auto px-4 py-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center mb-12"
          >
            <h1 className="text-6xl font-bold bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400 bg-clip-text text-transparent mb-4">
              Quantum Nexus Engine
            </h1>
            <p className="text-xl text-slate-300 max-w-2xl mx-auto">
              Harness quantum computing power for next-generation portfolio optimization
            </p>
          </motion.div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
            {/* Market Data */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="lg:col-span-2"
            >
              <GlassCard>
                <h2 className="text-2xl font-bold text-white mb-6">Market Intelligence</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {marketData.map((asset, index) => (
                    <motion.div
                      key={asset.symbol}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.5, delay: index * 0.1 }}
                      className="p-4 rounded-lg bg-white/5 border border-white/10 hover:bg-white/10 transition-all duration-300"
                    >
                      <div className="flex justify-between items-start mb-2">
                        <span className="font-bold text-white">{asset.symbol}</span>
                        <span className={`text-sm px-2 py-1 rounded ${asset.change >= 0 ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'}`}>
                          {asset.change >= 0 ? '+' : ''}{asset.change.toFixed(2)}%
                        </span>
                      </div>
                      <div className="text-2xl font-bold text-white mb-1">
                        ${asset.price.toFixed(2)}
                      </div>
                      {asset.prediction && (
                        <div className="text-sm text-slate-300">
                          <div className="flex items-center gap-2">
                            <span className={`w-2 h-2 rounded-full ${asset.prediction.direction === 'up' ? 'bg-green-400' : 'bg-red-400'}`}></span>
                            Target: ${asset.prediction.target_price.toFixed(2)}
                          </div>
                          <div className="text-xs text-slate-400">
                            Confidence: {(asset.prediction.confidence * 100).toFixed(0)}%
                          </div>
                        </div>
                      )}
                    </motion.div>
                  ))}
                </div>
              </GlassCard>
            </motion.div>

            {/* Controls */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
            >
              <GlassCard>
                <h2 className="text-2xl font-bold text-white mb-6">Optimization Parameters</h2>
                
                <div className="space-y-6">
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">
                      Risk Tolerance
                    </label>
                    <input
                      type="range"
                      min="0"
                      max="1"
                      step="0.1"
                      value={riskTolerance}
                      onChange={(e) => setRiskTolerance(parseFloat(e.target.value))}
                      className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer slider"
                    />
                    <div className="text-center text-sm text-slate-400 mt-1">
                      {(riskTolerance * 100).toFixed(0)}%
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">
                      Time Horizon
                    </label>
                    <GlassSelect
                      value={timeHorizon}
                      onChange={(e) => setTimeHorizon(e.target.value)}
                    >
                      <option value="1W">1 Week</option>
                      <option value="1M">1 Month</option>
                      <option value="3M">3 Months</option>
                      <option value="6M">6 Months</option>
                      <option value="1Y">1 Year</option>
                    </GlassSelect>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">
                      Selected Assets
                    </label>
                    <div className="flex flex-wrap gap-2">
                      {marketData.map((asset) => (
                        <button
                          key={asset.symbol}
                          onClick={() => {
                            setSelectedAssets(prev => 
                              prev.includes(asset.symbol)
                                ? prev.filter(s => s !== asset.symbol)
                                : [...prev, asset.symbol]
                            )
                          }}
                          className={`px-3 py-1 rounded-full text-sm transition-all duration-300 ${
                            selectedAssets.includes(asset.symbol)
                              ? 'bg-cyan-500/30 text-cyan-300 border border-cyan-400/50'
                              : 'bg-white/10 text-slate-300 border border-white/20 hover:bg-white/20'
                          }`}
                        >
                          {asset.symbol}
                        </button>
                      ))}
                    </div>
                  </div>

                  <GlassButton
                    onClick={handleOptimize}
                    disabled={isLoading || selectedAssets.length === 0}
                    className="w-full"
                  >
                    {isLoading ? (
                      <div className="flex items-center justify-center gap-2">
                        <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                        Optimizing...
                      </div>
                    ) : (
                      'Run Quantum Optimization'
                    )}
                  </GlassButton>
                </div>
              </GlassCard>
            </motion.div>
          </div>

          {/* Results */}
          {result && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
            >
              <GlassCard>
                <h2 className="text-2xl font-bold text-white mb-6">Quantum Optimization Results</h2>
                
                {result.status === 'completed' && result.result && (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    <div className="text-center">
                      <div className="text-3xl font-bold text-cyan-400 mb-2">
                        {formatQuantumNumber(result.result.energy)}
                      </div>
                      <div className="text-sm text-slate-400">Energy Level</div>
                    </div>
                    
                    <div className="text-center">
                      <div className="text-3xl font-bold text-purple-400 mb-2">
                        {result.result.quantum_advantage.toFixed(2)}x
                      </div>
                      <div className="text-sm text-slate-400">Quantum Advantage</div>
                    </div>
                    
                    <div className="text-center">
                      <div className="text-3xl font-bold text-pink-400 mb-2">
                        {(result.result.execution_time / 1000).toFixed(2)}s
                      </div>
                      <div className="text-sm text-slate-400">Execution Time</div>
                    </div>
                    
                    <div className="text-center">
                      <div className="text-3xl font-bold text-green-400 mb-2">
                        {selectedAssets.length}
                      </div>
                      <div className="text-sm text-slate-400">Assets Optimized</div>
                    </div>
                  </div>
                )}
                
                {result.status === 'failed' && (
                  <div className="text-center py-8">
                    <div className="text-red-400 text-lg font-semibold mb-2">
                      Optimization Failed
                    </div>
                    <div className="text-slate-400">
                      {result.error}
                    </div>
                  </div>
                )}
              </GlassCard>
            </motion.div>
          )}
        </div>
      </div>
    </>
  )
}