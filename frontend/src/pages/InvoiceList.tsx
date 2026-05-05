import React from "react";
import { useEffect, useState } from "react";
import api from "../services/api";

const InvoiceCard = ({ invoice }) => (
  <div className="bg-white rounded-lg shadow-sm p-4 mb-4">
    <div className="flex justify-between mb-2">
      <span className="font-semibold text-lg">{invoice.invoiceNumber}</span>
      <span className={`text-xs ${invoice.status === 'approved' ? 'text-green-500' : invoice.status === 'rejected' ? 'text-red-500' : 'text-blue-500'}`}>
        {invoice.status}
      </span>
    </div>
    <div className="flex flex-col gap-1">
      <strong>Cliente:</strong> {invoice.clientName} (<em>{invoice.clientNit}</em>)
      <strong>Fecha emisi�n:</strong> {new Date(invoice.issueDate).toLocaleDateString()}
      <strong>Fecha vencimiento:</strong> {new Date(invoice.dueDate).toLocaleDateString()}
      <strong>Total:</strong> ${invoice.totalAmount.toFixed(2)}
    </div>
  </div>
);

const InvoiceList = () => {
  const [invoices, setInvoices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchInvoices = async () => {
      try {
        setLoading(true);
        const response = await api.get("/invoices");
        setInvoices(response.data);
        setError(null);
      } catch (err) {
        setError("Error al cargar las facturas");
        setInvoices([]);
      } finally {
        setLoading(false);
      }
    };
    fetchInvoices();
  }, []);

  if (loading) return <div className="flex items-center justify-center mt-12">Cargando...</div>;
  if (error) return <div className="text-red-500 text-center">{error}</div>;

  return (
    <>
      <h2 className="text-2xl font-semibold mb-4">Listado de Facturas</h2>
      {invoices.length === 0 ? (
        <div className="text-center mt-16 text-gray-500">
          <p>No hay facturas registradas.</p>
          <p className="text-sm text-blue-500 mt-1">Puedes crear una nueva factura desde abajo.</p>
        </div>
      ) : (
        <div>
          {invoices.map((invoice) => (
            <InvoiceCard key={invoice._id} invoice={invoice} />
          ))}
        </div>
      )}
      <div className="text-right mt-6">
        <a href="/create" className="text-indigo-600 hover:underline">
          + Crear nueva factura
        </a>
      </div>
    </>
  );
};

export default InvoiceList;
