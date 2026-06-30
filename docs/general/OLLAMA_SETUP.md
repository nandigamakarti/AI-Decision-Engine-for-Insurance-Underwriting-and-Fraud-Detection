# Insurance Risk Assessment Engine - Ollama Integration Guide

## Overview

This project is an AI-assisted insurance underwriting system that uses **Ollama** to dynamically assess customer risk. Instead of using hardcoded rules, it leverages a local LLM (Language Model) to analyze comprehensive customer data and generate structured risk assessments.

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.ai/) installed and running
- [uv](https://github.com/astral-sh/uv) package manager

## Installation & Setup

### 1. Install Ollama

Download and install Ollama from [ollama.ai](https://ollama.ai/).

### 2. Pull a Model

Pull a model to use. We recommend **Mistral** for insurance risk assessment:

```bash
ollama pull mistral
```

Other options:
- `ollama pull llama2` - Larger, more capable
- `ollama pull neural-chat` - Optimized for instructions

### 3. Start Ollama Service

Open a terminal and start Ollama (it will run on `localhost:11434` by default):

```bash
ollama serve
```

You should see output like:
```
2025/11/20 10:00:00 "GET /api/tags HTTP/1.1" 200 0
```

### 4. Set Up Python Environment

Clone the repository and create a virtual environment:

```bash
cd uw-risk-assessment-engine
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 5. Install Dependencies

```bash
uv sync
```

This installs:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `pydantic` - Data validation
- `requests` - HTTP client for Ollama
- `python-dotenv` - Environment configuration
- `ollama` - Ollama Python library (optional, using requests instead)

### 6. Configure Environment

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```env
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral
OLLAMA_TEMPERATURE=0.7
OLLAMA_TOP_P=0.9
OLLAMA_TIMEOUT=120

# FastAPI Configuration
API_HOST=127.0.0.1
API_PORT=8000
API_RELOAD=true
API_LOG_LEVEL=info
```

## Running the Application

### Terminal 1: Start Ollama Service

```bash
ollama serve
```

Keep this running in the background.

### Terminal 2: Start FastAPI Server

```bash
cd uw-risk-assessment-engine
source .venv/bin/activate  # Activate virtual environment
uvicorn main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

## API Documentation

### Access Interactive Documentation

Once the server is running, visit:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

### Main Endpoint: Risk Assessment

**POST** `/api/risk-assessment`

Accepts a comprehensive customer profile and returns AI-generated risk assessment.

#### Request Example

```json
{
  "customer_id": "CUST001",
  "personal_info": {
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "1978-05-15",
    "age": 47,
    "gender": "Male",
    "email": "john.doe@example.com",
    "phone": "555-0123"
  },
  "health_info": {
    "health_conditions": ["Type 2 Diabetes", "Hypertension"],
    "medications": ["Metformin", "Lisinopril"],
    "medical_history": "Diagnosed with diabetes 5 years ago, well managed with medication",
    "smoker": false,
    "alcohol_consumption": "Moderate (3-4 units per week)",
    "exercise_frequency": "3 times per week",
    "bmi": 28.5
  },
  "financial_info": {
    "annual_income": 85000,
    "employment_status": "Employed",
    "occupation": "Software Engineer",
    "credit_score": 740,
    "outstanding_debts": 25000,
    "assets": 250000
  },
  "claims_history": {
    "total_claims": 2,
    "major_claims": ["Hospitalization - 2019"],
    "claim_frequency": "Occasional",
    "last_claim_date": "2020-03-15",
    "claim_amount_total": 45000
  }
}
```

#### Response Example

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
      "description": "Customer has Type 2 Diabetes and Hypertension, both requiring ongoing management and medication. These conditions increase healthcare costs and potential complications."
    },
    {
      "factor_name": "BMI and Weight Management",
      "risk_level": "MEDIUM",
      "score": 48,
      "description": "BMI of 28.5 falls into the overweight category, which is associated with increased health risks"
    },
    {
      "factor_name": "Financial Stability",
      "risk_level": "LOW",
      "score": 25,
      "description": "Good credit score of 740, stable employment, and reasonable debt-to-income ratio indicate financial stability"
    },
    {
      "factor_name": "Claims History",
      "risk_level": "MEDIUM",
      "score": 45,
      "description": "2 claims in history with one major hospitalization claim. Pattern suggests manageable but present health risks"
    }
  ],
  "recommendations": [
    "REQUEST: Obtain updated medical reports for both diabetes and hypertension management",
    "REQUEST: Provide evidence of medication adherence and regular specialist visits",
    "CONSIDER: Wellness program enrollment with premium incentives for fitness tracking",
    "APPROVE: Standard underwriting with possible 10-15% risk adjustment based on condition management verification",
    "MONITOR: Annual reviews recommended to track disease progression"
  ],
  "assessment_date": "2025-11-20T14:30:22.123456",
  "additional_notes": "Overall risk profile is moderate. Customer demonstrates good financial responsibility and non-smoking status which are positive indicators. Primary concern is the management and progression of chronic conditions. With proper documentation of disease control and medication compliance, this customer represents acceptable risk."
}
```

### Health Checks

**GET** `/api/health`

Simple health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "Risk Assessment Engine"
}
```

**GET** `/api/ollama-status`

Check if Ollama service is running and accessible.

**Response:**
```json
{
  "status": "healthy",
  "service": "Ollama",
  "base_url": "http://localhost:11434",
  "model": "mistral",
  "temperature": 0.7,
  "top_p": 0.9
}
```

## Using with cURL

### Test the API

```bash
curl -X POST "http://127.0.0.1:8000/api/risk-assessment" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "TEST001",
    "personal_info": {
      "first_name": "Jane",
      "last_name": "Smith",
      "age": 35,
      "email": "jane@example.com"
    },
    "health_info": {
      "smoker": false,
      "bmi": 22.0
    },
    "financial_info": {
      "annual_income": 95000,
      "credit_score": 800
    }
  }'
```

## Configuration Options

### Ollama Models

Different models with different trade-offs:

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| Mistral | 7.3B | Fast | Good | Balanced, insurance assessments |
| Llama2 | 7B/13B/70B | Medium | Excellent | Complex reasoning |
| Neural-chat | 6.7B | Fast | Good | Instructions/queries |
| Dolphin | 2.6B/7B | Very Fast | Fair | Low-latency responses |

Pull additional models:
```bash
ollama pull llama2
ollama pull neural-chat
```

### Temperature & Top-P

Adjust in `.env`:

```env
OLLAMA_TEMPERATURE=0.7      # 0.0 = deterministic, 1.0 = creative
OLLAMA_TOP_P=0.9            # Nucleus sampling (0.0-1.0)
OLLAMA_TIMEOUT=120          # Request timeout in seconds
```

Lower temperature (0.3-0.5) = More consistent, structured responses  
Higher temperature (0.8-1.0) = More creative, variable responses

## Project Structure

```
uw-risk-assessment-engine/
├── main.py                           # FastAPI entry point
├── config.py                         # Configuration management
├── pyproject.toml                    # Project dependencies
├── .env.example                      # Example environment file
├── api/
│   ├── __init__.py
│   ├── models.py                     # Pydantic data models
│   └── routes.py                     # API endpoints
├── services/
│   ├── __init__.py
│   ├── ollama_service.py             # Ollama integration
│   ├── risk_assessment_ollama.py     # AI-driven assessment logic
│   └── risk_assessment.py            # Legacy hardcoded rules (optional)
└── README.md                         # This file
```

## Troubleshooting

### Issue: "Could not connect to Ollama at http://localhost:11434"

**Solution:**
1. Make sure Ollama is running: `ollama serve`
2. Check Ollama is accessible: `curl http://localhost:11434/api/tags`
3. Verify `OLLAMA_BASE_URL` in `.env` is correct
4. Try `http://host.docker.internal:11434` if running in Docker

### Issue: "Request timed out"

**Solution:**
1. Increase `OLLAMA_TIMEOUT` in `.env` (current: 120 seconds)
2. Larger models take more time. Check model size:
   ```bash
   ollama list
   ```
3. Try a smaller/faster model

### Issue: "Model not found"

**Solution:**
```bash
ollama pull mistral  # or your preferred model
ollama list          # verify it's installed
```

### Issue: High CPU/Memory usage

**Solution:**
- Use a smaller model: `ollama pull mistral` instead of `llama2:70b`
- Reduce concurrent requests
- Check system resources: `ollama ps`

## Performance Notes

**Response Times** (approximate):
- Mistral 7B: 10-30 seconds
- Llama2 7B: 15-40 seconds
- Llama2 13B: 30-60 seconds
- Llama2 70B: 60-120+ seconds

First request may be slower due to model loading into memory.

## Production Deployment

For production:

1. **Security:**
   - Set `allow_origins` in CORS to specific domains
   - Add authentication/API keys
   - Use environment variables for sensitive config

2. **Performance:**
   - Deploy Ollama on GPU hardware
   - Use a production ASGI server (Gunicorn + Uvicorn)
   - Implement request queuing/rate limiting

3. **Monitoring:**
   - Add structured logging (JSON)
   - Set up error tracking (Sentry)
   - Monitor Ollama health

4. **Docker Deployment:**
   ```bash
   docker run -d -p 11434:11434 ollama/ollama
   docker build -t risk-assessment .
   docker run -p 8000:8000 risk-assessment
   ```

## API Examples

### Python Client

```python
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

customer_data = {
    "customer_id": "CUST001",
    "personal_info": {
        "first_name": "John",
        "last_name": "Doe",
        "age": 45
    },
    "health_info": {
        "smoker": False,
        "bmi": 24.5
    },
    "financial_info": {
        "annual_income": 75000,
        "credit_score": 750
    }
}

response = requests.post(
    f"{BASE_URL}/api/risk-assessment",
    json=customer_data
)

assessment = response.json()
print(json.dumps(assessment, indent=2))
```

### JavaScript/Node.js Client

```javascript
const baseURL = "http://127.0.0.1:8000";

const customerData = {
    customer_id: "CUST001",
    personal_info: {
        first_name: "John",
        last_name: "Doe",
        age: 45
    },
    health_info: {
        smoker: false,
        bmi: 24.5
    }
};

fetch(`${baseURL}/api/risk-assessment`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(customerData)
})
.then(res => res.json())
.then(assessment => console.log(JSON.stringify(assessment, null, 2)));
```

## Additional Resources

- [Ollama Documentation](https://github.com/ollama/ollama)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Ollama Model Library](https://ollama.ai/library)

## License

This project is part of the Monocept Insurance Underwriting PoC.

## Support

For issues or questions, please contact the development team.
