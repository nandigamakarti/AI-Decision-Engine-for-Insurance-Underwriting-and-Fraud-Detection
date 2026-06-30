```
╔══════════════════════════════════════════════════════════════════════════════╗
║                 RISK ASSESSMENT ENGINE - SYSTEM ARCHITECTURE                 ║
║                         (Ollama AI Integration)                              ║
╚══════════════════════════════════════════════════════════════════════════════╝


┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLIENT LAYER                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Browser    │  │   Python     │  │   Node.js    │  │   cURL/      │  │
│  │   (Swagger   │  │   (requests) │  │ (fetch API)  │  │ Postman      │  │
│  │    Docs)     │  │              │  │              │  │              │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
│         │                 │                 │                 │          │
│         └─────────────────┴─────────────────┴─────────────────┘          │
│                            │                                             │
│                    HTTP POST /api/risk-assessment                         │
│                         (Customer JSON)                                   │
│                                                                            │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         API APPLICATION LAYER                               │
│                              (main.py)                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────┐     │
│  │  FastAPI Application                                             │     │
│  │  - CORS Middleware                                               │     │
│  │  - Request/Response validation                                   │     │
│  │  - Automatic API documentation                                   │     │
│  └──────────────────────┬───────────────────────────────────────────┘     │
│                         │                                                  │
│                         ▼                                                  │
│  ┌──────────────────────────────────────────────────────────────────┐     │
│  │  api/routes.py                                                   │     │
│  │  • POST /api/risk-assessment  ◄─── Handles customer data         │     │
│  │  • GET  /api/health           ◄─── Health check                  │     │
│  │  • GET  /api/ollama-status    ◄─── Ollama service status         │     │
│  │  • GET  /                     ◄─── API information               │     │
│  └──────────────────────┬───────────────────────────────────────────┘     │
│                         │                                                  │
│                         ▼                                                  │
│  ┌──────────────────────────────────────────────────────────────────┐     │
│  │  Input Validation (api/models.py)                                │     │
│  │                                                                  │     │
│  │  CustomerDataInput                                               │     │
│  │  ├── personal_info (required)                                    │     │
│  │  ├── health_info (optional)                                      │     │
│  │  ├── financial_info (optional)                                   │     │
│  │  ├── claims_history (optional)                                   │     │
│  │  └── additional_data (optional)                                  │     │
│  └──────────────────────┬───────────────────────────────────────────┘     │
│                         │                                                  │
└────────────────────────┬───────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        BUSINESS LOGIC LAYER                                 │
│              (services/risk_assessment_ollama.py)                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  RiskAssessmentServiceOllama                                                │
│  • Coordinates risk assessment workflow                                      │
│  • Logs assessment process                                                   │
│  • Handles errors gracefully                                                 │
│                         │                                                  │
│                         ▼                                                  │
│  ┌──────────────────────────────────────────────────────────────────┐     │
│  │  services/ollama_service.py                                      │     │
│  │                                                                  │     │
│  │  OllamaService                                                   │     │
│  │  ├── health_check()                                              │     │
│  │  │   └─► Verify Ollama is running                               │     │
│  │  │                                                               │     │
│  │  ├── assess_risk()                                               │     │
│  │  │   ├─► _build_risk_assessment_prompt()                        │     │
│  │  │   ├─► _call_ollama()                                          │     │
│  │  │   ├─► _parse_risk_assessment()                                │     │
│  │  │   └─► Return RiskAssessmentOutput                             │     │
│  │  │                                                               │     │
│  │  └── _extract_json()                                             │     │
│  │      └─► Parse AI response (robust JSON extraction)              │     │
│  └──────────────────────┬───────────────────────────────────────────┘     │
│                         │                                                  │
└────────────────────────┬───────────────────────────────────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         │                               │
         ▼                               ▼
    Config Check                   HTTP Request
    (config.py)              (requests library)
    
    • OLLAMA_BASE_URL                │
    • OLLAMA_MODEL                   ▼
    • OLLAMA_TEMPERATURE        ┌──────────────────────────────┐
    • OLLAMA_TIMEOUT            │  JSON Prompt Construction    │
    • etc.                      │                              │
                               │  "Analyze this customer...   │
                               │   Return risk assessment...  │
                               │   Format as JSON..."          │
                               └──────────────┬───────────────┘
                                             │
                                             ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         EXTERNAL AI SERVICE LAYER                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Ollama API Server (localhost:11434)                                         │
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────┐    │
│  │ POST /api/generate                                                │    │
│  │ {                                                                 │    │
│  │   "model": "mistral" | "llama2" | "neural-chat",                │    │
│  │   "prompt": "...",                                                │    │
│  │   "temperature": 0.7,                                             │    │
│  │   "top_p": 0.9,                                                   │    │
│  │   "stream": false                                                 │    │
│  │ }                                                                 │    │
│  └───────────────────┬──────────────────────────────────────────────┘    │
│                      │                                                    │
│                      ▼                                                    │
│  ┌───────────────────────────────────────────────────────────────────┐   │
│  │ Language Model Inference                                          │   │
│  │                                                                   │   │
│  │ • Mistral 7.3B  (Fast, good balance)                              │   │
│  │ • Llama2 7B-70B (More capable, slower)                            │   │
│  │ • Neural-Chat 6.7B (Instruction-optimized)                        │   │
│  │ • Others (Dolphin, Orca, etc.)                                    │   │
│  │                                                                   │   │
│  │ Processes:                                                        │   │
│  │ 1. Tokenizes prompt                                               │   │
│  │ 2. Analyzes customer data                                         │   │
│  │ 3. Generates risk assessment in JSON format                       │   │
│  │ 4. Returns structured response                                    │   │
│  └───────────────────┬──────────────────────────────────────────────┘   │
│                      │                                                   │
│                      ▼                                                   │
│  ┌───────────────────────────────────────────────────────────────────┐   │
│  │ Response                                                          │   │
│  │ {                                                                 │   │
│  │   "overall_risk_level": "MEDIUM",                                │   │
│  │   "overall_risk_score": 52.3,                                    │   │
│  │   "risk_factors": [                                              │   │
│  │     {                                                             │   │
│  │       "factor_name": "...",                                      │   │
│  │       "risk_level": "...",                                       │   │
│  │       "score": 55,                                               │   │
│  │       "description": "..."                                       │   │
│  │     }                                                             │   │
│  │   ],                                                              │   │
│  │   "recommendations": ["..."],                                    │   │
│  │   "additional_notes": "..."                                      │   │
│  │ }                                                                 │   │
│  └───────────────────┬──────────────────────────────────────────────┘   │
│                      │                                                   │
└──────────────────────┬───────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         RESPONSE PARSING LAYER                              │
│                  (OllamaService._parse_risk_assessment)                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. Extract JSON from response text                                         │
│  2. Parse JSON string to Python dict                                        │
│  3. Validate risk factor fields                                             │
│  4. Convert to RiskAssessmentOutput model                                   │
│  5. Return structured response                                              │
│                                                                              │
└────────────────────────────────┬───────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                       RESPONSE MODEL VALIDATION                             │
│                     (api/models.py - RiskAssessmentOutput)                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  RiskAssessmentOutput                                                        │
│  ├── customer_id: str (optional)                                            │
│  ├── overall_risk_level: str (LOW|MEDIUM|HIGH|CRITICAL)                     │
│  ├── overall_risk_score: float (0-100)                                      │
│  ├── risk_factors: List[RiskFactor]                                         │
│  │   └── RiskFactor                                                         │
│  │       ├── factor_name: str                                               │
│  │       ├── risk_level: str (LOW|MEDIUM|HIGH|CRITICAL)                     │
│  │       ├── score: float (0-100)                                           │
│  │       └── description: str                                               │
│  ├── recommendations: List[str]                                             │
│  ├── assessment_date: str (ISO format)                                      │
│  └── additional_notes: str (optional)                                       │
│                                                                              │
└────────────────────────────────┬───────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         RESPONSE LAYER                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  HTTP 200 OK                                                                 │
│  Content-Type: application/json                                              │
│                                                                              │
│  {                                                                           │
│    "customer_id": "CUST001",                                                 │
│    "overall_risk_level": "MEDIUM",                                           │
│    "overall_risk_score": 52.3,                                               │
│    "risk_factors": [...],                                                    │
│    "recommendations": [...],                                                 │
│    "assessment_date": "2025-11-20T14:30:22.123456",                         │
│    "additional_notes": "..."                                                 │
│  }                                                                           │
│                                                                              │
└────────────────────────────────┬───────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        CLIENT RECEIVES RESPONSE                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐         │
│  │ Browser displays │  │ Python script    │  │ JavaScript app   │         │
│  │ assessment in    │  │ processes data   │  │ updates UI       │         │
│  │ Swagger UI       │  │ and makes        │  │ with results     │         │
│  │                  │  │ decisions        │  │                  │         │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘


╔══════════════════════════════════════════════════════════════════════════════╗
║                            DATA FLOW SUMMARY                                 ║
╚══════════════════════════════════════════════════════════════════════════════╝

1. CLIENT SENDS CUSTOMER DATA
   └─► JSON request with customer information

2. FASTAPI VALIDATES INPUT
   └─► Pydantic models ensure data integrity

3. SERVICE ORCHESTRATES ASSESSMENT
   └─► RiskAssessmentServiceOllama coordinates the workflow

4. OLLAMA SERVICE PREPARES REQUEST
   └─► Builds intelligent prompt from customer data

5. OLLAMA API PROCESSES REQUEST
   └─► Language model analyzes and generates assessment

6. RESPONSE IS PARSED
   └─► AI response converted to structured JSON

7. OUTPUT IS VALIDATED
   └─► Pydantic ensures response format correctness

8. CLIENT RECEIVES RISK ASSESSMENT
   └─► Structured JSON with risk factors and recommendations


╔══════════════════════════════════════════════════════════════════════════════╗
║                         KEY COMPONENTS                                       ║
╚══════════════════════════════════════════════════════════════════════════════╝

┌─ CONFIGURATION ─────────────────────────────────────────────┐
│ • config.py: Settings management and environment variables │
│ • .env: Runtime configuration                              │
└─────────────────────────────────────────────────────────────┘

┌─ API LAYER ─────────────────────────────────────────────────┐
│ • main.py: FastAPI application setup                       │
│ • api/routes.py: Endpoint definitions                      │
│ • api/models.py: Request/response data models             │
└─────────────────────────────────────────────────────────────┘

┌─ BUSINESS LOGIC ────────────────────────────────────────────┐
│ • services/risk_assessment_ollama.py: Assessment logic     │
│ • services/ollama_service.py: Ollama integration           │
│ • services/risk_assessment.py: Legacy rules (optional)     │
└─────────────────────────────────────────────────────────────┘

┌─ EXTERNAL SERVICES ─────────────────────────────────────────┐
│ • Ollama API: Language model inference                     │
│ • HTTP Requests: Communication bridge                      │
└─────────────────────────────────────────────────────────────┘


╔══════════════════════════════════════════════════════════════════════════════╗
║                          ERROR HANDLING                                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

Exception Type          │ Handler                │ Response
────────────────────────┼────────────────────────┼──────────────────────
Ollama unavailable      │ health_check()        │ 503 Service Unavailable
Invalid customer data   │ Pydantic validation   │ 422 Unprocessable Entity
JSON parse error        │ _extract_json()       │ 500 Internal Server Error
Request timeout         │ requests timeout      │ 500 with timeout message
Network error           │ RequestException      │ 500 with error details


╔══════════════════════════════════════════════════════════════════════════════╗
║                    DEPLOYMENT ARCHITECTURE                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

DEVELOPMENT:
┌──────────┐
│ Terminal │ ollama serve ◄─── Ollama Service (localhost:11434)
└──────────┘

┌──────────┐
│ Terminal │ uvicorn main:app --reload ◄─── FastAPI (localhost:8000)
└──────────┘

┌──────────┐
│ Terminal │ Browser / curl / Python ◄─── Client Applications
└──────────┘


PRODUCTION:
┌──────────────┐
│ Ollama VM    │ GPU-enabled instance with Ollama service
│ (Separate)   │
└──────┬───────┘
       │
       │ HTTP/HTTPS
       │
┌──────▼───────────────────┐
│ FastAPI Container        │
│ (Production ASGI Server) │
│ - Gunicorn + Uvicorn    │
│ - Load Balancer         │
│ - Rate Limiting         │
│ - Request Queuing       │
└──────────────────────────┘
       │
       │ HTTP/HTTPS
       │
┌──────▼──────────────────────┐
│ Client Applications         │
│ - Web Dashboard            │
│ - Mobile App               │
│ - Integrations             │
└─────────────────────────────┘
```

## Key Characteristics

✅ **Modular Design** - Separate concerns (API, business logic, integration)  
✅ **Robust Error Handling** - Graceful failure at each layer  
✅ **Clear Data Flow** - Customer data → Processing → Risk assessment  
✅ **Extensible** - Easy to add new risk factors or rules  
✅ **Configurable** - Model, temperature, timeout all adjustable  
✅ **Observable** - Logging at each stage for debugging  
✅ **Tested** - Health checks and validation throughout  
