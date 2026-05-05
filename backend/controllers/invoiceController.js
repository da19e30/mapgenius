const Invoice = require('../models/invoice');

// Función para generar XML de factura (simulado)
const generateInvoiceXML = (invoice) => {
  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<Invoice xmlns="http://www.dian.gov.co/schema/Invoice">
  <InvoiceNumber>${invoice.invoiceNumber}</InvoiceNumber>
  <IssueDate>${invoice.issueDate.toISOString().split('T')[0]}</IssueDate>
  <TotalAmount>${invoice.totalAmount}</TotalAmount>
  <ClientName>${invoice.clientName}</ClientName>
  <ClientNIT>${invoice.clientNit}</ClientNIT>
</Invoice>`;
  return xml;
};

// Función para simular envío a DIAN
const simulateDianResponse = async (invoice) => {
  // Simular un retraso de red
  await new Promise(resolve => setTimeout(resolve, 2000));

  // Simular 70% de aprobación, 30% de rechazo
  const isApproved = Math.random() > 0.3;

  return {
    success: true,
    response: {
      status: isApproved ? 'approved' : 'rejected',
      message: isApproved ?
        'Factura aprobada por la DIAN' :
        'Factura rechazada: información inconsistente',
      processedAt: new Date()
    }
  };
};

// Crear nueva factura
exports.createInvoice = async (req, res) => {
  try {
    const { invoiceNumber, clientName, clientNit, issueDate, dueDate, totalAmount } = req.body;

    // Validar datos
    if (!invoiceNumber || !clientName || !clientNit || !issueDate || !dueDate || !totalAmount) {
      return res.status(400).json({ success: false, message: 'Todos los campos son requeridos' });
    }

    // Verificar si el número de factura ya existe
    const existingInvoice = await Invoice.findOne({ invoiceNumber });
    if (existingInvoice) {
      return res.status(400).json({ success: false, message: 'El número de factura ya existe' });
    }

    const invoice = new Invoice({
      invoiceNumber,
      clientName,
      clientNit,
      issueDate: new Date(issueDate),
      dueDate: new Date(dueDate),
      totalAmount
    });

    // Generar XML
    invoice.xmlContent = generateInvoiceXML(invoice);

    await invoice.save();

    res.status(201).json({
      success: true,
      data: invoice
    });

  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
};

// Listar todas las facturas
exports.getInvoices = async (req, res) => {
  try {
    const invoices = await Invoice.find().sort({ issueDate: -1 });
    res.json({
      success: true,
      data: invoices
    });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
};

// Obtener factura por ID
exports.getInvoiceById = async (req, res) => {
  try {
    const invoice = await Invoice.findById(req.params.id);

    if (!invoice) {
      return res.status(404).json({ success: false, message: 'Factura no encontrada' });
    }

    res.json({
      success: true,
      data: invoice
    });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
};

// Enviar factura a DIAN
exports.sendToDian = async (req, res) => {
  try {
    const invoice = await Invoice.findById(req.params.id);

    if (!invoice) {
      return res.status(404).json({ success: false, message: 'Factura no encontrada' });
    }

    if (invoice.status !== 'draft') {
      return res.status(400).json({ success: false, message: 'Solo se pueden enviar facturas en estado "draft"' });
    }

    // Actualizar estado a processing
    invoice.status = 'processing';
    await invoice.save();

    // Simular envío a DIAN
    const dianResponse = await simulateDianResponse(invoice);

    // Actualizar estado según respuesta
    invoice.status = dianResponse.response.status;
    invoice.processedAt = dianResponse.response.processedAt;
    await invoice.save();

    res.json({
      success: true,
      data: {
        invoice,
        dianResponse: dianResponse.response
      }
    });

  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
};