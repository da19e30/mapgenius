# Arquitectura del Backend: Mapgenius Solutions - Facturación Electrónica DIAN

## 1. Stack Tecnológico Sugerido
Para garantizar alta concurrencia, seguridad y facilidad de integración con servicios SOAP (DIAN), la arquitectura se basa en:
- **Runtime:** Node.js con NestJS (TypeScript). NestJS proporciona una estructura modular ideal para sistemas empresariales.
- **Base de Datos:** PostgreSQL para datos estructurados (Clientes, Facturas, Productos) debido a su robustez en integridad referencial.
- **Cache & Colas:** Redis para el manejo de trabajos asíncronos (envío de facturas, generación de PDFs).
- **IA Engine:** Integración con LangChain y OpenAI/Anthropic para procesamiento de lenguaje natural y OCR.

## 2. Capas del Sistema (Modular Monolith)

### A. Módulo de Facturación Electrónica (Core)
Es el corazón del sistema, encargado del ciclo de vida del UBL 2.1.
- **Generador UBL:** Transforma objetos JSON de la base de datos en XML estructurado bajo el estándar OASIS UBL 2.1.
- **Servicio de Firma (XAdES-EPES):** Firma digitalmente el XML usando certificados .p12. Utiliza bibliotecas de criptografía para asegurar que la firma cumpla con la normativa DIAN.
- **Calculador de CUFE:** Algoritmo SHA-384 que concatena datos clave (NumFac, NitEmisor, NitAdquirente, etc.) para generar el hash único.

### B. Módulo de Integración DIAN (Middleware)
- **Cliente SOAP/REST:** Gestiona la comunicación con los Web Services de la DIAN. Maneja reintentos automáticos y logs detallados de cada petición/respuesta.
- **Validador de Respuestas:** Procesa el `ApplicationResponse` de la DIAN para extraer códigos de error o el estado de aceptación.

### C. Módulo de Inteligencia Artificial
- **Extractor OCR:** Servicio que recibe documentos (PDF/JPG) y utiliza IA para identificar proveedores, montos e impuestos, convirtiéndolos en registros contables.
- **Analista Predictivo:** Analiza el histórico de facturación para proyectar el flujo de caja y sugerir optimizaciones fiscales.

## 3. Modelo de Datos (Esquema Principal)
- **Tenants/Empresas:** Configuración fiscal, resolución de facturación y certificados.
- **Documentos:** Estado del envío, CUFE, XML (almacenado en S3), y referencia al cliente.
- **Auditoría:** Logs completos de cada interacción con la DIAN para cumplimiento legal.

## 4. Flujo de Trabajo Asíncrono
1. **Petición:** El frontend envía los datos de la factura.
2. **Cola:** La factura entra en una cola de procesamiento en Redis.
3. **Procesamiento:** El worker genera el XML, lo firma y lo envía a la DIAN.
4. **Notificación:** Una vez recibida la respuesta, se actualiza el estado mediante WebSockets en el frontend y se envía el correo al adquirente.

## 5. Seguridad
- **JWT con Rotación de Tokens:** Para sesiones de usuario seguras.
- **Cifrado de Certificados:** Los certificados digitales se almacenan cifrados en reposo (AES-256) en un Key Vault.
- **Aislamiento de Datos (Multi-tenant):** Garantiza que cada empresa solo acceda a su propia información contable.