from fastapi import FastAPI, Body
from pydantic import BaseModel
from .legacy_wrapper import LegacyWrapper
import uvicorn

app = FastAPI(title="Legacy System Integration API")

wrapper = LegacyWrapper()

class AnalyzeRequest(BaseModel):
    documentation: str
    code_snippets: list[str] = []
    protocol: str = "OPC UA"

class TranslateRequest(BaseModel):
    modern_api_call: dict
    target_system: str

class ExecuteRequest(BaseModel):
    command: str
    system_type: str

@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    result = wrapper.analyze_legacy_system(
        request.documentation,
        request.code_snippets,
        request.protocol
    )
    return result

@app.post("/translate")
async def translate(request: TranslateRequest):
    result = wrapper.translate_api_call(
        request.modern_api_call,
        request.target_system
    )
    return {"legacy_command": result}

@app.post("/execute")
async def execute(request: ExecuteRequest):
    result = wrapper.execute_legacy_command(
        request.command,
        request.system_type
    )
    return result

@app.post("/dispatch_mcp")
async def dispatch_mcp(tool: str = Body(...), payload: dict = Body(...)):
    result = await wrapper.dispatch_mcp(tool, payload)
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)