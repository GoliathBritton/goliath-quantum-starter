import type { NextApiRequest, NextApiResponse } from "next";

// NOTE: This is a minimal demo persistence (in-memory). Replace with DB (Postgres) in prod
let workflows: any[] = [];

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === "POST") {
    const payload = req.body;
    payload.id = `wf_${Date.now()}`;
    payload.createdAt = new Date().toISOString();
    payload.status = "draft";
    
    workflows.push(payload);
    return res.status(201).json({ id: payload.id });
  }
  
  if (req.method === "GET") {
    return res.status(200).json({ workflows });
  }
  
  return res.status(405).end();
}