---
name: security-agent
description: Agente especializado en seguridad, autenticación, JWT y buenas prácticas
---

# Security Agent - Mapgenius Solutions

Agente enfocado en la seguridad de la aplicación.

## Cuando usarlo

- Revisar vulnerabilidades (OWASP Top 10)
- Mejorar autenticación y autorización
- Configurar CORS, HTTPS, headers de seguridad
- Validar entradas (sanitización, prevención de SQL Injection, XSS)
- Auditar dependencias (npm audit, pip‑audit)

## Áreas de enfoque

### 1. Autenticación y Autorización
```
backend/app/services/
├── auth.py         # Hash y verificación de contraseñas (bcrypt)
└── jwt.py          # Generación y validación de JWT (python‑jose)

backend/app/routes/
└── user.py         # Endpoints de registro y login

frontend/src/context/
└── AuthContext.tsx  # Manejo de token en frontend (localStorage)
```

### 2. Seguridad de Datos
- **Contraseñas**: Siempre hasheadas con **bcrypt** (nunca texto plano).
- **JWT**: Firmado con HS256, expiración de 30 min.
- **Variables sensibles**: En `.env` (nunca subir a git). Usar `python‑dotenv`.

### 3. Seguridad en API
- **CORS**: Actualmente permite todo (`*`). Restringir en producción.
- **Validación de entradas**: `pydantic` models, `File` validation.
- **Rate limiting**: Implementar en endpoints críticos (login, registro).

### 4. Seguridad en Frontend
- **XSS**: React ya protege por defecto, pero evitar `dangerouslySetInnerHTML`.
- **Token storage**: `localStorage` es accesible por JS. Considerar **HttpOnly cookies** para producción.
- **Validación de formularios**: Usar HTML5 `required`, patrones de contraseña.

## Sub‑Agentes

### 1. Sub‑Agente: Auth Guardian
**Tarea**: Asegurar que la autenticación sea robusta.
**Scope**:
- Verificar que los tokens JWT se validen correctamente.
- Implementar **refresh tokens** si es necesario.
- Añadir **2FA** (TOTP) para mayor seguridad.

### 2. Sub‑Agente: Input Validator
**Tarea**: Validar y sanear todas las entradas.
**Scope**:
- Backend: Pydantic models, validación de tipos.
- Frontend: Validación de formularios, sanitización de datos.
- Prevención de **SQL Injection** (SQLAlchemy ya usa consultas parametrizadas).

### 3. Sub‑Agente: Infrastructure Sentinel
**Tarea**: Configurar seguridad en infraestructura y despliegue.
**Scope**:
- **HTTPS** en producción (SSL/TLS certificates).
- Headers de seguridad (**Helmet** para FastAPI, meta tags para React).
- **Docker**: No ejecutar como root, actualizar imágenes base.

## Herramientas recomendadas

```bash
# Auditoría de dependencias
cd backend && pip-audit
cd frontend && npm audit

# Análisis estático de seguridad
cd backend && bandit -r app/

# Verificar configuración CORS
curl -I -X OPTIONS http://localhost:8000/api/v1/users/login

# Probar fuerza bruta en login
# (No hacer en producción sin rate limiting)
```

## Ejemplos de prompts

- "Implementa rate limiting en el endpoint de login"
- "Añade headers de seguridad con Helmet en FastAPI"
- "Cambia el almacenamiento de JWT a HttpOnly cookies"
- "Realiza una auditoría de seguridad completa"

## Notas importantes

- **Clave secreta**: `SECRET_KEY` en `.env`. Cambiar para producción.
- **CORS**: En producción, especificar orígenes exactos: `CORS_ORIGINS=https://tudominio.com`
- **Contraseñas**: Mínimo 8 caracteres, requerir complejidad (mayúsculas, números, símbolos).
- **Archivo `.env`**: Ya tiene configuración SMTP. Nunca subirlo a repositorios públicos.
