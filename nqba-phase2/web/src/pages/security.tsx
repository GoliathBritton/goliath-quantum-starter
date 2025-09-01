"use client";
import { useState, useEffect } from "react";
import Header from "../components/Header";
import Footer from "../components/Footer";

interface SecurityStatus {
  quantum_backend: string;
  key_rotation_enabled: boolean;
  encryption_status: string;
  compliance_status: string;
  last_audit: string;
}

interface AuditLog {
  id: string;
  action: string;
  user: string;
  timestamp: string;
  details: Record<string, any>;
  status: string;
}

export default function Security() {
  const [securityStatus, setSecurityStatus] = useState<SecurityStatus | null>(null);
  const [auditLogs, setAuditLogs] = useState<AuditLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [keyId, setKeyId] = useState("");
  const [rotationReason, setRotationReason] = useState("scheduled_rotation");

  useEffect(() => {
    fetchSecurityData();
  }, []);

  const fetchSecurityData = async () => {
    try {
      const [statusResponse, logsResponse] = await Promise.all([
        fetch('http://localhost:8000/v2/security/status'),
        fetch('http://localhost:8000/v2/security/audit-logs')
      ]);
      
      const statusData = await statusResponse.json();
      const logsData = await logsResponse.json();
      
      setSecurityStatus(statusData);
      setAuditLogs(logsData.logs || []);
    } catch (error) {
      console.error('Error fetching security data:', error);
    } finally {
      setLoading(false);
    }
  };

  const rotateKey = async () => {
    if (!keyId) return;

    try {
      const response = await fetch('http://localhost:8000/v2/security/rotate-key', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          key_id: keyId,
          reason: rotationReason,
        }),
      });

      if (response.ok) {
        alert('Key rotation initiated successfully');
        fetchSecurityData();
        setKeyId("");
        setRotationReason("scheduled_rotation");
      }
    } catch (error) {
      console.error('Error rotating key:', error);
    }
  };

  const runComplianceCheck = async () => {
    try {
      const response = await fetch('http://localhost:8000/v2/security/compliance-check', {
        method: 'POST',
      });

      const result = await response.json();
      alert(`Compliance check completed: ${result.status}`);
      fetchSecurityData();
    } catch (error) {
      console.error('Error running compliance check:', error);
    }
  };

  const getEncryptionStatus = async () => {
    try {
      const response = await fetch('http://localhost:8000/v2/security/encryption-status');
      const result = await response.json();
      alert(`Encryption Status: ${result.status}`);
    } catch (error) {
      console.error('Error getting encryption status:', error);
    }
  };

  if (loading) {
    return (
      <>
        <Header />
        <main className="max-w-6xl mx-auto p-8">
          <div className="text-center">Loading security data...</div>
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
          <h1 className="text-3xl font-bold">Quantum Security</h1>
          <p className="text-gray-600">Quantum-anchored security and compliance management</p>
        </div>

        {securityStatus && (
          <>
            {/* Security Status Overview */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              <div className="bg-white p-6 rounded-lg shadow border">
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">{securityStatus.quantum_backend}</div>
                  <div className="text-sm text-gray-600">Quantum Backend</div>
                </div>
              </div>
              <div className="bg-white p-6 rounded-lg shadow border">
                <div className="text-center">
                  <div className={`text-2xl font-bold ${securityStatus.key_rotation_enabled ? 'text-green-600' : 'text-red-600'}`}>
                    {securityStatus.key_rotation_enabled ? '✓' : '✗'}
                  </div>
                  <div className="text-sm text-gray-600">Key Rotation</div>
                </div>
              </div>
              <div className="bg-white p-6 rounded-lg shadow border">
                <div className="text-center">
                  <div className={`text-2xl font-bold ${
                    securityStatus.encryption_status === 'active' ? 'text-green-600' : 'text-yellow-600'
                  }`}>
                    {securityStatus.encryption_status === 'active' ? '✓' : '⚠'}
                  </div>
                  <div className="text-sm text-gray-600">Encryption</div>
                </div>
              </div>
              <div className="bg-white p-6 rounded-lg shadow border">
                <div className="text-center">
                  <div className={`text-2xl font-bold ${
                    securityStatus.compliance_status === 'compliant' ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {securityStatus.compliance_status === 'compliant' ? '✓' : '✗'}
                  </div>
                  <div className="text-sm text-gray-600">Compliance</div>
                </div>
              </div>
            </div>

            {/* Key Rotation */}
            <div className="bg-white p-6 rounded-lg shadow border mb-8">
              <h2 className="text-xl font-semibold mb-4">Quantum-Anchored Key Rotation</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Key ID
                  </label>
                  <input
                    type="text"
                    value={keyId}
                    onChange={(e) => setKeyId(e.target.value)}
                    className="w-full p-2 border border-gray-300 rounded-md"
                    placeholder="Enter key ID"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Reason
                  </label>
                  <select
                    value={rotationReason}
                    onChange={(e) => setRotationReason(e.target.value)}
                    className="w-full p-2 border border-gray-300 rounded-md"
                  >
                    <option value="scheduled_rotation">Scheduled Rotation</option>
                    <option value="security_incident">Security Incident</option>
                    <option value="compliance_requirement">Compliance Requirement</option>
                    <option value="manual_request">Manual Request</option>
                  </select>
                </div>
                <div className="flex items-end">
                  <button
                    onClick={rotateKey}
                    disabled={!keyId}
                    className="w-full bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:bg-gray-400"
                  >
                    Rotate Key
                  </button>
                </div>
              </div>
              <p className="text-sm text-gray-600">
                Quantum-anchored key rotation uses Dynex to ensure cryptographic security and compliance.
              </p>
            </div>

            {/* Security Actions */}
            <div className="bg-white p-6 rounded-lg shadow border mb-8">
              <h2 className="text-xl font-semibold mb-4">Security Actions</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <button
                  onClick={runComplianceCheck}
                  className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700"
                >
                  Run Compliance Check
                </button>
                <button
                  onClick={getEncryptionStatus}
                  className="bg-purple-600 text-white px-4 py-2 rounded-md hover:bg-purple-700"
                >
                  Check Encryption Status
                </button>
              </div>
            </div>

            {/* Audit Logs */}
            <div className="bg-white p-6 rounded-lg shadow border">
              <h2 className="text-xl font-semibold mb-4">Audit Logs</h2>
              {auditLogs.length === 0 ? (
                <p className="text-gray-500">No audit logs available.</p>
              ) : (
                <div className="space-y-4">
                  {auditLogs.map((log) => (
                    <div key={log.id} className="border border-gray-200 rounded-lg p-4">
                      <div className="flex items-center justify-between">
                        <div>
                          <h3 className="font-medium">{log.action}</h3>
                          <p className="text-sm text-gray-600">
                            User: {log.user} • {new Date(log.timestamp).toLocaleString()}
                          </p>
                          <p className="text-sm text-gray-600">
                            Details: {JSON.stringify(log.details)}
                          </p>
                        </div>
                        <span className={`inline-block px-2 py-1 text-xs rounded-full ${
                          log.status === 'success' 
                            ? 'bg-green-100 text-green-800' 
                            : log.status === 'pending'
                            ? 'bg-yellow-100 text-yellow-800'
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {log.status}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div className="mt-6 text-sm text-gray-500 text-center">
              Last audit: {new Date(securityStatus.last_audit).toLocaleString()}
            </div>
          </>
        )}

        {/* Security Features Overview */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white p-4 rounded-lg shadow border text-center">
            <div className="text-2xl font-bold text-blue-600 mb-2">Quantum Anchoring</div>
            <p className="text-sm text-gray-600">Dynex-backed cryptographic security with 410x performance</p>
          </div>
          <div className="bg-white p-4 rounded-lg shadow border text-center">
            <div className="text-2xl font-bold text-green-600 mb-2">Compliance</div>
            <p className="text-sm text-gray-600">Automated compliance checks and audit trail management</p>
          </div>
          <div className="bg-white p-4 rounded-lg shadow border text-center">
            <div className="text-2xl font-bold text-purple-600 mb-2">Encryption</div>
            <p className="text-sm text-gray-600">Field-level encryption with quantum-enhanced key management</p>
          </div>
        </div>
      </main>
      <Footer />
    </>
  );
}
