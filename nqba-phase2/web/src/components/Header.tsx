import { useState } from "react";
import Link from "next/link";

export default function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const navigation = [
    {
      name: "Platform",
      href: "/platform",
      description: "Jobs, Agents, Pipelines",
      icon: "🚀"
    },
    {
      name: "Ecosystem",
      href: "/ecosystem",
      description: "NQBA, Council, Architects",
      icon: "🌐"
    },
    {
      name: "Sigma Select",
      href: "/sigma-select",
      description: "Sales Intelligence Platform",
      icon: "Σ"
    },
    {
      name: "Docs",
      href: "/docs",
      description: "API, SDK, Guides",
      icon: "📚"
    },
    {
      name: "Company",
      href: "/company",
      description: "Case Studies, Partners",
      icon: "🏢"
    }
  ];

  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-20">
          {/* Logo */}
          <div className="flex items-center">
            <Link href="/" className="flex items-center space-x-3 group">
              <div className="w-12 h-12 bg-gradient-to-br from-blue-600 to-purple-600 rounded-xl flex items-center justify-center text-white font-bold text-xl group-hover:scale-105 transition-transform">
                🦊
              </div>
              <div className="hidden sm:block">
                <div className="text-2xl font-bold text-gray-900">FLYFOX AI</div>
                <div className="text-xs text-gray-500">Powered by NQBA</div>
              </div>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden lg:flex space-x-8">
            {navigation.map((item) => (
              <div key={item.name} className="relative group">
                <Link
                  href={item.href}
                  className="text-gray-700 hover:text-blue-600 px-3 py-2 text-sm font-medium transition-colors duration-200 flex items-center space-x-2"
                >
                  <span>{item.icon}</span>
                  <span>{item.name}</span>
                </Link>
                
                {/* Dropdown */}
                <div className="absolute left-0 mt-2 w-64 bg-white rounded-xl shadow-lg border border-gray-200 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50">
                  <div className="p-6">
                    <div className="text-sm font-semibold text-gray-900 mb-2">{item.name}</div>
                    <p className="text-sm text-gray-600 mb-4">{item.description}</p>
                    <Link
                      href={item.href}
                      className="inline-flex items-center text-sm text-blue-600 hover:text-blue-700 font-medium"
                    >
                      Explore {item.name} →
                    </Link>
                  </div>
                </div>
              </div>
            ))}
          </nav>

          {/* CTA Buttons */}
          <div className="hidden lg:flex items-center space-x-4">
            <Link
              href="/contact"
              className="text-gray-700 hover:text-blue-600 px-3 py-2 text-sm font-medium transition-colors duration-200"
            >
              Contact
            </Link>
            <Link
              href="/platform"
              className="bg-blue-600 text-white px-6 py-3 rounded-lg text-sm font-semibold hover:bg-blue-700 transition-all duration-200"
            >
              Launch Platform
            </Link>
          </div>

          {/* Mobile menu button */}
          <div className="lg:hidden">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="text-gray-700 hover:text-blue-600 p-2"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                {isMenuOpen ? (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="lg:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 bg-gray-50 rounded-lg mt-2 mb-4">
              {navigation.map((item) => (
                <Link
                  key={item.name}
                  href={item.href}
                  className="block px-3 py-2 text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-100 rounded-md transition-colors duration-200"
                  onClick={() => setIsMenuOpen(false)}
                >
                  <div className="flex items-center space-x-3">
                    <span className="text-lg">{item.icon}</span>
                    <div>
                      <div className="font-semibold">{item.name}</div>
                      <div className="text-sm text-gray-500">{item.description}</div>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
            
            <div className="px-2 pt-2 pb-3 space-y-2">
              <Link
                href="/contact"
                className="block px-3 py-2 text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-100 rounded-md transition-colors duration-200"
                onClick={() => setIsMenuOpen(false)}
              >
                Contact
              </Link>
              <Link
                href="/platform"
                className="block px-3 py-2 text-base font-medium bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-all duration-200"
                onClick={() => setIsMenuOpen(false)}
              >
                Launch Platform
              </Link>
            </div>
          </div>
        )}
      </div>
    </header>
  );
}