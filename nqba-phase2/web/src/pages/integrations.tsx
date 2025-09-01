"use client";
import { useState, useEffect } from "react";
import Header from "../components/Header";
import Footer from "../components/Footer";

interface Integration {
  provider: string;
  status: string;
  connected_at: string;
  config: Record<string, any>;
}

export default function Integrations() {
  const [integrations, setIntegrations] = useState<Integration[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedProvider, setSelectedProvider] = useState<string>("");
  const [config, setConfig] = useState<Record<string, any>>({});

  useEffect(() => {
    fetchIntegrations();
  }, []);

  const fetchIntegrations = async () => {
    try {
      const response = await fetch('http://localhost:8000/v2/integrations/status');
      const data = await response.json();
      setIntegrations(data.integrations || []);
    } catch (error) {
      console.error('Error fetching integrations:', error);
    } finally {
      setLoading(false);
    }
  };

  const connectIntegration = async () => {
    if (!selectedProvider || Object.keys(config).length === 0) return;

    try {
      const response = await fetch('http://localhost:8000/v2/integrations/connect', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          provider: selectedProvider,
          config: config,
        }),
      });

      if (response.ok) {
        fetchIntegrations();
        setSelectedProvider("");
        setConfig({});
      }
    } catch (error) {
      console.error('Error connecting integration:', error);
    }
  };

  const disconnectIntegration = async (provider: string) => {
    try {
      const response = await fetch(`http://localhost:8000/v2/integrations/disconnect`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ provider }),
      });

      if (response.ok) {
        fetchIntegrations();
      }
    } catch (error) {
      console.error('Error disconnecting integration:', error);
    }
  };

  const testIntegration = async (provider: string) => {
    try {
      const response = await fetch(`http://localhost:8000/v2/integrations/test`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ provider }),
      });

      const result = await response.json();
      alert(`Test result for ${provider}: ${result.status}`);
    } catch (error) {
      console.error('Error testing integration:', error);
    }
  };

  const getProviderConfig = (provider: string) => {
    const configs = {
      uipath: {
        api_key: "",
        base_url: "https://cloud.uipath.com",
        tenant: "",
      },
      n8n: {
        webhook_url: "",
        api_key: "",
        base_url: "",
      },
      mendix: {
        app_id: "",
        api_key: "",
        environment: "production",
      },
      prismatic: {
        api_key: "",
        instance_url: "",
        organization: "",
      },
    };
    return configs[provider as keyof typeof configs] || {};
  };

  if (loading) {
    return (
      <>
        <Header />
        <main className="max-w-6xl mx-auto p-8">
          <div className="text-center">Loading integrations...</div>
        </main>
        <Footer />
      </>
    );
  }

  return (
    <>
      <Header />
      <main className="max-w-6xl mx-auto p-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold">Integrations</h1>
          <p className="text-gray-600">Connect external platforms and automation tools</p>
        </div>

        {/* Connect New Integration */}
        <div className="bg-white p-6 rounded-lg shadow border mb-8">
          <h2 className="text-xl font-semibold mb-4">Connect New Integration</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Provider
              </label>
              <select
                value={selectedProvider}
                onChange={(e) => {
                  setSelectedProvider(e.target.value);
                  setConfig(getProviderConfig(e.target.value));
                }}
                className="w-full p-2 border border-gray-300 rounded-md"
              >
                <option value="">Select a provider</option>
                <option value="uipath">UiPath</option>
                <option value="n8n">n8n</option>
                <option value="mendix">Mendix</option>
                <option value="prismatic">Prismatic</option>
              </select>
            </div>
          </div>

          {selectedProvider && (
            <div className="mt-4">
              <h3 className="text-lg font-medium mb-3">Configuration for {selectedProvider}</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {Object.entries(config).map(([key, value]) => (
                  <div key={key}>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      {key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                    </label>
                    <input
                      type={key.includes('key') || key.includes('secret') ? 'password' : 'text'}
                      value={value}
                      onChange={(e) => setConfig({ ...config, [key]: e.target.value })}
                      className="w-full p-2 border border-gray-300 rounded-md"
                      placeholder={`Enter ${key.replace(/_/g, ' ')}`}
                    />
                  </div>
                ))}
              </div>
              <button
                onClick={connectIntegration}
                className="mt-4 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
              >
                Connect {selectedProvider}
              </button>
            </div>
          )}
        </div>

        {/* Connected Integrations */}
        <div className="bg-white p-6 rounded-lg shadow border">
          <h2 className="text-xl font-semibold mb-4">Connected Integrations</h2>
          {integrations.length === 0 ? (
            <p className="text-gray-500">No integrations connected yet.</p>
          ) : (
            <div className="space-y-4">
              {integrations.map((integration) => (
                <div key={integration.provider} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="text-lg font-medium capitalize">{integration.provider}</h3>
                      <p className="text-sm text-gray-600">
                        Connected: {new Date(integration.connected_at).toLocaleDateString()}
                      </p>
                      <span className={`inline-block px-2 py-1 text-xs rounded-full ${
                        integration.status === 'connected' 
                          ? 'bg-green-100 text-green-800' 
                          : 'bg-red-100 text-red-800'
                      }`}>
                        {integration.status}
                      </span>
                    </div>
                    <div className="flex space-x-2">
                      <button
                        onClick={() => testIntegration(integration.provider)}
                        className="bg-green-600 text-white px-3 py-1 rounded text-sm hover:bg-green-700"
                      >
                        Test
                      </button>
                      <button
                        onClick={() => disconnectIntegration(integration.provider)}
                        className="bg-red-600 text-white px-3 py-1 rounded text-sm hover:bg-red-700"
                      >
                        Disconnect
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Integration Benefits */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-white p-4 rounded-lg shadow border text-center">
            <div className="text-2xl font-bold text-blue-600 mb-2">UiPath</div>
            <p className="text-sm text-gray-600">RPA automation workflows and process optimization</p>
          </div>
          <div className="bg-white p-4 rounded-lg shadow border text-center">
            <div className="text-2xl font-bold text-green-600 mb-2">n8n</div>
            <p className="text-sm text-gray-600">Workflow automation and API integrations</p>
          </div>
          <div className="bg-white p-4 rounded-lg shadow border text-center">
            <div className="text-2xl font-bold text-purple-600 mb-2">Mendix</div>
            <p className="text-sm text-gray-600">Low-code application development platform</p>
          </div>
          <div className="bg-white p-4 rounded-lg shadow border text-center">
            <div className="text-2xl font-bold text-orange-600 mb-2">Prismatic</div>
            <p className="text-sm text-gray-600">Enterprise integration platform and connectors</p>
          </div>
        </div>
      </main>
      <Footer />
    </>
  );
}
