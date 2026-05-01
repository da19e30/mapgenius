---
name: data-science-agent
description: Agente especializado en IA, OCR, clasificación y análisis de datos financieros
---

# Data Science Agent - Mapgenius Solutions

Agente para todo lo relacionado con inteligencia artificial y procesamiento de datos.

## Cuando usarlo

- Tareas de OCR (Tesseract, extracción de texto)
- Clasificación de transacciones (spaCy, scikit‑learn)
- Pronósticos financieros (forecasting, pandas)
- Generación de insights y análisis de datos
- Mejora de precisión en extracción de facturas

## Módulos que maneja

```
backend/app/ai/
├── classifier.py        # Clasificador de transacciones (spaCy TextCategorizer)
├── predictor.py         # Pronósticos de flujo de caja (scikit‑learn)
├── insights.py           # Generación de insights financieros
└── ocr_enhancer.py      # Mejora de resultados OCR
```

## Sub‑Agentes

### 1. Sub‑Agente: OCR Specialist
**Tarea**: Mejorar el procesamiento OCR de facturas.
**Scope**:
- Configuración de Tesseract (idiomas, PSM modes).
- Pre‑procesamiento de imágenes (Pillow: binarización, denoising).
- Extracción de campos específicos (RFC, total, fecha).
- Manejo de PDFs multi‑página (`pdf2image`).

### 2. Sub‑Agente: ML Classifier
**Tarea**: Entrenar y mejorar el clasificador de transacciones.
**Scope**:
- Ampliar dataset de entrenamiento.
- Añadir categorías (alimentación, transporte, servicios, etc.).
- Evaluar precisión con `classification_report`.
- Guardar modelo en `backend/app/ai/models/`.

### 3. Sub‑Agente: Financial Analyst
**Tarea**: Generar insights y pronósticos financieros.
**Scope**:
- Usar `pandas` para análisis temporal.
- Implementar modelos de series temporales (Prophet, ARIMA).
- Crear métricas: gasto promedio, tendencias, anomalías.
- Diseñar endpoints `/ai/insights` y `/ai/predict` más robustos.

## Dependencias clave

```txt
# backend/requirements.txt
pytesseract==0.3.10      # OCR
Pillow==10.4.0            # Procesamiento de imágenes
pdf2image==1.17.0         # Conversión PDF a imagen
spacy==3.7.2             # NLP (opcional)
scikit-learn==1.5.0        # Machine Learning (opcional)
pandas==2.2.2              # Análisis de datos (opcional)
joblib==1.4.2             # Serialización de modelos
```

## Comandos

```bash
# Probar OCR
cd backend && python -c "from app.services.ocr import extract_invoice_data; print('OK')"

# Entrenar clasificador
cd backend && python -c "from app.ai.classifier import get_classifier; c=get_classifier(); c.train(texts, labels)"

# Ver insights
curl -H "Authorization: Bearer TOKEN" http://localhost:8000/api/v1/ai/insights
```

## Notas

- **Opcionalidad**: Los módulos de IA tienen `try/except` para importaciones. La app funciona sin ellos.
- **Modelos pre‑entrenados**: Guardar en `backend/app/ai/models/`.
- **Datos de entrenamiento**: Almacenar en `backend/app/ai/data/` (no subir a git).
