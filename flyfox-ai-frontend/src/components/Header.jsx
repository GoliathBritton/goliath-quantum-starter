import React from 'react';
import { ArrowRight } from 'lucide-react';

const Header = () => {
  return (
    <header className="bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <div className="flex items-center">
            <img src="/flyfox-logo.svg" alt="Fly Fox AI Logo" className="h-8 mr-2" />
            <span className="text-2xl font-bold text-dark-blue">FLYFOX AI</span>
          </div>

          {/* Primary Navigation */}
          <nav className="hidden lg:flex items-center space-x-8">
            <a href="/solutions" className="text-dark-blue hover:text-gold font-medium">Solutions</a>
            <a href="/products" className="text-dark-blue hover:text-gold font-medium">Products</a>
            <a href="/services" className="text-dark-blue hover:text-gold font-medium">Services & Support</a>
            <a href="/resources" className="text-dark-blue hover:text-gold font-medium">Resources</a>
            <a href="/contact" className="text-dark-blue hover:text-gold font-medium">Contact</a>
            <a href="/company" className="text-dark-blue hover:text-gold font-medium">Company</a>
            <a href="/blog" className="text-dark-blue hover:text-gold font-medium">Blog</a>
            <a href="/customer-portal" className="text-dark-blue hover:text-gold font-medium">Customer Portal</a>
          </nav>

          {/* CTA Button */}
          <button className="bg-dark-blue text-white px-6 py-2 rounded-lg font-semibold hover:bg-gold flex items-center">
            Start your trial
            <ArrowRight className="w-4 h-4 ml-2" />
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;