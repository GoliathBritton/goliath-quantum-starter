'use client';

import React from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { Mail, Phone, MapPin, Facebook, Twitter, Linkedin, Instagram, Github } from 'lucide-react';

const MotionFooter = motion.footer as any;
const FacebookIcon = Facebook as any;
const TwitterIcon = Twitter as any;
const LinkedinIcon = Linkedin as any;
const InstagramIcon = Instagram as any;
const GithubIcon = Github as any;
const MapPinIcon = MapPin as any;
const PhoneIcon = Phone as any;
const MailIcon = Mail as any;
const NextLink = Link as any;

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
                <FacebookIcon size={20} aria-hidden="true" />
              </a>
              <a href="#" aria-label="Twitter" className="text-gray-400 hover:text-white transition-colors">
                <TwitterIcon size={20} aria-hidden="true" />
              </a>
              <a href="#" aria-label="LinkedIn" className="text-gray-400 hover:text-white transition-colors">
                <LinkedinIcon size={20} aria-hidden="true" />
              </a>
              <a href="#" aria-label="Instagram" className="text-gray-400 hover:text-white transition-colors">
                <InstagramIcon size={20} aria-hidden="true" />
              </a>
              <a href="#" aria-label="GitHub" className="text-gray-400 hover:text-white transition-colors">
                <GithubIcon size={20} aria-hidden="true" />
              </a>
            </div>
          </div>
          
          {/* Quick Links */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <NextLink href="/" className="text-gray-300 hover:text-white transition-colors">Home</NextLink>
              </li>
              <li>
                <NextLink href="#about" className="text-gray-300 hover:text-white transition-colors">About Us</NextLink>
              </li>
              <li>
                <NextLink href="#services" className="text-gray-300 hover:text-white transition-colors">Services</NextLink>
              </li>
              <li>
                <NextLink href="#products" className="text-gray-300 hover:text-white transition-colors">Products</NextLink>
              </li>
              <li>
                <NextLink href="#contact" className="text-gray-300 hover:text-white transition-colors">Contact</NextLink>
              </li>
            </ul>
          </div>
          
          {/* Services */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Our Solutions</h3>
            <ul className="space-y-2">
              <li>
                <NextLink href="#quantum" className="text-gray-300 hover:text-white transition-colors">Quantum Computing</NextLink>
              </li>
              <li>
                <NextLink href="#ai" className="text-gray-300 hover:text-white transition-colors">AI Integration</NextLink>
              </li>
              <li>
                <NextLink href="#energy" className="text-gray-300 hover:text-white transition-colors">Energy Services</NextLink>
              </li>
              <li>
                <NextLink href="#blockchain" className="text-gray-300 hover:text-white transition-colors">Blockchain Solutions</NextLink>
              </li>
              <li>
                <NextLink href="#consulting" className="text-gray-300 hover:text-white transition-colors">Business Consulting</NextLink>
              </li>
            </ul>
          </div>
          
          {/* Contact Info */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Contact Us</h3>
            <ul className="space-y-3">
              <li className="flex items-start space-x-3">
                <MapPinIcon size={20} className="text-blue-400 mt-1 flex-shrink-0" />
                <span className="text-gray-300">123 Quantum Avenue, Innovation District, CA 94103</span>
              </li>
              <li className="flex items-center space-x-3">
                <PhoneIcon size={20} className="text-blue-400 flex-shrink-0" />
                <span className="text-gray-300">+1 (555) 123-4567</span>
              </li>
              <li className="flex items-center space-x-3">
                <MailIcon size={20} className="text-blue-400 flex-shrink-0" />
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
            <NextLink href="/privacy" className="text-gray-400 hover:text-white text-sm transition-colors">Privacy Policy</NextLink>
            <NextLink href="/terms" className="text-gray-400 hover:text-white text-sm transition-colors">Terms of Service</NextLink>
            <NextLink href="/cookies" className="text-gray-400 hover:text-white text-sm transition-colors">Cookie Policy</NextLink>
          </div>
        </div>
      </div>
    </MotionFooter>
  );
}