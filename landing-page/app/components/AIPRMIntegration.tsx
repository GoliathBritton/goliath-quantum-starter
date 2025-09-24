'use client';

import React, { useState } from 'react';

// Simplified AIPRM Integration component without external UI dependencies
export default function AIPRMIntegration() {
  const [activeTab, setActiveTab] = useState('templates');
  const [isLoading, setIsLoading] = useState(false);

  // Mock data for development
  const promptTemplates = [
    { id: 1, title: 'Energy Market Analysis', category: 'Energy', description: 'Analyze current energy market trends and provide insights.' },
    { id: 2, title: 'Financial Report Generator', category: 'Finance', description: 'Generate comprehensive financial reports based on provided data.' },
    { id: 3, title: 'Quantum Algorithm Optimizer', category: 'Quantum', description: 'Optimize quantum algorithms for specific use cases.' },
  ];

  const extensions = [
    { id: 1, name: 'Quantum Prompt Enhancer', description: 'Enhances prompts with quantum computing terminology and concepts.', installed: true },
    { id: 2, name: 'Energy Domain Knowledge', description: 'Adds specialized energy sector knowledge to responses.', installed: false },
    { id: 3, name: 'Financial Analysis Tools', description: 'Provides tools for financial data analysis and visualization.', installed: false },
    { id: 4, name: 'Diversegy Integration Extension', description: 'Connects AIPRM with Diversegy energy services.', installed: true },
    { id: 5, name: 'Prompt Library', description: 'Access to a library of pre-built prompts for various domains.', installed: false },
  ];

  const handleInstallExtension = (id: number) => {
    setIsLoading(true);
    // Simulate API call
    setTimeout(() => {
      setIsLoading(false);
      alert(`Extension ${id} installed successfully!`);
    }, 1000);
  };

  const handleExecutePrompt = (id: number) => {
    setIsLoading(true);
    // Simulate API call
    setTimeout(() => {
      setIsLoading(false);
      alert(`Prompt ${id} executed successfully!`);
    }, 1000);
  };

  return (
    <div className="w-full max-w-7xl mx-auto p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-3xl font-bold mb-6 text-center text-gray-800">AIPRM Integration</h2>
      <p className="text-center text-gray-600 mb-8">
        Access AI prompt templates, extensions, and tools to enhance your workflow
      </p>

      {/* Simple Tabs */}
      <div className="flex border-b mb-6">
        <button
          className={`px-4 py-2 font-medium ${activeTab === 'templates' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500'}`}
          onClick={() => setActiveTab('templates')}
        >
          Prompt Templates
        </button>
        <button
          className={`px-4 py-2 font-medium ${activeTab === 'extensions' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500'}`}
          onClick={() => setActiveTab('extensions')}
        >
          Extensions
        </button>
        <button
          className={`px-4 py-2 font-medium ${activeTab === 'playground' ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500'}`}
          onClick={() => setActiveTab('playground')}
        >
          AI Playground
        </button>
      </div>

      {/* Tab Content */}
      <div className="mt-4">
        {activeTab === 'templates' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {promptTemplates.map((template) => (
              <div key={template.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="font-semibold text-lg">{template.title}</h3>
                  <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">{template.category}</span>
                </div>
                <p className="text-gray-600 text-sm mb-4">{template.description}</p>
                <button
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded disabled:opacity-50"
                  onClick={() => handleExecutePrompt(template.id)}
                  disabled={isLoading}
                >
                  {isLoading ? 'Loading...' : 'Use Template'}
                </button>
              </div>
            ))}
          </div>
        )}

        {activeTab === 'extensions' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {extensions.map((extension) => (
              <div key={extension.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                <h3 className="font-semibold text-lg mb-1">{extension.name}</h3>
                <p className="text-gray-600 text-sm mb-4">{extension.description}</p>
                <button
                  className={`w-full py-2 px-4 rounded ${
                    extension.installed
                      ? 'bg-green-100 text-green-800 cursor-default'
                      : 'bg-blue-600 hover:bg-blue-700 text-white'
                  }`}
                  onClick={() => !extension.installed && handleInstallExtension(extension.id)}
                  disabled={extension.installed || isLoading}
                >
                  {isLoading ? 'Installing...' : extension.installed ? 'Installed' : 'Install Extension'}
                </button>
              </div>
            ))}
          </div>
        )}

        {activeTab === 'playground' && (
          <div className="border rounded-lg p-6">
            <h3 className="font-semibold text-xl mb-4">AI Playground</h3>
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">Prompt</label>
              <textarea
                className="w-full border rounded-md p-2 min-h-[150px]"
                placeholder="Enter your prompt here..."
              />
            </div>
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">Model</label>
              <select className="w-full border rounded-md p-2">
                <option>GPT-4</option>
                <option>GPT-3.5 Turbo</option>
                <option>Claude 2</option>
                <option>Quantum-Enhanced LLM</option>
              </select>
            </div>
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">Extensions to Apply</label>
              <div className="space-y-2">
                {extensions.filter(e => e.installed).map((ext) => (
                  <div key={ext.id} className="flex items-center">
                    <input type="checkbox" id={`ext-${ext.id}`} className="mr-2" />
                    <label htmlFor={`ext-${ext.id}`}>{ext.name}</label>
                  </div>
                ))}
              </div>
            </div>
            <button
              className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded disabled:opacity-50"
              disabled={isLoading}
            >
              {isLoading ? 'Processing...' : 'Execute Prompt'}
            </button>
          </div>
        )}
      </div>
      
      <div className="mt-8 text-center">
        <p className="text-sm text-gray-500">
          Powered by <strong>Goliath of All Trade</strong> - Integrating advanced AI capabilities with quantum computing
        </p>
      </div>
    </div>
  );
}