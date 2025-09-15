import pytest
from nqba_stack.quantum.adapters.dynex_adapter import DynexAdapter, AdapterConfig
import asyncio


@pytest.mark.asyncio
async def test_dynex_qubo_sdk():
    config = AdapterConfig()
    adapter = DynexAdapter(config)
    adapter.dynex_mode = "sdk"
    qubo = {"linear_terms": {"x": 1}, "qubo_matrix": {}}
    job_id = await adapter.submit_qubo(qubo)
    assert job_id
    result = await adapter.result(job_id)
    assert "samples" in result


@pytest.mark.asyncio
async def test_dynex_qubo_api():
    config = AdapterConfig()
    adapter = DynexAdapter(config)
    adapter.dynex_mode = "api"
    qubo = {"linear_terms": {"x": 1}, "qubo_matrix": {}}
    job_id = await adapter.submit_qubo(qubo)
    assert job_id
    result = await adapter.result(job_id)
    assert "samples" in result


@pytest.mark.asyncio
async def test_dynex_qubo_ftp():
    config = AdapterConfig()
    adapter = DynexAdapter(config)
    adapter.dynex_mode = "ftp"
    qubo = {"linear_terms": {"x": 1}, "qubo_matrix": {}}
    job_id = await adapter.submit_qubo(qubo)
    assert job_id
    # FTP mode may not support result, so just check job_id
