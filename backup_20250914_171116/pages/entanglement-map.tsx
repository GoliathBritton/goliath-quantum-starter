import React, { useRef, useEffect, useState } from "react";
import dynamic from "next/dynamic";
import QuantumUpsellModal from "../components/QuantumUpsellModal";

const ForceGraph3D = dynamic(() => import("react-force-graph-3d"), {
  ssr: false,
});

type NodeType = { id: string; name: string; group?: string; activity?: number };
type LinkType = { source: string; target: string; weight?: number };

const sampleNodes: NodeType[] = [
  { id: "QHC", name: "Quantum High Council", group: "governance", activity: 8 },
  { id: "NQBA", name: "NQBA Core", group: "core", activity: 10 },
  { id: "QSAI", name: "Q-SAI", group: "core", activity: 9 },
  { id: "AGENTS", name: "Agent Factory", group: "agents", activity: 7 },
  { id: "CLIENTS", name: "Clients", group: "clients", activity: 5 },
  { id: "CTO", name: "CTO", group: "roles", activity: 6 },
  { id: "CMO", name: "CMO", group: "roles", activity: 4 },
  { id: "DYNEX", name: "Dynex Network", group: "quantum", activity: 9 },
  { id: "FLYFOX", name: "FLYFOX AI", group: "core", activity: 8 },
  { id: "GOLIATH", name: "Goliath Capital", group: "business", activity: 6 },
  { id: "SIGMA", name: "Sigma Select", group: "business", activity: 7 },
];

const sampleLinks: LinkType[] = [
  { source: "QHC", target: "NQBA", weight: 4 },
  { source: "NQBA", target: "QSAI", weight: 6 },
  { source: "NQBA", target: "AGENTS", weight: 7 },
  { source: "AGENTS", target: "CLIENTS", weight: 6 },
  { source: "NQBA", target: "CTO", weight: 4 },
  { source: "NQBA", target: "CMO", weight: 3 },
  { source: "NQBA", target: "DYNEX", weight: 8 },
  { source: "FLYFOX", target: "NQBA", weight: 9 },
  { source: "GOLIATH", target: "NQBA", weight: 5 },
  { source: "SIGMA", target: "NQBA", weight: 6 },
  { source: "DYNEX", target: "QSAI", weight: 7 },
];

const groupColors: { [key: string]: string } = {
  governance: "#8B5CF6",
  core: "#06B6D4",
  agents: "#10B981",
  clients: "#F59E0B",
  roles: "#EF4444",
  quantum: "#EC4899",
  business: "#6366F1",
};

export default function EntanglementMap() {
  const fgRef = useRef<any>();
  const [nodes, setNodes] = useState(sampleNodes);
  const [links, setLinks] = useState(sampleLinks);
  const [selectedGroup, setSelectedGroup] = useState<string | null>(null);
  const [showUpsellModal, setShowUpsellModal] = useState(false);
  const [userHasPremium, setUserHasPremium] = useState(false); // In production, get from user context

  useEffect(() => {
    // Demo: animate activity pulses over time
    const interval = setInterval(() => {
      setNodes((prev) =>
        prev.map((n) => ({
          ...n,
          activity: Math.max(
            1,
            (n.activity || 1) + (Math.random() - 0.5) * 2
          ),
        }))
      );
    }, 1500);
    return () => clearInterval(interval);
  }, []);

  const filteredNodes = selectedGroup
    ? nodes.filter((n) => n.group === selectedGroup)
    : nodes;

  const filteredLinks = selectedGroup
    ? links.filter(
        (l) =>
          filteredNodes.some((n) => n.id === l.source) &&
          filteredNodes.some((n) => n.id === l.target)
      )
    : links;

  const createNodeObject = (node: any) => {
    // Create a sprite with canvas texture for better text rendering
    const sprite = new (window as any).THREE.Sprite();
    const canvas = document.createElement("canvas");
    canvas.width = 256;
    canvas.height = 64;
    const ctx = canvas.getContext("2d");
    
    if (ctx) {
      // Background
      ctx.fillStyle = groupColors[node.group] || "#111827";
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      // Text
      ctx.font = "18px Inter, sans-serif";
      ctx.fillStyle = "#ffffff";
      ctx.textAlign = "center";
      ctx.fillText(node.name, canvas.width / 2, canvas.height / 2 + 6);
    }
    
    const texture = new (window as any).THREE.CanvasTexture(canvas);
    const material = new (window as any).THREE.SpriteMaterial({ map: texture });
    sprite.material = material;
    sprite.scale.set(8 + (node.activity || 1), 2.5, 1);
    
    return sprite;
  };

  return (
    <div className="min-h-screen bg-quantum-gradient">
      <div className="p-6">
        <div className="max-w-7xl mx-auto">
          <div className="flex justify-between items-center mb-6">
            <h1 className="text-3xl font-bold text-white bg-gradient-to-r from-flyfox-400 to-quantum-400 bg-clip-text text-transparent quantum-glow">
              3D Entanglement Map — Living Ecosystem
            </h1>
            <div className="flex gap-2">
              <button
                onClick={() => setSelectedGroup(null)}
                className={`px-3 py-2 rounded text-sm ${
                  !selectedGroup
                    ? "bg-flyfox text-black"
                    : "bg-gray-700 text-white hover:bg-gray-600"
                }`}
              >
                All
              </button>
              {Object.keys(groupColors).map((group) => (
                <button
                  key={group}
                  onClick={() => setSelectedGroup(group)}
                  className={`px-3 py-2 rounded text-sm capitalize ${
                    selectedGroup === group
                      ? "bg-flyfox text-black"
                      : "bg-gray-700 text-white hover:bg-gray-600"
                  }`}
                >
                  {group}
                </button>
              ))}
            </div>
          </div>

          <div className="bg-white/5 rounded-xl p-4 backdrop-blur-sm">
            <div className="h-[720px] rounded-lg overflow-hidden border border-gray-700">
              <ForceGraph3D
                ref={fgRef}
                graphData={{
                  nodes: filteredNodes.map((n) => ({ ...n, val: n.activity })),
                  links: filteredLinks,
                }}
                nodeAutoColorBy="group"
                nodeThreeObject={createNodeObject}
                linkWidth={(l: any) => (l.weight || 1)}
                linkColor={() => "rgba(255,255,255,0.15)"}
                onNodeClick={(node: any) => {
                  // Check if this is a premium feature
                  if ((node.group === "quantum" || node.group === "dynex") && !userHasPremium) {
                    setShowUpsellModal(true);
                    return;
                  }
                  
                  alert(
                    `${node.name}\nGroup: ${node.group}\nActivity: ${Math.round(
                      node.activity
                    )}`
                  );
                }}
                backgroundColor="#071024"
                showNavInfo={false}
                controlType="orbit"
              />
            </div>

            <div className="mt-4 flex flex-wrap gap-4 text-sm">
              <div className="bg-flyfox px-3 py-2 rounded text-black font-medium">
                Live
              </div>
              <div className="px-3 py-2 rounded bg-gray-800 text-white">
                Entanglement strength = link weight
              </div>
              <div className="px-3 py-2 rounded bg-gray-800 text-white">
                Nodes sized by activity
              </div>
              <div className="px-3 py-2 rounded bg-gray-800 text-white">
                Click nodes for details
              </div>
            </div>

            <div className="mt-4 grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-2">
              {Object.entries(groupColors).map(([group, color]) => (
                <div key={group} className="flex items-center gap-2 text-sm">
                  <div
                    className="w-3 h-3 rounded"
                    style={{ backgroundColor: color }}
                  ></div>
                  <span className="text-gray-300 capitalize">{group}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
      
      {/* Quantum Upsell Modal */}
      <QuantumUpsellModal
        isOpen={showUpsellModal}
        onClose={() => setShowUpsellModal(false)}
        onUpgrade={() => {
          // In production, integrate with Stripe/payment processor
          console.log("Redirecting to payment processor...");
          // Simulate successful upgrade
          setTimeout(() => {
            setUserHasPremium(true);
            setShowUpsellModal(false);
            alert("Welcome to Quantum Premium! Advanced entanglement features unlocked! 🚀");
          }, 1000);
        }}
        triggerContext="entanglement_map"
      />
    </div>
  );
}