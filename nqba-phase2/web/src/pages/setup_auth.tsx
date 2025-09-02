import { useState, useEffect } from "react";
import Link from "next/link";
import Header from "../components/Header";
import Footer from "../components/Footer";

export default function SetupAuth() {
  const [currentStep, setCurrentStep] = useState(1);
  const [authConfig, setAuthConfig] = useState({
    platformAdmin: {
      username: "",
      email: "",
      password: "",
      confirmPassword: ""
    },
    businessUnits: {
      flyfox: { enabled: true, admin: "", email: "" },
      goliath: { enabled: true, admin: "", email: "" },
      sigma: { enabled: true, admin: "", email: "" }
    },
    security: {
      mfa: true,
      sso: false,
      encryption: "AES-256",
      sessionTimeout: 24
    },
    integration: {
      nqba: true,
      quantum: true,
      ai: true
    }
  });

  const [setupProgress, setSetupProgress] = useState(0);
  const [isConfiguring, setIsConfiguring] = useState(false);
  const [configComplete, setConfigComplete] = useState(false);

  const authSteps = [
    {
      id: 1,
      title: "Platform Administrator",
      description: "Create the main NQBA platform administrator account",
      icon: "👑",
      status: "active"
    },
    {
      id: 2,
      title: "Business Unit Access",
      description: "Configure access for each business unit",
      icon: "🏢",
      status: "pending"
    },
    {
      id: 3,
      title: "Security Configuration",
      description: "Set up security policies and authentication methods",
      icon: "🔒",
      status: "pending"
    },
    {
      id: 4,
      title: "NQBA Integration",
      description: "Connect all systems to the unified NQBA core",
      icon: "🔗",
      status: "pending"
    }
  ];

  const handleInputChange = (section: string, field: string, value: any) => {
    setAuthConfig(prev => ({
      ...prev,
      [section]: {
        ...prev[section as keyof typeof prev],
        [field]: value
      }
    }));
  };

  const handleBusinessUnitChange = (unit: string, field: string, value: any) => {
    setAuthConfig(prev => ({
      ...prev,
      businessUnits: {
        ...prev.businessUnits,
        [unit]: {
          ...prev.businessUnits[unit as keyof typeof prev.businessUnits],
          [field]: value
        }
      }
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsConfiguring(true);
    
    // Simulate configuration process
    for (let i = 0; i <= 100; i += 10) {
      setSetupProgress(i);
      await new Promise(resolve => setTimeout(resolve, 200));
    }
    
    setIsConfiguring(false);
    setConfigComplete(true);
  };

  const validateForm = () => {
    const { platformAdmin } = authConfig;
    return (
      platformAdmin.username &&
      platformAdmin.email &&
      platformAdmin.password &&
      platformAdmin.password === platformAdmin.confirmPassword &&
      platformAdmin.password.length >= 8
    );
  };

  return (
    <>
      <Header />

      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-flyfox-950 via-goliath-950 to-goliathNavy-950 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h1 className="text-5xl md:text-6xl font-bold mb-6">
              NQBA Authentication Setup
            </h1>
            <p className="text-xl md:text-2xl text-gray-300 max-w-4xl mx-auto leading-relaxed">
              Configure unified authentication and access control across the entire NQBA ecosystem.
              Powered by FLYFOX AI - Secure, scalable, and quantum-enhanced.
            </p>
          </div>
        </div>
      </section>

      {/* Setup Progress */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Authentication Setup Progress</h2>
            <p className="text-xl text-gray-600">Step-by-step configuration of the unified NQBA authentication system</p>
          </div>

          <div className="space-y-6">
            {authSteps.map((step) => (
              <div key={step.id} className="bg-gray-50 rounded-2xl p-6 border border-gray-200">
                <div className="flex items-center space-x-6">
                  <div className="flex-shrink-0">
                    <div className={`w-16 h-16 rounded-2xl flex items-center justify-center text-2xl ${
                      step.status === 'active' 
                        ? 'bg-gradient-to-br from-indigo-500 to-purple-500 text-white animate-pulse'
                        : step.status === 'completed'
                        ? 'bg-gradient-to-br from-green-500 to-emerald-500 text-white'
                        : 'bg-gray-300 text-gray-600'
                    }`}>
                      {step.icon}
                    </div>
                  </div>
                  
                  <div className="flex-1">
                    <h3 className="text-xl font-bold text-gray-900 mb-2">{step.title}</h3>
                    <p className="text-gray-600">{step.description}</p>
                  </div>
                  
                  <div className="flex-shrink-0">
                    <span className={`px-4 py-2 rounded-full text-sm font-semibold ${
                      step.status === 'active'
                        ? 'bg-indigo-100 text-indigo-800'
                        : step.status === 'completed'
                        ? 'bg-green-100 text-green-800'
                        : 'bg-gray-100 text-gray-600'
                    }`}>
                      {step.status === 'active' ? 'In Progress' : 
                       step.status === 'completed' ? 'Completed' : 'Pending'}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Configuration Form */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          {configComplete ? (
            <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200 text-center">
              <div className="text-6xl mb-6">✅</div>
              <h2 className="text-3xl font-bold text-gray-900 mb-4">Authentication Setup Complete!</h2>
              <p className="text-xl text-gray-600 mb-8">
                Your NQBA authentication system has been successfully configured.
                All business units are now connected to the unified security framework.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link href="/platform-dashboard" className="bg-gradient-to-r from-flyfoxSilver-600 to-goliathNavy-600 text-white px-8 py-4 rounded-xl font-semibold hover:from-flyfoxSilver-700 hover:to-goliathNavy-700 transition-all">
                  Access Platform Dashboard
                </Link>
                <Link href="/setup" className="bg-gray-600 text-white px-8 py-4 rounded-xl font-semibold hover:bg-gray-700 transition-all">
                  Continue Setup
                </Link>
              </div>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200">
              <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">Configure NQBA Authentication</h2>
              
              {/* Platform Administrator */}
              <div className="mb-8">
                <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
                  <span className="mr-3">👑</span>
                  Platform Administrator
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Username *</label>
                    <input
                      type="text"
                      required
                      value={authConfig.platformAdmin.username}
                      onChange={(e) => handleInputChange('platformAdmin', 'username', e.target.value)}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                      placeholder="Enter admin username"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Email *</label>
                    <input
                      type="email"
                      required
                      value={authConfig.platformAdmin.email}
                      onChange={(e) => handleInputChange('platformAdmin', 'email', e.target.value)}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                      placeholder="Enter admin email"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Password *</label>
                    <input
                      type="password"
                      required
                      value={authConfig.platformAdmin.password}
                      onChange={(e) => handleInputChange('platformAdmin', 'password', e.target.value)}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                      placeholder="Enter password (min 8 characters)"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Confirm Password *</label>
                    <input
                      type="password"
                      required
                      value={authConfig.platformAdmin.confirmPassword}
                      onChange={(e) => handleInputChange('platformAdmin', 'confirmPassword', e.target.value)}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                      placeholder="Confirm password"
                    />
                  </div>
                </div>
              </div>

              {/* Business Unit Access */}
              <div className="mb-8">
                <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
                  <span className="mr-3">🏢</span>
                  Business Unit Access
                </h3>
                <div className="space-y-4">
                  {Object.entries(authConfig.businessUnits).map(([unit, config]) => (
                    <div key={unit} className="flex items-center space-x-4 p-4 bg-gray-50 rounded-lg">
                      <input
                        type="checkbox"
                        checked={config.enabled}
                        onChange={(e) => handleBusinessUnitChange(unit, 'enabled', e.target.checked)}
                        className="w-5 h-5 text-indigo-600 rounded focus:ring-indigo-500"
                      />
                      <div className="flex-1">
                        <label className="text-sm font-medium text-gray-900 capitalize">{unit} Select</label>
                        <p className="text-xs text-gray-600">Enable access to this business unit</p>
                      </div>
                      {config.enabled && (
                        <div className="flex space-x-2">
                          <input
                            type="text"
                            placeholder="Admin username"
                            value={config.admin}
                            onChange={(e) => handleBusinessUnitChange(unit, 'admin', e.target.value)}
                            className="px-3 py-2 border border-gray-300 rounded text-sm focus:ring-2 focus:ring-indigo-500"
                          />
                          <input
                            type="email"
                            placeholder="Admin email"
                            value={config.email}
                            onChange={(e) => handleBusinessUnitChange(unit, 'email', e.target.value)}
                            className="px-3 py-2 border border-gray-300 rounded text-sm focus:ring-2 focus:ring-indigo-500"
                          />
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>

              {/* Security Configuration */}
              <div className="mb-8">
                <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
                  <span className="mr-3">🔒</span>
                  Security Configuration
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Multi-Factor Authentication</label>
                    <select
                      value={authConfig.security.mfa ? "enabled" : "disabled"}
                      onChange={(e) => handleInputChange('security', 'mfa', e.target.value === "enabled")}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                    >
                      <option value="enabled">Enabled</option>
                      <option value="disabled">Disabled</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Encryption Level</label>
                    <select
                      value={authConfig.security.encryption}
                      onChange={(e) => handleInputChange('security', 'encryption', e.target.value)}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                    >
                      <option value="AES-256">AES-256 (Recommended)</option>
                      <option value="AES-192">AES-192</option>
                      <option value="AES-128">AES-128</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Session Timeout (hours)</label>
                    <input
                      type="number"
                      min="1"
                      max="168"
                      value={authConfig.security.sessionTimeout}
                      onChange={(e) => handleInputChange('security', 'sessionTimeout', parseInt(e.target.value))}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Single Sign-On (SSO)</label>
                    <select
                      value={authConfig.security.sso ? "enabled" : "disabled"}
                      onChange={(e) => handleInputChange('security', 'sso', e.target.value === "enabled")}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                    >
                      <option value="enabled">Enabled</option>
                      <option value="disabled">Disabled</option>
                    </select>
                  </div>
                </div>
              </div>

              {/* NQBA Integration */}
              <div className="mb-8">
                <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
                  <span className="mr-3">🔗</span>
                  NQBA Core Integration
                </h3>
                <div className="space-y-4">
                  {Object.entries(authConfig.integration).map(([system, enabled]) => (
                    <div key={system} className="flex items-center space-x-4 p-4 bg-gray-50 rounded-lg">
                      <input
                        type="checkbox"
                        checked={enabled}
                        onChange={(e) => handleInputChange('integration', system, e.target.checked)}
                        className="w-5 h-5 text-indigo-600 rounded focus:ring-indigo-500"
                      />
                      <div>
                        <label className="text-sm font-medium text-gray-900 capitalize">{system} System</label>
                        <p className="text-xs text-gray-600">Integrate with NQBA core authentication</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Submit Button */}
              <div className="text-center">
                <button
                  type="submit"
                  disabled={!validateForm() || isConfiguring}
                  className="bg-gradient-to-r from-flyfox-950 to-goliathNavy-600 text-white px-12 py-4 rounded-xl font-semibold text-lg hover:from-flyfox-900 hover:to-goliathNavy-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isConfiguring ? `Configuring... ${setupProgress}%` : 'Complete Authentication Setup'}
                </button>
                
                {isConfiguring && (
                  <div className="mt-4">
                    <div className="w-full bg-gray-200 rounded-full h-3">
                      <div 
                        className="bg-gradient-to-r from-flyfox-950 to-goliathNavy-600 h-3 rounded-full transition-all duration-300"
                        style={{ width: `${setupProgress}%` }}
                      ></div>
                    </div>
                  </div>
                )}
              </div>
            </form>
          )}
        </div>
      </section>

      {/* Security Features */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Security Features</h2>
            <p className="text-xl text-gray-600">Enterprise-grade security powered by quantum computing</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-20 h-20 bg-gradient-to-br from-flyfox-950 to-flyfoxSilver-800 rounded-2xl flex items-center justify-center text-white text-3xl mx-auto mb-6">🔐</div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">Quantum Encryption</h3>
              <p className="text-gray-600">
                AES-256 encryption enhanced with quantum-resistant algorithms for maximum security
              </p>
            </div>

            <div className="text-center">
              <div className="w-20 h-20 bg-gradient-to-br from-goliathMaize-500 to-goliathMaize-600 rounded-2xl flex items-center justify-center text-white text-3xl mx-auto mb-6">🔄</div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">Unified Access Control</h3>
              <p className="text-gray-600">
                Single sign-on across all business units with centralized user management
              </p>
            </div>

            <div className="text-center">
              <div className="w-20 h-20 bg-gradient-to-br from-goliathNavy-600 to-goliathNavy-700 rounded-2xl flex items-center justify-center text-white text-3xl mx-auto mb-6">📊</div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">Real-time Monitoring</h3>
              <p className="text-gray-600">
                Continuous security monitoring with AI-powered threat detection and response
              </p>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </>
  );
}
