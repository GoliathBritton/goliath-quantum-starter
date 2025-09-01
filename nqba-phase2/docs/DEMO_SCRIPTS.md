# FLYFOX AI — Demo Scripts (Live Integration)

These scripts walk through end-to-end demos using the live NQBA Phase 2 stack.

Prereqs:
- API: http://localhost:8000
- Web: http://localhost:3000

---

## 1) Lead Capture → Quantum Scoring → Dashboard Update

Objective: Show a captured lead being quantum-scored (Dynex 410x) and reflected on the dashboard.

Steps:
1. Create a lead via API (quantum scoring):
   ```bash
   curl -s -X POST "http://localhost:8000/v2/sigma/quantum-scoring" \
     -H "Content-Type: application/json" \
     -d '{
       "company": "FutureTech Solutions",
       "industry": "technology",
       "name": "John Smith",
       "email": "john@futuretech.com",
       "budget": 25000,
       "signals": {"intent": 4.2, "hiring": 2.8, "techfit": 3.5}
     }'
   ```
2. Verify performance summary:
   ```bash
   curl -s "http://localhost:8000/v2/sigma/performance-summary" | jq
   ```
3. Open the web portal and navigate to Dashboard:
   - URL: http://localhost:3000/dashboard
   - Confirm KPIs updated (leads processed, averages).

Notes:
- Backend: dynex
- Multiplier: 410x

---

## 2) QEI (Quantum Efficiency Intelligence) Calculation

Objective: Demonstrate revenue intelligence with quantum boost.

Steps:
1. Run QEI calculation:
   ```bash
   curl -s -X POST "http://localhost:8000/v2/sigma/qei-calculation" \
     -H "Content-Type: application/json" \
     -d '{
       "inputs": {"cycle_time": 42, "win_rate": 31, "acv": 85, "cac": 23, "ltv": 420},
       "window": "7d"
     }' | jq
   ```
2. Highlight:
   - qei_score
   - drivers (cycle_time, win_rate, acv, cac, ltv)
   - quantum_backend = dynex, multiplier = 410

---

## 3) Integrations Status (UiPath, n8n, Mendix, Prismatic)

Objective: Prove integration layer wiring.

Steps:
1. Fetch status:
   ```bash
   curl -s "http://localhost:8000/v2/integrations/status" | jq
   ```
2. (Optional) Connect a provider (example payload):
   ```bash
   curl -s -X POST "http://localhost:8000/v2/integrations/connect" \
     -H "Content-Type: application/json" \
     -d '{"provider":"n8n","config":{"webhook_url":"https://example.webhook","api_key":"REDACTED"}}' | jq
   ```

---

## 4) Quantum Security (Dynex-Anchored)

Objective: Demonstrate quantum key rotation + compliance visibility.

Steps:
1. Rotate a key:
   ```bash
   curl -s -X POST "http://localhost:8000/v2/security/rotate-key" \
     -H "Content-Type: application/json" \
     -d '{"key_id":"demo-key-001","reason":"scheduled_rotation"}' | jq
   ```
2. Check status:
   ```bash
   curl -s "http://localhost:8000/v2/security/status" | jq
   ```
3. Audit logs:
   ```bash
   curl -s "http://localhost:8000/v2/security/audit-logs" | jq
   ```

---

## 5) n8n Webhook Demo (Optional Live Flow)

Use importable workflow: `nqba-phase2/integrations/n8n-demo-workflow.json`

- Trigger: HTTP Webhook `/lead-capture`
- Action: POST → `/v2/sigma/quantum-scoring`
- Result: Dashboard metrics update live

Validation:
- API: `/v2/sigma/performance-summary`
- UI: http://localhost:3000/dashboard
