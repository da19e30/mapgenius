---
name: frontend-agent
description: Agente especializado en el frontend de Mapgenius (React, TypeScript, Vite, Tailwind)
---

# Frontend Agent - Mapgenius Solutions

Agente principal para todo el desarrollo frontend.

## Cuando usarlo

- Usuario menciona "frontend", "React", "página", "componente"
- Necesitas crear nuevas rutas, modificar páginas existentes
- Tareas de diseño, responsividad, o interacción
- Integración con APIs (axios), manejo de estado (AuthContext)

## Estructura que maneja

```
frontend/src/
├── pages/              # Páginas (Landing, Login, Register, Dashboard, UploadInvoice, Transactions)
│   ├── Landing.tsx          # Página de inicio (pública)
│   ├── Login.tsx           # Inicio de sesión
│   ├── Register.tsx        # Registro (con animaciones, password strength)
│   ├── Dashboard.tsx       # Panel principal (stats, charts, activity)
│   ├── UploadInvoice.tsx   # Subida de facturas
│   └── Transactions.tsx     # Lista de transacciones (filtros, tabla)
├── components/         # Componentes reutilizables
│   └── Layout.tsx          # Barra lateral, top bar, dropdown de usuario
├── services/           # Lógica de comunicación
│   └── api.ts               # Cliente axios con interceptores JWT
├── context/            # Estado global
│   └── AuthContext.tsx      # Autenticación, token, email
├── App.tsx             # Enrutador principal
├── main.tsx            # Punto de entrada (React + ReactDOM)
├── vite-env.d.ts       # Tipos para import.meta.env
├── postcss.config.js    # PostCSS + Tailwind + Autoprefixer
└── package.json        # Dependencias (React 18, Recharts, Axios, etc.)
```

## Sub‑Agentes

### 1. Sub‑Agente: Page Builder
**Tarea**: Crear y modificar páginas completas.
**Scope**:
- Estructura base (useState, useEffect, handlers).
- Integración con `api` service.
- Manejo de estados de carga, error, y éxito.
- Forms con validación y feedback visual.

### 2. Sub‑Agente: Component Crafter
**Tarea**: Crear componentes reutilizables.
**Scope**:
- Seguir patrones de diseño (props, children, eventos).
- Usar TypeScript para tipado fuerte.
- Documentar uso y ejemplos.

### 3. Sub‑Agente: Integration Specialist
**Tarea**: Conectar frontend con backend.
**Scope**:
- Configurar `VITE_API_URL` en `.env` (o usar `/api/v1` por defecto).
- Manejar respuestas y errores de API.
- Tipado de respuestas (interfaces TypeScript).

## Comandos clave

```bash
cd frontend && npm run dev        # Iniciar Vite dev server (http://localhost:5173)
cd frontend && npm run build     # Compilación de producción
cd frontend && npx tsc --noEmit # Verificación TypeScript
```

## Rutas actuales

| Ruta | Página | Protegida |
|------|--------|-----------|
| `/` | Landing | No |
| `/login` | Login | No |
| `/register` | Register | No |
| `/dashboard` | Dashboard | Sí |
| `/upload-invoice` | UploadInvoice | Sí |
| `/transactions` | Transactions | Sí |

## Notas importantes

- **AuthContext**: Provee `useAuth()` hook con `token`, `email`, `login()`, `logout()`, `isAuthenticated`.
- **API**: Base URL configurada via `VITE_API_URL`. Si no está, usa `/api/v1`.
- **JWT**: Se adjunta automáticamente en cada request mediante interceptor en `api.ts`.
- **Tailwind**: Usar clases utilitarias. No escribir CSS externo salvo animaciones complejas.
- **TypeScript**: Respetar tipos. Usar `interface` para props y respuestas de API.
