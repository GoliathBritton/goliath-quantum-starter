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

// Custom Node Types
import DataSourceNode from './nodes/DataSourceNode';
import ProcessorNode from './nodes/ProcessorNode';
import AIModelNode from './nodes/AIModelNode';
import QuantumNode from './nodes/QuantumNode';
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
    description: 'Quantum computing operations',
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
  
  const reactFlowWrapper = useRef<HTMLDivElement>(null);
  const { project, getViewport } = useReactFlow();
  const [reactFlowInstance, setReactFlowInstance] = useState<ReactFlowInstance | null>(null);

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

    try {
      const compileRequest: CompileRequest = {
        flow_definition: {
          nodes,
          edges,
          metadata: {
            name: recipeName,
            description: recipeDescription,
            version: '1.0.0',
            created_at: new Date().toISOString(),
            viewport: getViewport(),
          },
        },
        optimization_level: optimizationLevel,
        target_runtime: targetRuntime,
      };

      const response = await fetch('/api/recipes/compile', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
        },
        body: JSON.stringify(compileRequest),
      });

      if (!response.ok) {
        throw new Error(`Compilation failed: ${response.statusText}`);
      }

      const result: CompiledRecipe = await response.json();
      setCompilationResult(result);
      
      if (onCompile) {
        onCompile(result);
      }
    } catch (error) {
      console.error('Compilation error:', error);
      alert(`Compilation failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
    } finally {
      setIsCompiling(false);
    }
  };

  // Save recipe
  const saveRecipe = async () => {
    const recipe: Recipe = {
      id: initialRecipe?.id,
      name: recipeName,
      description: recipeDescription,
      nodes,
      edges,
      metadata: {
        version: '1.0.0',
        created_at: initialRecipe?.metadata?.created_at || new Date().toISOString(),
        updated_at: new Date().toISOString(),
      },
    };

    if (onSave) {
      onSave(recipe);
    }
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
            <button className="btn btn-outline-primary btn-sm" onClick={saveRecipe}>
              💾 Save
            </button>
            <button className="btn btn-outline-danger btn-sm" onClick={clearRecipe}>
              🗑️ Clear
            </button>
          </div>
          
          <div className="d-flex align-items-center gap-2">
            {validationErrors.length > 0 && (
              <div className="text-danger small">
                ⚠️ {validationErrors.length} error(s)
              </div>
            )}
            <button
              className={`btn btn-primary btn-sm ${!canCompile ? 'disabled' : ''}`}
              onClick={compileRecipe}
              disabled={!canCompile}
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