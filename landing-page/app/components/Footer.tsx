'use client';

import React from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { Mail, Phone, MapPin, Facebook, Twitter, Linkedin, Instagram, Github } from 'lucide-react';

const MotionFooter = motion.footer as any;

export default function Footer() {
  const currentYear = new Date().getFullYear();
  
  return (
    <MotionFooter 
      role="contentinfo"
      className="bg-gradient-to-br from-gray-900 to-blue-900 text-white"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <div className="container mx-auto px-6 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Company Info */}
          <div>
            <h3 className="text-xl font-bold mb-4 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">FLYFOX AI</h3>
            <p className="text-gray-300 mb-2">Goliath of All Trade</p>
            <p className="text-gray-300 mb-4">Sigma Select</p>
            <p className="text-gray-300 mb-4">
              Empowering businesses with quantum computing and AI solutions for the future.
            </p>
            <div className="flex space-x-4">
              <a href="#" aria-label="Facebook" className="text-gray-400 hover:text-white transition-colors">
                <Facebook size={20} aria-hidden="true" />
              </a>
              <a href="#" aria-label="Twitter" className="text-gray-400 hover:text-white transition-colors">
                <Twitter size={20} aria-hidden="true" />
              </a>
              <a href="#" aria-label="LinkedIn" className="text-gray-400 hover:text-white transition-colors">
                <Linkedin size={20} aria-hidden="true" />
              </a>
              <a href="#" aria-label="Instagram" className="text-gray-400 hover:text-white transition-colors">
                <Instagram size={20} aria-hidden="true" />
              </a>
              <a href="#" aria-label="GitHub" className="text-gray-400 hover:text-white transition-colors">
                <Github size={20} aria-hidden="true" />
              </a>
            </div>
          </div>
          
          {/* Quick Links */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <Link href="/" className="text-gray-300 hover:text-white transition-colors">Home</Link>
              </li>
              <li>
                <Link href="#about" className="text-gray-300 hover:text-white transition-colors">About Us</Link>
              </li>
              <li>
                <Link href="#services" className="text-gray-300 hover:text-white transition-colors">Services</Link>
              </li>
              <li>
                <Link href="#products" className="text-gray-300 hover:text-white transition-colors">Products</Link>
              </li>
              <li>
                <Link href="#contact" className="text-gray-300 hover:text-white transition-colors">Contact</Link>
              </li>
            </ul>
          </div>
          
          {/* Services */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Our Solutions</h3>
            <ul className="space-y-2">
              <li>
                <Link href="#quantum" className="text-gray-300 hover:text-white transition-colors">Quantum Computing</Link>
              </li>
              <li>
                <Link href="#ai" className="text-gray-300 hover:text-white transition-colors">AI Integration</Link>
              </li>
              <li>
                <Link href="#energy" className="text-gray-300 hover:text-white transition-colors">Energy Services</Link>
              </li>
              <li>
                <Link href="#blockchain" className="text-gray-300 hover:text-white transition-colors">Blockchain Solutions</Link>
              </li>
              <li>
                <Link href="#consulting" className="text-gray-300 hover:text-white transition-colors">Business Consulting</Link>
              </li>
            </ul>
          </div>
          
          {/* Contact Info */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Contact Us</h3>
            <ul className="space-y-3">
              <li className="flex items-start space-x-3">
                <MapPin size={20} className="text-blue-400 mt-1 flex-shrink-0" />
                <span className="text-gray-300">123 Quantum Avenue, Innovation District, CA 94103</span>
              </li>
              <li className="flex items-center space-x-3">
                <Phone size={20} className="text-blue-400 flex-shrink-0" />
                <span className="text-gray-300">+1 (555) 123-4567</span>
              </li>
              <li className="flex items-center space-x-3">
                <Mail size={20} className="text-blue-400 flex-shrink-0" />
                <span className="text-gray-300">info@goliath-platform.com</span>
              </li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-gray-700 mt-10 pt-6 flex flex-col md:flex-row justify-between items-center">
          <p className="text-gray-400 text-sm">
  © {currentYear} FLYFOX AI | Goliath of All Trade | Sigma Select. All rights reserved.
</p>
          <div className="mt-4 md:mt-0 flex space-x-6">
            <Link href="/privacy" className="text-gray-400 hover:text-white text-sm transition-colors">Privacy Policy</Link>
            <Link href="/terms" className="text-gray-400 hover:text-white text-sm transition-colors">Terms of Service</Link>
            <Link href="/cookies" className="text-gray-400 hover:text-white text-sm transition-colors">Cookie Policy</Link>
          </div>
        </div>
      </div>
    </MotionFooter>
  );
}