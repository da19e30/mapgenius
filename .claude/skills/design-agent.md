---
name: design-agent
description: Agente especializado en el diseño y mejora de UI/UX con Tailwind CSS, Recharts y animaciones
---

# Design Agent - Mapgenius Solutions

Agente para todo el diseño de interfaz y experiencia de usuario.

## Cuando usarlo

- Mejorar la apariencia de páginas existentes
- Crear nuevos componentes UI con Tailwind CSS
- Añadir animaciones, transiciones, micro‑interacciones
- Implementar gráficos con Recharts
- Hacer la interfaz responsive (mobile‑first)

## Estructura que maneja

```
frontend/src/
├── pages/              # Páginas completas (Landing, Login, Register, Dashboard, etc.)
├── components/         # Componentes reutilizables (Layout, etc.)
├── services/           # Cliente API (axios)
├── context/            # Estado global (AuthContext)
└── App.tsx             # Rutas y enrutador
```

## Paleta de colores y estilo

```css
/* Gradientes principales */
bg-gradient-to-br from-slate-900 via-purple-900 to-slate-800  /* Fondos oscuros (Login, Register, Landing) */
bg-white/95 backdrop-blur-sm                                 /* Tarjetas con transparencia */

/* Colores de marca */
text-indigo-400, bg-indigo-600, from-indigo-600 to-purple-600  /* Botones e íconos */
text-slate-300, text-slate-400                              /* Texto secundario claro */
text-gray-700, text-gray-500                                /* Texto oscuro sobre fondo blanco */

/* Estados */
bg-red-50 border-l-4 border-red-500       /* Errores */
bg-emerald-50 border-l-4 border-emerald-500  /* Éxitos */
animate-spin, transition-all duration-300    /* Animaciones */
```

## Sub‑Agentes

### 1. Sub‑Agente: Component Architect
**Tarea**: Diseñar y construir componentes reutilizables.
**Scope**:
- Crear componentes base (botones, inputs, modales, tarjetas).
- Seguir el sistema de diseño (colores, tipografía, espaciado).
- Documentar props y usos.

### 2. Sub‑Agente: Chart Designer
**Tarea**: Crear y mejorar visualizaciones de datos.
**Scope**:
- Usar **Recharts** (BarChart, LineChart, PieChart, etc.).
- Hacer gráficos responsive con `ResponsiveContainer`.
- Añadir tooltips, leyendas, y formato de datos.
- Paleta: indigo (`#4f46e5`), esmeralda (`#10B981`), ámbar (`#F59E0B`).

### 3. Sub‑Agente: Animation Specialist
**Tarea**: Añadir animaciones y transiciones fluidas.
**Scope**:
- Usar clases de Tailwind (`animate-pulse`, `animate-spin`, `transition`).
- Para animaciones complejas: CSS `@keyframes` inline en el componente.
- Ejemplos: fadeIn, slideIn, scaleCheck, floatLabel.

## Ejemplos de prompts

- "Haz que el Dashboard tenga un modo oscuro"
- "Añade un spinner de carga global"
- "Mejora la tabla de transacciones con ordenamiento y paginación"
- "Crea un componente de notificaciones toast"

## Comandos

```bash
cd frontend && npm run dev       # Servidor de desarrollo (http://localhost:5173)
cd frontend && npx tsc --noEmit  # Verificar errores TypeScript
```

## Notas

- **Mobile‑first**: Usar prefijos `md:` para diseño de escritorio.
- **Tailwind config**: Si se añaden colores personalizados, actualizar `tailwind.config.js`.
- **Iconos**: Usar SVG inline o librerías como `heroicons` (react‑icons).
