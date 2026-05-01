---
name: database-agent
description: Agente especializado en bases de datos, modelos SQLAlchemy y consultas
---

# Database Agent - Mapgenius Solutions

Agente para todo lo relacionado con persistencia de datos.

## Cuando usarlo

- Cambios en modelos (`backend/app/models/`)
- Configuración de motor de base de datos (`backend/app/database.py`)
- Consultas SQL, optimización, índices
- Migraciones y cambios de esquema

## Estructura

### Modelos principales

```python
# User (backend/app/models/user.py)
- id, username, email, password, created_at
- Relaciones: invoices, financial_data

# Invoice (backend/app/models/invoice.py)
- id, user_id, filename, file_type, file_size, filepath
- extracted_text, total_amount, issue_date
- rfc_emisor, rfc_receptor, currency, invoice_number
- ocr_status, ocr_language, uploaded_at, processed_at
- Relación: financial_data

# FinancialData (backend/app/models/financial_data.py)
- id, user_id, invoice_id, category, amount, currency
- transaction_date, rfc_emisor, rfc_receptor
- invoice_number, extracted_at, confidence_score
```

### Configuración de BD

```python
# backend/app/database.py
engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=10)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

## Sub‑Agentes

### 1. Sub‑Agente: Schema Designer
**Tarea**: Diseñar y modificar el esquema de base de datos.
**Scope**:
- Añadir nuevas tablas o columnas.
- Definir relaciones (ForeignKey, back_populates).
- Asegurar que los modelos tienen `Tablename__` correcto.

### 2. Sub‑Agente: Query Optimizer
**Tarea**: Optimizar consultas y añadir índices.
**Scope**:
- Revisar `index=True` en columnas de búsqueda frecuente.
- Usar `joinedload()` para evitar N+1 queries.
- Añadir `relationship(lazy='selectin')` cuando sea apropiado.

### 3. Sub‑Agente: Migration Manager
**Tarea**: Gestionar cambios de esquema y migraciones.
**Scope**:
- Para SQLite: borrar `mapgenius.db` y dejar que `init_db()` recree tablas.
- Para PostgreSQL: usar Alembic (`backend/alembic/`).
- Siempre hacer backup antes de cambios mayores.

## Comandos

```bash
# Recrear base de datos (SQLite)
rm -f backend/mapgenius.db
cd backend && python -c "from app.database import init_db; init_db()"

# Verificar tablas
sqlite3 backend/mapgenius.db ".tables"

# Consulta rápida
sqlite3 backend/mapgenius.db "SELECT * FROM users LIMIT 5;"
```

## Notas

- **SQLite en desarrollo**: Los cambios de esquema requieren borrar y recrear la BD.
- **PostgreSQL en producción**: Usar `DATABASE_URL=postgresql+psycopg2://...`
- **Relaciones**: Siempre definir `back_populates` en ambos lados para evitar errores de mapeo.
