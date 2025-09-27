import React from 'react';
import { motion } from 'framer-motion';
import { Target, History, Users } from 'lucide-react';

const Company = () => {
  return (
    <div className="bg-gray-100 min-h-screen font-sans">
      <header className="bg-[#003366] text-white p-5 text-center">
        <h1 className="text-3xl font-bold">About FLYFOX AI</h1>
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
          <h2 className="text-[#003366] text-2xl font-bold mb-2 flex items-center"><Target className="mr-2" /> Our Vision</h2>
          <p>Transforming technology through innovative neuromorphic quantum solutions for global challenges.</p>
        </motion.div>
        <motion.div className="bg-gray-50 p-4 rounded shadow hover:shadow-lg" initial={{ opacity: 0, y: 50 }} whileInView={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.1 }}>
          <h2 className="text-[#003366] text-2xl font-bold mb-2 flex items-center"><History className="mr-2" /> Our Journey</h2>
          <p>Established in 2015, leading advancements in quantum computing.</p>
        </motion.div>
        <motion.div className="bg-gray-50 p-4 rounded shadow hover:shadow-lg" initial={{ opacity: 0, y: 50 }} whileInView={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.2 }}>
          <h2 className="text-[#003366] text-2xl font-bold mb-2 flex items-center"><Users className="mr-2" /> Our Experts</h2>
          <p>A team of specialists in quantum sciences, computing, and engineering.</p>
        </motion.div>
        {/* Add more company cards as needed */}
      </main>
      <footer className="bg-[#003366] text-white text-center p-2.5 fixed bottom-0 w-full">
        <p>&copy; 2023 FLYFOX AI. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default Company;