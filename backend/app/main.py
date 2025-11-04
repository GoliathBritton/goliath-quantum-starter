from fastapi import FastAPI
from crm.routes_contacts import router as contacts_router
from crm.routes_companies import router as companies_router
from crm.routes_deals import router as deals_router
from crm.routes_tasks import router as tasks_router
from crm.routes_messages import router as messages_router
from crm.routes_automations import router as automations_router
from crm.routes_reports import router as reports_router

app = FastAPI(title="NQBA Sentinel API", version="0.2.0")

app.include_router(contacts_router, prefix="/crm")
app.include_router(companies_router, prefix="/crm")
app.include_router(deals_router, prefix="/crm")
app.include_router(tasks_router, prefix="/crm")
app.include_router(messages_router, prefix="/crm")
app.include_router(automations_router, prefix="/crm")
app.include_router(reports_router, prefix="/crm")

@app.get("/health")
def health():
    return {"ok": True}
