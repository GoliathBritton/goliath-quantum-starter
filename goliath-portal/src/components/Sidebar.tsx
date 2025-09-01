"use client"

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
  Target
} from 'lucide-react'

export default function Sidebar() {
  const pathname = usePathname()

  const navigation = [
    {
      name: 'Dashboard',
      href: '/',
      icon: Home,
      description: 'Overview and analytics'
    },
    {
      name: 'Packages',
      href: '/packages',
      icon: Package,
      description: 'Q-Sales Division™ pricing'
    },
    {
      name: 'Contacts',
      href: '/contacts',
      icon: Users,
      description: 'Import and manage contacts'
    },
    {
      name: 'Sales Pods',
      href: '/pods',
      icon: Rocket,
      description: 'Deploy autonomous agents'
    }
  ]

  const quickActions = [
    {
      name: 'Analytics',
      href: '/analytics',
      icon: BarChart3,
      description: 'Performance metrics'
    },
    {
      name: 'Settings',
      href: '/settings',
      icon: Settings,
      description: 'Account configuration'
    }
  ]

  const isActive = (href: string) => {
    if (href === '/') {
      return pathname === '/'
    }
    return pathname.startsWith(href)
  }

  return (
    <aside className="w-64 hidden lg:flex flex-col bg-white border-r border-gray-200 shadow-sm">
      {/* Logo and Brand */}
      <div className="p-6 border-b border-gray-200">
        <Link href="/" className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-gradient-to-br from-goliath-600 to-flyfox-600 rounded-xl flex items-center justify-center">
            <Zap className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-gray-900">Goliath Portal</h1>
            <p className="text-xs text-gray-500">Quantum-Powered CRM</p>
          </div>
        </Link>
      </div>

      {/* Main Navigation */}
      <div className="flex-1 p-4">
        <div className="mb-6">
          <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
            Main Navigation
          </h3>
          <nav className="space-y-1">
            {navigation.map((item) => {
              const Icon = item.icon
              const active = isActive(item.href)
              
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className={`
                    group flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors
                    ${active 
                      ? 'bg-goliath-50 text-goliath-700 border-r-2 border-goliath-600' 
                      : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
                    }
                  `}
                >
                  <Icon 
                    className={`
                      mr-3 h-5 w-5 transition-colors
                      ${active ? 'text-goliath-600' : 'text-gray-400 group-hover:text-gray-500'}
                    `} 
                  />
                  <div>
                    <div className="font-medium">{item.name}</div>
                    <div className="text-xs text-gray-500">{item.description}</div>
                  </div>
                </Link>
              )
            })}
          </nav>
        </div>

        {/* Quick Actions */}
        <div className="mb-6">
          <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
            Quick Actions
          </h3>
          <nav className="space-y-1">
            {quickActions.map((item) => {
              const Icon = item.icon
              const active = isActive(item.href)
              
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className={`
                    group flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors
                    ${active 
                      ? 'bg-goliath-50 text-goliath-700 border-r-2 border-goliath-600' 
                      : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
                    }
                  `}
                >
                  <Icon 
                    className={`
                      mr-3 h-5 w-5 transition-colors
                      ${active ? 'text-goliath-600' : 'text-gray-400 group-hover:text-gray-500'}
                    `} 
                  />
                  <div>
                    <div className="font-medium">{item.name}</div>
                    <div className="text-xs text-gray-500">{item.description}</div>
                  </div>
                </Link>
              )
            })}
          </nav>
        </div>

        {/* Business Pillars */}
        <div className="mb-6">
          <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
            Business Pillars
          </h3>
          <div className="space-y-2">
            <div className="px-3 py-2">
              <div className="flex items-center text-sm">
                <div className="w-2 h-2 bg-goliath-500 rounded-full mr-3"></div>
                <span className="font-medium text-goliath-700">GOLIATH</span>
              </div>
              <p className="text-xs text-gray-500 ml-5">Financial & CRM</p>
            </div>
            
            <div className="px-3 py-2">
              <div className="flex items-center text-sm">
                <div className="w-2 h-2 bg-flyfox-500 rounded-full mr-3"></div>
                <span className="font-medium text-flyfox-700">FLYFOX AI</span>
              </div>
              <p className="text-xs text-gray-500 ml-5">Tech & Energy</p>
            </div>
            
            <div className="px-3 py-2">
              <div className="flex items-center text-sm">
                <div className="w-2 h-2 bg-sigma-500 rounded-full mr-3"></div>
                <span className="font-medium text-sigma-700">SIGMA SELECT</span>
              </div>
              <p className="text-xs text-gray-500 ml-5">Sales & Revenue</p>
            </div>
          </div>
        </div>

        {/* Quantum Computing Badge */}
        <div className="p-3 bg-gradient-to-r from-goliath-50 to-flyfox-50 rounded-lg border border-goliath-200">
          <div className="flex items-center space-x-2 mb-2">
            <Brain className="w-4 h-4 text-goliath-600" />
            <span className="text-xs font-semibold text-goliath-700">Quantum Powered</span>
          </div>
          <p className="text-xs text-gray-600">
            Powered by Dynex (410x performance) + NVIDIA acceleration
          </p>
        </div>
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-gray-200">
        <div className="text-center">
          <p className="text-xs text-gray-500">
            © 2024 Goliath Family
          </p>
          <p className="text-xs text-gray-400 mt-1">
            Quantum Revolution
          </p>
        </div>
      </div>
    </aside>
  )
}
