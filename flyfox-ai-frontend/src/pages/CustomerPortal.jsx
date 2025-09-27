import React from 'react';
import { motion } from 'framer-motion';
import { User, LayoutDashboard } from 'lucide-react';

const CustomerPortal = () => {
  return (
    <div className="bg-gray-100 min-h-screen font-sans">
      <header className="bg-[#003366] text-white p-5 text-center">
        <h1 className="text-3xl font-bold">FLYFOX AI Customer Portal</h1>
      </header>
      <nav className="bg-[#004488] p-2.5 text-center">
        <a href="/" className="text-white mx-3.5 no-underline">Home</a>
        <a href="/solutions" className="text-white mx-3.5 no-underline">Solutions</a>
        <a href="/products" className="text-white mx-3.5 no-underline">Products</a>
        <a href="/services" className="text-white mx-3.5 no-underline">Services & Support</a>
        <a href="/resources" className="text-white mx-3.5 no-underline">Resources</a>
        <a href="/contact" className="text-white mx-3.5 no-underline">Contact</a>
        <a href="/company" className="text-white mx-3.5 no-underline">Company</a>
        <a href="/blog" className="text-white mx-3.5 no-underline">Blog</a>
        <a href="/customer-portal" className="text-white mx-3.5 no-underline">Customer Portal</a>
      </nav>
      <main className="max-w-6xl mx-auto p-5 bg-white rounded-lg my-5 flex flex-col md:flex-row gap-6">
        <motion.div className="flex-1 bg-gray-50 p-4 rounded shadow hover:shadow-lg" initial={{ opacity: 0, x: -50 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.5 }}>
          <h2 className="text-[#003366] text-2xl font-bold mb-4 flex items-center"><User className="mr-2" /> Account Access</h2>
          <form className="space-y-4">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">Email</label>
              <input id="email" type="email" placeholder="Your Email" required className="block w-full p-2.5 border border-gray-300 rounded mt-1" />
            </div>
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700">Password</label>
              <input id="password" type="password" placeholder="Your Password" required className="block w-full p-2.5 border border-gray-300 rounded mt-1" />
            </div>
            <motion.button 
              type="submit" 
              className="bg-[#003366] text-white p-2.5 w-full rounded cursor-pointer hover:bg-blue-800 transition-colors" 
              whileHover={{ scale: 1.02 }} 
              whileTap={{ scale: 0.98 }}
            >
              Sign In
            </motion.button>
          </form>
        </motion.div>
        <motion.div className="flex-1 bg-gray-50 p-4 rounded shadow hover:shadow-lg" initial={{ opacity: 0, x: 50 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.5, delay: 0.2 }}>
          <h2 className="text-[#003366] text-2xl font-bold mb-4 flex items-center"><LayoutDashboard className="mr-2" /> Control Panel Summary</h2>
          <p>Manage your quantum resources, monitor usage, and handle FLYFOX AI SDK plans.</p>
        </motion.div>
      </main>
      <footer className="bg-[#003366] text-white text-center p-2.5 fixed bottom-0 w-full">
        <p>&copy; 2023 FLYFOX AI. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default CustomerPortal;