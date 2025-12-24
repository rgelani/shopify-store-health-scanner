# Shopify Store Health Scanner - Backend API

FastAPI backend that scans Shopify stores and returns health reports.

## Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
uvicorn main:app --reload
```

## API Endpoints

- `GET /` - API info
- `GET /health` - Health check
- `POST /scan` - Scan a Shopify store

## Deploy to Railway
```bash
railway login
railway init
railway up
```