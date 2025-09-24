# Customer Journeys Documentation

This document defines three distinct customer journeys within the Goliath Quantum Starter ecosystem, based on the system's business pods and core functionalities. These journeys are designed to validate key pathways, flows, and components, ensuring the system is fully operational. Each journey includes step-by-step processes, involved components, and any prerequisites.

## Journey 1: Lead Scoring and Qualification (Sigma Select Pod)
**Description:** A sales user qualifies and scores potential leads using quantum-enhanced optimization to prioritize high-value opportunities.

**Prerequisites:** API server running, user authentication (if required), sample lead data.

**Steps:**
1. **Access the System:** User logs into the dashboard or accesses the API endpoint.
2. **Submit Lead Data:** POST request to `/sigma-select/score-leads` with lead details, scoring criteria, and optimization level.
3. **Quantum Processing:** System routes the request to the Sigma Select pod, which formulates a QUBO problem and submits to quantum backend.
4. **Receive Results:** System returns scored leads with quantum advantage metrics.
5. **Review and Act:** User reviews scores in the dashboard and initiates follow-up actions.

**Involved Components:** API server, Sigma Select pod, Quantum Adapter, LTC logging.

## Journey 2: Quantum Job Submission and Execution
**Description:** A developer or researcher submits a custom quantum job for execution on available backends, monitors progress, and retrieves results.

**Prerequisites:** Quantum providers configured, API server running.

**Steps:**
1. **Prepare Job:** User creates quantum circuit or optimization problem definition.
2. **Submit Job:** POST request to `/quantum/submit-job` with job parameters (e.g., provider, circuit, shots).
3. **Job Routing:** Orchestrator routes job to selected quantum backend via Quantum Adapter.
4. **Monitor Status:** User queries `/quantum/job-status/{job_id}` for real-time updates.
5. **Retrieve Results:** Once complete, GET `/quantum/job-results/{job_id}` to obtain outcomes and metrics.

**Involved Components:** API server, Orchestrator, Quantum Adapter, multiple quantum providers.

## Journey 3: Performance Monitoring and Analytics
**Description:** An administrator monitors system performance, views metrics, and generates reports to ensure operational efficiency.

**Prerequisites:** Dashboard running, API server with metrics endpoint.

**Steps:**
1. **Access Dashboard:** User navigates to the performance dashboard (e.g., via frontend).
2. **View Real-time Metrics:** Dashboard pulls data from `/metrics` endpoint showing API response times, quantum advantages, pod statuses.
3. **Analyze Data:** Use filters to view specific pod performance or historical data.
4. **Generate Report:** Export analytics or trigger report generation via API.
5. **Take Actions:** Based on insights, adjust configurations or scale resources.

**Involved Components:** Frontend dashboard, API metrics endpoints, LTC for historical data, Orchestrator for status.

These journeys will be simulated in subsequent steps to validate and fix any issues.