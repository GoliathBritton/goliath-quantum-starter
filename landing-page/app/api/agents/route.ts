// NQBA Agents API Route
// Handles agent management and task assignment

import { NextRequest, NextResponse } from 'next/server';

// Types for NQBA Agents (aligned with backend)
interface Agent {
  id: string;
  name: string;
  type: 'quantum' | 'classical' | 'hybrid';
  status: 'active' | 'idle' | 'busy' | 'offline';
  capabilities: string[];
  current_task?: string;
  performance_metrics: {
    tasks_completed: number;
    success_rate: number;
    avg_execution_time: number;
  };
  metadata: {
    created: string;
    last_active: string;
    version: string;
  };
}

interface AgentTask {
  id: string;
  agent_id: string;
  type: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  priority: 'low' | 'normal' | 'high' | 'urgent';
  payload: Record<string, any>;
  created_at: string;
  started_at?: string;
  completed_at?: string;
  result?: Record<string, any>;
  error?: string;
}

interface TaskRequest {
  task_type: string;
  priority?: number;
  metadata?: Record<string, any>;
  payload?: Record<string, any>;
}

interface TaskResult {
  success: boolean;
  task_id?: string;
  result?: Record<string, any>;
  execution_time?: number;
  quantum_enhanced?: boolean;
  ltc_reference?: string;
  error?: string;
}

interface CreateAgentRequest {
  name: string
  type: Agent['type']
  tier?: Agent['metadata']['tier']
  capabilities?: string[]
}

interface AssignTaskRequest {
  agent_id: string
  task_type: AgentTask['type']
  priority: AgentTask['priority']
  payload: any
}

// NQBA Backend URL
const NQBA_BACKEND_URL = process.env.NQBA_BACKEND_URL || 'http://localhost:8000'

// Mock agents data for development
const mockAgents: Agent[] = [
  {
    id: 'agent_qc_001',
    name: 'Quantum Council Alpha',
    type: 'quantum_council',
    status: 'active',
    capabilities: ['governance', 'policy_enforcement', 'resource_allocation', 'strategic_planning'],
    performance_metrics: {
      tasks_completed: 1247,
      success_rate: 0.98,
      average_execution_time: 2.3,
      quantum_efficiency: 0.94
    },
    metadata: {
      created: '2024-01-15T10:00:00Z',
      last_active: new Date().toISOString(),
      version: '2.1.0',
      tier: 'enterprise'
    }
  },
  {
    id: 'agent_qa_002',
    name: 'Quantum Architect Beta',
    type: 'quantum_architect',
    status: 'active',
    capabilities: ['qubo_design', 'optimization_modeling', 'algorithm_selection', 'performance_tuning'],
    performance_metrics: {
      tasks_completed: 892,
      success_rate: 0.96,
      average_execution_time: 4.7,
      quantum_efficiency: 0.91
    },
    metadata: {
      created: '2024-01-20T14:30:00Z',
      last_active: new Date().toISOString(),
      version: '2.0.5',
      tier: 'pro'
    }
  },
  {
    id: 'agent_os_003',
    name: 'Optimization Specialist Gamma',
    type: 'optimization_specialist',
    status: 'busy',
    capabilities: ['dynex_optimization', 'cpu_fallback', 'gpu_acceleration', 'parameter_tuning'],
    current_task: 'Optimizing supply chain QUBO for Goliath Energy',
    performance_metrics: {
      tasks_completed: 2156,
      success_rate: 0.99,
      average_execution_time: 1.8,
      quantum_efficiency: 0.97
    },
    metadata: {
      created: '2024-01-10T09:15:00Z',
      last_active: new Date().toISOString(),
      version: '2.2.1',
      tier: 'enterprise'
    }
  }
]

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url)
  const agentId = searchParams.get('id')
  const type = searchParams.get('type')
  const status = searchParams.get('status')
  
  try {
    // Try to get system health and business pods info from NQBA backend
    try {
      const response = await fetch(`${NQBA_BACKEND_URL}/v1/system/health`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Source': 'frontend-agent-manager'
        },
      });

      if (response.ok) {
        const systemHealth = await response.json();
        
        // Transform system health data to agent format
        const agents: Agent[] = [
          {
            id: 'nqba-orchestrator',
            name: 'NQBA Stack Orchestrator',
            type: 'quantum',
            status: systemHealth.orchestrator_status === 'healthy' ? 'active' : 'offline',
            capabilities: ['task_routing', 'quantum_optimization', 'business_assessment'],
            performance_metrics: {
              tasks_completed: systemHealth.metrics?.tasks_completed || 0,
              success_rate: systemHealth.metrics?.success_rate || 0.95,
              avg_execution_time: systemHealth.metrics?.avg_execution_time || 150
            },
            metadata: {
              created: '2024-01-01T00:00:00Z',
              last_active: systemHealth.timestamp,
              version: '1.0.0'
            }
          }
        ];

        // Add business pods as agents
        for (let i = 0; i < systemHealth.business_pods; i++) {
          agents.push({
            id: `business-pod-${i + 1}`,
            name: `Business Pod ${i + 1}`,
            type: 'hybrid',
            status: i < systemHealth.active_pods ? 'active' : 'idle',
            capabilities: ['lead_scoring', 'sales_optimization', 'energy_optimization'],
            performance_metrics: {
              tasks_completed: Math.floor(Math.random() * 100),
              success_rate: 0.85 + Math.random() * 0.15,
              avg_execution_time: 100 + Math.random() * 100
            },
            metadata: {
              created: '2024-01-01T00:00:00Z',
              last_active: systemHealth.timestamp,
              version: '1.0.0'
            }
          });
        }

        // Apply filters
        let filteredAgents = agents;
        if (agentId) filteredAgents = agents.filter(agent => agent.id === agentId);
        if (type) filteredAgents = filteredAgents.filter(agent => agent.type === type);
        if (status) filteredAgents = filteredAgents.filter(agent => agent.status === status);

        return NextResponse.json({ 
          success: true, 
          agents: filteredAgents,
          total: filteredAgents.length,
          source: 'nqba_backend'
        });
      }
    } catch (error) {
      console.warn('NQBA backend unavailable, using mock data:', error);
    }
    
    // Fallback to mock data if backend is unavailable
    let filteredAgents = mockAgents;
    
    if (agentId) {
      filteredAgents = mockAgents.filter(agent => agent.id === agentId);
    }
    if (type) {
      filteredAgents = filteredAgents.filter(agent => agent.type === type);
    }
    if (status) {
      filteredAgents = filteredAgents.filter(agent => agent.status === status);
    }
    
    // Return filtered mock data
    return NextResponse.json({
      success: true,
      agents: filteredAgents,
      total: filteredAgents.length,
      source: 'mock_data',
      agent_types: {
        quantum_council: 'Strategic governance and policy enforcement',
        quantum_architect: 'QUBO design and optimization modeling',
        optimization_specialist: 'Platform-specific optimization execution',
        validation_agent: 'Result validation and quality assurance',
        integration_agent: 'Third-party system integration and workflow'
      }
    })
    
  } catch (error) {
    console.error('Agent retrieval error:', error)
    return NextResponse.json(
      {
        success: false,
        error: 'Failed to retrieve agents',
        code: 'RETRIEVAL_ERROR'
      },
      { status: 500 }
    )
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { action, agent_id, task_data } = body;

    // Forward to NQBA backend task submission system
    const nqbaBackendUrl = process.env.NQBA_BACKEND_URL || 'http://localhost:8000';
    
    if (action === 'submit_task') {
      try {
        // Transform to NQBA TaskRequest format
        const taskRequest: TaskRequest = {
          task_type: task_data.type || 'general_task',
          priority: task_data.priority || 5,
          metadata: {
            agent_id: agent_id,
            source: 'frontend_agent_api',
            ...task_data.metadata
          },
          payload: task_data.payload || {}
        };

        // Submit task to NQBA orchestrator
        const response = await fetch(`${nqbaBackendUrl}/v1/quantum/optimize`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            variables: task_data.variables || ['x', 'y'],
            constraints: task_data.constraints || [],
            objective_function: task_data.objective_function || 'minimize',
            provider: task_data.provider || 'dynex',
            priority: task_data.priority || 1
          }),
        });

        if (response.ok) {
          const result = await response.json();
          return NextResponse.json({
            success: true,
            task_id: result.request_id,
            status: 'submitted',
            message: 'Task submitted to NQBA orchestrator',
            result: result
          });
        }
      } catch (error) {
        console.warn('NQBA backend unavailable for task submission:', error);
      }
    }
    
    if (action === 'create_agent') {
      const createRequest: CreateAgentRequest = body.data
      
      // Validate request
      if (!createRequest.name || !createRequest.type) {
        return NextResponse.json(
          {
            success: false,
            error: 'Missing required fields: name and type are required',
            code: 'MISSING_FIELDS'
          },
          { status: 400 }
        )
      }
      
      const validTypes: Agent['type'][] = [
        'quantum_architect', 'quantum_council', 'optimization_specialist', 
        'validation_agent', 'integration_agent'
      ]
      
      if (!validTypes.includes(createRequest.type)) {
        return NextResponse.json(
          {
            success: false,
            error: `Invalid agent type. Must be one of: ${validTypes.join(', ')}`,
            code: 'INVALID_TYPE'
          },
          { status: 400 }
        )
      }
      
      // Forward to NQBA backend
      try {
        const nqbaResponse = await fetch(`${NQBA_BACKEND_URL}/api/agents/create`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-API-Source': 'frontend-agent-manager'
          },
          body: JSON.stringify(createRequest)
        })
        
        if (nqbaResponse.ok) {
          const result = await nqbaResponse.json()
          return NextResponse.json(result)
        }
      } catch (error) {
        console.warn('NQBA backend unavailable for agent creation')
      }
      
      // Mock response for development
      const newAgent: Agent = {
        id: `agent_${createRequest.type.substring(0, 2)}_${Date.now()}`,
        name: createRequest.name,
        type: createRequest.type,
        status: 'active',
        capabilities: createRequest.capabilities || [],
        performance_metrics: {
          tasks_completed: 0,
          success_rate: 1.0,
          average_execution_time: 0,
          quantum_efficiency: 1.0
        },
        metadata: {
          created: new Date().toISOString(),
          last_active: new Date().toISOString(),
          version: '1.0.0',
          tier: createRequest.tier || 'standard'
        }
      }
      
      return NextResponse.json({
        success: true,
        agent: newAgent,
        message: 'Agent created successfully (mock mode)'
      })
    }
    
    if (action === 'assign_task') {
      const taskRequest: AssignTaskRequest = body.data
      
      // Validate request
      if (!taskRequest.agent_id || !taskRequest.task_type || !taskRequest.payload) {
        return NextResponse.json(
          {
            success: false,
            error: 'Missing required fields: agent_id, task_type, and payload are required',
            code: 'MISSING_FIELDS'
          },
          { status: 400 }
        )
      }
      
      // Forward to NQBA backend
      try {
        const nqbaResponse = await fetch(`${NQBA_BACKEND_URL}/api/agents/assign-task`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-API-Source': 'frontend-agent-manager'
          },
          body: JSON.stringify(taskRequest)
        })
        
        if (nqbaResponse.ok) {
          const result = await nqbaResponse.json()
          return NextResponse.json(result)
        }
      } catch (error) {
        console.warn('NQBA backend unavailable for task assignment')
      }
      
      // Mock response for development
      const task: AgentTask = {
        id: `task_${Date.now()}`,
        agent_id: taskRequest.agent_id,
        type: taskRequest.task_type,
        priority: taskRequest.priority,
        status: 'assigned',
        payload: taskRequest.payload,
        created: new Date().toISOString(),
        assigned: new Date().toISOString()
      }
      
      return NextResponse.json({
        success: true,
        task,
        message: 'Task assigned successfully (mock mode)'
      })
    }
    
    return NextResponse.json(
      {
        success: false,
        error: 'Invalid action. Supported actions: create_agent, assign_task, submit_task',
        code: 'INVALID_ACTION'
      },
      { status: 400 }
    )
    
  } catch (error) {
    console.error('Agent operation error:', error)
    return NextResponse.json(
      {
        success: false,
        error: 'Internal server error during agent operation',
        code: 'INTERNAL_ERROR'
      },
      { status: 500 }
    )
  }
}