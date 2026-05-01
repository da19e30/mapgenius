---
name: deploy
description: Deploy Mapgenius Solutions (local Docker or production setup)
---

# Deploy Mapgenius Solutions

This skill provides deployment guidance for the Mapgenius project.

## When to Use

- User asks to "deploy", "dockerize", "production setup", or "go live"
- Need to run the full stack in Docker containers
- Need to configure production environment

## Local Deployment with Docker

### Prerequisites

- Docker Desktop installed and running
- Project files ready

### Create Dockerfile for Backend

Create `backend/Dockerfile`:
```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Create Dockerfile for Frontend

Create `frontend/Dockerfile`:
```dockerfile
FROM node:20-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY ../nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Create docker-compose.yml

Create in project root:
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    env_file:
      - ./backend/.env
    volumes:
      - ./backend:/app
    depends_on:
      - db

  frontend:
    build: ./frontend
    ports:
      - "5173:80"
    depends_on:
      - backend

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: mapgenius
      POSTGRES_PASSWORD: secure_password
      POSTGRES_DB: mapgenius
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

### Update backend/.env for Production

```
DATABASE_URL=postgresql+psycopg2://mapgenius:secure_password@db:5432/mapgenius
SECRET_KEY=your-strong-production-secret-key-here
ALGORITHM=HS256

# SMTP (update with real credentials)
SMTP_HOST=smtp-outlook.com
SMTP_PORT=587
SMTP_USER=your-email@outlook.com
SMTP_PASSWORD=your_app_password
SMTP_SENDER=your-email@outlook.com
ADMIN_EMAIL=admin@yourdomain.com
SMTP_USE_TLS=true

# CORS (update for production domain)
# CORS_ORIGINS=https://yourdomain.com
```

### Run with Docker Compose

```bash
docker-compose up -d --build
```

## Production Deployment Checklist

### Security
- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Set `ALGORITHM=HS256` (already set)
- [ ] Configure real SMTP credentials
- [ ] Restrict CORS origins (don't use `*` in production)
- [ ] Enable HTTPS (use nginx reverse proxy with SSL)
- [ ] Set `DATABASE_URL` to production PostgreSQL

### Performance
- [ ] Use gunicorn instead of uvicorn for backend:
  ```bash
  gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
  ```
- [ ] Enable caching for AI endpoints
- [ ] Set up database connection pooling

### Monitoring
- [ ] Add logging (structured logs)
- [ ] Set up health check endpoint (already at `/health`)
- [ ] Monitor disk space for uploaded files

## Quick Local Test

Without Docker, you can test production-like setup:

1. **Build frontend**:
   ```bash
   cd frontend && npm run build
   # Serve with any static server: npx serve dist/
   ```

2. **Run backend with gunicorn**:
   ```bash
   cd backend && gunicorn -w 2 app.main:app --bind 0.0.0.0:8000
   ```

## Common Issues

| Problem | Solution |
|----------|----------|
| `port already in use` | `docker-compose down` then `docker-compose up -d` |
| `ModuleNotFoundError: No module named 'psycopg2'` | Add `psycopg2-binary` to requirements.txt |
| Frontend can't reach backend | Check CORS settings; verify `VITE_API_URL` in frontend |
| Database connection error | Verify PostgreSQL is running; check `DATABASE_URL` format |

## Current Project Status

- Backend runs on FastAPI with Uvicorn (dev) or Gunicorn (prod)
- Frontend uses Vite dev server (dev) or static build (prod)
- Database: SQLite (dev) or PostgreSQL (prod-ready)
- Email: SMTP via Outlook/Hotmail (configurable in `.env`)
