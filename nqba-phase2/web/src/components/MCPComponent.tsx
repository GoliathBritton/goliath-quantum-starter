import { useState, useEffect } from "react";

export interface MCPModel {
  id: string;
  name: string;
  type: "llm" | "vision" | "audio" | "multimodal";
  provider: "openai" | "anthropic" | "google" | "custom";
  status: "active" | "inactive" | "training" | "error";
  contextWindow: number;
  performance: number;
  costPerToken: number;
  lastUpdated: string;
}

export interface MCPContext {
  id: string;
  name: string;
  description: string;
  models: string[];
  metadata: Record<string, any>;
  createdAt: string;
  lastAccessed: string;
}

export default function MCPComponent() {
  const [models, setModels] = useState<MCPModel[]>([]);
  const [contexts, setContexts] = useState<MCPContext[]>([]);
  const [activeModel, setActiveModel] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedContext, setSelectedContext] = useState<string | null>(null);

  // Simulate MCP data
  useEffect(() => {
    const fetchMCPData = async () => {
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const mockModels: MCPModel[] = [
        {
          id: "mcp_001",
          name: "FLYFOX-NQBA-7B",
          type: "llm",
          provider: "custom",
          status: "active",
          contextWindow: 32768,
          performance: 0.94,
          costPerToken: 0.0001,
          lastUpdated: "2024-01-15T10:30:00Z"
        },
        {
          id: "mcp_002",
          name: "Quantum-Vision-1.5",
          type: "vision",
          provider: "custom",
          status: "active",
          contextWindow: 16384,
          performance: 0.89,
          costPerToken: 0.0002,
          lastUpdated: "2024-01-14T15:45:00Z"
        },
        {
          id: "mcp_003",
          name: "GPT-4o-Mini",
          type: "multimodal",
          provider: "openai",
          status: "active",
          contextWindow: 128000,
          performance: 0.91,
          costPerToken: 0.00015,
          lastUpdated: "2024-01-15T09:15:00Z"
        },
        {
          id: "mcp_004",
          name: "Claude-3-Sonnet",
          type: "llm",
          provider: "anthropic",
          status: "active",
          contextWindow: 200000,
          performance: 0.93,
          costPerToken: 0.00012,
          lastUpdated: "2024-01-15T11:20:00Z"
        }
      ];

      const mockContexts: MCPContext[] = [
        {
          id: "ctx_001",
          name: "NQBA Business Intelligence",
          description: "Context for business intelligence and decision-making across all verticals",
          models: ["mcp_001", "mcp_003"],
          metadata: {
            industry: "multi-sector",
            compliance: ["GDPR", "SOX", "HIPAA"],
            security: "quantum-encrypted"
          },
          createdAt: "2024-01-01T00:00:00Z",
          lastAccessed: "2024-01-15T12:00:00Z"
        },
        {
          id: "ctx_002",
          name: "Quantum Financial Analysis",
          description: "Specialized context for financial modeling and risk assessment",
          models: ["mcp_001", "mcp_004"],
          metadata: {
            industry: "financial",
            compliance: ["SOX", "Basel III"],
            riskLevel: "high"
          },
          createdAt: "2024-01-05T00:00:00Z",
          lastAccessed: "2024-01-15T11:30:00Z"
        },
        {
          id: "ctx_003",
          name: "AI Agent Training",
          description: "Context for training and optimizing AI agents across the ecosystem",
          models: ["mcp_001", "mcp_002"],
          metadata: {
            purpose: "agent-training",
            learningRate: "adaptive",
            optimization: "quantum-enhanced"
          },
          createdAt: "2024-01-10T00:00:00Z",
          lastAccessed: "2024-01-15T10:45:00Z"
        }
      ];

      setModels(mockModels);
      setContexts(mockContexts);
      setIsLoading(false);
    };

    fetchMCPData();
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case "active": return "text-green-600 bg-green-100";
      case "inactive": return "text-gray-600 bg-gray-100";
      case "training": return "text-blue-600 bg-blue-100";
      case "error": return "text-red-600 bg-red-100";
      default: return "text-gray-600 bg-gray-100";
    }
  };

  const getProviderIcon = (provider: string) => {
    switch (provider) {
      case "openai": return "🤖";
      case "anthropic": return "🧠";
      case "google": return "🔍";
      case "custom": return "⚡";
      default: return "❓";
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case "llm": return "📝";
      case "vision": return "👁️";
      case "audio": return "🎵";
      case "multimodal": return "🔗";
      default: return "❓";
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
      {/* MCP Header */}
      <div className="bg-gradient-to-r from-flyfox-950 to-flyfoxSilver-800 text-white p-6 rounded-2xl">
        <div className="flex items-center space-x-4 mb-4">
          <div className="w-16 h-16 bg-white/20 rounded-2xl flex items-center justify-center text-3xl">
            🔗
          </div>
          <div>
            <h2 className="text-3xl font-bold">Model Context Protocol (MCP)</h2>
            <p className="text-flyfoxSilver-200">
              Unified AI model management and context orchestration across the FLYFOX AI ecosystem
            </p>
          </div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="text-center">
            <div className="text-2xl font-bold">{models.length}</div>
            <div className="text-sm text-flyfoxSilver-200">Active Models</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold">{contexts.length}</div>
            <div className="text-sm text-flyfoxSilver-200">Contexts</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold">
              {models.filter(m => m.status === 'active').length}
            </div>
            <div className="text-sm text-flyfoxSilver-200">Online</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold">
              {Math.round(models.reduce((acc, m) => acc + m.performance, 0) / models.length * 100)}%
            </div>
            <div className="text-sm text-flyfoxSilver-200">Avg Performance</div>
          </div>
        </div>
      </div>

      {/* Models Section */}
      <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-200">
        <h3 className="text-2xl font-bold text-gray-900 mb-6">AI Models</h3>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {models.map((model) => (
            <div 
              key={model.id}
              className={`p-6 rounded-xl border-2 transition-all cursor-pointer ${
                activeModel === model.id 
                  ? 'border-flyfox-950 bg-flyfox-50' 
                  : 'border-gray-200 hover:border-flyfox-300'
              }`}
              onClick={() => setActiveModel(activeModel === model.id ? null : model.id)}
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <div className="text-2xl">{getProviderIcon(model.provider)}</div>
                  <div className="text-xl">{getTypeIcon(model.type)}</div>
                </div>
                <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(model.status)}`}>
                  {model.status}
                </span>
              </div>
              
              <h4 className="text-xl font-bold text-gray-900 mb-2">{model.name}</h4>
              
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="text-gray-600">Context:</span>
                  <div className="font-semibold">{model.contextWindow.toLocaleString()}</div>
                </div>
                <div>
                  <span className="text-gray-600">Performance:</span>
                  <div className="font-semibold text-green-600">{(model.performance * 100).toFixed(1)}%</div>
                </div>
                <div>
                  <span className="text-gray-600">Cost/Token:</span>
                  <div className="font-semibold">${model.costPerToken.toFixed(4)}</div>
                </div>
                <div>
                  <span className="text-gray-600">Provider:</span>
                  <div className="font-semibold capitalize">{model.provider}</div>
                </div>
              </div>
              
              <div className="mt-4 text-xs text-gray-500">
                Updated: {new Date(model.lastUpdated).toLocaleDateString()}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Contexts Section */}
      <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-200">
        <h3 className="text-2xl font-bold text-gray-900 mb-6">Context Management</h3>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {contexts.map((context) => (
            <div 
              key={context.id}
              className={`p-6 rounded-xl border-2 transition-all cursor-pointer ${
                selectedContext === context.id 
                  ? 'border-goliathNavy-600 bg-goliathNavy-50' 
                  : 'border-gray-200 hover:border-goliathNavy-300'
              }`}
              onClick={() => setSelectedContext(selectedContext === context.id ? null : context.id)}
            >
              <h4 className="text-xl font-bold text-gray-900 mb-3">{context.name}</h4>
              <p className="text-gray-600 text-sm mb-4">{context.description}</p>
              
              <div className="mb-4">
                <span className="text-sm font-medium text-gray-700">Models:</span>
                <div className="flex flex-wrap gap-2 mt-2">
                  {context.models.map((modelId) => {
                    const model = models.find(m => m.id === modelId);
                    return (
                      <span 
                        key={modelId}
                        className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-full"
                      >
                        {model?.name || modelId}
                      </span>
                    );
                  })}
                </div>
              </div>
              
              <div className="space-y-2 text-xs">
                {Object.entries(context.metadata).map(([key, value]) => (
                  <div key={key} className="flex justify-between">
                    <span className="text-gray-600 capitalize">{key}:</span>
                    <span className="font-medium">
                      {Array.isArray(value) ? value.join(", ") : String(value)}
                    </span>
                  </div>
                ))}
              </div>
              
              <div className="mt-4 text-xs text-gray-500">
                Created: {new Date(context.createdAt).toLocaleDateString()}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* MCP Integration Status */}
      <div className="bg-gradient-to-r from-sigma-500 to-sigma-600 text-white p-6 rounded-2xl">
        <h3 className="text-2xl font-bold mb-4">MCP Integration Status</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="text-center">
            <div className="text-3xl mb-2">✅</div>
            <div className="font-semibold">NQBA Core</div>
            <div className="text-sm text-sigma-200">Fully Integrated</div>
          </div>
          <div className="text-center">
            <div className="text-3xl mb-2">✅</div>
            <div className="font-semibold">Quantum Agents</div>
            <div className="text-sm text-sigma-200">Context Aware</div>
          </div>
          <div className="text-center">
            <div className="text-3xl mb-2">✅</div>
            <div className="font-semibold">Sigma Select</div>
            <div className="text-sm text-sigma-200">MCP Enabled</div>
          </div>
        </div>
        
        <div className="mt-6 p-4 bg-white/10 rounded-lg">
          <div className="text-sm">
            <strong>MCP Benefits:</strong> Unified model management, context sharing across agents, 
            cost optimization, performance monitoring, and seamless integration with OpenAI, Anthropic, 
            and custom FLYFOX AI models.
          </div>
        </div>
      </div>
    </div>
  );
}
