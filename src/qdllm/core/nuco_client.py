import requests
import json
from typing import Dict, Any, Optional

class NucoClient:
    def __init__(self, api_key: str, base_url: str = "https://api.nuco.cloud/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def submit_gpu_job(self, payload: Dict[str, Any]) -> str:
        """
        Submit GPU job to nuco.cloud (e.g., agent training).
        Payload: {'job_type': 'training', 'resources': {'gpu': 8, 'memory': '64GB'}, 'data': {...}}
        Returns: job_id
        """
        url = f"{self.base_url}/jobs/submit"
        response = requests.post(url, headers=self.headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json().get("job_id")

    def get_job_result(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve job status/results."""
        url = f"{self.base_url}/jobs/{job_id}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        return None

    def get_job_status(self, job_id: str) -> str:
        """Get status (queued, running, completed, failed)."""
        result = self.get_job_result(job_id)
        return result.get("status", "unknown") if result else "failed"

    def list_available_servers(self) -> Dict[str, Any]:
        """List available GPU/CPU servers (real-time monitoring)."""
        url = f"{self.base_url}/servers/available"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()  # e.g., {"servers": [{"id": "gpu-rtx", "price": 0.5, "crypto_pay": True}]}

    def provision_gpu(self, gpu_type: str = "RTX 4090", duration: int = 3600) -> str:
        """Provision GPU instance (programmatic mgmt)."""
        payload = {"type": gpu_type, "duration_secs": duration, "payment": "crypto"}  # NCDT disc
        url = f"{self.base_url}/instances/provision"
        response = requests.post(url, headers=self.headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json().get("instance_id")

    def pause_reboot_instance(self, instance_id: str, action: str = "pause") -> Dict[str, Any]:
        """Pause/reboot/terminate instance."""
        url = f"{self.base_url}/instances/{instance_id}/{action}"
        response = requests.post(url, headers=self.headers)
        response.raise_for_status()
        return response.json()  # e.g., {"status": "paused", "credits_used": 100}

    def get_credit_balance(self) -> float:
        """Monitor credits (real-time)."""
        url = f"{self.base_url}/account/credits"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json().get("balance", 0.0)

    def cancel_booking(self, booking_id: str) -> bool:
        """Cancel server booking."""
        url = f"{self.base_url}/bookings/{booking_id}/cancel"
        response = requests.delete(url, headers=self.headers)
        return response.status_code == 200

# Example usage (mock for local testing)
if __name__ == "__main__":
    client = NucoClient(api_key="your_nuco_api_key")
    job_id = client.submit_gpu_job({
        "job_type": "agent_training",
        "backend": "nuco",
        "resources": {"gpu": 8, "memory": "64GB"},
        "tenant_id": "flyfox_enterprise"
    })
    print(f"Submitted job: {job_id}")
    status = client.get_job_status(job_id)
    print(f"Status: {status}")
    client = NucoClient()  # Auto-loads your env key
    servers = client.list_available_servers()
    print(f"Available: {servers}")
    instance_id = client.provision_gpu(duration=1800)  # 30min test
    print(f"Provisioned: {instance_id}")
    balance = client.get_credit_balance()
    print(f"Balance: {balance}")