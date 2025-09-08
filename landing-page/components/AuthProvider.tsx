'use client'

import { createContext, useContext, useState, useEffect, ReactNode } from 'react'

interface User {
  id: string
  email: string
  name: string
  tier: 'standard' | 'pro' | 'partner'
  businessUnit?: string
  permissions: string[]
}

interface AuthContextType {
  user: User | null
  isLoading: boolean
  signIn: (email: string, password: string) => Promise<void>
  signOut: () => void
  isAuthenticated: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

interface AuthProviderProps {
  children: ReactNode
}

export default function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Check for existing session on mount
    checkAuthStatus()
  }, [])

  const checkAuthStatus = async () => {
    try {
      // In a real implementation, this would check with your auth service
      // For now, we'll check localStorage for demo purposes
      const storedUser = localStorage.getItem('flyfox_user')
      if (storedUser) {
        setUser(JSON.parse(storedUser))
      }
    } catch (error) {
      console.error('Auth check failed:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const signIn = async (email: string, password: string) => {
    setIsLoading(true)
    try {
      // In a real implementation, this would call your auth API
      // For demo purposes, we'll simulate authentication
      
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // Mock user based on email domain
      let mockUser: User
      
      if (email.includes('@goliath')) {
        mockUser = {
          id: '1',
          email,
          name: 'Goliath Executive',
          tier: 'partner',
          businessUnit: 'Goliath of All Trade',
          permissions: ['admin', 'quantum_access', 'all_business_units']
        }
      } else if (email.includes('@sigma')) {
        mockUser = {
          id: '2',
          email,
          name: 'Sigma Select Member',
          tier: 'pro',
          businessUnit: 'Sigma Select',
          permissions: ['pro_features', 'quantum_access', 'training_access']
        }
      } else {
        mockUser = {
          id: '3',
          email,
          name: 'FLYFOX User',
          tier: 'standard',
          permissions: ['basic_features', 'limited_quantum_access']
        }
      }
      
      setUser(mockUser)
      localStorage.setItem('flyfox_user', JSON.stringify(mockUser))
      
    } catch (error) {
      console.error('Sign in failed:', error)
      throw new Error('Authentication failed. Please check your credentials.')
    } finally {
      setIsLoading(false)
    }
  }

  const signOut = () => {
    setUser(null)
    localStorage.removeItem('flyfox_user')
    // In a real implementation, you would also invalidate the session on the server
  }

  const value: AuthContextType = {
    user,
    isLoading,
    signIn,
    signOut,
    isAuthenticated: !!user
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

// Hook for checking user permissions
export function usePermissions() {
  const { user } = useAuth()
  
  const hasPermission = (permission: string) => {
    return user?.permissions.includes(permission) || false
  }
  
  const hasAnyPermission = (permissions: string[]) => {
    return permissions.some(permission => hasPermission(permission))
  }
  
  const hasAllPermissions = (permissions: string[]) => {
    return permissions.every(permission => hasPermission(permission))
  }
  
  return {
    hasPermission,
    hasAnyPermission,
    hasAllPermissions,
    userTier: user?.tier || 'standard',
    businessUnit: user?.businessUnit
  }
}

// Component for protecting routes based on authentication
interface ProtectedRouteProps {
  children: ReactNode
  fallback?: ReactNode
  requireAuth?: boolean
  requiredPermissions?: string[]
}

export function ProtectedRoute({ 
  children, 
  fallback = null, 
  requireAuth = true,
  requiredPermissions = []
}: ProtectedRouteProps) {
  const { isAuthenticated, isLoading } = useAuth()
  const { hasAllPermissions } = usePermissions()
  
  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-brand-cyan"></div>
      </div>
    )
  }
  
  if (requireAuth && !isAuthenticated) {
    return fallback || (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Authentication Required</h2>
          <p className="text-gray-600 mb-6">Please sign in to access this page.</p>
          <a href="/flyfox-ai/sign-in" className="btn-primary">
            Sign In
          </a>
        </div>
      </div>
    )
  }
  
  if (requiredPermissions.length > 0 && !hasAllPermissions(requiredPermissions)) {
    return fallback || (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Access Denied</h2>
          <p className="text-gray-600 mb-6">You don't have permission to access this page.</p>
          <a href="/" className="btn-primary">
            Go Home
          </a>
        </div>
      </div>
    )
  }
  
  return <>{children}</>
}