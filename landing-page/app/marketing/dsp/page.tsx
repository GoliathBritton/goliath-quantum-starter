'use client';

import React from 'react';
import { motion } from 'framer-motion';

// Placeholder for MiQ DSP integration
const MiQIntegration = () => (
  <section>
    <h2>MiQ Demand-Side Platform</h2>
    <p>Seamlessly integrated DSP solutions for advanced marketing campaigns.</p>
    {/* Add API calls or embeds here */}
  </section>
);

// Placeholder for Celonis-like process mining
const ProcessMining = () => (
  <section className="my-8">
    <h2 className="text-2xl font-bold mb-4">Process Mining & Analytics (Inspired by Celonis)</h2>
    <p className="mb-4">Our platform incorporates advanced process mining capabilities similar to Celonis, enabling you to analyze and optimize business processes with AI-powered insights.</p>
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div className="border p-4 rounded-lg">
        <h3 className="text-xl font-semibold mb-2">Process Intelligence API</h3>
        <p>Generate custom API endpoints for insights, test connections, and integrate seamlessly with your systems.</p>
      </div>
      <div className="border p-4 rounded-lg">
        <h3 className="text-xl font-semibold mb-2">Task Mining</h3>
        <p>Capture and process task data, apply labels, and analyze workflows to identify optimization opportunities.</p>
      </div>
    </div>
    {/* Mock API integration placeholder */}
    <button className="mt-4 bg-blue-500 text-white px-4 py-2 rounded">Test API Connection</button>
  </section>
);

// Placeholder for n8n/UiPath compatibility
const AutomationCompatibility = () => (
  <section className="my-8">
    <h2 className="text-2xl font-bold mb-4">Automation Integration</h2>
    <p className="mb-4">Our platform ensures seamless compatibility with n8n.io for workflow automation and UiPath for robotic process automation, allowing easy integration via APIs.</p>
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div className="border p-4 rounded-lg">
        <h3 className="text-xl font-semibold mb-2">n8n.io Compatibility</h3>
        <p>Use n8n's nodes to connect to our APIs for automating workflows across services.</p>
      </div>
      <div className="border p-4 rounded-lg">
        <h3 className="text-xl font-semibold mb-2">UiPath Integration</h3>
        <p>Leverage UiPath Orchestrator and APIs to incorporate RPA into your processes.</p>
      </div>
    </div>
    <a href="https://docs.n8n.io/" target="_blank" rel="noopener noreferrer" className="mt-4 inline-block bg-blue-500 text-white px-4 py-2 rounded">n8n Documentation</a>
    <a href="https://docs.uipath.com/" target="_blank" rel="noopener noreferrer" className="mt-4 ml-4 inline-block bg-green-500 text-white px-4 py-2 rounded">UiPath Documentation</a>
  </section>
);

// Placeholder for Dynex SDK
const DynexIntegration = () => (
  <section className="my-8">
    <h2 className="text-2xl font-bold mb-4">Dynex Quantum Integration</h2>
    <p className="mb-4">Our platform integrates with the Dynex neuromorphic quantum computing SDK for solving complex problems at scale using quantum annealing and gate-based circuits.</p>
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div className="border p-4 rounded-lg">
        <h3 className="text-xl font-semibold mb-2">Dynex SDK</h3>
        <p>Install via pip: pip install dynex. Supports Qiskit, Cirq, and more for seamless quantum computing integration.</p>
      </div>
      <div className="border p-4 rounded-lg">
        <h3 className="text-xl font-semibold mb-2">Dynex Wiki & Guides</h3>
        <p>Access comprehensive documentation, tutorials, and examples for implementing quantum algorithms.</p>
      </div>
    </div>
    <a href="https://github.com/dynexcoin/DynexSDK" target="_blank" rel="noopener noreferrer" className="mt-4 inline-block bg-blue-500 text-white px-4 py-2 rounded">Visit Dynex SDK GitHub</a>
    <a href="https://github.com/dynexcoin/DynexSDK/wiki" target="_blank" rel="noopener noreferrer" className="mt-4 ml-4 inline-block bg-green-500 text-white px-4 py-2 rounded">Dynex SDK Wiki</a>
  </section>
);

// Implementation Options
const ImplementationOptions = () => (
  <section className="my-8">
    <motion.h2 
      className="text-2xl font-bold mb-4"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      Implementation Options
    </motion.h2>
    <motion.p 
      className="mb-4"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.2 }}
    >
      Choose the approach that fits your technical expertise for integrating these solutions into the NQBA platform:
    </motion.p>
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <motion.div 
        className="border p-4 rounded-lg"
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5, delay: 0.4 }}
        whileHover={{ scale: 1.05 }}
      >
        <h3 className="text-xl font-semibold mb-2">No-Code</h3>
        <p>Use visual builders like n8n.io workflows or UiPath Studio's drag-and-drop interface to configure integrations without writing code. Connect via pre-built nodes and our platform's APIs.</p>
      </motion.div>
      <motion.div 
        className="border p-4 rounded-lg"
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5, delay: 0.6 }}
        whileHover={{ scale: 1.05 }}
      >
        <h3 className="text-xl font-semibold mb-2">Low-Code</h3>
        <p>Customize templates in Framer or similar tools, add minimal scripts for API calls (e.g., to Dynex SDK or Celonis-like analytics), and deploy with guided setups.</p>
      </motion.div>
      <motion.div 
        className="border p-4 rounded-lg"
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5, delay: 0.8 }}
        whileHover={{ scale: 1.05 }}
      >
        <h3 className="text-xl font-semibold mb-2">Full-Code</h3>
        <p>Directly code integrations using SDKs (e.g., pip install dynex), API endpoints, and frameworks like React for UI, with full access to source code for advanced customizations.</p>
      </motion.div>
    </div>
  </section>
);

const DSPPage = () => {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="container mx-auto px-4 py-8"
    >
      <h1 className="text-4xl font-bold mb-8">Integrated DSP Solutions</h1>
      <MiQIntegration />
      <ProcessMining />
      <AutomationCompatibility />
      <DynexIntegration />
      <ImplementationOptions />
    </motion.div>
  );
};

export default DSPPage;