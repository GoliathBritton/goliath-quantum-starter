import type { NextApiRequest, NextApiResponse } from "next";

// In-memory storage for demo purposes
// In production, use a proper database
let workflows: any[] = [];

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === "POST") {
    const payload = req.body;
    
    // Add timestamp and ID if not provided
    if (!payload.id) {
      payload.id = `workflow_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }
    payload.createdAt = new Date().toISOString();
    payload.updatedAt = new Date().toISOString();
    
    workflows.push(payload);
    return res.status(201).json({ id: payload.id });
  }
  
  if (req.method === "GET") {
    return res.status(200).json({ workflows });
  }
  
  return res.status(405).end();
}