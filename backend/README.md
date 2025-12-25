# Backend API

FastAPI backend for Shopify Store Health Scanner.

## Setup

```bash
# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn main:app --reload
```

Server runs on: http://localhost:8000

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info |
| GET | `/health` | Health check |
| POST | `/scan` | Scan Shopify store |

## Request Example

```bash
curl -X POST "http://localhost:8000/scan" \
  -H "Content-Type: application/json" \
  -d '{"store_url": "https://gymshark.com"}'
```

## Response Example

```json
{
  "store_url": "https://gymshark.com",
  "overall_score": 78,
  "seo_score": 85,
  "performance_score": 72,
  "image_score": 80,
  "mobile_score": 75,
  "issues": ["Missing meta description", "23 images without alt text"],
  "recommendations": ["Fix SEO issues first", "Optimize images"]
}
```

## Environment Variables

Create `.env` file:

```env
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=["http://localhost:5173"]
```

## Deploy to Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

## Dependencies

- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `httpx` - HTTP client
- `beautifulsoup4` - HTML parser
- `pydantic` - Data validation

## API Documentation

Visit http://localhost:8000/docs for interactive Swagger UI documentation.