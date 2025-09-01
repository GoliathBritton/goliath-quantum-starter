"""
FastAPI MCP API for Quantum/AI Tool Dispatch
-------------------------------------------
- Exposes all MCP tools as async API endpoints
- Validates input, dispatches to mcp_handler, returns result
- Ready for real backend logic and production extension
"""

import uvicorn
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel
from typing import Any, Dict
import asyncio
import logging
from nqba_stack import mcp_handler
from src.branding import BRANDING

logger = logging.getLogger("mcp.api")
app = FastAPI(
    title=f"{BRANDING['goliath']['name']} | {BRANDING['flyfox']['name']} | {BRANDING['sigma_select']['name']} Quantum/AI API",
    description=f"{BRANDING['goliath']['tagline']}<br>{BRANDING['flyfox']['tagline']}<br>{BRANDING['sigma_select']['tagline']}",
    version="1.0.0",
)


class ToolRequest(BaseModel):
    payload: Dict[str, Any]
    user: str = "anonymous"


@app.get("/", response_class=HTMLResponse)
def root():
    return f"""
    <div style="text-align:center; background:#111; color:#eee; padding:2em;">
        <img src="{BRANDING['goliath']['logo']}" width="180" style="margin:1em;"/>
        <img src="{BRANDING['flyfox']['logo']}" width="120" style="margin:1em;"/>
        <img src="{BRANDING['sigma_select']['logo']}" width="120" style="margin:1em;"/>
        <h1>{BRANDING['goliath']['name']} | {BRANDING['flyfox']['name']} | {BRANDING['sigma_select']['name']}</h1>
        <p>{BRANDING['goliath']['tagline']}<br>{BRANDING['flyfox']['tagline']}<br>{BRANDING['sigma_select']['tagline']}</p>
    </div>
    """


@app.get("/tools")
def list_tools():
    """List all available MCP tools"""
    return {
        "brand": f"{BRANDING['goliath']['name']} | {BRANDING['flyfox']['name']} | {BRANDING['sigma_select']['name']}",
        "tools": mcp_handler.list_tools(),
    }


@app.get("/tools/{tool}")
def get_tool_schema(tool: str):
    """Get input schema for a tool"""
    try:
        return {
            "brand": f"{BRANDING['goliath']['name']} | {BRANDING['flyfox']['name']} | {BRANDING['sigma_select']['name']}",
            "schema": mcp_handler.get_tool_schema(tool),
        }
    except Exception as e:
        raise HTTPException(404, str(e))


@app.get("/status")
def get_status():
    """Get backend health status"""
    return {
        "brand": f"{BRANDING['goliath']['name']} | {BRANDING['flyfox']['name']} | {BRANDING['sigma_select']['name']}",
        "status": mcp_handler.get_backend_status(),
    }


@app.post("/tools/{tool}")
async def run_tool(tool: str, req: ToolRequest):
    """Run a tool with input payload"""
    try:
        result = await mcp_handler.dispatch_tool(tool, req.payload, user=req.user)
        return result
    except Exception as e:
        logger.exception(f"Tool {tool} failed")
        raise HTTPException(400, str(e))


if __name__ == "__main__":
    uvicorn.run("mcp_api:app", host="0.0.0.0", port=8000, reload=True)
