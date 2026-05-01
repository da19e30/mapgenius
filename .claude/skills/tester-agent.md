---
name: tester-agent
description: Agente especializado en pruebas, calidad y automatización de testing
---

# Tester Agent - Mapgenius Solutions

Agente dedicado a asegurar la calidad del código y funcionamiento correcto.

## Cuando usarlo

- Usuario pide "pruebas", "tests", "verificar", "validar"
- Necesitas cubrir código con tests unitarios o de integración
- Revisar que los flujos completos funcionen (registro → login → subir factura)
- Automatizar pruebas E2E (Playwright, Cypress)

## Tipos de pruebas

### 1. Backend Tests (pytest)
```
backend/tests/
├── test_routes/
│   ├── test_user.py          # Registro, login, get_me
│   ├── test_invoices.py      # Upload, list, get, delete
│   └── test_ai.py             # Insights, predict, classify
├── test_services/
│   ├── test_auth.py         # Hash, verify, JWT
│   ├── test_ocr.py          # Extracción de texto
│   └── test_email.py        # Envío de correos
└── conftest.py                 # Fixtures (client, db, token)
```

### 2. Frontend Tests (Vitest + Testing Library)
```
frontend/src/
├── __tests__/
│   ├── Login.test.tsx
│   ├── Register.test.tsx
│   └── Dashboard.test.tsx
└── components/
    └── __tests__/
        └── Layout.test.tsx
```

### 3. E2E Tests (Playwright)
```
e2e/
├── tests/
│   ├── auth.spec.ts           # Flujo registro + login
│   ├── invoice.spec.ts        # Subir factura y verificar
│   └── dashboard.spec.ts     # Verificar gráficos y datos
└── playwright.config.ts
```

## Sub‑Agentes

### 1. Sub‑Agente: Unit Tester
**Tarea**: Crear pruebas unitarias para funciones y componentes aislados.
**Scope**:
- Backend: `pytest` para servicios y modelos.
- Frontend: `vitest` + `@testing-library/react`.
- Mocking de dependencias externas (axios, DB).

### 2. Sub‑Agente: Integration Tester
**Tarea**: Verificar que los módulos funcionan juntos.
**Scope**:
- Probar flujos completos (API calls reales).
- Usar `test_flow.py` como base.
- Configurar base de datos de prueba (`test.db`).

### 3. Sub‑Agente: E2E Automation
**Tarea**: Automatizar pruebas de interfaz de usuario.
**Scope**:
- Instalar y configurar **Playwright** o **Cypress**.
- Grabar flujos críticos (login, registro, subida de factura).
- Ejecutar en CI/CD (GitHub Actions).

## Comandos

```bash
# Backend unit tests
cd backend && python -m pytest tests/ -v

# Frontend unit tests
cd frontend && npm test

# E2E tests
cd e2e && npx playwright test

# Cobertura de código
cd backend && python -m pytest --cov=app tests/
```

## Ejemplos de prompts

- "Crea pruebas unitarias para el clasificador de IA"
- "Verifica que el registro envíe correos correctamente"
- "Implementa un test E2E que suba una factura y verifique que aparezca en el Dashboard"

## Notas

- **Todavía no hay pruebas escritas**: El proyecto necesita crear la estructura de `tests/`.
- **test_flow.py**: Es un script de verificación manual, no un test automatizado.
- **Cobertura**: Idealmente >80% en backend y frontend crítico.
