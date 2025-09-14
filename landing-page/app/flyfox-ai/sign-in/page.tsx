'use client'

import { motion } from 'framer-motion'

// Type assertions for Framer Motion components
const MotionDiv = motion.div as any
const MotionH1 = motion.h1 as any
const MotionP = motion.p as any
const MotionForm = motion.form as any

// Type assertions for Lucide icons
const ZapIcon = Zap as any
const ShieldIcon = Shield as any
const UsersIcon = Users as any
const Building2Icon = Building2 as any
const CheckCircleIcon = CheckCircle as any
const AlertCircleIcon = AlertCircle as any
const Loader2Icon = Loader2 as any
const GithubIcon = Github as any
const LinkedinIcon = Linkedin as any
const ChromeIcon = Chrome as any
const MailIcon = Mail as any
const LockIcon = Lock as any
const EyeIcon = Eye as any
const EyeOffIcon = EyeOff as any
const ArrowRightIcon = ArrowRight as any

// Type assertion for Next.js Link
const LinkComponent = Link as any
import { 
  Mail, 
  Lock, 
  Eye, 
  EyeOff, 
  ArrowRight, 
  Shield, 
  Zap, 
  Users, 
  Building2,
  CheckCircle,
  AlertCircle,
  Loader2,
  Github,
  Linkedin,
  Chrome
} from 'lucide-react'
import Link from 'next/link'
import { useState } from 'react'
import { useAuth } from '@/components/AuthProvider'
import { useRouter } from 'next/navigation'
import { businessUnits, pricingTiers } from '@/lib/brand'

export default function SignInPage() {
  const { signIn } = useAuth()
  const router = useRouter()
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    rememberMe: false
  })
  const [showPassword, setShowPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const fadeInUp = {
    initial: { opacity: 0, y: 60 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.6 }
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
    setError('')
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')
    
    try {
      // Simulate authentication
      await new Promise(resolve => setTimeout(resolve, 1500))
      
      // Demo credentials check
      if (formData.email === 'demo@flyfoxai.com' && formData.password === 'quantum2024') {
        await signIn(formData.email, formData.password)
        setSuccess('Successfully signed in! Redirecting...')
        setTimeout(() => {
          router.push('/resources/recipes')
        }, 1000)
      } else {
        setError('Invalid credentials. Try demo@flyfoxai.com / quantum2024')
      }
    } catch (err) {
      setError('Authentication failed. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleSocialSignIn = (provider: string) => {
    setError('')
    setSuccess(`Redirecting to ${provider} authentication...`)
    // In a real app, this would redirect to the OAuth provider
  }

  return (
    <div className="bg-white min-h-screen">
      {/* Hero Section */}
      <section className="hero-gradient section-padding">
        <div className="container-quantum">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            {/* Left Side - Branding */}
            <MotionDiv
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
            >
              <h1 className="text-5xl md:text-6xl font-bold text-black mb-6">
                Welcome to <span className="text-gradient-cyan">FLYFOX AI</span>
              </h1>
              <p className="text-xl text-gray-600 mb-8">
                Access your quantum intelligence platform and unlock the power of 
                exponential business transformation.
              </p>
              
              <div className="space-y-6">
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-brand-cyan rounded-lg flex items-center justify-center">
                    <ZapIcon className="h-6 w-6 text-white" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-black">Quantum-Powered Analytics</h3>
                    <p className="text-gray-600">Exponential performance gains through quantum computing</p>
                  </div>
                </div>
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-brand-gold rounded-lg flex items-center justify-center">
                    <ShieldIcon className="h-6 w-6 text-white" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-black">Enterprise Security</h3>
                    <p className="text-gray-600">Bank-grade security with quantum-resistant encryption</p>
                  </div>
                </div>
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-brand-navy rounded-lg flex items-center justify-center">
                    <UsersIcon className="h-6 w-6 text-white" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-black">Global Collaboration</h3>
                    <p className="text-gray-600">Connect with quantum experts worldwide</p>
                  </div>
                </div>
              </div>
            </MotionDiv>

            {/* Right Side - Sign In Form */}
            <MotionDiv
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="card bg-white shadow-xl"
            >
              <div className="text-center mb-8">
                <h2 className="text-3xl font-bold text-black mb-2">Sign In</h2>
                <p className="text-gray-600">Access your quantum intelligence dashboard</p>
              </div>

              {/* Demo Credentials Notice */}
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
                <div className="flex items-start space-x-3">
                  <AlertCircleIcon className="h-5 w-5 text-blue-600 mt-0.5 flex-shrink-0" />
                  <div>
                    <h4 className="text-sm font-medium text-blue-800 mb-1">Demo Access</h4>
                    <p className="text-sm text-blue-700 mb-2">
                      Use these credentials to explore the platform:
                    </p>
                    <div className="text-sm font-mono bg-white rounded px-2 py-1 text-blue-800">
                      Email: demo@flyfoxai.com<br />
                      Password: quantum2024
                    </div>
                  </div>
                </div>
              </div>

              {/* Error/Success Messages */}
              {error && (
                <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
                  <div className="flex items-center space-x-3">
                    <AlertCircleIcon className="h-5 w-5 text-red-600 flex-shrink-0" />
                    <span className="text-sm text-red-700">{error}</span>
                  </div>
                </div>
              )}

              {success && (
                <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
                  <div className="flex items-center space-x-3">
                    <CheckCircleIcon className="h-5 w-5 text-green-600 flex-shrink-0" />
                    <span className="text-sm text-green-700">{success}</span>
                  </div>
                </div>
              )}

              <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-black mb-2">
                    Email Address
                  </label>
                  <div className="relative">
                    <MailIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                    <input
                      type="email"
                      name="email"
                      value={formData.email}
                      onChange={handleInputChange}
                      required
                      className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-brand-cyan focus:border-transparent transition-colors duration-200"
                      placeholder="Enter your email"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-black mb-2">
                    Password
                  </label>
                  <div className="relative">
                    <LockIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                    <input
                      type={showPassword ? 'text' : 'password'}
                      name="password"
                      value={formData.password}
                      onChange={handleInputChange}
                      required
                      className="w-full pl-10 pr-12 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-brand-cyan focus:border-transparent transition-colors duration-200"
                      placeholder="Enter your password"
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors duration-200"
                    >
                      {showPassword ? <EyeOffIcon className="h-5 w-5" /> : <EyeIcon className="h-5 w-5" />}
                    </button>
                  </div>
                </div>

                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <input
                      type="checkbox"
                      name="rememberMe"
                      checked={formData.rememberMe}
                      onChange={handleInputChange}
                      className="h-4 w-4 text-brand-cyan focus:ring-brand-cyan border-gray-300 rounded"
                    />
                    <label className="text-sm text-gray-600">
                      Remember me
                    </label>
                  </div>
                  <LinkComponent
                    href="#"
                    className="text-sm text-brand-cyan hover:text-brand-gold transition-colors duration-200"
                  >
                    Forgot password?
                  </LinkComponent>
                </div>

                <button
                  type="submit"
                  disabled={isLoading}
                  className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isLoading ? (
                    <>
                      <Loader2Icon className="animate-spin h-5 w-5 mr-2" />
                      Signing In...
                    </>
                  ) : (
                    <>
                      Sign In
                      <ArrowRightIcon className="ml-2 h-5 w-5" />
                    </>
                  )}
                </button>
              </form>

              <div className="mt-8">
                <div className="relative">
                  <div className="absolute inset-0 flex items-center">
                    <div className="w-full border-t border-gray-300" />
                  </div>
                  <div className="relative flex justify-center text-sm">
                    <span className="px-2 bg-white text-gray-500">Or continue with</span>
                  </div>
                </div>

                <div className="mt-6 grid grid-cols-3 gap-3">
                  <button
                    onClick={() => handleSocialSignIn('Google')}
                    className="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-lg bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 transition-colors duration-200"
                  >
                    <ChromeIcon className="h-5 w-5" />
                  </button>
                  <button
                    onClick={() => handleSocialSignIn('LinkedIn')}
                    className="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-lg bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 transition-colors duration-200"
                  >
                    <LinkedinIcon className="h-5 w-5" />
                  </button>
                  <button
                    onClick={() => handleSocialSignIn('GitHub')}
                    className="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-lg bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 transition-colors duration-200"
                  >
                    <GithubIcon className="h-5 w-5" />
                  </button>
                </div>
              </div>

              <div className="mt-8 text-center">
                <p className="text-sm text-gray-600">
                  Don't have an account?{' '}
                  <LinkComponent
                    href="/contact"
                    className="text-brand-cyan hover:text-brand-gold transition-colors duration-200 font-medium"
                  >
                    Contact Sales
                  </LinkComponent>
                </p>
              </div>
            </MotionDiv>
          </div>
        </div>
      </section>

      {/* Business Units Overview */}
      <section className="section-padding bg-gray-50">
        <div className="container-quantum">
          <MotionDiv
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-black mb-6">
              Intelligence Economy Access
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Your credentials provide access to our complete ecosystem of quantum-powered business units.
            </p>
          </MotionDiv>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {businessUnits.map((unit, index) => (
              <MotionDiv
                key={unit.name}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="card text-center group hover:shadow-lg transition-shadow duration-200"
              >
                <div className={`w-16 h-16 ${unit.color} rounded-full flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-200`}>
                  <Building2Icon className="h-8 w-8 text-white" />
                </div>
                <h3 className="text-xl font-bold text-black mb-3">{unit.name}</h3>
                <p className="text-gray-600 mb-4">{unit.description}</p>
                <div className="text-sm text-brand-cyan font-medium">
                  {unit.focus}
                </div>
              </MotionDiv>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing Tiers */}
      <section className="section-padding">
        <div className="container-quantum">
          <MotionDiv
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-black mb-6">
              Choose Your Access Level
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Flexible pricing tiers designed to scale with your quantum transformation journey.
            </p>
          </MotionDiv>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {pricingTiers.map((tier, index) => (
              <MotionDiv
                key={tier.name}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="card relative group hover:shadow-lg transition-shadow duration-200"
              >

                <div className="text-center">
                  <h3 className="text-2xl font-bold text-black mb-2">{tier.name}</h3>
                  <div className="text-4xl font-bold text-brand-cyan mb-6">{tier.price}</div>
                  <p className="text-gray-600 mb-8">{tier.description}</p>
                  
                  <div className="space-y-4 mb-8">
                    {tier.features.map((feature, idx) => (
                      <div key={idx} className="flex items-center space-x-3">
                        <CheckCircleIcon className="h-5 w-5 text-brand-cyan flex-shrink-0" />
                        <span className="text-gray-700">{feature}</span>
                      </div>
                    ))}
                  </div>
                  
                  <LinkComponent
                    href="/contact"
                    className="w-full inline-flex items-center justify-center px-6 py-3 rounded-lg font-medium transition-colors duration-200 bg-white text-brand-cyan border-2 border-brand-cyan hover:bg-brand-cyan hover:text-white"
                  >
                    Get Started
                    <ArrowRightIcon className="ml-2 h-4 w-4" />
                  </LinkComponent>
                </div>
              </MotionDiv>
            ))}
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="section-padding bg-gray-50">
        <div className="container-narrow text-center">
          <MotionDiv
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl md:text-5xl font-bold text-black mb-6">
              Need Help Getting Started?
            </h2>
            <p className="text-xl text-gray-600 mb-8">
              Our quantum intelligence experts are here to guide your transformation journey.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <LinkComponent href="/contact" className="btn-primary">
                Contact Sales Team
                <ArrowRightIcon className="ml-2 h-5 w-5" />
              </LinkComponent>
              <LinkComponent href="/resources" className="btn-secondary">
                Explore Resources
              </LinkComponent>
            </div>
          </MotionDiv>
        </div>
      </section>
    </div>
  )
}