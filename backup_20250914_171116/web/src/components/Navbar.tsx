import Link from 'next/link'
import { useState, useEffect, useRef } from 'react'
import { useSession, signOut } from 'next-auth/react'
import { Menu, X, Zap, BarChart3, Users, Settings, CreditCard, LogOut, User } from 'lucide-react'

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false)
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false)
  const { data: session, status } = useSession()
  const userMenuRef = useRef<HTMLDivElement>(null)

  // Close user menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (userMenuRef.current && !userMenuRef.current.contains(event.target as Node)) {
        setIsUserMenuOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [])

  const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: BarChart3 },
    { name: 'Partners', href: '/partners', icon: Users },
    { name: 'Billing', href: '/billing', icon: CreditCard },
    { name: 'Pricing', href: '/pricing', icon: Settings },
  ]

  return (
    <nav className="bg-white/80 backdrop-blur-md border-b border-slate-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo */}
          <div className="flex items-center">
            <Link href="/" className="flex items-center space-x-2 group">
              <div className="relative">
                <Zap className="h-8 w-8 text-quantum-primary group-hover:text-quantum-secondary transition-colors duration-300" />
                <div className="absolute inset-0 bg-quantum-primary/20 rounded-full blur-lg group-hover:bg-quantum-secondary/20 transition-colors duration-300"></div>
              </div>
              <div className="flex flex-col">
                <span className="text-xl font-bold gradient-text">Goliath</span>
                <span className="text-xs text-slate-500 -mt-1">Quantum Computing</span>
              </div>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            {navigation.map((item) => {
              const Icon = item.icon
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className="flex items-center space-x-1 text-slate-600 hover:text-quantum-primary transition-colors duration-200 group"
                >
                  <Icon className="h-4 w-4 group-hover:scale-110 transition-transform duration-200" />
                  <span className="font-medium">{item.name}</span>
                </Link>
              )
            })}
            
            {/* Authentication Section */}
            {status === 'loading' ? (
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-quantum-primary"></div>
            ) : session ? (
              <div className="relative" ref={userMenuRef}>
                <button
                  onClick={() => setIsUserMenuOpen(!isUserMenuOpen)}
                  className="flex items-center space-x-2 text-slate-600 hover:text-quantum-primary transition-colors duration-200 group"
                >
                  <User className="h-5 w-5 group-hover:scale-110 transition-transform duration-200" />
                  <span className="font-medium">{session.user.first_name}</span>
                </button>
                
                {isUserMenuOpen && (
                  <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-slate-200 py-2 z-50">
                    <div className="px-4 py-2 border-b border-slate-200">
                      <p className="text-sm font-medium text-slate-800">{session.user.first_name} {session.user.last_name}</p>
                      <p className="text-xs text-slate-500">{session.user.email}</p>
                      <p className="text-xs text-quantum-primary capitalize">{session.user.role}</p>
                    </div>
                    <Link
                      href="/dashboard"
                      className="flex items-center px-4 py-2 text-sm text-slate-700 hover:bg-slate-50 transition-colors duration-200"
                      onClick={() => setIsUserMenuOpen(false)}
                    >
                      <BarChart3 className="h-4 w-4 mr-2" />
                      Dashboard
                    </Link>
                    <Link
                      href="/billing"
                      className="flex items-center px-4 py-2 text-sm text-slate-700 hover:bg-slate-50 transition-colors duration-200"
                      onClick={() => setIsUserMenuOpen(false)}
                    >
                      <CreditCard className="h-4 w-4 mr-2" />
                      Billing
                    </Link>
                    <button
                      onClick={() => {
                        setIsUserMenuOpen(false)
                        signOut({ callbackUrl: '/' })
                      }}
                      className="flex items-center w-full px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors duration-200"
                    >
                      <LogOut className="h-4 w-4 mr-2" />
                      Sign Out
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <Link
                href="/sign-in"
                className="btn-quantum text-white px-6 py-2 rounded-lg font-medium shadow-lg hover:shadow-xl transition-all duration-300"
              >
                Sign In
              </Link>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="text-slate-600 hover:text-quantum-primary transition-colors duration-200"
            >
              {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Navigation */}
      {isOpen && (
        <div className="md:hidden bg-white/95 backdrop-blur-md border-t border-slate-200">
          <div className="px-2 pt-2 pb-3 space-y-1">
            {navigation.map((item) => {
              const Icon = item.icon
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className="flex items-center space-x-2 text-slate-600 hover:text-quantum-primary hover:bg-slate-50 block px-3 py-2 rounded-md transition-all duration-200"
                  onClick={() => setIsOpen(false)}
                >
                  <Icon className="h-4 w-4" />
                  <span className="font-medium">{item.name}</span>
                </Link>
              )
            })}
            
            {/* Mobile Authentication Section */}
            {status === 'loading' ? (
              <div className="flex justify-center py-4">
                <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-quantum-primary"></div>
              </div>
            ) : session ? (
              <div className="border-t border-slate-200 mt-4 pt-4">
                <div className="px-3 py-2">
                  <div className="flex items-center space-x-2 mb-3">
                    <User className="h-5 w-5 text-quantum-primary" />
                    <div>
                      <p className="text-sm font-medium text-slate-800">{session.user.first_name} {session.user.last_name}</p>
                      <p className="text-xs text-slate-500">{session.user.email}</p>
                      <p className="text-xs text-quantum-primary capitalize">{session.user.role}</p>
                    </div>
                  </div>
                  <Link
                    href="/dashboard"
                    className="flex items-center space-x-2 text-slate-600 hover:text-quantum-primary hover:bg-slate-50 block px-3 py-2 rounded-md transition-all duration-200"
                    onClick={() => setIsOpen(false)}
                  >
                    <BarChart3 className="h-4 w-4" />
                    <span className="font-medium">Dashboard</span>
                  </Link>
                  <Link
                    href="/billing"
                    className="flex items-center space-x-2 text-slate-600 hover:text-quantum-primary hover:bg-slate-50 block px-3 py-2 rounded-md transition-all duration-200"
                    onClick={() => setIsOpen(false)}
                  >
                    <CreditCard className="h-4 w-4" />
                    <span className="font-medium">Billing</span>
                  </Link>
                  <button
                    onClick={() => {
                      setIsOpen(false)
                      signOut({ callbackUrl: '/' })
                    }}
                    className="flex items-center space-x-2 text-red-600 hover:text-red-700 hover:bg-red-50 block px-3 py-2 rounded-md transition-all duration-200 w-full text-left"
                  >
                    <LogOut className="h-4 w-4" />
                    <span className="font-medium">Sign Out</span>
                  </button>
                </div>
              </div>
            ) : (
              <Link
                href="/sign-in"
                className="btn-quantum text-white px-3 py-2 rounded-md font-medium block text-center mt-4 mx-3"
                onClick={() => setIsOpen(false)}
              >
                Sign In
              </Link>
            )}
          </div>
        </div>
      )}
    </nav>
  )
}

export default Navbar