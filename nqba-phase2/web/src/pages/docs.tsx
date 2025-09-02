import Link from "next/link";
import Header from "../components/Header";
import Footer from "../components/Footer";

export default function Docs() {
  const apiEndpoints = [
    {
      name: "Quantum Job Submission",
      endpoint: "POST /api/quantum/submit",
      description: "Submit quantum computing jobs to the NQBA backend",
      parameters: ["job_name", "algorithm_type", "parameters"],
      response: "job_id, status, estimated_completion"
    },
    {
      name: "Agent Management",
      endpoint: "GET /api/agents/list",
      description: "Retrieve list of available AI agents and their capabilities",
      parameters: ["category", "status", "limit"],
      response: "agents array with metadata"
    },
    {
      name: "Pipeline Execution",
      endpoint: "POST /api/pipelines/execute",
      description: "Execute automated business pipelines",
      parameters: ["pipeline_id", "input_data", "execution_mode"],
      response: "execution_id, status, progress"
    },
    {
      name: "Performance Metrics",
      endpoint: "GET /api/metrics/performance",
      description: "Get real-time performance metrics and quantum advantage data",
      parameters: ["timeframe", "metric_type"],
      response: "metrics object with current values"
    }
  ];

  const sdkGuides = [
    {
      title: "Python SDK",
      description: "Full Python integration for quantum computing and AI agents",
      features: ["QUBO optimization", "Agent orchestration", "Pipeline automation"],
      codeExample: `from flyfox_ai import FLYFOXClient

client = FLYFOXClient(api_key="your_key")
job = client.submit_quantum_job(
    algorithm="grover",
    parameters={"database_size": 1000}
)`,
      download: "pip install flyfox-ai-sdk"
    },
    {
      title: "JavaScript SDK",
      description: "Node.js and browser integration for web applications",
      features: ["Real-time updates", "WebSocket connections", "Browser compatibility"],
      codeExample: `import { FLYFOXClient } from '@flyfox-ai/js-sdk';

const client = new FLYFOXClient({ apiKey: 'your_key' });
const job = await client.submitQuantumJob({
  algorithm: 'deutsch-jozsa',
  parameters: { functionType: 'balanced' }
});`,
      download: "npm install @flyfox-ai/js-sdk"
    },
    {
      title: "REST API",
      description: "Direct HTTP integration for any programming language",
      features: ["Standard REST endpoints", "JSON responses", "OAuth2 authentication"],
      codeExample: `curl -X POST https://api.goliathomniedge.com/quantum/submit \\
  -H "Authorization: Bearer YOUR_TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{"algorithm": "shor", "parameters": {"number": 15}}'`,
      download: "Full API reference below"
    }
  ];

  const integrationGuides = [
    {
      title: "n8n Integration",
      description: "Connect FLYFOX AI to your n8n automation workflows",
      steps: [
        "Install FLYFOX AI n8n node",
        "Configure API credentials",
        "Add quantum computing nodes to workflows",
        "Automate business processes with AI agents"
      ],
      benefits: ["No-code automation", "Real-time processing", "Scalable workflows"]
    },
    {
      title: "UiPath Integration",
      description: "Integrate FLYFOX AI agents into UiPath RPA processes",
      steps: [
        "Download FLYFOX AI UiPath package",
        "Configure connection settings",
        "Add AI decision nodes to automations",
        "Enable intelligent process automation"
      ],
      benefits: ["RPA + AI", "Cognitive automation", "Process optimization"]
    },
    {
      title: "Mendix Integration",
      description: "Build intelligent applications with FLYFOX AI in Mendix",
      steps: [
        "Import FLYFOX AI Mendix module",
        "Configure AI service connections",
        "Add intelligent widgets to apps",
        "Enable AI-powered user experiences"
      ],
      benefits: ["Low-code AI", "Rapid development", "Scalable applications"]
    }
  ];

  return (
    <>
      <Header />
      
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-flyfox-950 via-goliath-950 to-goliathNavy-950 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-5xl md:text-6xl font-bold mb-6">
            FLYFOX AI Documentation
          </h1>
          <p className="text-xl md:text-2xl text-gray-300 max-w-4xl mx-auto leading-relaxed">
            Everything you need to integrate FLYFOX AI into your applications. 
            From API endpoints to SDK guides, we've got you covered.
          </p>
          
          <div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center">
            <a 
              href="#api-reference"
              className="bg-gradient-to-r from-cyan-500 to-purple-600 hover:from-cyan-600 hover:to-purple-700 text-white px-8 py-4 rounded-xl font-semibold text-lg transition-all transform hover:scale-105"
            >
              📚 API Reference
            </a>
            <a 
              href="#sdk-guides"
              className="border border-white/30 text-white hover:bg-white/10 px-8 py-4 rounded-xl font-semibold text-lg transition-all transform hover:scale-105"
            >
              🛠️ SDK Guides
            </a>
          </div>
        </div>
      </section>

      {/* Quick Start Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Get Started in 5 Minutes
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Follow this quick start guide to get your first quantum job running on FLYFOX AI.
            </p>
          </div>
          
          <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-200">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div>
                <h3 className="text-2xl font-bold text-gray-900 mb-6">Step-by-Step Guide</h3>
                <div className="space-y-4">
                  <div className="flex items-start space-x-3">
                    <div className="w-8 h-8 bg-cyan-500 text-white rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0">
                      1
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-900">Get Your API Key</h4>
                      <p className="text-gray-600 text-sm">Sign up and generate your API key from the platform dashboard.</p>
                    </div>
                  </div>
                  
                  <div className="flex items-start space-x-3">
                    <div className="w-8 h-8 bg-purple-500 text-white rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0">
                      2
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-900">Install SDK</h4>
                      <p className="text-gray-600 text-sm">Install the FLYFOX AI SDK for your preferred language.</p>
                    </div>
                  </div>
                  
                  <div className="flex items-start space-x-3">
                    <div className="w-8 h-8 bg-green-500 text-white rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0">
                      3
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-900">Submit Your First Job</h4>
                      <p className="text-gray-600 text-sm">Use the SDK to submit a quantum computing job.</p>
                    </div>
                  </div>
                  
                  <div className="flex items-start space-x-3">
                    <div className="w-8 h-8 bg-orange-500 text-white rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0">
                      4
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-900">Monitor Progress</h4>
                      <p className="text-gray-600 text-sm">Track your job's progress and get results in real-time.</p>
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl p-6">
                <h4 className="text-lg font-bold text-gray-900 mb-4">Quick Code Example</h4>
                <div className="bg-gray-900 text-green-400 p-4 rounded-lg font-mono text-sm overflow-x-auto">
                  <pre>{`# Python Quick Start
from flyfox_ai import FLYFOXClient

# Initialize client
client = FLYFOXClient(
    api_key="your_api_key_here"
)

# Submit quantum job
job = client.submit_quantum_job(
    algorithm="grover",
    parameters={
        "database_size": 1000,
        "target_item": "solution"
    }
)

# Monitor progress
while job.status != "completed":
    job.refresh()
    print(f"Progress: {job.progress}%")
    time.sleep(5)

# Get results
results = job.get_results()
print(f"Found solution in {results.iterations} iterations")`}</pre>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* API Reference Section */}
      <section id="api-reference" className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              API Reference
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Complete API documentation for all FLYFOX AI endpoints. 
              All endpoints return JSON responses and support OAuth2 authentication.
            </p>
          </div>
          
          <div className="space-y-8">
            {apiEndpoints.map((endpoint, index) => (
              <div key={index} className="bg-gray-50 rounded-2xl p-8 border border-gray-200">
                <div className="flex items-start justify-between mb-4">
                  <h3 className="text-2xl font-bold text-gray-900">{endpoint.name}</h3>
                  <span className="bg-cyan-100 text-cyan-800 px-3 py-1 rounded-full text-sm font-medium">
                    {endpoint.endpoint}
                  </span>
                </div>
                
                <p className="text-gray-600 mb-6">{endpoint.description}</p>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-3">Parameters</h4>
                    <div className="space-y-2">
                      {endpoint.parameters.map((param, paramIndex) => (
                        <div key={paramIndex} className="flex items-center space-x-2">
                          <span className="w-2 h-2 bg-cyan-500 rounded-full"></span>
                          <span className="text-sm text-gray-700">{param}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                  
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-3">Response</h4>
                    <div className="bg-gray-100 p-3 rounded-lg">
                      <code className="text-sm text-gray-800">{endpoint.response}</code>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* SDK Guides Section */}
      <section id="sdk-guides" className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              SDK & Integration Guides
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Choose your preferred programming language and get started with our comprehensive SDKs.
            </p>
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {sdkGuides.map((sdk, index) => (
              <div key={index} className="bg-white rounded-2xl shadow-xl p-8 border border-gray-200 hover:shadow-2xl transition-all transform hover:scale-105">
                <h3 className="text-2xl font-bold text-gray-900 mb-4">{sdk.title}</h3>
                <p className="text-gray-600 mb-6">{sdk.description}</p>
                
                <div className="mb-6">
                  <h4 className="font-semibold text-gray-900 mb-3">Key Features</h4>
                  <div className="space-y-2">
                    {sdk.features.map((feature, featureIndex) => (
                      <div key={featureIndex} className="flex items-center space-x-2">
                        <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                        <span className="text-sm text-gray-700">{feature}</span>
                      </div>
                    ))}
                  </div>
                </div>
                
                <div className="mb-6">
                  <h4 className="font-semibold text-gray-900 mb-3">Code Example</h4>
                  <div className="bg-gray-900 text-green-400 p-3 rounded-lg font-mono text-xs overflow-x-auto">
                    <pre>{sdk.codeExample}</pre>
                  </div>
                </div>
                
                <div className="bg-gradient-to-r from-cyan-50 to-purple-50 p-4 rounded-lg border border-cyan-200">
                  <p className="text-cyan-800 text-sm font-medium mb-2">Installation</p>
                  <code className="text-cyan-700 text-sm">{sdk.download}</code>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Integration Guides Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Platform Integrations
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Seamlessly integrate FLYFOX AI with your existing automation and development platforms.
            </p>
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {integrationGuides.map((integration, index) => (
              <div key={index} className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-2xl p-8 border border-gray-200 hover:shadow-xl transition-all transform hover:scale-105">
                <h3 className="text-2xl font-bold text-gray-900 mb-4">{integration.title}</h3>
                <p className="text-gray-600 mb-6">{integration.description}</p>
                
                <div className="mb-6">
                  <h4 className="font-semibold text-gray-900 mb-3">Integration Steps</h4>
                  <div className="space-y-2">
                    {integration.steps.map((step, stepIndex) => (
                      <div key={stepIndex} className="flex items-start space-x-2">
                        <span className="w-6 h-6 bg-cyan-500 text-white rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0 mt-0.5">
                          {stepIndex + 1}
                        </span>
                        <span className="text-sm text-gray-700">{step}</span>
                      </div>
                    ))}
                  </div>
                </div>
                
                <div className="mb-6">
                  <h4 className="font-semibold text-gray-900 mb-3">Key Benefits</h4>
                  <div className="space-y-2">
                    {integration.benefits.map((benefit, benefitIndex) => (
                      <div key={benefitIndex} className="flex items-center space-x-2">
                        <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                        <span className="text-sm text-gray-700">{benefit}</span>
                      </div>
                    ))}
                  </div>
                </div>
                
                <button className="w-full bg-gradient-to-r from-cyan-500 to-purple-600 text-white py-3 px-6 rounded-lg font-semibold hover:from-cyan-600 hover:to-purple-700 transition-all transform hover:scale-105">
                  📖 View Full Guide
                </button>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-20 bg-gradient-to-br from-flyfox-950 via-goliath-950 to-goliathNavy-950 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            Ready to Build Something Amazing?
          </h2>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto mb-8">
            Start integrating FLYFOX AI into your applications today. 
            Get access to quantum computing power and AI agents in minutes.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-8">
            <Link 
              href="/platform"
              className="bg-gradient-to-r from-cyan-500 to-purple-600 hover:from-cyan-600 hover:to-purple-700 text-white px-8 py-4 rounded-xl font-semibold text-lg transition-all transform hover:scale-105"
            >
              🚀 Launch Platform
            </Link>
            <Link 
              href="/contact"
              className="border border-white/30 text-white hover:bg-white/10 px-8 py-4 rounded-xl font-semibold text-lg transition-all transform hover:scale-105"
            >
              📞 Get Support
            </Link>
          </div>
          
          <div className="bg-white/5 backdrop-blur-md border border-white/10 rounded-2xl p-6 max-w-2xl mx-auto">
            <p className="text-cyan-300 text-sm">
              <strong>Need help?</strong> Our team is available 24/7 to support your integration. 
              Contact us for custom solutions and enterprise support.
            </p>
          </div>
        </div>
      </section>

      <Footer />
    </>
  );
}
