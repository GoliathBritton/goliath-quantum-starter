'use client'

import { motion } from 'framer-motion'
import { 
  Plus, 
  Download, 
  Upload, 
  Save, 
  Play, 
  Trash2, 
  Copy, 
  Settings, 
  Info, 
  ArrowRight,
  Zap,
  Database,
  Cpu,
  Network,
  Target,
  GitBranch,
  Code,
  FileJson
} from 'lucide-react'
import { useState, useRef } from 'react'
import { DragDropContext, Droppable, Draggable } from '@hello-pangea/dnd'

interface QUBONode {
  id: string
  type: 'variable' | 'constraint' | 'objective' | 'parameter'
  label: string
  value?: number
  description: string
  position: { x: number; y: number }
  connections: string[]
}

interface QUBORecipe {
  id: string
  name: string
  description: string
  nodes: QUBONode[]
  metadata: {
    created: string
    modified: string
    version: string
    author: string
  }
}

export default function QUBORecipePage() {
  const [recipe, setRecipe] = useState<QUBORecipe>({
    id: 'recipe-' + Date.now(),
    name: 'New QUBO Recipe',
    description: 'Quantum optimization recipe for business intelligence',
    nodes: [],
    metadata: {
      created: new Date().toISOString(),
      modified: new Date().toISOString(),
      version: '1.0.0',
      author: 'NQBA User'
    }
  })

  const [selectedNode, setSelectedNode] = useState<QUBONode | null>(null)
  const [isCompiling, setIsCompiling] = useState(false)
  const canvasRef = useRef<HTMLDivElement>(null)

  const nodeTypes = [
    {
      type: 'variable' as const,
      label: 'Decision Variable',
      icon: Target,
      color: 'bg-blue-500',
      description: 'Binary or continuous decision variables'
    },
    {
      type: 'constraint' as const,
      label: 'Constraint',
      icon: GitBranch,
      color: 'bg-red-500',
      description: 'Problem constraints and limitations'
    },
    {
      type: 'objective' as const,
      label: 'Objective Function',
      icon: Zap,
      color: 'bg-green-500',
      description: 'Optimization objective to minimize/maximize'
    },
    {
      type: 'parameter' as const,
      label: 'Parameter',
      icon: Settings,
      color: 'bg-purple-500',
      description: 'Problem parameters and coefficients'
    }
  ]

  const addNode = (type: QUBONode['type']) => {
    const newNode: QUBONode = {
      id: `node-${Date.now()}`,
      type,
      label: `${type.charAt(0).toUpperCase() + type.slice(1)} ${recipe.nodes.filter(n => n.type === type).length + 1}`,
      description: `New ${type} node`,
      position: { x: Math.random() * 400, y: Math.random() * 300 },
      connections: [],
      value: type === 'parameter' ? 1 : undefined
    }

    setRecipe(prev => ({
      ...prev,
      nodes: [...prev.nodes, newNode],
      metadata: {
        ...prev.metadata,
        modified: new Date().toISOString()
      }
    }))
  }

  const updateNode = (nodeId: string, updates: Partial<QUBONode>) => {
    setRecipe(prev => ({
      ...prev,
      nodes: prev.nodes.map(node => 
        node.id === nodeId ? { ...node, ...updates } : node
      ),
      metadata: {
        ...prev.metadata,
        modified: new Date().toISOString()
      }
    }))
  }

  const deleteNode = (nodeId: string) => {
    setRecipe(prev => ({
      ...prev,
      nodes: prev.nodes.filter(node => node.id !== nodeId),
      metadata: {
        ...prev.metadata,
        modified: new Date().toISOString()
      }
    }))
    if (selectedNode?.id === nodeId) {
      setSelectedNode(null)
    }
  }

  const exportRecipe = () => {
    const dataStr = JSON.stringify(recipe, null, 2)
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr)
    
    const exportFileDefaultName = `${recipe.name.replace(/\s+/g, '-').toLowerCase()}.json`
    
    const linkElement = document.createElement('a')
    linkElement.setAttribute('href', dataUri)
    linkElement.setAttribute('download', exportFileDefaultName)
    linkElement.click()
  }

  const compileAndRun = async () => {
    if (recipe.nodes.length === 0) {
      alert('Please add at least one node to the recipe before compiling.')
      return
    }

    setIsCompiling(true)
    
    try {
      // Transform nodes to the expected backend format
      const transformedNodes = recipe.nodes.map(node => ({
        id: node.id,
        type: node.type,
        position: node.position,
        data: {
          label: node.data.label,
          description: node.data.description || '',
          config: node.data.config || {},
          inputs: node.data.inputs || [],
          outputs: node.data.outputs || []
        },
        config: node.data.config || {}
      }))

      // Step 1: Compile the recipe
      const compileResponse = await fetch('/api/nqba/compile', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          recipe: {
            name: recipe.name,
            description: recipe.description,
            nodes: transformedNodes,
            edges: [], // Add edges if needed
            metadata: {
              name: recipe.name,
              description: recipe.description,
              version: recipe.metadata.version,
              author: recipe.metadata.author
            }
          },
          optimization_level: 'optimized',
          target_runtime: 'quantum'
        }),
      })

      if (!compileResponse.ok) {
        const errorData = await compileResponse.json()
        alert(`Compilation failed: ${errorData.error}`)
        return
      }

      const compileResult = await compileResponse.json()
      
      if (!compileResult.success) {
        alert(`Compilation failed: ${compileResult.error}`)
        return
      }

      alert(`Recipe compiled successfully! Recipe ID: ${compileResult.recipe_id}`)

      // Step 2: Execute the compiled recipe
      const runResponse = await fetch('/api/nqba/run', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          recipe_id: compileResult.recipe_id,
          priority: 'normal',
          timeout: 300
        }),
      })

      if (!runResponse.ok) {
        const errorData = await runResponse.json()
        alert(`Execution failed: ${errorData.error}`)
        return
      }

      const runResult = await runResponse.json()
      
      if (!runResult.success) {
        alert(`Execution failed: ${runResult.error}`)
        return
      }

      // Display execution results
      const resultMessage = `
        Execution started successfully!
        Job ID: ${runResult.job_id}
        Status: ${runResult.status}
        ${runResult.message ? `Message: ${runResult.message}` : ''}
        ${runResult.estimated_completion ? `Estimated completion: ${runResult.estimated_completion}` : ''}
      `
      
      alert(resultMessage)

      // Optionally, you could poll for results here
      // pollForResults(runResult.job_id)

    } catch (error) {
      console.error('Compile and run error:', error)
      alert(`Error: ${error instanceof Error ? error.message : 'Unknown error occurred'}`)
    } finally {
      setIsCompiling(false)
    }
  }

  const getNodeIcon = (type: QUBONode['type']) => {
    const nodeType = nodeTypes.find(nt => nt.type === type)
    return nodeType?.icon || Target
  }

  const getNodeColor = (type: QUBONode['type']) => {
    const nodeType = nodeTypes.find(nt => nt.type === type)
    return nodeType?.color || 'bg-black'
  }

  return (
    <div className="bg-white min-h-screen">
      {/* Header */}
      <section className="border-b border-gray-200">
        <div className="container-quantum py-6">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
            <div>
              <h1 className="text-3xl md:text-4xl font-bold text-black mb-2">
                <span className="text-gradient-cyan">QUBO</span> Recipe Builder
              </h1>
              <p className="text-gray-600">
                Create quantum optimization recipes with visual drag-and-drop interface
              </p>
            </div>
            <div className="flex flex-wrap gap-3">
              <button
                onClick={exportRecipe}
                className="btn-secondary flex items-center"
              >
                <Download className="mr-2 h-4 w-4" />
                Export JSON
              </button>
              <button
                onClick={compileAndRun}
                disabled={isCompiling || recipe.nodes.length === 0}
        className="btn-primary flex items-center disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {isCompiling ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Building...
                  </>
                ) : (
                  <>
                    <Play className="mr-2 h-4 w-4" />
                    Compile & Run
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      </section>

      <div className="container-quantum py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Node Palette */}
          <div className="lg:col-span-1">
            <div className="card">
              <h3 className="text-lg font-semibold text-black mb-4 flex items-center">
                <Code className="mr-2 h-5 w-5 text-brand-cyan" />
                Node Palette
              </h3>
              <div className="space-y-3">
                {nodeTypes.map((nodeType) => {
                  const Icon = nodeType.icon
                  return (
                    <button
                      key={nodeType.type}
                      onClick={() => addNode(nodeType.type)}
                      className="w-full p-3 border border-gray-200 rounded-lg hover:border-brand-cyan hover:border-2 transition-colors duration-200 text-left group bg-white"
                    >
                      <div className="flex items-center space-x-3">
                        <div className={`w-8 h-8 ${nodeType.color} rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform duration-200`}>
                          <Icon className="h-4 w-4 text-white" />
                        </div>
                        <div>
                          <div className="font-medium text-black text-sm">{nodeType.label}</div>
                          <div className="text-xs text-gray-500">{nodeType.description}</div>
                        </div>
                      </div>
                    </button>
                  )
                })}
              </div>

              {/* Recipe Info */}
              <div className="mt-8 pt-6 border-t border-gray-200">
                <h4 className="font-semibold text-black mb-3">Recipe Info</h4>
                <div className="space-y-3">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Name
                    </label>
                    <input
                      type="text"
                      value={recipe.name}
                      onChange={(e) => setRecipe(prev => ({ ...prev, name: e.target.value }))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-brand-cyan focus:border-transparent text-sm"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Description
                    </label>
                    <textarea
                      value={recipe.description}
                      onChange={(e) => setRecipe(prev => ({ ...prev, description: e.target.value }))}
                      rows={3}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-brand-cyan focus:border-transparent text-sm"
                    />
                  </div>
                  <div className="text-xs text-gray-500">
                    <div>Nodes: {recipe.nodes.length}</div>
                    <div>Modified: {new Date(recipe.metadata.modified).toLocaleString()}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Canvas */}
          <div className="lg:col-span-2">
            <div className="card h-[600px] relative overflow-hidden">
              <div className="absolute top-4 left-4 z-10">
                <h3 className="text-lg font-semibold text-black flex items-center">
                  <Network className="mr-2 h-5 w-5 text-brand-cyan" />
                  Recipe Canvas
                </h3>
              </div>
              
              <div 
                ref={canvasRef}
                className="w-full h-full bg-white border border-gray-200 relative overflow-auto"
                style={{
                  backgroundImage: 'radial-gradient(circle, #e5e7eb 1px, transparent 1px)',
                  backgroundSize: '20px 20px'
                }}
              >
                {recipe.nodes.length === 0 ? (
                  <div className="absolute inset-0 flex items-center justify-center">
                    <div className="text-center text-gray-500">
                      <Network className="h-12 w-12 mx-auto mb-4 opacity-50" />
                      <p className="text-lg font-medium mb-2">Start Building Your QUBO Recipe</p>
                      <p className="text-sm">Add nodes from the palette to begin</p>
                    </div>
                  </div>
                ) : (
                  recipe.nodes.map((node) => {
                    const Icon = getNodeIcon(node.type)
                    return (
                      <div
                        key={node.id}
                        className={`absolute w-32 p-3 bg-white border-2 rounded-lg shadow-sm cursor-pointer transition-all duration-200 ${
                          selectedNode?.id === node.id 
                            ? 'border-brand-cyan shadow-lg scale-105' 
                            : 'border-gray-200 hover:border-gray-300 hover:shadow-md'
                        }`}
                        style={{
                          left: node.position.x,
                          top: node.position.y
                        }}
                        onClick={() => setSelectedNode(node)}
                      >
                        <div className="flex items-center space-x-2 mb-2">
                          <div className={`w-6 h-6 ${getNodeColor(node.type)} rounded flex items-center justify-center`}>
                            <Icon className="h-3 w-3 text-white" />
                          </div>
                          <div className="text-xs font-medium text-gray-600 uppercase tracking-wide">
                            {node.type}
                          </div>
                        </div>
                        <div className="text-sm font-medium text-black truncate" title={node.label}>
                          {node.label}
                        </div>
                        {node.value !== undefined && (
                          <div className="text-xs text-gray-500 mt-1">
                            Value: {node.value}
                          </div>
                        )}
                      </div>
                    )
                  })
                )}
              </div>
            </div>
          </div>

          {/* Properties Panel */}
          <div className="lg:col-span-1">
            <div className="card">
              <h3 className="text-lg font-semibold text-black mb-4 flex items-center">
                <Settings className="mr-2 h-5 w-5 text-brand-cyan" />
                Properties
              </h3>
              
              {selectedNode ? (
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Label
                    </label>
                    <input
                      type="text"
                      value={selectedNode.label}
                      onChange={(e) => updateNode(selectedNode.id, { label: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-brand-cyan focus:border-transparent text-sm"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Description
                    </label>
                    <textarea
                      value={selectedNode.description}
                      onChange={(e) => updateNode(selectedNode.id, { description: e.target.value })}
                      rows={3}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-brand-cyan focus:border-transparent text-sm"
                    />
                  </div>
                  
                  {selectedNode.type === 'parameter' && (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Value
                      </label>
                      <input
                        type="number"
                        value={selectedNode.value || 0}
                        onChange={(e) => updateNode(selectedNode.id, { value: parseFloat(e.target.value) || 0 })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-brand-cyan focus:border-transparent text-sm"
                      />
                    </div>
                  )}
                  
                  <div className="pt-4 border-t border-gray-200">
                    <button
                      onClick={() => deleteNode(selectedNode.id)}
                      className="w-full flex items-center justify-center px-3 py-2 border border-red-300 text-red-700 rounded-md hover:bg-red-50 transition-colors duration-200"
                    >
                      <Trash2 className="mr-2 h-4 w-4" />
                      Delete Node
                    </button>
                  </div>
                </div>
              ) : (
                <div className="text-center text-gray-500 py-8">
                  <Info className="h-8 w-8 mx-auto mb-3 opacity-50" />
                  <p className="text-sm">Select a node to edit its properties</p>
                </div>
              )}
            </div>

            {/* Quick Actions */}
            <div className="card mt-6">
              <h4 className="font-semibold text-black mb-3">Quick Actions</h4>
              <div className="space-y-2">
                <button
                  onClick={() => setRecipe(prev => ({ ...prev, nodes: [] }))}
                  className="w-full text-left px-3 py-2 text-sm text-gray-600 hover:border hover:border-brand-cyan rounded-md transition-colors duration-200 bg-white"
                >
                  Clear Canvas
                </button>
                <button
                  onClick={exportRecipe}
                  className="w-full text-left px-3 py-2 text-sm text-gray-600 hover:bg-gray-50 rounded-md transition-colors duration-200"
                >
                  Export Recipe
                </button>
                <button
                  onClick={() => {
                    const input = document.createElement('input')
                    input.type = 'file'
                    input.accept = '.json'
                    input.onchange = (e) => {
                      const file = (e.target as HTMLInputElement).files?.[0]
                      if (file) {
                        const reader = new FileReader()
                        reader.onload = (e) => {
                          try {
                            const imported = JSON.parse(e.target?.result as string)
                            setRecipe(imported)
                          } catch (error) {
                            console.error('Error importing recipe:', error)
                          }
                        }
                        reader.readAsText(file)
                      }
                    }
                    input.click()
                  }}
                  className="w-full text-left px-3 py-2 text-sm text-gray-600 hover:bg-gray-50 rounded-md transition-colors duration-200"
                >
                  Import Recipe
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Integration Info */}
      <section className="section-padding bg-white border-t border-gray-200">
        <div className="container-quantum">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <h2 className="text-3xl md:text-4xl font-bold text-black mb-6">
              NQBA Integration
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Your QUBO recipes integrate seamlessly with the NQBA quantum computing platform.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                title: "Dynex Primary",
                description: "Recipes execute on Dynex quantum computing platform for optimal performance.",
                icon: Zap,
                color: "text-brand-cyan"
              },
              {
                title: "CPU/GPU Fallback",
                description: "Automatic fallback to classical computing when quantum resources are unavailable.",
                icon: Cpu,
                color: "text-brand-gold"
              },
              {
                title: "Real-time Results",
                description: "Get optimization results in real-time with comprehensive performance metrics.",
                icon: Database,
                color: "text-brand-navy"
              }
            ].map((feature) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
                viewport={{ once: true }}
                className="card text-center"
              >
                <div className={`w-12 h-12 ${feature.color} mx-auto mb-4`}>
                  <feature.icon className="w-full h-full" />
                </div>
                <h3 className="text-xl font-bold text-black mb-3">{feature.title}</h3>
                <p className="text-gray-600 leading-relaxed">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>
    </div>
  )
}