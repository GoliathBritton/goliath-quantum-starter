import React, { useState, useCallback, useRef, useEffect } from 'react';
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
  EdgeChange,
  NodeChange,
  ReactFlowProvider,
  Panel,
  useReactFlow,
  ReactFlowInstance,
} from 'reactflow';
import 'reactflow/dist/style.css';
import useWebSocket from '../hooks/useWebSocket';
import PipelineLibrary from './PipelineLibrary';

// Import custom node components
import DataSourceNode from './nodes/DataSourceNode';
import ProcessorNode from './nodes/ProcessorNode';
import AIModelNode from './nodes/AIModelNode';
import QuantumNode from './nodes/QuantumNode';
import QuantumGateNode from './nodes/QuantumGateNode';
import QuantumCircuitNode from './nodes/QuantumCircuitNode';
import QuantumAlgorithmNode from './nodes/QuantumAlgorithmNode';
import OutputNode from './nodes/OutputNode';
import ConditionalNode from './nodes/ConditionalNode';
import IntegrationNode from './nodes/IntegrationNode';

// Types
interface PipelineBuilderProps {
  onCompile?: (compiledRecipe: CompiledRecipe) => void;
  onSave?: (recipe: Recipe) => void;
  initialRecipe?: Recipe;
  className?: string;
}

interface Recipe {
  id?: string;
  name: string;
  description?: string;
  nodes: Node[];
  edges: Edge[];
  metadata?: {
    version: string;
    created_at: string;
    updated_at: string;
    author?: string;
  };
}

interface CompiledRecipe {
  recipe_id: string;
  compiled_code: string;
  execution_plan: any;
  estimated_cost: number;
  estimated_duration: number;
  warnings: string[];
}

interface CompileRequest {
  flow_definition: {
    nodes: Node[];
    edges: Edge[];
    metadata: any;
  };
  optimization_level: 'basic' | 'optimized' | 'aggressive';
  target_runtime: 'python' | 'javascript' | 'quantum';
}

// Node Types Registry
const nodeTypes = {
  dataSource: DataSourceNode,
  processor: ProcessorNode,
  aiModel: AIModelNode,
  quantum: QuantumNode,
  quantumGate: QuantumGateNode,
  quantumCircuit: QuantumCircuitNode,
  quantumAlgorithm: QuantumAlgorithmNode,
  output: OutputNode,
  conditional: ConditionalNode,
  integration: IntegrationNode,
};

// Initial nodes and edges
const initialNodes: Node[] = [];
const initialEdges: Edge[] = [];

// Node Templates for Drag & Drop
const nodeTemplates = [
  {
    type: 'dataSource',
    label: 'Data Source',
    icon: '📊',
    description: 'Import data from various sources',
    category: 'Input',
  },
  {
    type: 'processor',
    label: 'Data Processor',
    icon: '⚙️',
    description: 'Transform and process data',
    category: 'Processing',
  },
  {
    type: 'aiModel',
    label: 'AI Model',
    icon: '🤖',
    description: 'Apply AI/ML models',
    category: 'AI/ML',
  },
  {
    type: 'quantum',
    label: 'Quantum Compute',
    icon: '⚛️',
    description: 'Basic quantum computing operations',
    category: 'Quantum',
  },
  {
    type: 'quantumGate',
    label: 'Quantum Gate',
    icon: '🚪',
    description: 'Individual quantum gates (H, X, Y, Z, CNOT)',
    category: 'Quantum',
  },
  {
    type: 'quantumCircuit',
    label: 'Quantum Circuit',
    icon: '🔄',
    description: 'Complex quantum circuits (QAOA, VQE, QFT)',
    category: 'Quantum',
  },
  {
    type: 'quantumAlgorithm',
    label: 'Quantum Algorithm',
    icon: '🧠',
    description: 'High-level quantum algorithms (Portfolio, Risk, Energy)',
    category: 'Quantum',
  },
  {
    type: 'conditional',
    label: 'Conditional',
    icon: '🔀',
    description: 'Conditional logic and branching',
    category: 'Logic',
  },
  {
    type: 'integration',
    label: 'Integration',
    icon: '🔗',
    description: 'Third-party integrations',
    category: 'Integration',
  },
  {
    type: 'output',
    label: 'Output',
    icon: '📤',
    description: 'Export results',
    category: 'Output',
  },
];

const PipelineBuilderInner: React.FC<PipelineBuilderProps> = ({
  onCompile,
  onSave,
  initialRecipe,
  className = '',
}) => {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialRecipe?.nodes || initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialRecipe?.edges || initialEdges);
  const [recipeName, setRecipeName] = useState(initialRecipe?.name || 'Untitled Recipe');
  const [recipeDescription, setRecipeDescription] = useState(initialRecipe?.description || '');
  const [isCompiling, setIsCompiling] = useState(false);
  const [compilationResult, setCompilationResult] = useState<CompiledRecipe | null>(null);
  const [optimizationLevel, setOptimizationLevel] = useState<'basic' | 'optimized' | 'aggressive'>('optimized');
  const [targetRuntime, setTargetRuntime] = useState<'python' | 'javascript' | 'quantum'>('python');
  const [showSidebar, setShowSidebar] = useState(true);
  const [selectedNode, setSelectedNode] = useState<Node | null>(null);
  const [compilationProgress, setCompilationProgress] = useState(0);
  const [compilationMessage, setCompilationMessage] = useState('');
  const [currentCompilationId, setCurrentCompilationId] = useState<string | null>(null);
  const [isSaving, setIsSaving] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [savedPipelineId, setSavedPipelineId] = useState<string | null>(initialRecipe?.id || null);
  const [showLibrary, setShowLibrary] = useState(false);
  
  const reactFlowWrapper = useRef<HTMLDivElement>(null);
  const { project, getViewport } = useReactFlow();
  const [reactFlowInstance, setReactFlowInstance] = useState<ReactFlowInstance | null>(null);
  
  // WebSocket connection for real-time updates
  const { isConnected, executionUpdates, subscribe, unsubscribe } = useWebSocket('ws://localhost:8000/ws');
  
  // Listen for compilation updates
  useEffect(() => {
    if (currentCompilationId && executionUpdates.has(currentCompilationId)) {
      const update = executionUpdates.get(currentCompilationId)!;
      setCompilationProgress(update.progress * 100);
      setCompilationMessage(update.message);
      
      if (update.status === 'completed' && update.result) {
        setCompilationResult({
          recipe_id: update.result.recipe_id,
          compiled_code: '',
          execution_plan: {},
          estimated_cost: 0,
          estimated_duration: 0,
          warnings: []
        });
        setIsCompiling(false);
        setCurrentCompilationId(null);
      } else if (update.status === 'failed') {
        setIsCompiling(false);
        setCurrentCompilationId(null);
        alert(`Compilation failed: ${update.error || 'Unknown error'}`);
      }
    }
  }, [currentCompilationId, executionUpdates]);

  // Generate unique ID for nodes
  const generateNodeId = () => `node_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

  // Handle connection between nodes
  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  // Handle drag over for drop zone
  const onDragOver = useCallback((event: React.DragEvent) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

  // Handle drop of new nodes
  const onDrop = useCallback(
    (event: React.DragEvent) => {
      event.preventDefault();

      const type = event.dataTransfer.getData('application/reactflow');
      const template = nodeTemplates.find(t => t.type === type);

      if (!type || !template || !reactFlowInstance) {
        return;
      }

      const position = reactFlowInstance.screenToFlowPosition({
        x: event.clientX,
        y: event.clientY,
      });

      const newNode: Node = {
        id: generateNodeId(),
        type,
        position,
        data: {
          label: template.label,
          icon: template.icon,
          description: template.description,
          config: {},
        },
      };

      setNodes((nds) => nds.concat(newNode));
    },
    [reactFlowInstance, setNodes]
  );

  // Handle node selection
  const onNodeClick = useCallback((event: React.MouseEvent, node: Node) => {
    setSelectedNode(node);
  }, []);

  // Compile recipe to executable format
  const compileRecipe = async () => {
    setIsCompiling(true);
    setCompilationResult(null);
    setCompilationProgress(0);
    setCompilationMessage('Preparing compilation...');

    try {
      // Transform nodes to match backend format
      const transformedNodes = nodes.map(node => ({
        id: node.id,
        type: node.type || 'default',
        position: {
          x: node.position.x,
          y: node.position.y
        },
        data: {
          label: node.data?.label || '',
          description: node.data?.description || '',
          config: node.data?.config || {},
          inputs: node.data?.inputs || [],
          outputs: node.data?.outputs || []
        },
        config: node.data?.config || {}
      }));

      // Transform edges to match backend format
      const transformedEdges = edges.map(edge => ({
        id: edge.id,
        source: edge.source,
        target: edge.target,
        source_handle: edge.sourceHandle || null,
        target_handle: edge.targetHandle || null,
        data: edge.data || {}
      }));

      const compileRequest = {
        nodes: transformedNodes,
        edges: transformedEdges,
        metadata: {
          name: recipeName || 'Untitled Recipe',
          description: recipeDescription || '',
          version: '1.0.0',
          author: 'Pipeline Builder User',
          tags: []
        },
        optimization_level: optimizationLevel,
        target_runtime: targetRuntime,
        recipe_name: recipeName || 'Untitled Recipe',
        description: recipeDescription || ''
      };

      console.log('Sending compilation request:', compileRequest);

      const response = await fetch('http://localhost:8000/api/recipes/compile', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(compileRequest),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: response.statusText }));
        throw new Error(`Compilation failed: ${errorData.detail || response.statusText}`);
      }

      const result: CompiledRecipe = await response.json();
      console.log('Compilation result:', result);
      
      // If WebSocket is not connected, handle result immediately
      if (!isConnected) {
        setCompilationResult(result);
        setCompilationProgress(100);
        setCompilationMessage('Compilation completed!');
        
        if (onCompile) {
          onCompile(result);
        }
      }
      // If WebSocket is connected, the result will be handled by the useEffect hook
      
    } catch (error) {
      console.error('Compilation error:', error);
      setCompilationMessage(`Compilation failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
      alert(`Compilation failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
    } finally {
      if (!isConnected) {
        setIsCompiling(false);
      }
    }
  };

  // Save recipe to backend
  const saveRecipe = async () => {
    setIsSaving(true);
    try {
      const saveRequest = {
        name: recipeName,
        description: recipeDescription,
        nodes: nodes.map(node => ({
          id: node.id,
          type: node.type,
          position: node.position,
          data: node.data,
          config: node.data || {}
        })),
        edges: edges.map(edge => ({
          id: edge.id,
          source: edge.source,
          target: edge.target,
          sourceHandle: edge.sourceHandle,
          targetHandle: edge.targetHandle
        })),
        metadata: {
          version: '1.0.0',
          created_at: initialRecipe?.metadata?.created_at || new Date().toISOString(),
          updated_at: new Date().toISOString(),
          viewport: getViewport()
        },
        tags: []
      };

      const url = savedPipelineId 
        ? `http://localhost:8000/api/pipelines/${savedPipelineId}`
        : 'http://localhost:8000/api/pipelines';
      
      const method = savedPipelineId ? 'PUT' : 'POST';

      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(saveRequest),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: response.statusText }));
        throw new Error(`Save failed: ${errorData.detail || response.statusText}`);
      }

      const result = await response.json();
      setSavedPipelineId(result.id);
      
      alert(`Pipeline ${savedPipelineId ? 'updated' : 'saved'} successfully!`);
      
      // Call the original onSave prop if provided
      if (onSave) {
        const recipe: Recipe = {
          id: result.id,
          name: recipeName,
          description: recipeDescription,
          nodes,
          edges,
          metadata: {
            version: '1.0.0',
            created_at: result.created_at,
            updated_at: result.updated_at,
          },
        };
        onSave(recipe);
      }
    } catch (error) {
      console.error('Save error:', error);
      alert(`Save failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
    } finally {
      setIsSaving(false);
    }
  };

  // Load pipeline configuration
  const loadPipeline = async (pipelineId: string) => {
    setIsLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/api/pipelines/${pipelineId}`);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: response.statusText }));
        throw new Error(`Load failed: ${errorData.detail || response.statusText}`);
      }

      const pipeline = await response.json();
      
      // Update the pipeline builder state
      setRecipeName(pipeline.name);
      setRecipeDescription(pipeline.description || '');
      setNodes(pipeline.nodes || []);
      setEdges(pipeline.edges || []);
      setSavedPipelineId(pipeline.id);
      
      // Reset compilation state
      setCompilationResult(null);
      setSelectedNode(null);
      
      alert('Pipeline loaded successfully!');
    } catch (error) {
      console.error('Load error:', error);
      alert(`Load failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
    } finally {
      setIsLoading(false);
    }
  };

  // Create new pipeline
  const newPipeline = () => {
    setNodes([]);
    setEdges([]);
    setRecipeName('Untitled Recipe');
    setRecipeDescription('');
    setCompilationResult(null);
    setSelectedNode(null);
    setSavedPipelineId(null);
  };

  // Validate recipe before compilation
  const validateRecipe = (): string[] => {
    const errors: string[] = [];
    
    if (nodes.length === 0) {
      errors.push('Recipe must contain at least one node');
    }
    
    const hasOutput = nodes.some(node => node.type === 'output');
    if (!hasOutput) {
      errors.push('Recipe must have at least one output node');
    }
    
    const hasInput = nodes.some(node => node.type === 'dataSource');
    if (!hasInput) {
      errors.push('Recipe must have at least one data source');
    }
    
    // Check for disconnected nodes
    const connectedNodeIds = new Set();
    edges.forEach(edge => {
      connectedNodeIds.add(edge.source);
      connectedNodeIds.add(edge.target);
    });
    
    const disconnectedNodes = nodes.filter(node => !connectedNodeIds.has(node.id));
    if (disconnectedNodes.length > 0 && nodes.length > 1) {
      errors.push(`${disconnectedNodes.length} node(s) are not connected to the pipeline`);
    }
    
    return errors;
  };

  // Clear recipe
  const clearRecipe = () => {
    setNodes([]);
    setEdges([]);
    setRecipeName('Untitled Recipe');
    setRecipeDescription('');
    setCompilationResult(null);
    setSelectedNode(null);
  };

  const validationErrors = validateRecipe();
  const canCompile = validationErrors.length === 0 && !isCompiling;

  return (
    <div className={`pipeline-builder ${className}`} style={{ height: '100vh', display: 'flex' }}>
      {/* Sidebar */}
      {showSidebar && (
        <div className="sidebar" style={{ width: '300px', background: '#f8f9fa', borderRight: '1px solid #dee2e6', overflow: 'auto' }}>
          {/* Recipe Info */}
          <div className="p-4 border-bottom">
            <h5>Recipe Configuration</h5>
            <div className="mb-3">
              <label className="form-label">Name</label>
              <input
                type="text"
                className="form-control"
                value={recipeName}
                onChange={(e) => setRecipeName(e.target.value)}
                placeholder="Enter recipe name"
              />
            </div>
            <div className="mb-3">
              <label className="form-label">Description</label>
              <textarea
                className="form-control"
                rows={3}
                value={recipeDescription}
                onChange={(e) => setRecipeDescription(e.target.value)}
                placeholder="Describe your recipe"
              />
            </div>
          </div>

          {/* Compilation Settings */}
          <div className="p-4 border-bottom">
            <h6>Compilation Settings</h6>
            <div className="mb-3">
              <label className="form-label">Optimization Level</label>
              <select
                className="form-select"
                value={optimizationLevel}
                onChange={(e) => setOptimizationLevel(e.target.value as any)}
              >
                <option value="basic">Basic</option>
                <option value="optimized">Optimized</option>
                <option value="aggressive">Aggressive</option>
              </select>
            </div>
            <div className="mb-3">
              <label className="form-label">Target Runtime</label>
              <select
                className="form-select"
                value={targetRuntime}
                onChange={(e) => setTargetRuntime(e.target.value as any)}
              >
                <option value="python">Python</option>
                <option value="javascript">JavaScript</option>
                <option value="quantum">Quantum</option>
              </select>
            </div>
          </div>

          {/* Node Templates */}
          <div className="p-4">
            <h6>Available Nodes</h6>
            <div className="node-templates">
              {Object.entries(
                nodeTemplates.reduce((acc, template) => {
                  if (!acc[template.category]) acc[template.category] = [];
                  acc[template.category].push(template);
                  return acc;
                }, {} as Record<string, typeof nodeTemplates>)
              ).map(([category, templates]) => (
                <div key={category} className="mb-3">
                  <div className="fw-bold text-muted small mb-2">{category}</div>
                  {templates.map((template) => (
                    <div
                      key={template.type}
                      className="node-template p-2 mb-2 border rounded cursor-pointer hover-bg-light"
                      draggable
                      onDragStart={(event) => {
                        event.dataTransfer.setData('application/reactflow', template.type);
                        event.dataTransfer.effectAllowed = 'move';
                      }}
                      style={{
                        cursor: 'grab',
                        border: '1px solid #dee2e6',
                        borderRadius: '4px',
                        backgroundColor: '#fff',
                      }}
                    >
                      <div className="d-flex align-items-center">
                        <span className="me-2" style={{ fontSize: '1.2em' }}>{template.icon}</span>
                        <div>
                          <div className="fw-medium">{template.label}</div>
                          <div className="text-muted small">{template.description}</div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ))}
            </div>
          </div>

          {/* Selected Node Properties */}
          {selectedNode && (
            <div className="p-4 border-top">
              <h6>Node Properties</h6>
              <div className="mb-2">
                <strong>Type:</strong> {selectedNode.type}
              </div>
              <div className="mb-2">
                <strong>ID:</strong> {selectedNode.id}
              </div>
              <div className="mb-3">
                <label className="form-label">Label</label>
                <input
                  type="text"
                  className="form-control"
                  value={selectedNode.data?.label || ''}
                  onChange={(e) => {
                    setNodes((nds) =>
                      nds.map((node) =>
                        node.id === selectedNode.id
                          ? { ...node, data: { ...node.data, label: e.target.value } }
                          : node
                      )
                    );
                    setSelectedNode({ ...selectedNode, data: { ...selectedNode.data, label: e.target.value } });
                  }}
                />
              </div>
            </div>
          )}
        </div>
      )}

      {/* Main Canvas */}
      <div className="flex-1" style={{ position: 'relative' }}>
        {/* Toolbar */}
        <div className="toolbar p-3 bg-white border-bottom d-flex justify-content-between align-items-center">
          <div className="d-flex align-items-center gap-2">
            <button
              className="btn btn-outline-secondary btn-sm"
              onClick={() => setShowSidebar(!showSidebar)}
            >
              {showSidebar ? '◀' : '▶'} {showSidebar ? 'Hide' : 'Show'} Sidebar
            </button>
            <button className="btn btn-outline-success btn-sm" onClick={newPipeline}>
              📄 New
            </button>
            <button 
              className="btn btn-outline-info btn-sm" 
              onClick={() => setShowLibrary(true)}
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <span className="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true"></span>
                  Loading...
                </>
              ) : (
                <>📂 Load</>
              )}
            </button>
            <button 
              className="btn btn-outline-primary btn-sm" 
              onClick={saveRecipe}
              disabled={isSaving}
            >
              {isSaving ? (
                <>
                  <span className="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true"></span>
                  Saving...
                </>
              ) : (
                <>
                  💾 {savedPipelineId ? 'Update' : 'Save'}
                </>
              )}
            </button>
            {savedPipelineId && (
              <span className="badge bg-success text-white small">
                ✓ Saved
              </span>
            )}
          </div>
          
          <div className="d-flex align-items-center gap-2">
            {validationErrors.length > 0 && (
              <div className="text-danger small">
                ⚠️ {validationErrors.length} error(s)
              </div>
            )}
            <div className="d-flex flex-column align-items-end">
              <button
                className={`btn btn-primary btn-sm ${!canCompile ? 'disabled' : ''}`}
                onClick={compileRecipe}
                disabled={!canCompile || isCompiling}
              >
                {isCompiling ? (
                  <>
                    <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                    Compiling...
                  </>
                ) : (
                  <>⚡ Compile Recipe</>
                )}
              </button>
              
              {/* WebSocket Connection Status */}
              <div className="small text-muted mt-1">
                WebSocket: {isConnected ? (
                  <span className="text-success">🟢 Connected</span>
                ) : (
                  <span className="text-warning">🟡 Disconnected</span>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Validation Errors */}
        {validationErrors.length > 0 && (
          <div className="alert alert-warning m-3 mb-0">
            <strong>Validation Errors:</strong>
            <ul className="mb-0 mt-2">
              {validationErrors.map((error, index) => (
                <li key={index}>{error}</li>
              ))}
            </ul>
          </div>
        )}
        
        {/* Real-time Compilation Progress */}
        {isCompiling && (
          <div className="alert alert-info m-3 mb-0">
            <div className="d-flex justify-content-between align-items-center mb-2">
              <strong>🔄 Compiling Recipe...</strong>
              <span className="small">{Math.round(compilationProgress)}%</span>
            </div>
            <div className="progress mb-2" style={{ height: '8px' }}>
              <div 
                className="progress-bar progress-bar-striped progress-bar-animated" 
                role="progressbar" 
                style={{ width: `${compilationProgress}%` }}
                aria-valuenow={compilationProgress} 
                aria-valuemin={0} 
                aria-valuemax={100}
              ></div>
            </div>
            <div className="small text-muted">{compilationMessage}</div>
          </div>
        )}

        {/* Compilation Result */}
        {compilationResult && (
          <div className="alert alert-success m-3 mb-0">
            <strong>✅ Compilation Successful!</strong>
            <div className="mt-2">
              <div><strong>Recipe ID:</strong> {compilationResult.recipe_id}</div>
              <div><strong>Estimated Cost:</strong> ${compilationResult.estimated_cost.toFixed(2)}</div>
              <div><strong>Estimated Duration:</strong> {compilationResult.estimated_duration}s</div>
              {compilationResult.warnings.length > 0 && (
                <div className="mt-2">
                  <strong>Warnings:</strong>
                  <ul className="mb-0">
                    {compilationResult.warnings.map((warning, index) => (
                      <li key={index}>{warning}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        )}

        {/* React Flow Canvas */}
        <div ref={reactFlowWrapper} style={{ height: 'calc(100vh - 120px)' }}>
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            onInit={setReactFlowInstance}
            onDrop={onDrop}
            onDragOver={onDragOver}
            onNodeClick={onNodeClick}
            nodeTypes={nodeTypes}
            fitView
            attributionPosition="bottom-left"
          >
            <Background />
            <Controls />
            <MiniMap />
            
            {/* Instructions Panel */}
            {nodes.length === 0 && (
              <Panel position="top-center">
                <div className="alert alert-info text-center">
                  <h6>🚀 Start Building Your Pipeline</h6>
                  <p className="mb-0">Drag nodes from the sidebar to create your recipe</p>
                </div>
              </Panel>
            )}
          </ReactFlow>
        </div>
      </div>
      
      {/* Pipeline Library Modal */}
      <PipelineLibrary
        isOpen={showLibrary}
        onClose={() => setShowLibrary(false)}
        onLoad={loadPipeline}
      />
    </div>
  );
};

// Main component with ReactFlow provider
const PipelineBuilder: React.FC<PipelineBuilderProps> = (props) => {
  return (
    <ReactFlowProvider>
      <PipelineBuilderInner {...props} />
    </ReactFlowProvider>
  );
};

export default PipelineBuilder;
export type { Recipe, CompiledRecipe, CompileRequest };