import Link from "next/link";

export default function Footer() {
  return (
    <footer className="bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-12">
          {/* Company Info */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-3 mb-6">
              <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center">
                <span className="text-white font-bold text-xl">🦊</span>
              </div>
              <div>
                <h3 className="text-2xl font-bold text-white">FLYFOX AI</h3>
                <p className="text-sm text-gray-400">Powered by NQBA</p>
              </div>
            </div>
            <p className="text-gray-300 mb-6 max-w-md leading-relaxed">
              The world's first neuromorphic quantum business architecture platform. 
              Transform your business with 410x performance boost and autonomous AI agents.
            </p>
            <div className="flex flex-wrap gap-4">
              <div className="flex items-center space-x-2 text-sm text-gray-400">
                <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                <span>Quantum Powered by Dynex</span>
              </div>
              <div className="flex items-center space-x-2 text-sm text-gray-400">
                <div className="w-2 h-2 bg-blue-400 rounded-full"></div>
                <span>NQBA Architecture</span>
              </div>
            </div>
          </div>

          {/* Platform Links */}
          <div>
            <h4 className="text-lg font-semibold mb-6 text-white">Platform</h4>
            <ul className="space-y-3">
              <li><Link href="/platform/jobs" className="text-gray-400 hover:text-white transition-colors duration-200">Quantum Jobs</Link></li>
              <li><Link href="/platform/agents" className="text-gray-400 hover:text-white transition-colors duration-200">AI Agents</Link></li>
              <li><Link href="/platform/pipelines" className="text-gray-400 hover:text-white transition-colors duration-200">Pipelines</Link></li>
              <li><Link href="/monitoring" className="text-gray-400 hover:text-white transition-colors duration-200">Monitoring</Link></li>
            </ul>
          </div>

          {/* Company Links */}
          <div>
            <h4 className="text-lg font-semibold mb-6 text-white">Company</h4>
            <ul className="space-y-3">
              <li><Link href="/company" className="text-gray-400 hover:text-white transition-colors duration-200">About Us</Link></li>
              <li><Link href="/docs" className="text-gray-400 hover:text-white transition-colors duration-200">Documentation</Link></li>
              <li><Link href="/contact" className="text-gray-400 hover:text-white transition-colors duration-200">Contact</Link></li>
              <li><Link href="/platform" className="text-gray-400 hover:text-white transition-colors duration-200">Get Started</Link></li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-gray-800 mt-12 pt-8 flex flex-col md:flex-row justify-between items-center">
          <div className="text-gray-400 text-sm">
            © 2025 FLYFOX AI. All rights reserved. Built with quantum computing and AI.
          </div>
          <div className="flex flex-wrap gap-6 mt-4 md:mt-0">
            <span className="text-gray-400 text-sm hover:text-white transition-colors cursor-pointer">NQBA Architecture</span>
            <span className="text-gray-400 text-sm hover:text-white transition-colors cursor-pointer">Quantum Computing</span>
            <span className="text-gray-400 text-sm hover:text-white transition-colors cursor-pointer">AI Automation</span>
            <span className="text-gray-400 text-sm hover:text-white transition-colors cursor-pointer">Web3 Integration</span>
          </div>
        </div>
      </div>
    </footer>
  );
}