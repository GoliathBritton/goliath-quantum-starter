import React from 'react';
import { motion } from 'framer-motion';
import { Headset, BookOpen, Users } from 'lucide-react';

const ServicesSupport = () => {
  return (
    <div className="bg-gray-100 min-h-screen font-sans">
      <header className="bg-[#003366] text-white p-5 text-center">
        <h1 className="text-3xl font-bold">FLYFOX AI Services & Support</h1>
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
      <main className="max-w-6xl mx-auto p-5 bg-white rounded-lg my-5 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <motion.div className="bg-gray-50 p-4 rounded shadow hover:shadow-lg" initial={{ opacity: 0, y: 50 }} whileInView={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
          <h2 className="text-[#003366] text-2xl font-bold mb-2 flex items-center"><Users className="mr-2" /> Advisory Services</h2>
          <p>Professional advice on integrating advanced computing into your operations.</p>
        </motion.div>
        <motion.div className="bg-gray-50 p-4 rounded shadow hover:shadow-lg" initial={{ opacity: 0, y: 50 }} whileInView={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.1 }}>
          <h2 className="text-[#003366] text-2xl font-bold mb-2 flex items-center"><Headset className="mr-2" /> Customer Assistance</h2>
          <p>Round-the-clock help for all FLYFOX AI offerings.</p>
        </motion.div>
        <motion.div className="bg-gray-50 p-4 rounded shadow hover:shadow-lg" initial={{ opacity: 0, y: 50 }} whileInView={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.2 }}>
          <h2 className="text-[#003366] text-2xl font-bold mb-2 flex items-center"><BookOpen className="mr-2" /> Educational Workshops</h2>
          <p>In-depth sessions on FLYFOX AI tools and neuromorphic principles.</p>
        </motion.div>
        {/* Add more service cards as needed */}
      </main>
      <footer className="bg-[#003366] text-white text-center p-2.5 fixed bottom-0 w-full">
        <p>&copy; 2023 FLYFOX AI. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default ServicesSupport;