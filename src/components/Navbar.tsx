"use client"

import { useState } from 'react'
import Link from 'next/link'
import { Menu, X, User, Settings, LogOut, Zap, Bell } from 'lucide-react'

export default function Navbar() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false)

  return (
    <nav className="bg-white border-b border-gray-200 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo and Brand */}
          <div className="flex items-center">
            <Link href="/" className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-br from-goliath-600 to-flyfox-600 rounded-lg flex items-center justify-center">
                <Zap className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-gray-900">Goliath Portal</span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            <Link href="/packages" className="text-gray-700 hover:text-goliath-600 transition-colors">
              Q-Sales Packages
            </Link>
            <Link href="/contacts" className="text-gray-700 hover:text-goliath-600 transition-colors">
              Contact Import
            </Link>
            <Link href="/pods" className="text-gray-700 hover:text-goliath-600 transition-colors">
              Sales Pods
            </Link>
          </div>

          {/* Right Side */}
          <div className="flex items-center space-x-4">
            {/* Notifications */}
            <button className="p-2 text-gray-400 hover:text-gray-500 transition-colors relative">
              <Bell className="w-5 h-5" />
              <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
            </button>

            {/* User Menu */}
            <div className="relative">
              <button
                onClick={() => setIsUserMenuOpen(!isUserMenuOpen)}
                className="flex items-center space-x-2 p-2 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <div className="w-8 h-8 bg-goliath-100 rounded-full flex items-center justify-center">
                  <User className="w-5 h-5 text-goliath-600" />
                </div>
                <span className="hidden md:block text-sm font-medium text-gray-700">
                  John Business
                </span>
              </button>

              {/* User Dropdown */}
              {isUserMenuOpen && (
                <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-2 z-50">
                  <Link
                    href="/profile"
                    className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors"
                  >
                    <User className="w-4 h-4 mr-3" />
                    Profile
                  </Link>
                  <Link
                    href="/settings"
                    className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors"
                  >
                    <Settings className="w-4 h-4 mr-3" />
                    Settings
                  </Link>
                  <hr className="my-2" />
                  <button className="w-full flex items-center px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors">
                    <LogOut className="w-4 h-4 mr-3" />
                    Sign Out
                  </button>
                </div>
              )}
            </div>

            {/* Mobile Menu Button */}
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="md:hidden p-2 text-gray-400 hover:text-gray-500 transition-colors"
            >
              {isMenuOpen ? (
                <X className="w-6 h-6" />
              ) : (
                <Menu className="w-6 h-6" />
              )}
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden border-t border-gray-200 py-4">
            <div className="space-y-2">
              <Link
                href="/packages"
                className="block px-4 py-2 text-gray-700 hover:bg-gray-100 transition-colors"
                onClick={() => setIsMenuOpen(false)}
              >
                Q-Sales Packages
              </Link>
              <Link
                href="/contacts"
                className="block px-4 py-2 text-gray-700 hover:bg-gray-100 transition-colors"
                onClick={() => setIsMenuOpen(false)}
              >
                Contact Import
              </Link>
              <Link
                href="/pods"
                className="block px-4 py-2 text-gray-700 hover:bg-gray-100 transition-colors"
                onClick={() => setIsMenuOpen(false)}
              >
                Sales Pods
              </Link>
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}
