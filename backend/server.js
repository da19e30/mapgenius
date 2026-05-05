require('dotenv').config();
const express = require('express');
const cors = require('cors');
const connectDB = require('./database');
const invoiceRoutes = require('./routes/invoiceRoutes');

const app = express();
const PORT = process.env.PORT || 5000;

// Conectar a base de datos
connectDB();

// Middleware
app.use(cors());
app.use(express.json());

// Rutas
app.use('/api/v1/invoices', invoiceRoutes);

// Ruta principal
app.get('/', (req, res) => {
  res.json({
    name: 'Mapgenius Solutions - Invoice System',
    version: '1.0.0',
    endpoints: {
      'POST /api/v1/invoices': 'Crear factura',
      'GET /api/v1/invoices': 'Listar facturas',
      'GET /api/v1/invoices/:id': 'Obtener factura',
      'POST /api/v1/invoices/:id/send': 'Enviar factura a DIAN'
    }
  });
});

app.listen(PORT, () => {
  console.log(`
╔══════════════════════════════════════════╗
║   Iniciando Mapgenius Solutions          ║
╚══════════════════════════════════════════╝
Servidor backend corriendo en: http://localhost:${PORT}
Documentación: http://localhost:${PORT}
`);
});

module.exports = app;