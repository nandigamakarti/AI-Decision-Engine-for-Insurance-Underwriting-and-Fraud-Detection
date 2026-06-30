# AI-Assisted Insurance Underwriting Risk Assessment & Fraud Detection Engine

## What it is
An AI-powered insurance underwriting risk assessment and fraud detection engine. Built with FastAPI, LLM-driven DAG workflows, Azure Document Intelligence for OCR, and OpenTelemetry observability. The core/workflow framework from this project was reused in the Coding-Agents project.

## Tech Stack
- **Python 3.10+, FastAPI, SQLAlchemy, Alembic**
- **PostgreSQL** (primary DB + Phoenix traces DB)
- **Ollama** (local LLM, default model: `gpt-oss:20b`) with cloud fallback
- **Azure Document Intelligence** (OCR)
- **Claude 3.5 Vision** (VLM extraction)
- **Arize Phoenix** (OpenTelemetry tracing UI)
- **GPU service** (image forensics, separate HTTP service)
- **.NET Prompt Management API** (shared PostgreSQL, manages prompts)
- **Angular frontend** (risk-ui)

## Core Capabilities
- **10-dimension LLM risk assessment** (DAG workflow, 11 nodes)
- **10-dimension LLM fraud detection** (DAG workflow, 11 nodes)
- **Document extraction pipeline**: Azure OCR → LLM → structured JSON (15+ nodes)
- **VLM extraction** via Claude 3.5 Vision
- **Image manipulation forensics** (GPU-accelerated external service)
- **Async job queue** with per-step audit trails
- **TOON format** for ~40% prompt token reduction
- **Dynamic model selection** with local/cloud fallback

## Project Structure
```text
api/          → FastAPI endpoints (unified, v2, OCR, image detection)
core/         → Workflow framework (nodes, routers, DAG) ← shared with Coding-Agents
db/           → SQLAlchemy models + Alembic migrations
services/     → LLM, prompts, job processor, OCR, VLM, image detection
workflows/
  ├── risk_assessment/    → 11 nodes
  ├── fraud_detection/    → 11 nodes
  └── document_workflow/  → 15+ nodes
active_prompts/ → Markdown prompt templates
mappings/       → Vendor JSON transform YAMLs
config.py       → Environment config
main.py         → Entry point + Phoenix tracing + JobProcessor
```

## Key API Endpoints
- `POST /api/v2/jobs/assessments/new-combined` — submit risk assessment job
- `POST /api/v2/jobs/assessments/fraud` — submit fraud detection job
- `GET  /api/v2/jobs/{job_id}` — job status + result
- `GET  /api/v2/jobs/{job_id}/runs` — step-level audit trail
- `POST /api/ocr/extract-structured` — OCR → LLM → structured JSON
- `POST /api/ocr/extract-vlm` — VLM-based document extraction
- `POST /api/image-detection/detect` — image manipulation detection
- `GET  /api/v2/health` — health check

## Key Design Patterns
- **JobProcessor**: Polls pending async jobs, logs each step via `AsyncJobRun`.
- **UnifiedModelService**: Ollama local with intelligent cloud fallback.
- **DotNetPromptService**: Reads prompts dynamically from a shared DB managed by a .NET API.
- **DAG Workflows**: Directed Acyclic Graph execution with progress callbacks + dynamic routing.
- **TOON Format**: Advanced token optimization format.

## Database Tables
**Python-managed (Core Logic):**
- `underwriting_scores`, `claim_scores` — store final results with `dimension_scores` JSONB
- `async_jobs`, `async_job_runs` — manage the async job queue + step audit logs
- `api_request_logs`, `api_response_logs` — robust request/response audit trail

**Shared DB Tables (.NET managed, read-only from Python):**
- `prompts`, `prompt_versions`, `prompt_audit_logs`

## Environment Variables
```env
DATABASE_URL=postgresql://...
OLLAMA_LOCAL_URL=http://localhost:11434
OLLAMA_MODEL=gpt-oss:20b
AZURE_DOCUMENT_INTELLIGENCE_KEY=...
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT=...
IMAGE_DETECTION_SERVICE_URL=http://<gpu-machine-ip>:8000
USE_TOON_FORMAT=true
PHOENIX_ENABLED=true
```

## Common Commands
```bash
uv sync
uv run alembic upgrade head
uvicorn main:app --reload --port 8000
uv run pytest tests/ -v
uv run ruff check .
```

---

## Detailed Architecture & Workflow

### 1. Request Ingestion & Asynchronous Dispatch
When a user (via the Angular frontend) submits a risk or fraud assessment to `/api/v2/jobs/assessments/new-combined`, the API does not block. Instead, it immediately inserts a record into the `async_jobs` PostgreSQL table with a "Pending" status and returns a `job_id`. 
Simultaneously, the **JobProcessor** (a background daemon initialized in `main.py`) continuously polls this table. When it picks up the job, it begins executing the associated **DAG Workflow**.

### 2. Directed Acyclic Graph (DAG) Execution
The core logic resides in `core/` and `workflows/`. Depending on the job type, the engine routes the task to a specific 11-node (or 15+ node) DAG. 
- **Nodes**: Each dimension of risk (e.g., medical, financial, demographic) acts as an independent node. 
- **Audit Trails**: As each node starts, processes, and completes, the DAG framework fires a callback. This triggers an insert into the `async_job_runs` table, providing granular, step-level observability for the frontend to poll via `/api/v2/jobs/{job_id}/runs`.

### 3. Prompt & Context Management
Before querying an LLM, the system dynamically fetches the latest prompt templates via the **DotNetPromptService**. This allows prompt engineers to update prompts through a separate .NET portal without redeploying the Python backend. The context is then injected into these templates using the **TOON Format**, an optimized templating standard that shrinks the payload by ~40%, saving token context space.

### 4. LLM & VLM Processing Pipeline
- **Text & Extracted Data**: Data is passed to the **UnifiedModelService**. It defaults to querying the local Ollama instance (e.g., `gpt-oss:20b`). If the local GPU fails or times out, the service automatically implements a cloud fallback to ensure reliability.
- **Documents (PDFs/Images)**: If raw documents are provided, they flow through the `document_workflow`. 
  - Standard docs use **Azure Document Intelligence** to perform OCR, which is then parsed by the LLM into structured JSON.
  - Complex visual documents are directly passed to **Claude 3.5 Vision (VLM)**.

### 5. Forensics Integration
Any uploaded image files can be dynamically routed to the external **GPU Service** (`IMAGE_DETECTION_SERVICE_URL`) via HTTP. This isolated microservice handles heavy image manipulation forensics and returns anomaly scores back to the DAG.

### 6. Observability & Finalization
Throughout this entire lifecycle, **Arize Phoenix** (configured via OpenTelemetry) silently tracks spans and traces. This maps the entire journey of the LLM execution, token usage, and retrieval latency. Finally, the DAG resolves, updates the `async_jobs` table to "Completed", and writes the final JSONB payloads to `underwriting_scores` or `claim_scores`.
