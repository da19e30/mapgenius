const express = require('express');
const router = express.Router();
const invoiceController = require('../controllers/invoiceController');

// Crear factura
router.post('/', invoiceController.createInvoice);

// Listar facturas
router.get('/', invoiceController.getInvoices);

// Obtener factura por ID
router.get('/:id', invoiceController.getInvoiceById);

// Enviar factura a DIAN (simulado)
router.post('/:id/send', invoiceController.sendToDian);

module.exports = router;