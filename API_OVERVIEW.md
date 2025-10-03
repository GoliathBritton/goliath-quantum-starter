# Public API & Integration Overview

## API Principles
- RESTful and gRPC endpoints for all core services
- OAuth2/JWT authentication
- Versioned, backwards-compatible APIs

## Core API Endpoints

### System
- `/health` – System health and status
- `/metrics` – Platform and pod metrics
- `/pods` – List, deploy, and manage AI pods

### AI Modules (NQBA™-powered)
- `/ai/qdllm` – LLM inference and reasoning
- `/ai/qnlp` – NLP processing and sentiment analysis
- `/ai/qtransformers` – Predictions, classification, transfer learning

### Business Integrations
- `/integrations/{vertical}` – Pre-built connectors (ERP, CRM, EHR, etc.)

### Admin & Marketplace
- `/marketplace` – Discover and activate new pods/extensions
- `/admin/users` – User and permission management

## SDKs
- Python, JavaScript, Java (in-progress)

## Webhooks & Events
- Subscribe to workflow and pod events for orchestration and monitoring

---

**Full API specs are in development—see roadmap for release schedule. All APIs are proprietary and part of the exclusive Goliath, FLYFOX AI, and Sigma Select platform.**
