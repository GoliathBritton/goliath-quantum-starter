# API Spec (FastAPI)

Base URL: / (dev), versioned endpoints under /v1.

---

## Health
GET /healthz → {"status": "ok"}

---

## Decide
POST /v1/decide

**Input:**
```
{
  "policy_id": "sales.leads.v1",
  "features": {"acv": 25000, "region": "NA", "intent_score": 0.74}
}
```

**Output:**
```
{
  "decision_id": "dec_01H...",
  "result": {"score": 0.87, "tier": "A"},
  "explanation": "High ACV + intent",
  "ltc_ref": "ltc_2025-08-27T12:00:01Z_9f3c..."
}
```

---

## Optimize (QUBO)
POST /v1/optimize

**Input (QUBO or SAT model — MVP supports QUBO w/ heuristics):**
```
{
  "variables": 10,
  "Q": [[0,1,0],[1,0,-0.2],[0,-0.2,0]],
  "constraints": [{"type":"sum_le","vars":[0,1,2], "value": 2}],
  "objective": "maximize"
}
```

**Output:**
```
{
  "decision_id": "opt_01H...",
  "assignment": [1,0,1,0,0,1,0,0,1,0],
  "objective_value": 3.41,
  "backend": "heuristic.greedy",
  "ltc_ref": "ltc_2025-08-27T12:00:03Z_1ab2..."
}
```

---

## LTC
POST /v1/ltc/entries (internal)
GET /v1/ltc/entries/{id}

**Auth:** Add token header X-API-Key (dev); migrate to OAuth2/JWT later.
