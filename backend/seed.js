require('dotenv').config();
const mongoose = require('mongoose');
const Invoice = require('./models/invoice');

const sampleInvoices = [
  {
    invoiceNumber: 'INV-001',
    clientName: 'Cliente Ejemplo S.A.',
    clientNit: '900123456-7',
    issueDate: new Date('2025-01-15'),
    dueDate: new Date('2025-02-14'),
    totalAmount: 1500000,
    status: 'approved'
  },
  {
    invoiceNumber: 'INV-002',
    clientName: 'Tecnología Avanzada Ltda.',
    clientNit: '800987654-3',
    issueDate: new Date('2025-02-20'),
    dueDate: new Date('2025-03-20'),
    totalAmount: 2750000,
    status: 'approved'
  },
  {
    invoiceNumber: 'INV-003',
    clientName: 'Servicios Integrales S.A.S.',
    clientNit: '901234567-8',
    issueDate: new Date('2025-03-10'),
    dueDate: new Date('2025-04-09'),
    totalAmount: 890000,
    status: 'rejected'
  }
];

const seedDB = async () => {
  try {
    await mongoose.connect(process.env.DATABASE_URL);
    console.log('Conectado a MongoDB');

    // Limpiar colección existente
    await Invoice.deleteMany({});
    console.log('Colección limpiada');

    // Insertar datos de ejemplo
    await Invoice.insertMany(sampleInvoices);
    console.log('Datos de ejemplo insertados');

    process.exit(0);
  } catch (error) {
    console.error('Error al poblar la base de datos:', error);
    process.exit(1);
  }
};

seedDB();
