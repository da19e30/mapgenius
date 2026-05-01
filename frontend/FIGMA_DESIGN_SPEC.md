# 🎨 Mapgenius Solutions - Figma Design Specification
## Estilo: Revista Premium / SaaS Moderno (Tipo Stripe + Linear + Notion)

---

## 🎨 Paleta de Colores (Figma Styles)
```
Primary Gradient: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #8b5cf6 100%)
Accent Gradient: linear-gradient(135deg, #a855f7 0%, #ec4899 100%)
Success: #10b981
Warning: #f59e0b
Danger: #ef4444
Glass: rgba(255,255,255,0.08)
Glass Border: rgba(255,255,255,0.12)
Text Primary: #f8fafc (slate-50)
Text Secondary: #94a3b8 (slate-400)
```

---

## 📐 Wireframe: Login Page (`/login`)
```
┌─────────────────────────────────────────────────────────────┐
│  URL: http://localhost:3000/login                     │
├─────────────────────────────────────────────────────────────┤
│  ═ Fondo: Gradiente oscuro slate-900 → purple-900 → slate-800     │
│  ═ Overlay pattern sutil (puntos o grid)                       │
│  ═ Alineación: centro vertical y horizontal                 │
│                                                          │
│         ┌──────────────────────────────────────┐      │
│         │  📊 LOGO ZONA:                        │      │
│         │  Mapgenius Solutions (blanco + indigo-400)  │      │
│         │  "Inicia sesión en tu cuenta" (slate-300) │      │
│         │                                      │      │
│         │  ┌────────────────────────────────┐   │      │
│         │  │ 📧 Correo electrónico          │   │      │
│         │  │ [tu@email.com              ]   │   │      │
│         │  └────────────────────────────────┘   │      │
│         │  ┌────────────────────────────────┐   │      │
│         │  │ 🔒 Contraseña                 │   │      │
│         │  │ [•••••••••••••           ]   │   │      │
│         │  └────────────────────────────────┘   │      │
│         │                                      │      │
│         │  ┌────────────────────────────────┐   │      │
│         │  │ [ Entrar ] (Gradiente indigo→purple)│   │      │
│         │  └────────────────────────────────┘   │      │
│         │  "¿No tienes cuenta? Regístrate" (link)     │      │
│         └──────────────────────────────────────┘      │
│                                                          │
│  © 2026 Mapgenius Solutions (slate-400, small)       │
└─────────────────────────────────────────────────────────────┘
```

---

## 📐 Wireframe: Register Page (`/register`)
```
┌─────────────────────────────────────────────────────────────┐
│  URL: http://localhost:3000/register                    │
├─────────────────────────────────────────────────────────────┤
│  (Mismo fondo que Login)                             │
│         ┌──────────────────────────────────────┐      │
│         │  📊 Crear cuenta                       │      │
│         │  "Completa tus datos para comenzar"      │      │
│         │                                      │      │
│         │  Nombre de usuario [vasara1995   ]     │      │
│         │  Correo electrónico [patarroyo@...]     │      │
│         │  Contraseña        [•••••••••••• ]     │      │
│         │  Confirmar        [•••••••••••• ]     │      │
│         │                                      │      │
│         │  [ Crear cuenta ] (Gradiente indigo→purple) │      │
│         │  "¿Ya tienes cuenta? Inicia sesión"       │      │
│         └──────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

---

## 📐 Wireframe: Dashboard (`/dashboard`)
```
┌─────────────────────────────────────────────────────────────┐
│  URL: http://localhost:3000/dashboard                  │
├─────────────────────────────────────────────────────────────┤
│  🔲 Sidebar (w-64, bg-white, shadow-md)               │
│  ┌──────────┐                                    │
│  │ Dashboard │                                    │
│  │ 📤 Subir Factura │                                │
│  │ ⚙️ Cerrar sesión │                                │
│  └──────────┘                                    │
│                                                          │
│  📰 Main Content (bg-gray-100, p-6)                      │
│  ┌───────────────────────────────────────────────┐    │
│  │ H1: Dashboard - Mapgenius Solutions (text-2xl) │    │
│  └───────────────────────────────────────────────┘    │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐│
│  │ 📊 Estado   │ │ 📈 Métricas │ │ 💰 Facturas ││
│  │ {status:ok} │ │ [Gráfico]  │ │ [Lista]    ││
│  │ message...  │ │            │ │            ││
│  └──────────────┘ └──────────────┘ └──────────────┘│
│  ┌───────────────────────────────────────────────┐    │
│  │ 🚀 Subir Factura (Gradiente indigo→purple)   │    │
│  │ "Procesa tus facturas con OCR e IA"       │    │
│  └───────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## 📐 Wireframe: Upload Invoice (`/upload-invoice`)
```
┌─────────────────────────────────────────────────────────────┐
│  URL: http://localhost:3000/upload-invoice              │
├─────────────────────────────────────────────────────────────┤
│  (Mismo layout Dashboard + Sidebar)                    │
│  ┌───────────────────────────────────────────────┐    │
│  │ H1: Subir Factura (text-2xl)             │    │
│  └───────────────────────────────────────────────┘    │
│  ┌───────────────────────────────────────────────┐    │
│  │ 📤 Zona Drag & Drop (dashed-2, rounded-2xl)│    │
│  │                                     │    │
│  │        ┌──────────────┐             │    │
│  │        │ 📄 Subir factura│             │    │
│  │        │ PDF, JPG, PNG  │             │    │
│  │        │ [Seleccionar archivo]│             │    │
│  │        └──────────────┘             │    │
│  │                                     │    │
│  └───────────────────────────────────────────────┘    │
│  ┌───────────────────────────────────────────────┐    │
│  │ [Subir Factura] (Gradiente indigo→purple)    │    │
│  └───────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎨 Especificación de Componentes (Figma Components)

### Glass Card (Reusable)
```
- Background: rgba(255,255,255,0.08) o bg-white/95
- Backdrop Filter: blur(16px)
- Border: 1px solid rgba(255,255,255,0.12)
- Border Radius: 24px (rounded-2xl)
- Shadow: 0 25px 50px -12px rgba(0,0,0,0.25) (shadow-2xl)
- Padding: 32px (p-8)
- Margin bottom: 24px (mb-6)
```

### Gradient Button (Reusable)
```
- Background: linear-gradient(135deg, #3b82f6 0%, #a855f7 100%)
- Hover: linear-gradient(135deg, #2563eb 0%, #9333ea 100%)
- Text: white, font-semibold, text-sm
- Padding: py-3, px-6
- Border Radius: 12px (rounded-xl)
- Shadow: 0 10px 15px -3px rgba(59,130,246,0.4)
- Transition: all 300ms ease
- Disabled: opacity-60, cursor-not-allowed
```

### Input Field (Reusable)
```
- Background: bg-gray-50 o glass
- Border: 1px solid #e2e8f0 (gray-200)
- Focus: border-indigo-500, ring-2 ring-indigo-500/20
- Padding: py-2.5, pl-10 (icon space), pr-4
- Border Radius: 12px (rounded-xl)
- Font: text-sm
- Placeholder: text-gray-400
- Icon: absolute left-3, text-gray-400, w-5 h-5
```

### Sidebar Item (Reusable)
```
- Padding: py-2, px-4, rounded-lg
- Hover: bg-gray-200
- Active: bg-gray-200, font-medium
- Text: text-gray-700
- Active Text: text-gray-900, font-medium
```

---

## 🎨 Tipografía (Figma Text Styles)
```
H1 Display: font-extrabold, text-3xl, tracking-tight, text-white (login) o text-gray-900 (dashboard)
H2 Title: font-bold, text-2xl, text-gray-900
H3 Section: font-semibold, text-lg, text-gray-900
Body: font-normal, text-base, text-gray-600
Small: font-medium, text-sm, text-gray-500
Tiny: font-normal, text-xs, text-gray-400
```

---

## ✅ Checklist de Implementación (Para Agente Frontend)
- [x] Tailwind configurado con colores personalizados
- [x] postcss.config.js creado
- [x] index.css con animaciones personalizadas
- [ ] Login.tsx: Fondo gradiente, glass card, iconos SVG, botón gradiente
- [ ] Register.tsx: Mismo diseño que Login
- [ ] Dashboard.tsx: Cards glass, métricas, grid responsive
- [ ] UploadInvoice.tsx: Zona drag & drop styled, glass card
- [ ] Layout.tsx: Sidebar moderno, glass card main
- [ ] App.tsx: Lazy loading con Suspense
- [ ] api.ts: Interceptor JWT, base URL config
- [ ] AuthContext.tsx: Persistencia JWT
