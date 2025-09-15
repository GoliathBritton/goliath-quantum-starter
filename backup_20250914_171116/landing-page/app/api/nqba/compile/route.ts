// NQBA Compile API Route
// Handles QUBO recipe compilation requests

import { NextRequest, NextResponse } from 'next/server';

// Types for QUBO Recipe compilation (aligned with backend)
interface NodePosition {
  x: number;
  y: number;
}

interface NodeData {
  label: string;
  description?: string;
  config?: Record<string, any>;
  inputs?: string[];
  outputs?: string[];
}

interface FlowNode {
  id: string;
  type: string;
  position: NodePosition;
  data: NodeData;
  config?: Record<string, any>;
}

interface FlowEdge {
  id: string;
  source: string;
  target: string;
  source_handle?: string;
  target_handle?: string;
  data?: Record<string, any>;
}

interface FlowMetadata {
  name?: string;
  description?: string;
  version: string;
  author?: string;
  tags?: string[];
}

interface QUBORecipe {
  name: string;
  description: string;
  nodes: FlowNode[];
  edges?: FlowEdge[];
  metadata: FlowMetadata;
}

interface CompileRequest {
  recipe: QUBORecipe;
  optimization_level?: 'basic' | 'optimized' | 'aggressive';
  target_runtime?: 'python' | 'javascript' | 'quantum';
}

interface CompileResponse {
  success: boolean;
  recipe_id?: string;
  compiled_code?: string;
  execution_plan?: any;
  estimated_cost?: number;
  estimated_duration?: number;
  warnings?: string[];
  error?: string;
  metadata?: any;
}

// NQBA Backend URL - in production this would come from environment variables
const NQBA_BACKEND_URL = process.env.NQBA_BACKEND_URL || 'http://localhost:8000'

export async function POST(request: NextRequest) {
  try {
    const body: CompileRequest = await request.json();
    
    // Validate the request
    if (!body.recipe || !body.recipe.nodes || body.recipe.nodes.length === 0) {
      return NextResponse.json(
        { success: false, error: 'Invalid recipe: must contain at least one node' },
        { status: 400 }
      );
    }

    // Transform frontend recipe to NQBA backend format
    const nqbaRequest = {
      nodes: body.recipe.nodes,
      edges: body.recipe.edges || [],
      metadata: {
        name: body.recipe.name,
        description: body.recipe.description,
        version: body.recipe.metadata.version || '1.0.0',
        author: body.recipe.metadata.author,
        tags: body.recipe.metadata.tags
      },
      optimization_level: body.optimization_level || 'optimized',
      target_runtime: body.target_runtime || 'quantum',
      recipe_name: body.recipe.name,
      description: body.recipe.description
    };

    // Forward to NQBA backend
    const nqbaBackendUrl = process.env.NQBA_BACKEND_URL || 'http://localhost:8000';
    const response = await fetch(`${nqbaBackendUrl}/api/recipes/compile`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(nqbaRequest),
    });

    if (!response.ok) {
      const errorData = await response.text();
      return NextResponse.json(
        { 
          success: false, 
          error: `NQBA backend error: ${response.status} - ${errorData}` 
        },
        { status: response.status }
      );
    }

    const result = await response.json();
    
    // Transform backend response to frontend format
    const compileResponse: CompileResponse = {
      success: true,
      recipe_id: result.recipe_id,
      compiled_code: result.compiled_code,
      execution_plan: result.execution_plan,
      estimated_cost: result.estimated_cost,
      estimated_duration: result.estimated_duration,
      warnings: result.warnings || [],
      metadata: result.metadata
    };

    return NextResponse.json(compileResponse);

  } catch (error) {
    console.error('Compile API error:', error);
    return NextResponse.json(
      { 
        success: false, 
        error: error instanceof Error ? error.message : 'Unknown compilation error' 
      },
      { status: 500 }
    );
  }
}

export async function GET() {
  return NextResponse.json({
    service: 'NQBA QUBO Compiler',
    version: '1.0.0',
    status: 'active',
    supported_targets: ['dynex', 'cpu', 'gpu'],
    optimization_levels: ['basic', 'standard', 'aggressive'],
    endpoints: {
      compile: '/api/nqba/compile',
      run: '/api/nqba/run',
      status: '/api/nqba/status'
    }
  })
}