# Shopify Store Health Scanner

A free diagnostic tool that analyzes Shopify stores for SEO, performance, and optimization issues.

## Features

- SEO analysis (meta tags, titles, headings)
- Performance audit (load speed, scripts)
- Image optimization checks
- Mobile responsiveness validation
- Detailed scoring and recommendations

## Tech Stack

**Backend:** FastAPI (Python)  
**Frontend:** React + Vite  
**Styling:** Tailwind CSS

## Quick Start

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Visit: http://localhost:5173

## Deployment

- **Backend:** Railway.app
- **Frontend:** Netlify

## Project Structure

```
shopify-scanner/
├── backend/        # FastAPI backend
└── frontend/       # React frontend
```

## License

MIT