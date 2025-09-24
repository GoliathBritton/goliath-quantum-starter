import pytest
from fastapi.testclient import TestClient
from api.src.main import app
import time

def test_qdllm_status_websocket():
    client = TestClient(app)
    with client.websocket_connect("/ws/qdllm-status") as websocket:
        # Since it sends every 10 seconds, wait for one message
        data = websocket.receive_json()
        assert "status" in data
        assert isinstance(data["status"], str)
        # Optionally check more, but basic verification