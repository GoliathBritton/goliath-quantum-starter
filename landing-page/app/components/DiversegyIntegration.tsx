'use client';

import React, { useState } from 'react';
import Image from 'next/image';

const DiversegyIntegration = () => {
  const [activeTab, setActiveTab] = useState('plans');

  return (
    <section className="w-full py-12 md:py-24 bg-gradient-to-b from-slate-950 to-slate-900">
      <div className="container px-4 md:px-6 mx-auto">
        <div className="flex flex-col items-center text-center space-y-4">
          <div className="inline-block rounded-lg bg-slate-800/30 px-3 py-1 text-sm backdrop-blur-md border border-slate-700/30">
            <span className="text-emerald-400 font-medium">Goliath of All Trade</span> × Diversegy
          </div>
          
          <h2 className="text-3xl md:text-5xl font-bold tracking-tighter text-white">
            Energy Solutions <span className="bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent">Powered by Quantum</span>
          </h2>
          
          <p className="max-w-[700px] text-slate-400 md:text-xl/relaxed">
            Leverage our partnership with Diversegy to provide your clients with optimized energy plans and renewable options, all enhanced by our quantum algorithms.
          </p>
        </div>

        <div className="mt-12 grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          <div className="flex flex-col p-6 bg-slate-800/30 backdrop-blur-md rounded-xl border border-slate-700/30 hover:border-emerald-500/50 transition-all">
            <div className="rounded-lg p-2 bg-emerald-500/10 w-10 h-10 flex items-center justify-center mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-emerald-400">
                <path d="M12 2v8"></path>
                <path d="m4.93 10.93 1.41 1.41"></path>
                <path d="M2 18h2"></path>
                <path d="M20 18h2"></path>
                <path d="m19.07 10.93-1.41 1.41"></path>
                <path d="M22 22H2"></path>
                <path d="m8 6 4-4 4 4"></path>
                <path d="M16 18a4 4 0 0 0-8 0"></path>
              </svg>
            </div>
            <h3 className="text-xl font-bold text-white mb-2">Renewable Energy Plans</h3>
            <p className="text-slate-400 flex-1">Access 100% renewable energy options for your clients with competitive rates and flexible terms.</p>
            <button className="mt-4 inline-flex items-center justify-center rounded-md bg-emerald-600 px-4 py-2 text-sm font-medium text-white shadow transition-colors hover:bg-emerald-700 focus-visible:outline-none focus-visible:ring-1">
              Explore Plans
            </button>
          </div>

          <div className="flex flex-col p-6 bg-slate-800/30 backdrop-blur-md rounded-xl border border-slate-700/30 hover:border-emerald-500/50 transition-all">
            <div className="rounded-lg p-2 bg-emerald-500/10 w-10 h-10 flex items-center justify-center mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-emerald-400">
                <path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"></path>
                <path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"></path>
                <path d="M4 22h16"></path>
                <path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"></path>
                <path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"></path>
                <path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"></path>
              </svg>
            </div>
            <h3 className="text-xl font-bold text-white mb-2">Quantum-Optimized Pricing</h3>
            <p className="text-slate-400 flex-1">Our quantum algorithms analyze thousands of rate factors to find the best energy pricing for your clients.</p>
            <button className="mt-4 inline-flex items-center justify-center rounded-md bg-emerald-600 px-4 py-2 text-sm font-medium text-white shadow transition-colors hover:bg-emerald-700 focus-visible:outline-none focus-visible:ring-1">
              Get Quote
            </button>
          </div>

          <div className="flex flex-col p-6 bg-slate-800/30 backdrop-blur-md rounded-xl border border-slate-700/30 hover:border-emerald-500/50 transition-all">
            <div className="rounded-lg p-2 bg-emerald-500/10 w-10 h-10 flex items-center justify-center mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-emerald-400">
                <path d="M12 3v19"></path>
                <path d="M5 8h14"></path>
                <path d="M15 5h-3"></path>
                <path d="M18 11h-6"></path>
                <path d="M9 11h3"></path>
                <path d="M15 14h-3"></path>
                <path d="M9 17h6"></path>
              </svg>
            </div>
            <h3 className="text-xl font-bold text-white mb-2">Partner Commission</h3>
            <p className="text-slate-400 flex-1">Earn competitive commissions on every client enrollment through our Diversegy partnership.</p>
            <button className="mt-4 inline-flex items-center justify-center rounded-md bg-emerald-600 px-4 py-2 text-sm font-medium text-white shadow transition-colors hover:bg-emerald-700 focus-visible:outline-none focus-visible:ring-1">
              Partner Portal
            </button>
          </div>
        </div>

        <div className="mt-16 flex flex-col items-center justify-center space-y-4">
          <div className="flex items-center space-x-2">
            <div className="h-1 w-1 rounded-full bg-emerald-500"></div>
            <div className="h-1 w-1 rounded-full bg-emerald-500"></div>
            <div className="h-1 w-12 rounded-full bg-emerald-500"></div>
            <div className="h-1 w-1 rounded-full bg-emerald-500"></div>
            <div className="h-1 w-1 rounded-full bg-emerald-500"></div>
          </div>
          
          <div className="flex flex-col md:flex-row items-center justify-center space-y-4 md:space-y-0 md:space-x-4">
            <div className="flex items-center space-x-2">
              <div className="w-6 h-6 rounded-full bg-emerald-500/20 flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-emerald-400">
                  <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
              </div>
              <span className="text-sm text-slate-400">Quantum-Enhanced</span>
            </div>
            
            <div className="flex items-center space-x-2">
              <div className="w-6 h-6 rounded-full bg-emerald-500/20 flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-emerald-400">
                  <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
              </div>
              <span className="text-sm text-slate-400">Goliath of All Trade Branded</span>
            </div>
            
            <div className="flex items-center space-x-2">
              <div className="w-6 h-6 rounded-full bg-emerald-500/20 flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-emerald-400">
                  <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
              </div>
              <span className="text-sm text-slate-400">Diversegy Integrated</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default DiversegyIntegration;