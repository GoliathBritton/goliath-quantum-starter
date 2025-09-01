"use client"

import { useState } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { 
  Home, 
  Package, 
  Users, 
  Rocket, 
  BarChart3, 
  Settings, 
  Zap, 
  Brain,
  Crown,
  Target,
  Database,
  Shield,
  TrendingUp,
  ChevronDown
} from 'lucide-react'

export default function Sidebar() {
  const [isCollapsed, setIsCollapsed] = useState(false)
  const [expandedSections, setExpandedSections] = useState({
    goliath: true,
    flyfox: true,
    sigma: true
  })
  const pathname = usePathname()

  const toggleSection = (section: string) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section as keyof typeof prev]
    }))
  }

  const isActive = (path: string) => pathname === path

  const navItems = [
    { href: '/', icon: Home, label: 'Dashboard', badge: null },
    { href: '/packages', icon: Package, label: 'Q-Sales Packages', badge: 'New' },
    { href: '/contacts', icon: Users, label: 'Contact Import', badge: null },
    { href: '/pods', icon: Rocket, label: 'Sales Pods', badge: 'Hot' }
  ]

  const businessPillars = [
    {
      id: 'goliath',
      name: 'GOLIATH',
      description: 'Financial & CRM',
      color: 'goliath',
      icon: Shield,
      items: [
        { href: '/goliath/crm', label: 'CRM Dashboard' },
        { href: '/goliath/lending', label: 'Lending Portal' },
        { href: '/goliath/insurance', label: 'Insurance Hub' }
      ]
    },
    {
      id: 'flyfox',
      name: 'FLYFOX AI',
      description: 'Transformational Tech',
      color: 'flyfox',
      icon: Brain,
      items: [
        { href: '/flyfox/quantum', label: 'Quantum Computing' },
        { href: '/flyfox/energy', label: 'Energy Solutions' },
        { href: '/flyfox/ai', label: 'AI Platform' }
      ]
    },
    {
      id: 'sigma',
      name: 'SIGMA SELECT',
      description: 'Sales & Revenue',
      color: 'sigma',
      icon: Target,
      items: [
        { href: '/sigma/sales', label: 'Sales Dashboard' },
        { href: '/sigma/leads', label: 'Lead Generation' },
        { href: '/sigma/revenue', label: 'Revenue Analytics' }
      ]
    }
  ]

  return (
    <div className={`bg-white border-r border-gray-200 transition-all duration-300 ${
      isCollapsed ? 'w-16' : 'w-64'
    }`}>
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          {!isCollapsed && (
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-br from-goliath-600 to-flyfox-600 rounded-lg flex items-center justify-center">
                <Zap className="w-5 h-5 text-white" />
              </div>
              <span className="text-lg font-bold text-gray-900">Portal</span>
            </div>
          )}
          <button
            onClick={() => setIsCollapsed(!isCollapsed)}
            className="p-1 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <ChevronDown className={`w-4 h-4 text-gray-600 transition-transform ${
              isCollapsed ? 'rotate-90' : ''
            }`} />
          </button>
        </div>
      </div>

      {/* Main Navigation */}
      <div className="p-4 space-y-2">
        {navItems.map((item) => {
          const Icon = item.icon
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center space-x-3 px-3 py-2 rounded-lg transition-colors ${
                isActive(item.href)
                  ? 'bg-goliath-100 text-goliath-700'
                  : 'text-gray-700 hover:bg-gray-100'
              }`}
            >
              <Icon className="w-5 h-5 flex-shrink-0" />
              {!isCollapsed && (
                <>
                  <span className="flex-1">{item.label}</span>
                  {item.badge && (
                    <span className="px-2 py-1 text-xs font-medium bg-red-100 text-red-800 rounded-full">
                      {item.badge}
                    </span>
                  )}
                </>
              )}
            </Link>
          )
        })}
      </div>

      {/* Business Pillars */}
      <div className="p-4 space-y-4">
        {businessPillars.map((pillar) => {
          const Icon = pillar.icon
          const isExpanded = expandedSections[pillar.id as keyof typeof expandedSections]
          
          return (
            <div key={pillar.id} className="space-y-2">
              <button
                onClick={() => toggleSection(pillar.id)}
                className={`w-full flex items-center justify-between px-3 py-2 rounded-lg transition-colors ${
                  isCollapsed ? 'justify-center' : ''
                }`}
              >
                <div className="flex items-center space-x-3">
                  <Icon className={`w-5 h-5 text-${pillar.color}-600`} />
                  {!isCollapsed && (
                    <div className="text-left">
                      <div className="text-sm font-semibold text-gray-900">{pillar.name}</div>
                      <div className="text-xs text-gray-500">{pillar.description}</div>
                    </div>
                  )}
                </div>
                {!isCollapsed && (
                  <ChevronDown className={`w-4 h-4 text-gray-400 transition-transform ${
                    isExpanded ? 'rotate-180' : ''
                  }`} />
                )}
              </button>
              
              {isExpanded && !isCollapsed && (
                <div className="ml-8 space-y-1">
                  {pillar.items.map((item) => (
                    <Link
                      key={item.href}
                      href={item.href}
                      className={`block px-3 py-2 text-sm rounded-lg transition-colors ${
                        isActive(item.href)
                          ? `bg-${pillar.color}-50 text-${pillar.color}-700`
                          : 'text-gray-600 hover:bg-gray-50'
                      }`}
                    >
                      {item.label}
                    </Link>
                  ))}
                </div>
              )}
            </div>
          )
        })}
      </div>

      {/* Footer */}
      {!isCollapsed && (
        <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-200 bg-gray-50">
          <div className="text-center">
            <div className="text-xs text-gray-500 mb-2">Powered by</div>
            <div className="flex items-center justify-center space-x-2">
              <div className="w-6 h-6 bg-gradient-to-br from-goliath-600 to-flyfox-600 rounded flex items-center justify-center">
                <Zap className="w-4 h-4 text-white" />
              </div>
              <span className="text-sm font-semibold text-gray-700">Dynex Quantum</span>
            </div>
            <div className="text-xs text-gray-400 mt-1">410x Performance</div>
          </div>
        </div>
      )}
    </div>
  )
}
