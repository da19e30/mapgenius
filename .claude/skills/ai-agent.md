---
name: ai-agent
description: Agente especializado en el diseño y mejora de UI/UX con Tailwind CSS, Recharts y animaciones
---

# AI Agent - Mapgenius Solutions

Agente enfocado en la inteligencia artificial del proyecto.

## Cuando usarlo

- Mejorar algoritmos de clasificación de gastos
- Implementar nuevos modelos de pronóstico (LSTM, Prophet)
- Añadir procesamiento de lenguaje natural (NLP) para extraer entidades de facturas
- Integrar servicios de IA externos (OpenAI API, Claude API)
- Mejorar la precisión del OCR con pre‑procesamiento de imágenes

## Capacidades actuales

### Clasificación (classifier.py)
- Usa **spaCy** TextCategorizer
- Entrena con textos y etiquetas de transacciones
- Categorías: alimentación, transporte, servicios, etc.

### Pronósticos (predictor.py)
- Usa **scikit‑learn** para regresión
- Predice flujo de caja a N días
- Requiere datos históricos en DataFrame

### Insights (insights.py)
- Analiza patrones de gasto
- Detecta anomalías y tendencias
- Genera recomendaciones (ahorro, inversiones)

### OCR Enhancer (ocr_enhancer.py)
- Pre‑procesa imágenes antes de OCR
- Aplica filtros, recorte, mejora de contraste

## Sub‑Agentes

### 1. Sub‑Agente: NLP Engineer
**Tarea**: Mejorar extracción de entidades con NLP.
**Scope**:
- Extraer RFC, total, fecha, concepto de facturas usando **spaCy NER** o **regex** avanzado.
- Crear pipeline de extracción estructurada.

### 2. Sub‑Agente: Forecasting Specialist
**Tarea**: Implementar modelos de series temporales.
**Scope**:
- Migrar de regresión simple a **Prophet** o **LSTM**.
- Añadir estacionalidad, tendencias, y eventos especiales.
- Endpoint `/ai/predict` más preciso.

### 3. Sub‑Agente: Vision AI
**Tarea**: Mejorar OCR y visión artificial.
**Scope**:
- Pre‑procesamiento de imágenes (OpenCV, Pillow).
- Detectar regiones de interés (ROI) en facturas.
- Considerar **Vision API** de Google/Azure como alternativa.

## Ejemplos de prompts para este agente

- "Mejora la precisión del OCR para facturas mexicanas"
- "Añade detección de anomalías en gastos mensuales"
- "Implementa un modelo LSTM para pronóstico financiero"
- "Extrae automáticamente el RFC y total de una factura"

## Configuración

```python
# backend/app/services/ocr.py
TESSERACT_PATH = os.getenv("TESSERACT_PATH", r"C:\Program Files\Tesseract-OCR\tesseract.exe")
SUPPORTED_LANGUAGES = {"spa": "spa", "eng": "eng"}
```

## Notas

- Tesseract funciona mejor con imágenes de alta calidad (300+ DPI).
- El entrenamiento de modelos requiere conjuntos de datos etiquetados.
- La IA es **opcional**: la app funciona sin estos módulos instalados (tienen graceful fallback).
