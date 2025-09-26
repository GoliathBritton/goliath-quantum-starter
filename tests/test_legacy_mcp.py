import pytest
from src.nqba.integration.legacy_wrapper import LegacyWrapper
from src.nqba_stack.mcp_handler import dispatch_tool

@pytest.fixture
def legacy_wrapper():
    return LegacyWrapper()

@pytest.mark.asyncio
async def test_analyze_system(legacy_wrapper):
    result = legacy_wrapper.analyze_legacy_system("Sample doc", ["code1", "code2"])
    assert "analysis" in result
    assert "code_understanding" in result
    assert "protocol_interpretation" in result

@pytest.mark.asyncio
async def test_translate_api(legacy_wrapper):
    result = legacy_wrapper.translate_api_call({"method": "GET", "path": "/data"}, "old_system")
    assert isinstance(result, dict)  # Assuming it returns a mapping

@pytest.mark.asyncio
async def test_execute_command(legacy_wrapper):
    result = legacy_wrapper.execute_legacy_command("RUN TASK", "industrial")
    assert result["status"] == "success"

@pytest.mark.asyncio
async def test_mcp_dispatch(legacy_wrapper):
    # Test with a sample tool, assuming quantum.llm.generate exists
    payload = {"prompt": "Test prompt"}
    result = await legacy_wrapper.dispatch_mcp("quantum.llm.generate", payload)
    assert "result" in result

@pytest.mark.asyncio
async def test_legacy_mcp_tools():
    # Test legacy specific MCP tools
    analyze_payload = {"documentation": "Test doc", "code_snippets": []}
    result = await dispatch_tool("legacy.analyze.system", analyze_payload)
    assert result["success"]

    translate_payload = {"api_call": "GET /data", "parameters": {}}
    result = await dispatch_tool("legacy.translate.api", translate_payload)
    assert result["success"]

    execute_payload = {"command": "RUN", "system_state": {}}
    result = await dispatch_tool("legacy.execute.command", execute_payload)
    assert result["success"]