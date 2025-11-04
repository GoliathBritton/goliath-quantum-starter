from fastapi import FastAPI, Header, HTTPException

app = FastAPI(title="Starter Service", version="0.1.0")

def require_tenant(x_tenant_id: str | None):
    if not x_tenant_id:
        raise HTTPException(400, "Missing X-Tenant-Id")

@app.get("/health")
def health(x_tenant_id: str | None = Header(None)):
    require_tenant(x_tenant_id)
    return {"ok": True, "service": "starter"}
