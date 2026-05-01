# 🎨 Mapgenius Design System (Figma-inspired)

## 🎨 Paleta de Colores
```css
:root {
  /* Primarios - Gradiente principal */
  --primary-50: #eef2ff;
  --primary-100: #dbeafe;
  --primary-200: #bfdbfe;
  --primary-300: #93c5fd;
  --primary-400: #60a5fa;
  --primary-500: #3b82f6;
  --primary-600: #2563eb;
  --primary-700: #1d4ed;
  --primary-800: #1e40af;
  --primary-900: #1e3a8a;

  /* Acentos - Púrpura vibrante */
  --accent-50: #faf5ff;
  --accent-100: #f3e8ff;
  --accent-200: #e9d5ff;
  --accent-300: #d8b4ff;
  --accent-400: #c084fc;
  --accent-500: #a855f7;
  --accent-600: #9333ea;
  --accent-700: #7e22ce;
  --accent-800: #6b21a8;
  --accent-900: #581c87;

  /* Éxito - Verde esmeralda */
  --success-50: #ecfdf5;
  --success-500: #10b981;
  --success-600: #059669;

  /* Error - Rojo */
  --danger-50: #fef2f2;
  --danger-500: #ef4444;
  --danger-600: #dc2626;

  /* Grises - Carbon neutral */
  --gray-50: #fafafa;
  --gray-100: #f4f4f5;
  --gray-200: #e4e4e7;
  --gray-300: #d4d4d8;
  --gray-400: #a1a1a1;
  --gray-500: #71717a;
  --gray-600: #52525b;
  --gray-700: #3f3f46;
  --gray-800: #27272a;
  --gray-900: #18181b;

  /* Fondos especiales */
  --glass: rgba(255, 255, 255, 0.1);
  --glass-border: rgba(255, 255, 255, 0.2);
}
```

## 🔤 Tipografía
```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
```

Jerarquía:
- **H1**: 3xl, font-extrabold, tracking-tight, gradient-text
- **H2**: 2xl, font-bold
- **H3**: xl, font-semibold
- **Body**: base, font-normal
- **Small**: sm, font-medium

## 📐 Espaciado & Sombras
- **Cards**: rounded-2xl, shadow-2xl, p-8, space-y-6
- **Inputs**: rounded-xl, px-4 py-3, border-gray-200, focus:ring-2
- **Buttons**: rounded-xl, px-6 py-3, font-semibold, transition-all, shadow-lg hover:shadow-xl

## ✨ Efectos Especiales
1. **Glassmorphism**: backdrop-blur-xl, bg-white/10, border-white/20
2. **Gradientes**: bg-gradient-to-r from-indigo-600 to-purple-600
3. **Floating labels**: animate-float (translateY -10px)
4. **Gradient text**: bg-clip-text, text-transparent

## 🎯 Componentes Clave
### Login/Register
- Fondo: Gradiente oscuro (slate-900 → purple-900 → slate-800)
- Tarjeta: Glassmorphism centrada, max-w-md
- Logo: "Mapgenius" en blanco, "Solutions" en indigo-400
- Inputs: Con iconos SVG, fondo sutil, bordes redondeados
- Botón: Gradiente indigo-purple, sombra pronunciada

### Dashboard
- Cards de métricas: Glassmorphism, íconos grandes, números grandes
- Gráficos: Fondos de tarjeta, bordes suaves
- Sidebar: bg-white, shadow-md, w-64

### Upload Invoice
- Zona drag & drop: Dashed border, gradient-bg sutil, icono grande
- Progreso: Barra de progreso animada
- Resultado: Tarjeta de éxito con checkmark

## 📱 Responsive
- Mobile: 1 columna, p-4
- Tablet: 2 columnas, p-6
- Desktop: 3 columnas, p-8

## 🎨 Ilustración de la Tarjeta Principal
```
┌─────────────────────────────────────────┐
│  🎨 Mapgenius Solutions              │
│  ────────────────────────────────────┤
│  ┌─────────────────────────────┐    │
│  │  🔐 Iniciar sesión         │    │
│  │                          │    │
│  │  [📧 Correo electrónico]  │    │
│  │  [🔒 Contraseña]        │    │
│  │                          │    │
│  │  [ Entrar ] (gradiente)    │    │
│  │                          │    │
│  │  ¿No tienes cuenta? Registrate │    │
│  └─────────────────────────────┘    │
└─────────────────────────────────────────┘
```
