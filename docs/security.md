# Security & Compliance (Sprint-1)

Objectives
- Keep secrets out of code, enable least privilege, create immutable provenance.
- Establish a baseline that scales to SOC2/GDPR later.

Controls

**Secrets**
- .env (local only) + GitHub Actions Secrets for CI (DYNEX_API_KEY, WEB3_PROVIDER_URL, IPFS_PROJECT_*, LLM_API_KEY).
- Rotate keys before first production demo.
- Enable Dependabot, secret scanning, required reviewers.

**Access**
- GitHub orgs: owners (John), core-maintainers, contributors (least privilege).
- Branch protection: require PR + status checks.

**Provenance (LTC)**
- Log: input hash, policy id, code version (git sha), solver metadata, timing.
- Optional: pin LTC JSON to IPFS; include CID in response.

**Supply Chain**
- Lock dependencies (pip-tools or uv lock).
- Run pip-audit in CI.

**PII/Data**
- Avoid ingesting PII in Sprint-1. If unavoidable, pseudonymize before logging.

**Runtime**
- Limit outbound calls via allowlist (dev).
- Add rate limiting on /v1/* endpoints.

**Threat-Model (MVP)**
- Key leakage → Mitigate via secret scanning + .env ignored + rotation.
- Prompt/data exfiltration → Keep payloads minimal; LTC redaction.
- Model inversion → Avoid uploading sensitive corpora in Sprint-1.
