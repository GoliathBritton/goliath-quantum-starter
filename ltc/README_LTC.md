# Living Technical Codex (LTC)

Every decision, optimization, and agent action in the NQBA system is logged as an LTC entry for audit, compliance, and trust.

## LTC Entry Schema (JSON)

```
{
  "ltc_id": "ltc_2025-08-27T12:00:01Z_9f3c1d",
  "timestamp": "2025-08-27T12:00:01Z",
  "request_fingerprint": "sha256:...",
  "policy_id": "sales.leads.v1",
  "code_ref": {"repo": "flyfoxai/nqba-core", "git_sha": "abc123"},
  "solver": {"backend": "heuristic.greedy", "version": "0.1.0"},
  "inputs": {"features": {"acv": 25000, "intent_score": 0.74}},
  "outputs": {"score": 0.87, "tier": "A"},
  "timing_ms": {"total": 143, "solver": 89},
  "energy_estimate_j": 0.0,
  "receipts": {"ipfs_cid": null, "chain_tx": null},
  "explanation": "High ACV + intent",
  "redactions": ["email", "phone"]
}
```

- **Storage:**
  - Sprint-1: local JSONL under `./ltc/` (do not commit raw entries)
  - Later: push to IPFS and store CID; optional chain anchor
- **Naming:**
  - `ltc/YYYY/MM/DD/ltc_<ISO8601>_<shortid>.json`

## Usage
- All API decisions and agent actions must emit an LTC entry.
- LTC entries are referenced in API responses for traceability.
- LTC is the trust and compliance backbone for the intelligence economy.
