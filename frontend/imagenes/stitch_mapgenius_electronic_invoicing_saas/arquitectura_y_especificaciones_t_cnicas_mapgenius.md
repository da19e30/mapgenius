# Arquitectura de Software: Mapgenius Solutions - Facturación Electrónica DIAN

## 1. Descripción General
Mapgenius Solutions es un SaaS de facturación electrónica diseñado para el mercado colombiano, cumpliendo con el estándar UBL 2.1 de la DIAN. El sistema integra Inteligencia Artificial para la automatización de procesos contables y análisis financiero.

## 2. Arquitectura Técnica
- **Frontend:** React.js con Tailwind CSS para una interfaz tipo Stripe/Notion.
- **Backend:** Node.js (NestJS) o Python (FastAPI) para alta concurrencia y manejo de procesos asíncronos.
- **Base de Datos:** PostgreSQL para integridad referencial (clientes, facturas, productos).
- **IA Engine:** OpenAI/Anthropic para OCR de facturas y análisis predictivo.
- **Middleware DIAN:** Servicio encargado de la generación de XML, firma digital (XAdES-EPES) y comunicación SOAP/REST con los servicios de la DIAN.

## 3. Modelo de Datos (Core)
- **Empresa:** NIT, Resolución DIAN, Clave Técnica, Certificado Digital.
- **Cliente:** Tipo de documento, NIT, Razón Social, Régimen, Responsabilidad Fiscal.
- **Producto:** SKU, Nombre, Unidad, Precio, IVA (0%, 5%, 19%), Retenciones.
- **Factura:** CUFE, QR, XML, PDF, Estado (Borrador, Enviado, Aceptado, Rechazado).

## 4. Flujo de Integración DIAN
1. **Generación:** Creación de JSON estructurado desde el frontend.
2. **Transformación:** El backend convierte JSON a XML UBL 2.1.
3. **Firma:** Aplicación de firma digital con certificado (.p12).
4. **Cálculo CUFE:** Hash SHA-384 de datos clave de la factura.
5. **Envío:** Consumo de Web Service de la DIAN.
6. **Respuesta:** Procesamiento del ApplicationResponse (Aceptación/Rechazo).

## 5. Implementación de IA
- **OCR:** Procesamiento de facturas de proveedores para convertirlas en gastos automáticamente.
- **Validación:** Red neuronal simple para detectar anomalías en precios o impuestos antes del envío.
- **Insights:** Dashboards generados mediante lenguaje natural sobre la salud financiera.
