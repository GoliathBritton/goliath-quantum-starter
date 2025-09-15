import uuid
from datetime import datetime
import json
import os

try:
    import ipfshttpclient

    IPFS_AVAILABLE = True
except ImportError:
    IPFS_AVAILABLE = False

LTC_LOCAL_DIR = os.path.join(os.path.dirname(__file__), "../../ltc/entries")
os.makedirs(LTC_LOCAL_DIR, exist_ok=True)


def ltc_record(
    policy_id: str, inputs: dict, outputs: dict, explanation: str, solver_backend: str
) -> dict:
    """
    Write LTC (Living Technical Codex) record to IPFS if available, else local file.
    Returns dict with ltc_id and storage ref.
    """
    ltc_id = str(uuid.uuid4())
    entry = {
        "ltc_id": ltc_id,
        "timestamp": datetime.utcnow().isoformat(),
        "policy_id": policy_id,
        "inputs": inputs,
        "outputs": outputs,
        "explanation": explanation,
        "solver_backend": solver_backend,
    }
    storage_ref = None
    if IPFS_AVAILABLE:
        try:
            ipfs_url = os.environ.get("IPFS_API_URL", "/dns/localhost/tcp/5001/http")
            client = ipfshttpclient.connect(ipfs_url)
            res = client.add_json(entry)
            storage_ref = f"ipfs://{res}"
        except Exception as e:
            storage_ref = f"ipfs.error:{e}"
    if not storage_ref or storage_ref.startswith("ipfs.error"):
        # Fallback: write to local file
        fname = os.path.join(LTC_LOCAL_DIR, f"{ltc_id}.json")
        with open(fname, "w", encoding="utf-8") as f:
            json.dump(entry, f, indent=2)
        storage_ref = f"file://{fname}"
    entry["storage_ref"] = storage_ref
    return entry


class LTCLogger:
    """NQBA Living Technical Codex Logger for audit and compliance."""

    def __init__(self, business_unit: str = "nqba_core"):
        self.business_unit = business_unit
        self.log_entries = []
        self.storage_backend = "auto"

    def log_decision(
        self,
        policy_id: str,
        inputs: dict,
        outputs: dict,
        explanation: str,
        solver_backend: str,
    ) -> dict:
        """Log a decision to the LTC system."""
        entry = ltc_record(policy_id, inputs, outputs, explanation, solver_backend)
        entry["business_unit"] = self.business_unit
        entry["logger_instance"] = str(uuid.uuid4())
        self.log_entries.append(entry)
        return entry

    def log_quantum_operation(
        self, operation_type: str, parameters: dict, result: dict, backend: str
    ) -> dict:
        """Log a quantum computing operation."""
        entry = {
            "ltc_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "operation_type": operation_type,
            "parameters": parameters,
            "result": result,
            "solver_backend": backend,
            "business_unit": self.business_unit,
            "logger_instance": str(uuid.uuid4()),
        }
        self.log_entries.append(entry)
        return entry

    def get_log_entries(self, policy_id: str = None) -> list:
        """Get log entries, optionally filtered by policy_id."""
        if policy_id:
            return [
                entry
                for entry in self.log_entries
                if entry.get("policy_id") == policy_id
            ]
        return self.log_entries

    def clear_logs(self):
        """Clear all log entries."""
        self.log_entries.clear()

    def export_logs(self, format: str = "json") -> str:
        """Export logs in specified format."""
        if format == "json":
            return json.dumps(self.log_entries, indent=2)
        elif format == "csv":
            # Simple CSV export
            if not self.log_entries:
                return ""
            headers = list(self.log_entries[0].keys())
            csv_lines = [",".join(headers)]
            for entry in self.log_entries:
                csv_lines.append(",".join(str(entry.get(h, "")) for h in headers))
            return "\n".join(csv_lines)
        else:
            raise ValueError(f"Unsupported format: {format}")
