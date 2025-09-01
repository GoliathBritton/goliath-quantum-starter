"""
n8n adapter stub for NQBA/MCP.
Implements:
- trigger_flow(flow_id, data)
- create_webhook(flow_id)
- get_execution_status(execution_id)
"""

import os
from typing import Dict, Any, Optional


class N8nAdapter:
    def __init__(self, webhook_secret: str = None):
        self.webhook_secret = webhook_secret or os.getenv("N8N_WEBHOOK_SECRET", "")
        self.base_url = "https://n8n.io"

    def trigger_flow(self, flow_id: str, data: dict) -> dict:
        """Trigger an n8n workflow with the specified data"""
        execution_id = f"n8n_exec_{flow_id}_{len(data)}"

        return {
            "execution_id": execution_id,
            "flow_id": flow_id,
            "status": "triggered",
            "message": "n8n workflow triggered successfully",
        }

    def create_webhook(self, flow_id: str) -> dict:
        """Create a webhook for an n8n workflow"""
        webhook_url = f"https://n8n.io/webhook/{flow_id}"

        return {
            "webhook_id": f"webhook_{flow_id}",
            "webhook_url": webhook_url,
            "flow_id": flow_id,
            "status": "created",
            "message": "n8n webhook created successfully",
        }

    def get_execution_status(self, execution_id: str) -> dict:
        """Get the status of an n8n workflow execution"""
        # Mock status responses
        statuses = ["running", "completed", "failed", "waiting"]
        import random

        status = random.choice(statuses)

        return {
            "execution_id": execution_id,
            "status": status,
            "progress": random.randint(0, 100) if status == "running" else 100,
            "message": f"n8n execution {execution_id} is {status}",
        }

    def list_flows(self) -> list:
        """List all available n8n workflows"""
        return [
            {
                "id": "flow_001",
                "name": "Lead Processing",
                "description": "Automated lead processing workflow",
                "status": "active",
            },
            {
                "id": "flow_002",
                "name": "Data Sync",
                "description": "Data synchronization workflow",
                "status": "active",
            },
            {
                "id": "flow_003",
                "name": "Marketing Automation",
                "description": "Marketing automation workflow",
                "status": "active",
            },
        ]

    def get_flow_details(self, flow_id: str) -> dict:
        """Get detailed information about a specific n8n workflow"""
        return {
            "id": flow_id,
            "name": f"Flow {flow_id}",
            "description": "n8n workflow for process automation",
            "version": "1.0.0",
            "status": "active",
            "last_modified": "2024-01-15T10:30:00Z",
            "execution_count": 892,
            "success_rate": 95.2,
        }

    def stop_execution(self, execution_id: str) -> dict:
        """Stop a running n8n workflow execution"""
        return {
            "execution_id": execution_id,
            "status": "stopped",
            "message": f"n8n execution {execution_id} stopped successfully",
        }
