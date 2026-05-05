const mongoose = require('mongoose');
require('dotenv').config();

const invoiceSchema = new mongoose.Schema({
  invoiceNumber: {
    type: String,
    required: true,
    unique: true
  },
  clientName: {
    type: String,
    required: true
  },
  clientNit: {
    type: String,
    required: true
  },
  issueDate: {
    type: Date,
    required: true
  },
  dueDate: {
    type: Date,
    required: true
  },
  totalAmount: {
    type: Number,
    required: true
  },
  status: {
    type: String,
    enum: ['draft', 'processing', 'approved', 'rejected'],
    default: 'draft'
  },
  xmlContent: {
    type: String
  }
};

module.exports = mongoose.model('Invoice', invoiceSchema);