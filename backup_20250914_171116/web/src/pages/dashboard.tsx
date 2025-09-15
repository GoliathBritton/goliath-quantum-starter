import React, { useEffect, useState } from 'react'
import { Navbar } from '../components/Navbar'
import { Footer } from '../components/Footer'
import { DollarSign, Users, Target, TrendingUp, Activity, Zap } from 'lucide-react'

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000"

export default function Dashboard() {
  const [partners, setPartners] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(`${API_BASE}/api/partners`)
      .then(r => r.json())
      .then(data => {
        setPartners(data)
        setLoading(false)
      })
      .catch(() => {
        setPartners([])
        setLoading(false)
      })
  }, [])

  const totalRevenue = partners.reduce((sum, partner) => sum + (partner.monthlyRevenue || 0), 0)
  const totalCustomers = partners.reduce((sum, partner) => sum + (partner.totalCustomers || 0), 0)
  const avgCommission = partners.length > 0 ? partners.reduce((sum, partner) => sum + (partner.commissionRate || 0), 0) / partners.length : 0

  const metrics = [
    {
      title: 'Total Revenue',
      value: `$${(totalRevenue / 1000).toFixed(0)}K`,
      change: '+12.5%',
      icon: DollarSign,
      color: 'text-green-600'
    },
    {
      title: 'Active Partners',
      value: partners.length.toString(),
      change: '+2 this month',
      icon: Users,
      color: 'text-blue-600'
    },
    {
      title: 'Total Customers',
      value: totalCustomers.toString(),
      change: '+8.3%',
      icon: Target,
      color: 'text-purple-600'
    },
    {
      title: 'Avg Commission',
      value: `${(avgCommission * 100).toFixed(1)}%`,
      change: '+0.5%',
      icon: TrendingUp,
      color: 'text-orange-600'
    }
  ]

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50">
        <Navbar />
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex items-center justify-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-quantum-primary"></div>
          </div>
        </div>
        <Footer />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-900 mb-2">Partner Dashboard</h1>
          <p className="text-slate-600">Monitor your quantum-enhanced partner ecosystem performance</p>
        </div>

        {/* Quantum Processing Status */}
        <div className="bg-gradient-to-r from-quantum-primary to-quantum-secondary rounded-xl p-6 mb-8 text-white">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-semibold mb-2">Quantum Processing Status</h2>
              <p className="text-white/90">Real-time quantum computations active</p>
            </div>
            <div className="flex items-center space-x-2">
              <Activity className="h-6 w-6 animate-pulse" />
              <span className="text-sm font-mono">DYNEX ONLINE</span>
            </div>
          </div>
        </div>

        {/* Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {metrics.map((metric, index) => {
            const Icon = metric.icon
            return (
              <div key={index} className="bg-white rounded-xl p-6 shadow-sm border border-slate-200">
                <div className="flex items-center justify-between mb-4">
                  <div className={`p-2 rounded-lg bg-slate-50 ${metric.color}`}>
                    <Icon className="h-5 w-5" />
                  </div>
                  <span className="text-sm text-green-600 font-medium">{metric.change}</span>
                </div>
                <h3 className="text-2xl font-bold text-slate-900 mb-1">{metric.value}</h3>
                <p className="text-slate-600 text-sm">{metric.title}</p>
              </div>
            )
          })}
        </div>

        {/* Top Partners */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 mb-8">
          <div className="p-6 border-b border-slate-200">
            <h2 className="text-xl font-semibold text-slate-900">Top Partners</h2>
            <p className="text-slate-600 text-sm mt-1">Your highest performing quantum partners</p>
          </div>
          <div className="p-6">
            {partners.length === 0 ? (
              <div className="text-center py-8">
                <Users className="h-12 w-12 text-slate-400 mx-auto mb-4" />
                <p className="text-slate-600">No partners found. Check your API connection.</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {partners.map((partner) => (
                  <div key={partner.id} className="border border-slate-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                    <div className="flex justify-between items-start mb-3">
                      <div>
                        <span className={`inline-block px-2 py-1 rounded-full text-xs font-medium ${
                          partner.tier === 'platinum' ? 'bg-purple-100 text-purple-800' :
                          partner.tier === 'gold' ? 'bg-yellow-100 text-yellow-800' :
                          partner.tier === 'silver' ? 'bg-slate-100 text-slate-800' :
                          'bg-blue-100 text-blue-800'
                        }`}>
                          {partner.tier?.toUpperCase() || 'STANDARD'}
                        </span>
                      </div>
                      <Zap className="h-4 w-4 text-quantum-primary" />
                    </div>
                    <h3 className="font-semibold text-slate-900 mb-2">{partner.company || partner.name}</h3>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-slate-600">Monthly Revenue:</span>
                        <span className="font-medium">${(partner.monthlyRevenue || 0).toLocaleString()}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-600">Commission:</span>
                        <span className="font-medium">{((partner.commissionRate || 0) * 100).toFixed(1)}%</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-600">Customers:</span>
                        <span className="font-medium">{partner.totalCustomers || 0}</span>
                      </div>
                      {partner.focus && (
                        <div className="flex justify-between">
                          <span className="text-slate-600">Focus:</span>
                          <span className="font-medium">{partner.focus}</span>
                        </div>
                      )}
                      {partner.status && (
                        <div className="flex justify-between">
                          <span className="text-slate-600">Status:</span>
                          <span className={`font-medium ${
                            partner.status === 'active' ? 'text-green-600' :
                            partner.status === 'pending' ? 'text-yellow-600' :
                            'text-slate-600'
                          }`}>
                            {partner.status}
                          </span>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Quantum Insights */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200">
          <div className="p-6 border-b border-slate-200">
            <h2 className="text-xl font-semibold text-slate-900">Quantum Insights</h2>
            <p className="text-slate-600 text-sm mt-1">AI-powered recommendations for your partner ecosystem</p>
          </div>
          <div className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg p-4 border border-blue-200">
                <h3 className="font-semibold text-blue-900 mb-2">Growth Opportunity</h3>
                <p className="text-blue-800 text-sm">Consider expanding partnerships in the enterprise sector. Quantum analysis shows 23% higher conversion potential.</p>
              </div>
              <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-lg p-4 border border-green-200">
                <h3 className="font-semibold text-green-900 mb-2">Performance Alert</h3>
                <p className="text-green-800 text-sm">Top-tier partners showing 15% above-average performance this quarter. Consider reward programs.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <Footer />
    </div>
  )
}