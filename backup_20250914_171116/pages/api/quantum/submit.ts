import type { NextApiRequest, NextApiResponse } from "next";
import quantumWorker from "../../../quantum-worker";

interface SubmitJobRequest {
  workflowId: string;
  nodes: Array<{
    id: string;
    type: string;
    data: any;
    position: { x: number; y: number };
  }>;
  userId?: string;
  priority?: "low" | "normal" | "high";
  metadata?: Record<string, any>;
}

interface SubmitJobResponse {
  jobId: string;
  status: string;
  estimatedDuration?: number;
  message: string;
}

export default function handler(
  req: NextApiRequest,
  res: NextApiResponse<SubmitJobResponse | { error: string }>
) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  try {
    const { workflowId, nodes, userId, priority = "normal", metadata }: SubmitJobRequest = req.body;

    // Validate required fields
    if (!workflowId || !nodes || !Array.isArray(nodes)) {
      return res.status(400).json({ 
        error: "Missing required fields: workflowId and nodes are required" 
      });
    }

    // Validate nodes structure
    if (nodes.length === 0) {
      return res.status(400).json({ 
        error: "Workflow must contain at least one node" 
      });
    }

    // Check for premium quantum nodes
    const hasQuantumNodes = nodes.some(node => 
      node.type === "quantum" || 
      node.data?.isPremium || 
      node.data?.requiresQuantum
    );

    // Create job payload
    const jobPayload = {
      workflowId,
      nodes,
      userId: userId || "anonymous",
      priority,
      metadata: {
        ...metadata,
        hasQuantumNodes,
        nodeCount: nodes.length,
        submittedAt: new Date().toISOString(),
        userAgent: req.headers["user-agent"] || "unknown"
      }
    };

    // Submit job to quantum worker
    const job = quantumWorker.createJob('optimization', jobPayload);
    const jobId = job.id;

    console.log(`[API] Quantum job submitted: ${jobId} for workflow: ${workflowId}`);

    return res.status(201).json({
      jobId,
      status: "queued",
      message: hasQuantumNodes 
        ? "Quantum workflow submitted for neuromorphic processing"
        : "Workflow submitted for quantum-enhanced optimization"
    });

  } catch (error) {
    console.error("[API] Error submitting quantum job:", error);
    return res.status(500).json({ 
      error: "Internal server error while submitting job" 
    });
  }
}