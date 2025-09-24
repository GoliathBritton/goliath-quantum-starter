from unittest.mock import patch
import pytest
from src.quantum.quantum_job_manager import QuantumJobManager
from src.qdllm.core.nuco_client import NucoClient
from fastapi.testclient import TestClient

@pytest.fixture
def job_manager():
    nuco = NucoClient(api_key="test_key")
    return QuantumJobManager(nuco_client=nuco, start_processor=False)

@patch('src.qdllm.core.nuco_client.NucoClient.submit_gpu_job')
def test_submit_to_nuco(mock_submit, job_manager):
    mock_submit.return_value = 'mock_job_id'
    payload = {'task': 'compute', 'backend': 'nuco'}
    job_id = job_manager.submit_job(payload)
    assert job_id == 'mock_job_id'
    mock_submit.assert_called_once_with(payload)

@patch('src.qdllm.core.nuco_client.NucoClient.get_job_result')
def test_get_result_from_nuco(mock_get_result, job_manager):
    mock_get_result.return_value = {'status': 'completed', 'result': 42}
    job_id = 'mock_job_id'
    result = job_manager.get_result(job_id, backend='nuco')
    assert result == {'status': 'completed', 'result': 42}
    mock_get_result.assert_called_once_with(job_id)

def test_submit_compute_nuco():
    import sys
    print("Python executable:", sys.executable)
    print("sys.path:", sys.path)
    from api.src.main import app
    client = TestClient(app)
    with patch('api.src.main.nuco_client.submit_gpu_job') as mock_submit:
        mock_submit.return_value = 'mock_job_id'
        response = client.post("/api/compute/submit", json={'task': 'compute', 'backend': 'nuco'})
        assert response.status_code == 200
        data = response.json()
        assert data['job_id'] == 'mock_job_id'
        assert data['backend'] == 'nuco'