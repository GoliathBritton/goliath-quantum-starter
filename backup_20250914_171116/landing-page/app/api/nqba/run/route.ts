// NQBA Run API Route
// Handles QUBO recipe execution requests

import { NextRequest, NextResponse } from 'next/server';

interface RunRequest {
  recipe_id: string;
  input_data?: Record<string, any>;
  priority?: 'low' | 'normal' | 'high' | 'urgent';
  timeout?: number;
}

interface RunResponse {
  success: boolean;
  job_id?: string;
  recipe_id?: string;
  status?: string;
  message?: string;
  estimated_completion?: string;
  result?: {
    energy?: number;
    samples?: Array<Record<string, number>>;
    solution?: Record<string, number>;
    execution_time?: number;
    iterations?: number;
  };
  error?: string;
  metadata?: any;
}

interface JobStatusResponse {
  job_id: string;
  recipe_id: string;
  status: string;
  progress: number;
  result?: Record<string, any>;
  error?: string;
  started_at?: string;
  completed_at?: string;
  cost?: number;
  compute_provider?: string;
  metadata?: Record<string, any>;
}

// NQBA Backend URL
const NQBA_BACKEND_URL = process.env.NQBA_BACKEND_URL || 'http://localhost:8000'

export async function POST(request: NextRequest) {
  try {
    const body: RunRequest = await request.json();
    
    // Validate the request
    if (!body.recipe_id) {
      return NextResponse.json(
        { success: false, error: 'Recipe ID is required' },
        { status: 400 }
      );
    }

    // Transform frontend request to NQBA backend format
    const nqbaRequest = {
      recipe_id: body.recipe_id,
      input_data: body.input_data || {},
      priority: body.priority || 'normal',
      timeout: body.timeout || 300
    };

    // Forward to NQBA backend
    const nqbaBackendUrl = process.env.NQBA_BACKEND_URL || 'http://localhost:8000';
    const response = await fetch(`${nqbaBackendUrl}/api/recipes/execute`, {
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
    const runResponse: RunResponse = {
      success: true,
      job_id: result.job_id,
      recipe_id: result.recipe_id,
      status: result.status,
      message: result.message,
      estimated_completion: result.estimated_completion,
      metadata: result.metadata
    };

    return NextResponse.json(runResponse);

  } catch (error) {
    console.error('Run API error:', error);
    return NextResponse.json(
      { 
        success: false, 
        error: error instanceof Error ? error.message : 'Unknown execution error' 
      },
      { status: 500 }
    );
  }
}

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const jobId = searchParams.get('job_id');
    
    if (!jobId) {
      // Return general service information if no job ID provided
      return NextResponse.json({
        success: true,
        service: 'NQBA Recipe Execution API',
        status: 'active',
        endpoints: {
          execute: 'POST /api/nqba/run',
          status: 'GET /api/nqba/run?job_id={id}'
        }
      });
    }

    // Forward status request to NQBA backend
    const nqbaBackendUrl = process.env.NQBA_BACKEND_URL || 'http://localhost:8000';
    const response = await fetch(`${nqbaBackendUrl}/api/recipes/jobs/${jobId}/status`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
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

    const statusData = await response.json();
    
    // Transform backend response to frontend format
    const jobStatusResponse: JobStatusResponse = {
      job_id: statusData.job_id,
      recipe_id: statusData.recipe_id,
      status: statusData.status,
      progress: statusData.progress || 0,
      result: statusData.result,
      error: statusData.error,
      started_at: statusData.started_at,
      completed_at: statusData.completed_at,
      cost: statusData.cost,
      compute_provider: statusData.compute_provider,
      metadata: statusData.metadata
    };

    return NextResponse.json(jobStatusResponse);

  } catch (error) {
    console.error('Status check error:', error);
    return NextResponse.json(
      {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown status check error'
      },
      { status: 500 }
    );
  }
}