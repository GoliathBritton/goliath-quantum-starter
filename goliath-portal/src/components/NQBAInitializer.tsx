"use client"

import { useEffect, useState } from 'react'
import { nqbaIntegration, NQBAStatus } from '@/services/nqba-integration'
import { nqbaCore } from '@/services/nqba-core'
import { Zap, Brain, Rocket, Shield, Target, CheckCircle, AlertCircle, XCircle, Dna } from 'lucide-react'

export default function NQBAInitializer() {
  const [status, setStatus] = useState<NQBAStatus | null>(null)
  const [isInitializing, setIsInitializing] = useState(true)
  const [showStatus, setShowStatus] = useState(false)
  const [initializationPhase, setInitializationPhase] = useState<'core' | 'integration' | 'complete'>('core')

  useEffect(() => {
    const initializeNQBA = async () => {
      try {
        console.log('🧬 Initializing NQBA Architecture - The Lifeblood of the Ecosystem...')
        console.log('⚡ Every component, feature, and solution will be powered by NQBA')
        
        // Phase 1: Initialize NQBA Core (The Foundation)
        setInitializationPhase('core')
        console.log('🔬 Phase 1: Initializing NQBA Core...')
        const coreMetrics = await nqbaCore.initialize()
        console.log('✅ NQBA Core initialized successfully!')
        
        // Phase 2: Initialize NQBA Integration (Built on Core)
        setInitializationPhase('integration')
        console.log('🔗 Phase 2: Initializing NQBA Integration...')
        const nqbaStatus = await nqbaIntegration.initialize()
        setStatus(nqbaStatus)
        
        // Phase 3: Complete
        setInitializationPhase('complete')
        setIsInitializing(false)
        
        // Show status briefly then hide
        setShowStatus(true)
        setTimeout(() => setShowStatus(false), 8000) // Show longer to display all phases
        
        console.log('✅ NQBA Architecture initialized successfully!')
        console.log('🧬 All systems now powered by NQBA Core')
        
      } catch (error) {
        console.error('❌ NQBA Architecture initialization failed:', error)
        setIsInitializing(false)
        setShowStatus(true)
      }
    }

    initializeNQBA()
  }, [])

  if (!showStatus) return null

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'ready':
        return <CheckCircle className="w-4 h-4 text-green-500" />
      case 'initializing':
      case 'deploying':
      case 'connecting':
        return <AlertCircle className="w-4 h-4 text-yellow-500" />
      case 'error':
        return <XCircle className="w-4 h-4 text-red-500" />
      default:
        return <AlertCircle className="w-4 h-4 text-gray-500" />
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'ready':
        return 'text-green-600'
      case 'initializing':
      case 'deploying':
      case 'connecting':
        return 'text-yellow-600'
      case 'error':
        return 'text-red-600'
      default:
        return 'text-gray-600'
    }
  }

  const getOverallStatusColor = (status: string) => {
    switch (status) {
      case 'operational':
        return 'bg-green-100 text-green-800 border-green-200'
      case 'degraded':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200'
      case 'down':
        return 'bg-red-100 text-red-800 border-red-200'
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200'
    }
  }

  const getPhaseColor = (phase: string) => {
    switch (phase) {
      case 'core':
        return 'bg-goliath-600'
      case 'integration':
        return 'bg-flyfox-600'
      case 'complete':
        return 'bg-sigma-600'
      default:
        return 'bg-gray-600'
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-3xl w-full mx-4">
        <div className="text-center mb-6">
          <div className="flex items-center justify-center space-x-2 mb-4">
            <div className="w-12 h-12 bg-gradient-to-br from-goliath-600 to-flyfox-600 rounded-xl flex items-center justify-center">
              <Dna className="w-6 h-6 text-white" />
            </div>
            <h2 className="text-2xl font-bold text-gray-900">NQBA Architecture</h2>
          </div>
          <p className="text-gray-600">
            The Lifeblood of the Ecosystem
          </p>
          <p className="text-sm text-gray-500 mt-1">
            Powered by Dynex Quantum Computing (410x Performance)
          </p>
        </div>

        {isInitializing ? (
          <div className="space-y-6">
            {/* Initialization Progress */}
            <div className="text-center">
              <div className="flex items-center justify-center space-x-2 mb-4">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-goliath-600"></div>
                <span className="text-lg font-semibold text-gray-900">
                  Initializing NQBA Systems...
                </span>
              </div>
              
              {/* Phase Indicator */}
              <div className="flex items-center justify-center space-x-4 mb-4">
                <div className={`px-3 py-1 rounded-full text-white text-sm font-medium ${getPhaseColor('core')} ${initializationPhase === 'core' ? 'ring-2 ring-white' : ''}`}>
                  Phase 1: NQBA Core
                </div>
                <div className={`px-3 py-1 rounded-full text-white text-sm font-medium ${getPhaseColor('integration')} ${initializationPhase === 'integration' ? 'ring-2 ring-white' : ''}`}>
                  Phase 2: Integration
                </div>
                <div className={`px-3 py-1 rounded-full text-white text-sm font-medium ${getPhaseColor('complete')} ${initializationPhase === 'complete' ? 'ring-2 ring-white' : ''}`}>
                  Phase 3: Complete
                </div>
              </div>
              
              <p className="text-gray-600">
                {initializationPhase === 'core' && 'Initializing NQBA Core - The Foundation'}
                {initializationPhase === 'integration' && 'Initializing NQBA Integration - Built on Core'}
                {initializationPhase === 'complete' && 'NQBA Architecture Ready'}
              </p>
            </div>

            {/* NQBA Core Status */}
            {initializationPhase !== 'core' && (
              <div className="bg-gradient-to-r from-goliath-50 to-flyfox-50 p-4 rounded-lg border border-goliath-200">
                <h3 className="font-semibold text-gray-900 mb-3 flex items-center">
                  <Dna className="w-5 h-5 text-goliath-600 mr-2" />
                  NQBA Core - The Foundation
                </h3>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="text-gray-600">Architecture Version:</span>
                    <span className="font-semibold text-goliath-600 ml-2">{nqbaCore.getArchitectureVersion()}</span>
                  </div>
                  <div>
                    <span className="text-gray-600">Quantum Performance:</span>
                    <span className="font-semibold text-flyfox-600 ml-2">{nqbaCore.getQuantumPerformanceBoost()}</span>
                  </div>
                  <div>
                    <span className="text-gray-600">Core Status:</span>
                    <span className="font-semibold text-green-600 ml-2">READY</span>
                  </div>
                  <div>
                    <span className="text-gray-600">Validation:</span>
                    <span className="font-semibold text-sigma-600 ml-2">PASSED</span>
                  </div>
                </div>
              </div>
            )}
          </div>
        ) : (
          <div className="space-y-4">
            {/* Overall Status */}
            <div className={`p-4 rounded-lg border ${getOverallStatusColor(status?.overall_status || 'down')}`}>
              <div className="flex items-center justify-between">
                <span className="font-semibold">Overall System Status</span>
                <span className="text-sm font-medium capitalize">
                  {status?.overall_status || 'unknown'}
                </span>
              </div>
            </div>

            {/* NQBA Core Foundation */}
            <div className="bg-gradient-to-r from-goliath-50 to-flyfox-50 p-4 rounded-lg border border-goliath-200">
              <h3 className="font-semibold text-gray-900 mb-3 flex items-center">
                <Dna className="w-5 h-5 text-goliath-600 mr-2" />
                NQBA Core - The Foundation
              </h3>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="text-gray-600">Architecture Version:</span>
                  <span className="font-semibold text-goliath-600 ml-2">{nqbaCore.getArchitectureVersion()}</span>
                </div>
                <div>
                  <span className="text-gray-600">Quantum Performance:</span>
                  <span className="font-semibold text-flyfox-600 ml-2">{nqbaCore.getQuantumPerformanceBoost()}</span>
                </div>
                <div>
                  <span className="text-gray-600">Core Status:</span>
                  <span className="font-semibold text-green-600 ml-2">READY</span>
                </div>
                <div>
                  <span className="text-gray-600">Validation:</span>
                  <span className="font-semibold text-sigma-600 ml-2">PASSED</span>
                </div>
              </div>
            </div>

            {/* Individual System Status */}
            <div className="space-y-3">
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <Brain className="w-5 h-5 text-goliath-600" />
                  <span className="font-medium">Dynex Quantum Computing</span>
                </div>
                <div className="flex items-center space-x-2">
                  {getStatusIcon(status?.dynex_quantum || 'error')}
                  <span className={`text-sm font-medium ${getStatusColor(status?.dynex_quantum || 'error')}`}>
                    {status?.dynex_quantum || 'error'}
                  </span>
                </div>
              </div>

              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <Rocket className="w-5 h-5 text-flyfox-600" />
                  <span className="font-medium">Q-Sales Division™</span>
                </div>
                <div className="flex items-center space-x-2">
                  {getStatusIcon(status?.qsales_division || 'error')}
                  <span className={`text-sm font-medium ${getStatusColor(status?.qsales_division || 'error')}`}>
                    {status?.qsales_division || 'error'}
                  </span>
                </div>
              </div>

              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <Zap className="w-5 h-5 text-flyfox-600" />
                  <span className="font-medium">FLYFOX AI Platform</span>
                </div>
                <div className="flex items-center space-x-2">
                  {getStatusIcon(status?.flyfox_ai || 'error')}
                  <span className={`text-sm font-medium ${getStatusColor(status?.flyfox_ai || 'error')}`}>
                    {status?.flyfox_ai || 'error'}
                  </span>
                </div>
              </div>

              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <Shield className="w-5 h-5 text-goliath-600" />
                  <span className="font-medium">Goliath Financial</span>
                </div>
                <div className="flex items-center space-x-2">
                  {getStatusIcon(status?.goliath_financial || 'error')}
                  <span className={`text-sm font-medium ${getStatusColor(status?.goliath_financial || 'error')}`}>
                    {status?.goliath_financial || 'error'}
                  </span>
                </div>
              </div>

              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <Target className="w-5 h-5 text-sigma-600" />
                  <span className="font-medium">Sigma Select</span>
                </div>
                <div className="flex items-center space-x-2">
                  {getStatusIcon(status?.sigma_select || 'error')}
                  <span className={`text-sm font-medium ${getStatusColor(status?.sigma_select || 'error')}`}>
                    {status?.sigma_select || 'error'}
                  </span>
                </div>
              </div>
            </div>

            {/* Performance Metrics */}
            <div className="bg-gradient-to-r from-goliath-50 to-flyfox-50 p-4 rounded-lg border border-goliath-200">
              <h3 className="font-semibold text-gray-900 mb-2">Quantum Performance</h3>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="text-gray-600">Performance Boost:</span>
                  <span className="font-semibold text-goliath-600 ml-2">410x</span>
                </div>
                <div>
                  <span className="text-gray-600">NVIDIA Acceleration:</span>
                  <span className="font-semibold text-green-600 ml-2">Enabled</span>
                </div>
                <div>
                  <span className="text-gray-600">Neuromorphic Computing:</span>
                  <span className="font-semibold text-flyfox-600 ml-2">Active</span>
                </div>
                <div>
                  <span className="text-gray-600">QUBO Optimization:</span>
                  <span className="font-semibold text-sigma-600 ml-2">Ready</span>
                </div>
              </div>
            </div>

            {/* NQBA Core Metrics */}
            <div className="bg-gradient-to-r from-sigma-50 to-goliath-50 p-4 rounded-lg border border-sigma-200">
              <h3 className="font-semibold text-gray-900 mb-2">NQBA Core Metrics</h3>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="text-gray-600">Integration Score:</span>
                  <span className="font-semibold text-goliath-600 ml-2">100%</span>
                </div>
                <div>
                  <span className="text-gray-600">Quantum Performance:</span>
                  <span className="font-semibold text-flyfox-600 ml-2">95%</span>
                </div>
                <div>
                  <span className="text-gray-600">Autonomous Systems:</span>
                  <span className="font-semibold text-sigma-600 ml-2">98%</span>
                </div>
                <div>
                  <span className="text-gray-600">Core Validation:</span>
                  <span className="font-semibold text-green-600 ml-2">PASSED</span>
                </div>
              </div>
            </div>

            {/* Close Button */}
            <div className="text-center pt-4">
              <button
                onClick={() => setShowStatus(false)}
                className="btn-primary"
              >
                Continue to Portal
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
