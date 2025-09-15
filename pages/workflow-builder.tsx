import React, { useState, useCallback } from "react";
import ReactFlow, {
  Node,
  Edge,
  addEdge,
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
  Connection,
  ConnectionMode,
} from "react-flow-renderer";
import Modal from "react-modal";
import QuantumUpsellModal from "../components/QuantumUpsellModal";
import QuantumNexusEngine from '../components/QuantumNexusEngine';
import PricingPyramid from '../components/PricingPyramid';
import axios from 'axios';

type NodeData = {
  label: string;
  premium?: boolean;
  description?: string;
};

const initialNodes: Node<NodeData>[] = [
  {
    id: "1",
    type: "input",
    data: { label: "Lead Capture" },
    position: { x: 250, y: 25 },
  },
  {
    id: "2",
    data: { label: "Email Validation", premium: true, description: "AI-powered email validation with quantum scoring" },
    position: { x: 100, y: 125 },
  },
  {
    id: "3",
    data: { label: "Lead Scoring", premium: true, description: "QUBO-optimized lead scoring algorithm" },
    position: { x: 400, y: 125 },
  },
  {
    id: "4",
    data: { label: "CRM Integration" },
    position: { x: 250, y: 250 },
  },
  {
    id: "5",
    type: "output",
    data: { label: "Sales Handoff" },
    position: { x: 250, y: 350 },
  },
];

const initialEdges: Edge[] = [
  { id: "e1-2", source: "1", target: "2" },
  { id: "e1-3", source: "1", target: "3" },
  { id: "e2-4", source: "2", target: "4" },
  { id: "e3-4", source: "3", target: "4" },
  { id: "e4-5", source: "4", target: "5" },
];

const nodeTypes = {
  default: ({ data, selected }: { data: NodeData; selected: boolean }) => (
    <div
      className={`px-4 py-2 shadow-md rounded-md bg-white border-2 ${
        selected ? "border-flyfox" : "border-gray-200"
      }`}
    >
      <div className="flex items-center">
        <div className="ml-2">
          <div className="text-lg font-bold">{data.label}</div>
          {data.premium && (
            <span className="px-1 rounded bg-pink-600 text-white ml-1 text-xs">
              ⚡ Quantum
            </span>
          )}
        </div>
      </div>
    </div>
  ),
};

export default function WorkflowBuilder() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedNode, setSelectedNode] = useState<Node<NodeData> | null>(null);
  const [showUpsellModal, setShowUpsellModal] = useState(false);
  const [upsellContext, setUpsellContext] = useState("workflow_builder");
  const [userHasPremium, setUserHasPremium] = useState(false); // In production, get from user context
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [jobStatus, setJobStatus] = useState<any>(null);
  const [currentJobId, setCurrentJobId] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'builder' | 'Quantum Nexus' | 'pricing'>('builder');
  const [userTier, setUserTier] = useState<'basic' | 'premium' | 'elite'>('basic');

  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  const onNodeDoubleClick = useCallback(
    (event: React.MouseEvent, node: Node<NodeData>) => {
      if (node.data.premium && !userHasPremium) {
        setUpsellContext("premium_node");
        setShowUpsellModal(true);
      } else if (node.data.premium) {
        setSelectedNode(node);
        setModalOpen(true);
      }
    },
    [userHasPremium]
  );

  const handleUpgrade = () => {
    // In production, integrate with Stripe/payment processor
    console.log("Redirecting to payment processor...");
    // Simulate successful upgrade
    setTimeout(() => {
      setUserHasPremium(true);
      setShowUpsellModal(false);
      alert("Welcome to Quantum Premium! 🚀");
    }, 1000);
  };

  const submitToQuantum = async () => {
    try {
      setIsSubmitting(true);
      
      const response = await axios.post('/api/quantum/submit', {
        workflowId: 'workflow_' + Date.now(),
        nodes: nodes,
        userId: 'user_' + Date.now(),
        priority: 'normal',
        metadata: {
          submittedFrom: 'workflow_builder',
          nodeCount: nodes.length,
          edgeCount: edges.length
        }
      });
      
      const jobId = response.data.jobId;
      setCurrentJobId(jobId);
      
      // Start polling for job status
      pollJobStatus(jobId);
      
    } catch (error) {
      console.error('Error submitting to quantum:', error);
      alert('Failed to submit workflow to quantum processing');
    } finally {
      setIsSubmitting(false);
    }
  };

  const pollJobStatus = async (jobId: string) => {
    try {
      const response = await axios.get(`/api/quantum/status/${jobId}`);
      setJobStatus(response.data);
      
      // Continue polling if job is not completed
      if (response.data.status === 'queued' || response.data.status === 'initializing' || response.data.status === 'running') {
        setTimeout(() => pollJobStatus(jobId), 2000);
      }
    } catch (error) {
      console.error('Error polling job status:', error);
    }
  };

  const saveWorkflow = async () => {
    try {
      const response = await fetch("/api/workflows", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nodes, edges, name: "Demo Workflow" }),
      });
      const result = await response.json();
      alert(`Workflow saved with ID: ${result.id}`);
    } catch (error) {
      alert("Error saving workflow");
    }
  };

  return (
    <div className="min-h-screen bg-quantum-gradient">
      <div className="p-6">
        <div className="max-w-7xl mx-auto">
          <div className="flex justify-between items-center mb-6">
            <h1 className="text-3xl font-bold text-white bg-gradient-to-r from-flyfox-400 to-quantum-400 bg-clip-text text-transparent quantum-glow">
              Quantum Workflow Builder
            </h1>
            
            {/* Tab Navigation */}
            <div className="flex gap-4">
              <button
                onClick={() => setActiveTab('builder')}
                className={`px-6 py-3 rounded-lg font-medium transition-all ${
                  activeTab === 'builder'
                    ? 'bg-quantum-600 text-white shadow-lg'
                    : 'bg-space-700 text-gray-300 hover:bg-space-600'
                }`}
              >
                Workflow Builder
              </button>
              <button
                onClick={() => setActiveTab('Quantum Nexus')}
                className={`px-6 py-3 rounded-lg font-medium transition-all flex items-center gap-2 ${
                  activeTab === 'Quantum Nexus'
                    ? 'bg-gradient-to-r from-flyfox-600 to-quantum-600 text-white shadow-lg quantum-glow'
                    : 'bg-space-700 text-gray-300 hover:bg-space-600'
                }`}
              >
                <span>🔮</span>
                Quantum Omniscient™
                {userTier === 'basic' && (
                  <span className="text-xs bg-flyfox-500 px-2 py-1 rounded-full">PREMIUM</span>
                )}
              </button>
              <button
                onClick={() => setActiveTab('pricing')}
                className={`px-6 py-3 rounded-lg font-medium transition-all ${
                  activeTab === 'pricing'
                    ? 'bg-gradient-to-r from-yellow-500 to-orange-500 text-white shadow-lg'
                    : 'bg-space-700 text-gray-300 hover:bg-space-600'
                }`}
              >
                💎 Pricing Pyramid
              </button>
            </div>
            <div className="flex gap-3">
              <button
                onClick={saveWorkflow}
                className="px-4 py-2 rounded-md bg-flyfox text-black font-medium hover:bg-opacity-90"
              >
                Save Workflow
              </button>
              <button className="px-4 py-2 rounded-md bg-gray-700 text-white hover:bg-gray-600">
                Deploy
              </button>
              <button
                onClick={submitToQuantum}
                disabled={isSubmitting || nodes.length === 0}
                className="px-4 py-2 bg-gradient-to-r from-quantum-600 to-flyfox-600 text-white rounded-lg hover:from-quantum-700 hover:to-flyfox-700 transition-all quantum-glow disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
              >
                {isSubmitting ? (
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                ) : (
                  <span>⚡</span>
                )}
                {isSubmitting ? 'Submitting...' : 'Submit to Quantum'}
              </button>
            </div>
          </div>

          {/* Quantum Job Status */}
          {jobStatus && (
            <div className="mb-6 p-4 bg-space-800/50 border border-quantum-500/30 rounded-lg">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-lg font-semibold text-white flex items-center gap-2">
                  <span>⚡</span>
                  Quantum Job Status
                </h3>
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                  jobStatus.status === 'completed' ? 'bg-green-500/20 text-green-400' :
                  jobStatus.status === 'running' ? 'bg-yellow-500/20 text-yellow-400' :
                  jobStatus.status === 'failed' ? 'bg-red-500/20 text-red-400' :
                  'bg-blue-500/20 text-blue-400'
                }`}>
                  {jobStatus.status.toUpperCase()}
                </span>
              </div>
              <div className="text-gray-300 text-sm">
                <p><strong>Job ID:</strong> {currentJobId}</p>
                <p><strong>Created:</strong> {new Date(jobStatus.created).toLocaleString()}</p>
                {jobStatus.result && (
                  <div className="mt-2 p-3 bg-space-700/50 rounded border border-flyfox-500/30">
                    <p><strong>Result:</strong></p>
                    <p>Score: {jobStatus.result.score?.toFixed(2)}</p>
                    <p>Details: {jobStatus.result.details}</p>
                  </div>
                )}
              </div>
            </div>
          )}

          {activeTab === 'builder' ? (
            <div className="bg-white/10 rounded-xl p-4 backdrop-blur-sm">
              <div className="h-[600px] rounded-lg overflow-hidden border border-gray-600">
                <ReactFlow
                  nodes={nodes}
                  edges={edges}
                  onNodesChange={onNodesChange}
                  onEdgesChange={onEdgesChange}
                  onConnect={onConnect}
                  onNodeDoubleClick={onNodeDoubleClick}
                  nodeTypes={nodeTypes}
                  connectionMode={ConnectionMode.Loose}
                  fitView
                >
                  <Background />
                  <Controls />
                  <MiniMap />
                </ReactFlow>
              </div>

              <div className="mt-4 text-sm text-gray-300">
                Tip: Double-click a node. Premium steps show a{" "}
                <span className="px-1 rounded bg-pink-600 text-white ml-1">
                  ⚡ Quantum
                </span>{" "}
                badge and open the upsell modal.
              </div>
            </div>
          ) : activeTab === 'Quantum Nexus' ? (
            <QuantumNexusEngine 
              userTier={userTier}
              onUpgrade={() => setShowUpsellModal(true)}
            />
          ) : (
            <PricingPyramid />
          )}

          <Modal
            isOpen={modalOpen}
            onRequestClose={() => setModalOpen(false)}
            className="max-w-xl mx-auto mt-28 bg-white rounded-lg p-6"
            overlayClassName="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center"
          >
            <h3 className="text-lg font-bold mb-3">Quantum Workflow Upgrade</h3>
            <p className="text-sm text-gray-700 mb-4">
              This step uses heavy Quantum QUBO optimization (Dynex). It requires
              a Quantum Premium add-on. Benefits: faster optimization, higher
              conversion, exact optimization for multidimensional constraints.
            </p>
            {selectedNode && (
              <div className="mb-4 p-3 bg-gray-100 rounded">
                <strong>{selectedNode.data.label}</strong>
                <p className="text-sm text-gray-600 mt-1">
                  {selectedNode.data.description}
                </p>
              </div>
            )}
            <div className="flex justify-end gap-3">
              <button
                className="px-4 py-2 rounded-md border"
                onClick={() => setModalOpen(false)}
              >
                Close
              </button>
              <button
                className="px-4 py-2 rounded-md bg-flyfox text-black"
                onClick={() => {
                  alert("Upsell checkout - demo");
                }}
              >
                Purchase Quantum Add-on
              </button>
            </div>
          </Modal>

          {/* Quantum Upsell Modal */}
          <QuantumUpsellModal
            isOpen={showUpsellModal}
            onClose={() => setShowUpsellModal(false)}
            onUpgrade={handleUpgrade}
            triggerContext={upsellContext}
          />
        </div>
      </div>
    </div>
  );
}

// Set the app element for react-modal accessibility
if (typeof window !== "undefined") {
  Modal.setAppElement("#__next");
}