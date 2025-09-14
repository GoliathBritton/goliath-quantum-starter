'use client'

import { useState } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { motion, AnimatePresence } from 'framer-motion'
import { Menu, X, ChevronDown, User, LogOut } from 'lucide-react'

// Type assertions for components
const LinkComponent = Link as any
const MotionDiv = motion.div as any
const AnimatePresenceComponent = AnimatePresence as any
const MenuIcon = Menu as any
const XIcon = X as any
const ChevronDownIcon = ChevronDown as any
const UserIcon = User as any
const LogOutIcon = LogOut as any
import { brand, navigation, partners as strategicPartners } from '../lib/brand'

export default function Nav() {
  const [isOpen, setIsOpen] = useState(false)
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false)
  const pathname = usePathname()

  const isActive = (path: string) => {
    if (path === '/') return pathname === '/'
    return pathname.startsWith(path)
  }

  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="container-quantum">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <LinkComponent href="/" className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-lg overflow-hidden">
              <img 
                src="/logos/flyfox-logo.png" 
                alt="FLYFOX AI Logo"
                className="w-full h-full object-contain"
              />
            </div>
            <div>
              <div className="font-bold text-xl text-black">{brand.name}</div>
              <div className="text-xs text-gray-500 -mt-1">Powered by NQBA</div>
            </div>
          </LinkComponent>

          {/* Desktop Navigation */}
          <div className="hidden lg:flex items-center space-x-8">
            {navigation.main.map((item) => (
              <LinkComponent
                key={item.path}
                href={item.path}
                className={`text-sm font-medium transition-colors duration-200 ${
                  isActive(item.path)
                    ? 'text-brand-cyan border-b-2 border-brand-cyan pb-1'
                    : 'text-gray-700 hover:text-brand-cyan'
                }`}
              >
                {item.label}
              </LinkComponent>
            ))}
          </div>

          {/* Desktop Actions */}
          <div className="hidden lg:flex items-center space-x-4">
            {/* Partner Badge */}
            <div className="flex items-center space-x-2 px-3 py-1 border border-gray-200 rounded-full bg-white">
              <div className="w-2 h-2 bg-brand-cyan rounded-full"></div>
              <span className="text-xs font-medium text-black">Dynex Ready</span>
            </div>

            {/* User Menu */}
            <div className="relative">
              <button
                onClick={() => setIsUserMenuOpen(!isUserMenuOpen)}
                className="flex items-center space-x-2 px-3 py-2 rounded-lg border border-gray-200 bg-white hover:border-brand-cyan transition-colors duration-200"
              >
                <UserIcon className="h-4 w-4 text-gray-600" />
                <span className="text-sm font-medium text-gray-700">Account</span>
                <ChevronDownIcon className="h-4 w-4 text-gray-600" />
              </button>

              <AnimatePresenceComponent>
                {isUserMenuOpen && (
                  <MotionDiv
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    transition={{ duration: 0.2 }}
                    className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-2"
                  >
                    <LinkComponent
                      href="/flyfox-ai/sign-in"
                      className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors duration-200"
                      onClick={() => setIsUserMenuOpen(false)}
                    >
                      <UserIcon className="inline h-4 w-4 mr-2" />
                      Sign In
                    </LinkComponent>
                    <div className="border-t border-gray-200 my-2"></div>
                    <div className="px-4 py-2">
                      <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
                        Quick Access
                      </div>
                      <LinkComponent
                        href="/resources/recipes"
                        className="block text-sm text-gray-700 hover:text-brand-cyan transition-colors duration-200 mb-1"
                        onClick={() => setIsUserMenuOpen(false)}
                      >
                        QUBO Recipe Builder
                      </LinkComponent>
                      <LinkComponent
                        href="/products"
                        className="block text-sm text-gray-700 hover:text-brand-cyan transition-colors duration-200"
                        onClick={() => setIsUserMenuOpen(false)}
                      >
                        NQBA Core Platform
                      </LinkComponent>
                    </div>
                  </MotionDiv>
                )}
              </AnimatePresenceComponent>
            </div>

            <LinkComponent href="/contact" className="btn-primary text-sm">
              Get Started
            </LinkComponent>
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="lg:hidden p-2 rounded-lg border border-gray-200 bg-white hover:border-brand-cyan transition-colors duration-200"
          >
            {isOpen ? (
              <XIcon className="h-6 w-6 text-gray-600" />
            ) : (
              <MenuIcon className="h-6 w-6 text-gray-600" />
            )}
          </button>
        </div>

        {/* Mobile Navigation */}
        <AnimatePresenceComponent>
          {isOpen && (
            <MotionDiv
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              transition={{ duration: 0.3 }}
              className="lg:hidden border-t border-gray-200 py-4"
            >
              <div className="space-y-4">
                {navigation.main.map((item) => (
                  <LinkComponent
                    key={item.path}
                    href={item.path}
                    className={`block text-base font-medium transition-colors duration-200 ${
                      isActive(item.path)
                        ? 'text-brand-cyan'
                        : 'text-gray-700 hover:text-brand-cyan'
                    }`}
                    onClick={() => setIsOpen(false)}
                  >
                    {item.label}
                  </LinkComponent>
                ))}
                
                <div className="border-t border-gray-200 pt-4 mt-4">
                  <LinkComponent
                    href="/flyfox-ai/sign-in"
                    className="block text-base font-medium text-gray-700 hover:text-brand-cyan transition-colors duration-200 mb-3"
                    onClick={() => setIsOpen(false)}
                  >
                    Sign In
                  </LinkComponent>
                  <LinkComponent
                    href="/contact"
                    className="btn-primary w-full text-center"
                    onClick={() => setIsOpen(false)}
                  >
                    Get Started
                  </LinkComponent>
                </div>

                {/* Mobile Partner Status */}
                <div className="border-t border-gray-200 pt-4 mt-4">
                  <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
                    Partner Status
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {strategicPartners.slice(0, 3).map((partner) => (
                      <div
                        key={partner.name}
                        className="flex items-center space-x-1 px-2 py-1 border border-gray-200 bg-white rounded-full"
                      >
                        <div className="w-2 h-2 bg-brand-cyan rounded-full"></div>
                        <span className="text-xs font-medium text-gray-700">
                          {partner.name}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </MotionDiv>
          )}
        </AnimatePresenceComponent>
      </div>

      {/* Click outside to close user menu */}
      {isUserMenuOpen && (
        <div
          className="fixed inset-0 z-40"
          onClick={() => setIsUserMenuOpen(false)}
        />
      )}
    </nav>
  )
}