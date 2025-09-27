import React from 'react';
import { motion } from 'framer-motion';
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import { Cpu, Cloud, Server } from 'lucide-react';

const Products = () => {
  return (
    <div className="bg-gray-100 min-h-screen font-sans">
      <header className="bg-[#003366] text-white p-5 text-center">
        <h1 className="text-3xl font-bold">FLYFOX AI Products</h1>
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
      <main className="max-w-6xl mx-auto p-5 bg-white rounded-lg my-5">
        {/* Product Slider */}
        <Slider dots={true} infinite={true} speed={500} slidesToShow={1} slidesToScroll={1} className="mb-8">
          <div className="p-4">
            <h3 className="text-2xl font-bold mb-2">Featured: FLYFOX AI Development Kit</h3>
            <p>Core toolkit for neuromorphic computing.</p>
            {/* Placeholder for image */}
            <div className="bg-gray-200 h-48 flex items-center justify-center">Image Placeholder</div>
          </div>
          <div className="p-4">
            <h3 className="text-2xl font-bold mb-2">Featured: FLYFOX AI Cloud Services</h3>
            <p>Flexible cloud infrastructure.</p>
            <div className="bg-gray-200 h-48 flex items-center justify-center">Image Placeholder</div>
          </div>
          <div className="p-4">
            <h3 className="text-2xl font-bold mb-2">Featured: FLYFOX AI On-Premise Hardware</h3>
            <p>Dedicated local devices.</p>
            <div className="bg-gray-200 h-48 flex items-center justify-center">Image Placeholder</div>
          </div>
        </Slider>
        {/* Product Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <motion.div className="bg-gray-50 p-4 rounded shadow hover:shadow-lg" initial={{ opacity: 0, y: 50 }} whileInView={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
            <h2 className="text-[#003366] text-2xl font-bold mb-2 flex items-center"><Cpu className="mr-2" /> FLYFOX AI Development Kit</h2>
            <p>The core toolkit for harnessing advanced neuromorphic computing power. Includes SDK, APIs, and development tools.</p>
          </motion.div>
          <motion.div className="bg-gray-50 p-4 rounded shadow hover:shadow-lg" initial={{ opacity: 0, y: 50 }} whileInView={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.1 }}>
            <h2 className="text-[#003366] text-2xl font-bold mb-2 flex items-center"><Cloud className="mr-2" /> FLYFOX AI Cloud Services</h2>
            <p>Flexible cloud infrastructure for FLYFOX AI quantum resources. Scalable and secure.</p>
          </motion.div>
          <motion.div className="bg-gray-50 p-4 rounded shadow hover:shadow-lg" initial={{ opacity: 0, y: 50 }} whileInView={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.2 }}>
            <h2 className="text-[#003366] text-2xl font-bold mb-2 flex items-center"><Server className="mr-2" /> FLYFOX AI On-Premise Hardware</h2>
            <p>Dedicated devices for local quantum acceleration. High-performance and reliable.</p>
          </motion.div>
        </div>
      </main>
      <footer className="bg-[#003366] text-white text-center p-2.5 fixed bottom-0 w-full">
        <p>&copy; 2023 FLYFOX AI. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default Products;