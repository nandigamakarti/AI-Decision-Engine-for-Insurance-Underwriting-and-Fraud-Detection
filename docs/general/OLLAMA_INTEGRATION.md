# Ollama Integration Summary

## What Was Implemented

I've successfully integrated **Ollama** into your Risk Assessment Engine to replace hardcoded assessment logic with **AI-driven dynamic risk evaluation**. The system now generates structured JSON responses based on real customer data analysis by a language model.

## Key Components Created

### 1. **Configuration Management** (`config.py`)
- Centralized settings from environment variables
- Ollama connection details (URL, model, temperature, etc.)
- FastAPI server configuration

### 2. **Ollama Integration Service** (`services/ollama_service.py`)
- Communicates with Ollama API
- Builds intelligent prompts for risk assessment
- Parses AI responses into structured JSON format
- Handles errors and JSON extraction
- Health checks for Ollama connectivity

### 3. **AI-Driven Risk Assessment** (`services/risk_assessment_ollama.py`)
- New service that uses Ollama instead of hardcoded rules
- Seamlessly replaces the previous rule-based service
- Maintains compatibility with existing API contracts

### 4. **Enhanced API Routes** (`api/routes.py`)
- Updated endpoints to use Ollama service
- Added comprehensive logging
- Better error handling with detailed messages
- Health check for Ollama service status

### 5. **Updated Main Application** (`main.py`)
- Integrated configuration system
- Startup event to verify Ollama connectivity
- New `/api/ollama-status` endpoint to check service health
- Structured logging throughout

### 6. **Documentation** (`OLLAMA_SETUP.md`)
- Complete setup guide
- Troubleshooting section
- Performance notes
- Example API calls in multiple languages

### 7. **Testing & Validation** (`test_setup.py`)
- Validates Ollama installation
- Tests API connectivity
- Sample customer assessment
- Helpful error messages and setup instructions

## How It Works

### Old Approach (Hardcoded Rules)
```
Customer Data → Rule Engine → Hardcoded Scoring Logic → Risk Assessment
```

### New Approach (AI-Powered with Ollama)
```
Customer Data → Smart Prompt Generation → Ollama LLM → JSON Parsing → Risk Assessment
```

## Key Features

✅ **Dynamic Assessment**: AI analyzes each unique customer profile  
✅ **Structured Output**: Returns valid JSON with risk factors, scores, and recommendations  
✅ **Contextual Analysis**: Considers relationships between health, financial, and claims data  
✅ **Detailed Recommendations**: AI generates actionable underwriting guidance  
✅ **Proper Error Handling**: Clear messages if Ollama is unavailable  
✅ **Health Checks**: Built-in endpoints to verify system status  
✅ **Configurable Models**: Easy to switch between different Ollama models  
✅ **Detailed Logging**: Full visibility into assessment process  

## Quick Start

### 1. Install Ollama
Download from [ollama.ai](https://ollama.ai/) and install

### 2. Pull a Model
```bash
ollama pull mistral
```

### 3. Start Ollama (Terminal 1)
```bash
ollama serve
```

### 4. Install Dependencies (if not done)
```bash
uv sync
```

### 5. Start FastAPI (Terminal 2)
```bash
uvicorn main:app --reload
```

### 6. Test the Setup
```bash
python test_setup.py
```

### 7. Visit Documentation
Open http://127.0.0.1:8000/docs in your browser

## API Response Example

The new Ollama-powered endpoint returns intelligent, contextual risk assessments:

```json
{
  "customer_id": "CUST001",
  "overall_risk_level": "MEDIUM",
  "overall_risk_score": 52.3,
  "risk_factors": [
    {
      "factor_name": "Pre-existing Chronic Conditions",
      "risk_level": "MEDIUM",
      "score": 55,
      "description": "Customer has Type 2 Diabetes and Hypertension, both requiring ongoing management..."
    }
  ],
  "recommendations": [
    "REQUEST: Obtain updated medical reports for diabetes and hypertension",
    "CONSIDER: Wellness program enrollment with premium incentives",
    "APPROVE: Standard underwriting with possible 10-15% risk adjustment"
  ],
  "assessment_date": "2025-11-20T14:30:22.123456",
  "additional_notes": "Overall risk profile is moderate. Customer demonstrates good financial responsibility..."
}
```

## Configuration (`.env`)

```env
# Ollama Settings
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral                    # or llama2, neural-chat, etc.
OLLAMA_TEMPERATURE=0.7                  # Adjust for consistency
OLLAMA_TOP_P=0.9                        # Nucleus sampling
OLLAMA_TIMEOUT=120                      # Seconds to wait for response

# FastAPI Settings
API_HOST=127.0.0.1
API_PORT=8000
API_RELOAD=true
API_LOG_LEVEL=info
```

## New Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/risk-assessment` | POST | AI-powered risk assessment |
| `/api/health` | GET | Simple health check |
| `/api/ollama-status` | GET | Check Ollama service status |

## Environment Setup

1. Created `.env` - Configuration file (already populated)
2. Created `.env.example` - Template for reference
3. Created `config.py` - Configuration loader
4. All settings are environment-variable driven for easy deployment

## Switching Models

Change `OLLAMA_MODEL` in `.env`:

- `mistral` - Fast, good for insurance (7.3B)
- `llama2` - More capable (7B-70B variants)
- `neural-chat` - Instruction-following (6.7B)
- `dolphin` - Lightweight (2.6B-7B)

```bash
ollama pull llama2
# Then update .env: OLLAMA_MODEL=llama2
```

## Next Steps

1. **Set up Ollama** - Download and install from ollama.ai
2. **Pull a model** - `ollama pull mistral`
3. **Start Ollama** - `ollama serve`
4. **Run test** - `python test_setup.py`
5. **Access API** - Visit http://127.0.0.1:8000/docs

## Performance Notes

Expected response times:
- **Mistral 7B**: 10-30 seconds
- **Llama2 7B**: 15-40 seconds
- **Llama2 13B**: 30-60 seconds

First request may be slower due to model loading.

## Troubleshooting

**Q: "Could not connect to Ollama"**  
A: Make sure `ollama serve` is running in a separate terminal

**Q: "Request timed out"**  
A: Increase `OLLAMA_TIMEOUT` in `.env` or use a smaller model

**Q: "Model not found"**  
A: Run `ollama pull mistral` (or your chosen model)

## File Structure

```
api/
├── models.py              # ← Data models (updated)
└── routes.py              # ← API endpoints (updated)

services/
├── ollama_service.py      # ← NEW: Ollama integration
├── risk_assessment_ollama.py  # ← NEW: AI-driven assessment
└── risk_assessment.py     # ← OLD: Hardcoded rules (kept for reference)

config.py                  # ← NEW: Configuration management
main.py                    # ← UPDATED: Enhanced app setup
test_setup.py              # ← NEW: Setup validation script
.env                       # ← NEW: Environment configuration
.env.example               # ← NEW: Configuration template
OLLAMA_SETUP.md            # ← NEW: Complete setup guide
example_customer_request.json  # ← NEW: Example request
```

## Dependencies Added

```toml
"requests"      # HTTP calls to Ollama
"python-dotenv" # Environment variable loading
"ollama"        # Optional: Ollama Python library
```

All dependencies are in `pyproject.toml` and installed with `uv sync`.

## Backward Compatibility

- The original hardcoded rule-based service (`risk_assessment.py`) is still available
- You can switch back to hardcoded assessment by editing `api/routes.py` if needed
- API contract remains unchanged - same request/response format

---

**Your system is now AI-powered and ready to generate dynamic, context-aware risk assessments!** 🚀
