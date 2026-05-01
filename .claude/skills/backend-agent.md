---
name: backend-agent
description: Agente especializado en el backend de Mapgenius (FastAPI, SQLAlchemy, rutas, servicios)
---

# Backend Agent - Mapgenius Solutions

Agente principal para todo el desarrollo backend.

## Cuando usarlo

- Usuario menciona "backend", "API", "FastAPI", "rutas", "modelos", "SQLAlchemy"
- Necesitas añadir endpoints, modificar modelos, o arreglar errores en `backend/`
- Tareas de base de datos, migraciones, o consultas

## Estructura que maneja

```
backend/
├── app/
│   ├── main.py              # Punto de entrada, registro de rutas
│   ├── database.py          # Engine, sesión, Base
│   ├── models/              # User, Invoice, FinancialData
│   ├── routes/              # user, invoices, financial, ai_routes
│   ├── services/            # auth, jwt, ocr, email, file_validator
│   ├── ai/                  # classifier, predictor, insights, ocr_enhancer
│   └── middleware/          # Security middleware
├── .env                    # Variables de entorno
└── requirements.txt
```

## Sub‑Agentes recomendados

### 1. Sub‑Agente: Models & DB
**Tarea**: Crear, modificar modelos SQLAlchemy y configurar migraciones.
**Cuando**: Cambios en `backend/app/models/`, `database.py`, o esquema de BD.
**Scope**: 
- Añadir columnas, relaciones, índices.
- Ejecutar `init_db()` o migraciones.
- Borrar `mapgenius.db` si hay cambios de esquema.

### 2. Sub‑Agente: API Routes
**Tarea**: Crear y modificar endpoints en `backend/app/routes/`.
**Cuando**: Nuevos endpoints, cambios en request/response, validación.
**Scope**:
- Respetar prefijo `/api/v1`.
- Incluir `response_model`, manejo de errores.
- Proteger endpoints con `get_current_user` si requieren auth.

### 3. Sub‑Agente: Services
**Tarea**: Lógica de negocio en `backend/app/services/`.
**Cuando**: Nuevos servicios, integración con APIs externas, emails.
**Scope**:
- `auth.py`: hash, verify passwords.
- `jwt.py`: crear/validar tokens.
- `email.py`: enviar correos (SMTP).
- `ocr.py`: extracción de texto (Tesseract).
- `file_validator.py`: validación de archivos.

## Comandos clave

```bash
cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000  # Iniciar servidor
cd backend && python test_flow.py                                # Probar flujo completo
```

## Notas importantes

- **DB por defecto**: SQLite (`sqlite:///mapgenius.db`). Configurar `DATABASE_URL` para PostgreSQL.
- **OCR opcional**: Si Tesseract no está, las facturas se suben pero no se procesan (`ocr_status="uploaded"`).
- **JWT**: Expira en 30 min. Configurado en `backend/app/services/jwt.py`.
- **Email**: SMTP configurado en `.env`. Si no hay credenciales, simula envío (imprime en consola).
