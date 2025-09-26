'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { Menu, X, ChevronDown } from 'lucide-react';

// Type assertions
const MotionNav = motion('nav') as any;
const MotionDiv = motion.div as any;
const NextLink = Link as any;

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [windowWidth, setWindowWidth] = useState(typeof window !== 'undefined' ? window.innerWidth : 0);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 10);
    };
    
    const handleResize = () => {
      setWindowWidth(window.innerWidth);
      if (window.innerWidth >= 768) {
        setMobileMenuOpen(false);
      }
    };
    
    window.addEventListener('scroll', handleScroll);
    window.addEventListener('resize', handleResize);
    
    return () => {
      window.removeEventListener('scroll', handleScroll);
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  const navLinks = [
  { name: 'Home', href: '/' },
  { name: 'Solutions', href: '#solutions', 
    dropdown: [
      { name: 'Quantum Computing', href: '#quantum' },
      { name: 'AI Integration', href: '#ai' },
      { name: 'Energy Services', href: '#energy' }
    ]
  },
  { name: 'Products', href: '#products' },
  { name: 'DSP Solutions', href: '/marketing/dsp' },
  { name: 'About', href: '#about' },
  { name: 'Contact', href: '#contact' }
];

  return (
    //@ts-expect-error Motion component type issue
    <MotionNav role="navigation" 
      className={`fixed w-full z-50 transition-all duration-300 ${
        scrolled ? 'bg-white/90 backdrop-blur-md shadow-md py-2' : 'bg-transparent py-4'
      }`}
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="container mx-auto px-4 flex justify-between items-center">
        {/* Logo */}
        <NextLink href="/" className="flex items-center space-x-2">
          <div className="flex flex-col leading-tight">
            <span className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">FLYFOX AI</span>
            <span className="text-sm font-medium text-gray-600">Goliath of All Trade</span>
            <span className="text-sm font-medium text-gray-600">Sigma Select</span>
          </div>
        </Link>

        {/* Desktop Navigation */}
        <div className="hidden md:flex items-center space-x-8">
          {navLinks.map((link) => (
            <div key={link.name} className="relative group">
              <NextLink 
                href={link.href}
                className={`text-sm font-medium ${scrolled ? 'text-gray-800' : 'text-white'} hover:text-blue-500 transition-colors`}
              >
                <div className="flex items-center space-x-1">
                  <span>{link.name}</span>
                  {link.dropdown && <ChevronDown size={14} />}
                </div>
              </NextLink>
              
              {link.dropdown && (
                <div className="absolute left-0 mt-2 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 transform origin-top-right">
                  <div className="py-1">
                    {link.dropdown.map((item) => (
                      <NextLink 
                        key={item.name}
                        href={item.href}
                        className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      >
                        {item.name}
                      </NextLink>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>

        {/* CTA Button */}
        <div className="hidden md:block">
          <NextLink 
            href="/get-started"
            className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-2 rounded-full font-medium hover:shadow-lg transition-all duration-300 hover:scale-105"
          >
            Get Started
          </NextLink>
        </div>

        {/* Mobile Menu Button */}
        <div className="md:hidden">
          <button 
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className={`p-2 rounded-md ${scrolled ? 'text-gray-800' : 'text-white'} focus:outline-none`}
            aria-label={mobileMenuOpen ? "Close menu" : "Open menu"}
          >
            {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
      </div>

      {/* Mobile Menu with Animation */}
      {mobileMenuOpen && (
        <MotionDiv
          className="md:hidden bg-white shadow-xl absolute top-full left-0 right-0 overflow-hidden"
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          exit={{ height: 0, opacity: 0 }}
          transition={{ duration: 0.3 }}
        >
          <div className="px-4 py-5 space-y-4">
            {navLinks.map((link) => (
              <div key={link.name} className="py-2 border-b border-gray-100">
                <NextLink 
                  href={link.href}
                  className="text-gray-800 font-medium block"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  {link.name}
                </NextLink>
                
                {link.dropdown && (
                  <div className="pl-4 mt-2 space-y-2">
                    {link.dropdown.map((item) => (
                      <NextLink 
                        key={item.name}
                        href={item.href}
                        className="text-gray-600 text-sm block py-1"
                        onClick={() => setMobileMenuOpen(false)}
                      >
                        {item.name}
                      </NextLink>
                    ))}
                  </div>
                )}
              </div>
            ))}
            
            <NextLink 
              href="/get-started"
              className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-md font-medium block text-center transform hover:scale-105 transition-all"
              onClick={() => setMobileMenuOpen(false)}
            >
              Get Started
            </NextLink>
          </div>
        </MotionDiv>
      )}
    </MotionNav>
  );
}