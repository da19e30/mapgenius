# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Mapgenius Solutions - an AI-powered invoice automation and financial analytics platform.
- **Backend**: Python (FastAPI + SQLAlchemy) with SQLite (dev) / PostgreSQL (prod-ready)
- **Frontend**: React + TypeScript + Vite + Tailwind CSS + Recharts
- **AI**: OCR (Tesseract), classification (spaCy), forecasting (scikit-learn) - all optional graceful fallbacks

## Development Commands

### Backend
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000  # Start dev server
python test_flow.py                                 # Run full API test flow
python -m pytest                                          # Run tests (when available)
```

### Frontend
```bash
cd frontend
npm run dev          # Start Vite dev server (http://localhost:5173)
npm run build        # Production build
npx tsc --noEmit   # TypeScript type checking
```

### Environment Setup
- Backend: `python -m pip install -r backend/requirements.txt`
- Frontend: `cd frontend && npm install`
- Copy `backend/.env.example` to `backend/.env` and configure SMTP settings for email notifications

## Architecture

### Backend Structure
```
backend/
├── app/
│   ├── main.py              # FastAPI app, CORS, router registration
│   ├── database.py          # SQLAlchemy engine, session, Base
│   ├── models/              # SQLAlchemy models (User, Invoice, FinancialData)
│   ├── routes/              # API routes (user, invoices, financial, ai_routes)
│   ├── services/            # Business logic (auth, jwt, ocr, email, file_validator)
│   ├── ai/                  # AI modules (classifier, predictor, insights, ocr_enhancer)
│   └── middleware/          # Security middleware
├── .env                    # Environment variables (DATABASE_URL, JWT secrets, SMTP)
└── requirements.txt
```

### Frontend Structure
```
frontend/
├── src/
│   ├── pages/              # Page components (Landing, Login, Register, Dashboard, UploadInvoice, Transactions)
│   ├── components/         # Reusable UI (Layout with sidebar + top bar)
│   ├── services/           # API client (axios with JWT interceptor)
│   ├── context/            # AuthContext (JWT + email state, login/logout)
│   └── App.tsx             # Routing (public + private routes)
├── postcss.config.js      # PostCSS with Tailwind CSS + autoprefixer (ESM export)
├── vite-env.d.ts          # Vite client types for import.meta.env
└── package.json
```

## Key Patterns

### Authentication Flow
1. User registers → `POST /api/v1/users/register` → sends welcome email + admin notification
2. User logs in → `POST /api/v1/users/login` → returns JWT (30min expiry)
3. JWT attached to all subsequent requests via axios interceptor (`Authorization: Bearer <token>`)
4. `AuthContext` stores token + email in localStorage, provides `useAuth()` hook

### Invoice Processing Pipeline
1. Upload: `POST /api/v1/invoices/upload` (multipart file, validates extension/size)
2. OCR: Extract text via Tesseract (optional - graceful fallback if not installed)
3. Classification: AI categorization via spaCy (optional)
4. Storage: Invoice + FinancialData records in DB

### Email Notifications
- Configured via SMTP in `backend/.env` (supports Hotmail/Outlook/Gmail)
- `backend/app/services/email.py` handles:
  - Welcome emails to new users
  - Admin notifications to `ADMIN_EMAIL` (currently `vialfonsos.a@hotmail.com`)
- If SMTP not configured, emails are simulated (printed to console)

### Routing
- **Public**: `/` (Landing), `/login`, `/register`
- **Protected** (require JWT): `/dashboard`, `/upload-invoice`, `/transactions`
- Private routes wrapped in `PrivateRoute` component with `Layout` (sidebar + top bar)

## Important Notes

- **Database**: Defaults to SQLite (`sqlite:///mapgenius.db`). Set `DATABASE_URL` env var for PostgreSQL.
- **OCR**: Tesseract is optional. If not installed, invoices are stored with `ocr_status="uploaded"` but not processed.
- **AI modules**: Have try/except guards - the app starts even if `spacy`, `sklearn`, `pandas` are not installed.
- **CORS**: Currently allows all origins (`*`); restrict in production.
- **JWT secret**: Currently hardcoded in `.env` as `SECRET_KEY` - rotate for production.

## Common Tasks

- **Add new API route**: Create file in `backend/app/routes/`, add router to `backend/app/main.py`
- **Add new page**: Create in `frontend/src/pages/`, add route in `frontend/src/App.tsx`, link in `frontend/src/components/Layout.tsx`
- **Add new AI feature**: Extend `backend/app/ai/` modules, add endpoint in `backend/app/routes/ai_routes.py`

## UI/UX Patterns

- **Design system**: Indigo/purple gradient backgrounds, white cards, Tailwind CSS
- **Forms**: Floating labels, password strength indicator, show/hide toggle, social login buttons (Google/Microsoft - UI only)
- **Charts**: Recharts (BarChart for categories, LineChart for trends)
- **Responsive**: Mobile-first with `md:` breakpoints
