import { useState, useEffect } from "react";

export interface ProcessMiningData {
  id: string;
  processName: string;
  efficiency: number;
  automationPotential: number;
  bottlenecks: string[];
  costSavings: number;
  status: "active" | "analyzing" | "optimized" | "needs_attention";
  lastAnalyzed: string;
  businessUnit: "flyfox" | "goliath" | "sigma";
}

export interface AutomationOpportunity {
  id: string;
  processName: string;
  currentEffort: number;
  automatedEffort: number;
  roi: number;
  implementationTime: string;
  priority: "high" | "medium" | "low";
  businessImpact: string;
}

export interface PerformanceMetrics {
  totalProcesses: number;
  automatedProcesses: number;
  efficiencyGain: number;
  costSavings: number;
  timeReduction: number;
  complianceScore: number;
}

export default function FLYFOXProcessIntelligence() {
  const [processData, setProcessData] = useState<ProcessMiningData[]>([]);
  const [automationOpportunities, setAutomationOpportunities] = useState<AutomationOpportunity[]>([]);
  const [performanceMetrics, setPerformanceMetrics] = useState<PerformanceMetrics | null>(null);
  const [selectedProcess, setSelectedProcess] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<"overview" | "processes" | "automation" | "analytics">("overview");

  // Simulate FLYFOX Process Intelligence data
  useEffect(() => {
    const fetchProcessData = async () => {
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const mockProcessData: ProcessMiningData[] = [
        {
          id: "proc_001",
          processName: "FLYFOX AI Model Training Pipeline",
          efficiency: 87,
          automationPotential: 94,
          bottlenecks: ["Data preprocessing", "Model validation"],
          costSavings: 125000,
          status: "optimized",
          lastAnalyzed: "2024-01-15T10:30:00Z",
          businessUnit: "flyfox"
        },
        {
          id: "proc_002",
          processName: "Goliath Financial Risk Assessment",
          efficiency: 72,
          automationPotential: 89,
          bottlenecks: ["Manual data entry", "Compliance checks"],
          costSavings: 89000,
          status: "needs_attention",
          lastAnalyzed: "2024-01-14T15:45:00Z",
          businessUnit: "goliath"
        },
        {
          id: "proc_003",
          processName: "Sigma Select Lead Qualification",
          efficiency: 91,
          automationPotential: 78,
          bottlenecks: ["Initial screening"],
          costSavings: 156000,
          status: "active",
          lastAnalyzed: "2024-01-15T09:15:00Z",
          businessUnit: "sigma"
        },
        {
          id: "proc_004",
          processName: "NQBA Core Decision Engine",
          efficiency: 95,
          automationPotential: 67,
          bottlenecks: ["Edge case handling"],
          costSavings: 203000,
          status: "optimized",
          lastAnalyzed: "2024-01-15T11:20:00Z",
          businessUnit: "flyfox"
        },
        {
          id: "proc_005",
          processName: "Quantum Agent Deployment",
          efficiency: 68,
          automationPotential: 92,
          bottlenecks: ["Resource allocation", "Scaling decisions"],
          costSavings: 178000,
          status: "analyzing",
          lastAnalyzed: "2024-01-14T14:30:00Z",
          businessUnit: "goliath"
        }
      ];

      const mockAutomationOpportunities: AutomationOpportunity[] = [
        {
          id: "auto_001",
          processName: "Customer Onboarding",
          currentEffort: 45,
          automatedEffort: 8,
          roi: 463,
          implementationTime: "6 weeks",
          priority: "high",
          businessImpact: "Reduce onboarding time by 82%"
        },
        {
          id: "auto_002",
          processName: "Invoice Processing",
          currentEffort: 32,
          automatedEffort: 3,
          roi: 967,
          implementationTime: "4 weeks",
          priority: "high",
          businessImpact: "Eliminate manual data entry errors"
        },
        {
          id: "auto_003",
          processName: "Compliance Reporting",
          currentEffort: 28,
          automatedEffort: 5,
          roi: 460,
          implementationTime: "8 weeks",
          priority: "medium",
          businessImpact: "Ensure 100% compliance accuracy"
        }
      ];

      const mockPerformanceMetrics: PerformanceMetrics = {
        totalProcesses: 47,
        automatedProcesses: 31,
        efficiencyGain: 34,
        costSavings: 892000,
        timeReduction: 67,
        complianceScore: 98
      };

      setProcessData(mockProcessData);
      setAutomationOpportunities(mockAutomationOpportunities);
      setPerformanceMetrics(mockPerformanceMetrics);
      setIsLoading(false);
    };

          fetchProcessData();
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case "optimized": return "text-green-600 bg-green-100";
      case "active": return "text-blue-600 bg-blue-100";
      case "analyzing": return "text-yellow-600 bg-yellow-100";
      case "needs_attention": return "text-red-600 bg-red-100";
      default: return "text-gray-600 bg-gray-100";
    }
  };

  const getBusinessUnitColor = (unit: string) => {
    switch (unit) {
      case "flyfox": return "from-flyfox-950 to-flyfoxSilver-800";
      case "goliath": return "from-goliath-950 to-goliathNavy-600";
      case "sigma": return "from-sigma-500 to-sigma-600";
      default: return "from-gray-500 to-gray-600";
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case "high": return "text-red-600 bg-red-100";
      case "medium": return "text-yellow-600 bg-yellow-100";
      case "low": return "text-green-600 bg-green-100";
      default: return "text-gray-600 bg-gray-100";
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-flyfox-950"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
             {/* FLYFOX Process Intelligence Header */}
       <div className="bg-gradient-to-r from-purple-600 to-purple-800 text-white p-8 rounded-2xl">
         <div className="flex items-center space-x-6 mb-6">
           <div className="w-20 h-20 bg-white/20 rounded-2xl flex items-center justify-center text-4xl">
             🔍
           </div>
           <div>
             <h2 className="text-4xl font-bold">FLYFOX Process Intelligence</h2>
             <p className="text-purple-100 text-xl mt-2">
               Enterprise-grade process intelligence, automation discovery, and performance optimization 
               across FLYFOX AI, Goliath of All Trade Inc, and Sigma Select
             </p>
           </div>
         </div>
        
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="text-center">
            <div className="text-3xl font-bold">{performanceMetrics?.totalProcesses}</div>
            <div className="text-sm text-purple-200">Total Processes</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold">{performanceMetrics?.automatedProcesses}</div>
            <div className="text-sm text-purple-200">Automated</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold">{performanceMetrics?.efficiencyGain}%</div>
            <div className="text-sm text-purple-200">Efficiency Gain</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold">${(performanceMetrics?.costSavings || 0).toLocaleString()}</div>
            <div className="text-sm text-purple-200">Cost Savings</div>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-200">
        <nav className="flex space-x-8 border-b border-gray-200">
          {[
            { id: "overview", name: "Overview", icon: "📊" },
            { id: "processes", name: "Process Mining", icon: "🔍" },
            { id: "automation", name: "Automation Discovery", icon: "🤖" },
            { id: "analytics", name: "Performance Analytics", icon: "📈" }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`py-4 px-1 border-b-2 font-medium text-sm flex items-center space-x-2 ${
                activeTab === tab.id
                  ? "border-purple-600 text-purple-600"
                  : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
              }`}
            >
              <span>{tab.icon}</span>
              <span>{tab.name}</span>
            </button>
          ))}
        </nav>

        {/* Tab Content */}
        <div className="mt-6">
          {activeTab === "overview" && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div className="bg-gradient-to-br from-flyfox-950 to-flyfoxSilver-800 text-white p-6 rounded-xl">
                  <div className="text-3xl mb-2">🦊</div>
                  <h3 className="text-xl font-bold mb-2">FLYFOX AI</h3>
                  <div className="text-2xl font-bold mb-2">
                    {processData.filter(p => p.businessUnit === "flyfox").length} Processes
                  </div>
                  <div className="text-sm text-flyfoxSilver-200">
                    AI model training, NQBA core, quantum optimization
                  </div>
                </div>
                
                <div className="bg-gradient-to-br from-goliath-950 to-goliathNavy-600 text-white p-6 rounded-xl">
                  <div className="text-3xl mb-2">🏛️</div>
                  <h3 className="text-xl font-bold mb-2">Goliath of All Trade</h3>
                  <div className="text-2xl font-bold mb-2">
                    {processData.filter(p => p.businessUnit === "goliath").length} Processes
                  </div>
                  <div className="text-sm text-goliathNavy-200">
                    Financial services, risk assessment, compliance
                  </div>
                </div>
                
                <div className="bg-gradient-to-br from-sigma-500 to-sigma-600 text-white p-6 rounded-xl">
                  <div className="text-3xl mb-2">Σ</div>
                  <h3 className="text-xl font-bold mb-2">Sigma Select</h3>
                  <div className="text-2xl font-bold mb-2">
                    {processData.filter(p => p.businessUnit === "sigma").length} Processes
                  </div>
                  <div className="text-sm text-sigma-200">
                    Sales intelligence, lead qualification, revenue optimization
                  </div>
                </div>
              </div>

              <div className="bg-gray-50 rounded-xl p-6">
                <h3 className="text-xl font-bold text-gray-900 mb-4">Key Benefits</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="flex items-start space-x-3">
                    <div className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center text-purple-600 font-bold">1</div>
                    <div>
                      <h4 className="font-semibold text-gray-900">Process Discovery</h4>
                      <p className="text-sm text-gray-600">Automatically discover and map business processes across all three business units</p>
                    </div>
                  </div>
                  <div className="flex items-start space-x-3">
                    <div className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center text-purple-600 font-bold">2</div>
                    <div>
                      <h4 className="font-semibold text-gray-900">Automation Potential</h4>
                      <p className="text-sm text-gray-600">Identify high-ROI automation opportunities with AI-powered recommendations</p>
                    </div>
                  </div>
                  <div className="flex items-start space-x-3">
                    <div className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center text-purple-600 font-bold">3</div>
                    <div>
                      <h4 className="font-semibold text-gray-900">Performance Optimization</h4>
                      <p className="text-sm text-gray-600">Real-time monitoring and optimization of process efficiency and costs</p>
                    </div>
                  </div>
                  <div className="flex items-start space-x-3">
                    <div className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center text-purple-600 font-bold">4</div>
                    <div>
                      <h4 className="font-semibold text-gray-900">Compliance Assurance</h4>
                      <p className="text-sm text-gray-600">Ensure regulatory compliance across all business processes and units</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === "processes" && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {processData.map((process) => (
                  <div 
                    key={process.id}
                    className={`p-6 rounded-xl border-2 transition-all cursor-pointer ${
                      selectedProcess === process.id 
                        ? 'border-purple-500 bg-purple-50' 
                        : 'border-gray-200 hover:border-purple-300'
                    }`}
                    onClick={() => setSelectedProcess(selectedProcess === process.id ? null : process.id)}
                  >
                    <div className="flex items-start justify-between mb-4">
                      <div className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(process.status)}`}>
                        {process.status}
                      </div>
                      <div className={`w-8 h-8 bg-gradient-to-br ${getBusinessUnitColor(process.businessUnit)} rounded-lg flex items-center justify-center text-white text-sm font-bold`}>
                        {process.businessUnit === "flyfox" ? "🦊" : process.businessUnit === "goliath" ? "🏛️" : "Σ"}
                      </div>
                    </div>
                    
                    <h4 className="text-xl font-bold text-gray-900 mb-3">{process.processName}</h4>
                    
                    <div className="grid grid-cols-2 gap-4 mb-4">
                      <div>
                        <span className="text-sm text-gray-600">Efficiency:</span>
                        <div className="font-semibold text-green-600">{process.efficiency}%</div>
                      </div>
                      <div>
                        <span className="text-sm text-gray-600">Automation Potential:</span>
                        <div className="font-semibold text-blue-600">{process.automationPotential}%</div>
                      </div>
                      <div>
                        <span className="text-sm text-gray-600">Cost Savings:</span>
                        <div className="font-semibold">${process.costSavings.toLocaleString()}</div>
                      </div>
                      <div>
                        <span className="text-sm text-gray-600">Last Analyzed:</span>
                        <div className="font-semibold text-sm">{new Date(process.lastAnalyzed).toLocaleDateString()}</div>
                      </div>
                    </div>
                    
                    <div className="mb-4">
                      <span className="text-sm font-medium text-gray-700">Bottlenecks:</span>
                      <div className="flex flex-wrap gap-2 mt-2">
                        {process.bottlenecks.map((bottleneck, idx) => (
                          <span 
                            key={idx}
                            className="px-2 py-1 bg-red-100 text-red-700 text-xs rounded-full"
                          >
                            {bottleneck}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === "automation" && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {automationOpportunities.map((opportunity) => (
                  <div key={opportunity.id} className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
                    <div className="flex items-start justify-between mb-4">
                      <h4 className="text-xl font-bold text-gray-900">{opportunity.processName}</h4>
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${getPriorityColor(opportunity.priority)}`}>
                        {opportunity.priority} Priority
                      </span>
                    </div>
                    
                    <div className="grid grid-cols-2 gap-4 mb-4">
                      <div>
                        <span className="text-sm text-gray-600">Current Effort:</span>
                        <div className="font-semibold">{opportunity.currentEffort} hrs/week</div>
                      </div>
                      <div>
                        <span className="text-sm text-gray-600">Automated Effort:</span>
                        <div className="font-semibold text-green-600">{opportunity.automatedEffort} hrs/week</div>
                      </div>
                      <div>
                        <span className="text-sm text-gray-600">ROI:</span>
                        <div className="font-semibold text-blue-600">{opportunity.roi}%</div>
                      </div>
                      <div>
                        <span className="text-sm text-gray-600">Implementation:</span>
                        <div className="font-semibold">{opportunity.implementationTime}</div>
                      </div>
                    </div>
                    
                    <div className="mb-4">
                      <span className="text-sm font-medium text-gray-700">Business Impact:</span>
                      <div className="text-sm text-gray-600 mt-1">{opportunity.businessImpact}</div>
                    </div>
                    
                    <button className="w-full bg-gradient-to-r from-purple-600 to-purple-700 text-white py-2 px-4 rounded-lg font-medium hover:from-purple-700 hover:to-purple-800 transition-all">
                      Implement Automation
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === "analytics" && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
                  <h4 className="text-lg font-semibold text-gray-900 mb-4">Efficiency Trends</h4>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">FLYFOX AI:</span>
                      <span className="font-semibold text-green-600">+12%</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">Goliath Trade:</span>
                      <span className="font-semibold text-blue-600">+8%</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">Sigma Select:</span>
                      <span className="font-semibold text-purple-600">+15%</span>
                    </div>
                  </div>
                </div>
                
                <div className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
                  <h4 className="text-lg font-semibold text-gray-900 mb-4">Cost Optimization</h4>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">Total Savings:</span>
                      <span className="font-semibold text-green-600">${performanceMetrics?.costSavings.toLocaleString()}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">Monthly ROI:</span>
                      <span className="font-semibold text-blue-600">23%</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">Time Reduction:</span>
                      <span className="font-semibold text-purple-600">{performanceMetrics?.timeReduction}%</span>
                    </div>
                  </div>
                </div>
                
                <div className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
                  <h4 className="text-lg font-semibold text-gray-900 mb-4">Compliance Score</h4>
                  <div className="text-center">
                    <div className="text-4xl font-bold text-green-600 mb-2">{performanceMetrics?.complianceScore}%</div>
                    <div className="text-sm text-gray-600">Overall Compliance</div>
                    <div className="mt-3 text-xs text-gray-500">
                      GDPR: 100% | SOX: 98% | HIPAA: 96%
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

             {/* Integration Status */}
       <div className="bg-gradient-to-r from-purple-500 to-purple-600 text-white p-6 rounded-2xl">
         <h3 className="text-2xl font-bold mb-4">FLYFOX Process Intelligence Status</h3>
         <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
           <div className="text-center">
             <div className="text-3xl mb-2">✅</div>
             <div className="font-semibold">Process Discovery</div>
             <div className="text-sm text-purple-200">Active across all business units</div>
           </div>
           <div className="text-center">
             <div className="text-3xl mb-2">✅</div>
             <div className="font-semibold">Automation Engine</div>
             <div className="text-sm text-purple-200">AI-powered recommendations</div>
           </div>
           <div className="text-center">
             <div className="text-3xl mb-2">✅</div>
             <div className="font-semibold">Performance Analytics</div>
             <div className="text-sm text-purple-200">Real-time monitoring</div>
           </div>
         </div>
         
         <div className="mt-6 p-4 bg-white/10 rounded-lg">
           <div className="text-sm">
             <strong>FLYFOX Process Intelligence Benefits:</strong> Enterprise process mining, automation discovery, 
             performance optimization, compliance assurance, and cost reduction across FLYFOX AI, 
             Goliath of All Trade Inc, and Sigma Select business units.
           </div>
         </div>
       </div>
    </div>
  );
}
