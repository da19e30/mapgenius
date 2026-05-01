import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth } from '@/context/AuthContext';

interface Client {
  id: number;
  nit: string;
  name: string;
  email: string;
}

interface Product {
  id: number;
  code: string;
  name: string;
  price: number;
  iva_percent: number;
  unit: string;
}

interface LineItem {
  product_id: number;
  product_name: string;
  quantity: number;
  unit_price: number;
  iva_percent: number;
  total_price: number;
  iva_amount: number;
}

export default function InvoiceWizard() {
  const { token } = useAuth();
  const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
    headers: { Authorization: `Bearer ${token}` },
  });

  const [clients, setClients] = useState<Client[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [selectedClient, setSelectedClient] = useState<number | null>(null);
  const [lines, setLines] = useState<LineItem[]>([]);
  const [status, setStatus] = useState<string>('');
  const [loading, setLoading] = useState(false);

  // Load clients and products on mount
  useEffect(() => {
    const fetchData = async () => {
      const [cRes, pRes] = await Promise.all([
        api.get('/clients'),
        api.get('/products'),
      ]);
      setClients(cRes.data);
      setProducts(pRes.data);
    };
    fetchData();
  }, []);

  const addLine = () => {
    setLines(prev => [...prev, {
      product_id: 0,
      product_name: '',
      quantity: 1,
      unit_price: 0,
      iva_percent: 0,
      total_price: 0,
      iva_amount: 0,
    }]);
  };

  const updateLine = (index: number, field: keyof LineItem, value: any) => {
    setLines(prev => {
      const updated = [...prev];
      const line = { ...updated[index] };
      // Update selected product details if product_id changes
      if (field === 'product_id') {
        const prod = products.find(p => p.id === Number(value));
        if (prod) {
          line.product_id = prod.id;
          line.product_name = prod.name;
          line.unit_price = prod.price;
          line.iva_percent = prod.iva_percent;
        }
      } else {
        (line as any)[field] = field === 'quantity' ? Number(value) : value;
      }
      // Recalculate totals for the line
      line.total_price = line.unit_price * line.quantity;
      line.iva_amount = line.total_price * (line.iva_percent / 100);
      updated[index] = line;
      return updated;
    });
  };

  const removeLine = (index: number) => {
    setLines(prev => prev.filter((_, i) => i !== index));
  };

  const calculateTotals = () => {
    const subtotal = lines.reduce((sum, l) => sum + l.total_price, 0);
    const ivaTotal = lines.reduce((sum, l) => sum + l.iva_amount, 0);
    const total = subtotal + ivaTotal;
    return { subtotal, ivaTotal, total };
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedClient) return;
    setLoading(true);
    setStatus('');
    const payload = {
      client_id: selectedClient,
      line_items: lines.map(l => ({
        product_id: l.product_id,
        quantity: l.quantity,
        unit_price: l.unit_price,
        iva_percent: l.iva_percent,
      })),
    };
    try {
      const resp = await api.post('/invoices', payload);
      setStatus(`Factura creada con CUFE ${resp.data.cufe}. Estado: ${resp.data.status}`);
    } catch (err: any) {
      setStatus(`Error al crear factura: ${err.response?.data?.detail || err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const { subtotal, ivaTotal, total } = calculateTotals();

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Crear Factura Electrónica</h1>
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Cliente */}
        <div>
          <label className="block font-medium mb-1">Cliente</label>
          <select
            value={selectedClient ?? ''}
            onChange={e => setSelectedClient(Number(e.target.value) || null)}
            className="border p-2 w-full"
            required
          >
            <option value="" disabled>Selecciona un cliente</option>
            {clients.map(c => (
              <option key={c.id} value={c.id}>{c.name} ({c.nit})</option>
            ))}
          </select>
        </div>
        {/* Líneas */}
        <div>
          <h2 className="font-semibold mb-2">Detalle de ítems</h2>
          <button type="button" onClick={addLine} className="bg-indigo-600 text-white px-3 py-1 rounded mb-2">
            Añadir línea
          </button>
          {lines.map((line, idx) => (
            <div key={idx} className="grid grid-cols-6 gap-2 items-end mb-2 bg-gray-50 p-2 rounded">
              <select
                value={line.product_id}
                onChange={e => updateLine(idx, 'product_id', e.target.value)}
                className="border p-1"
                required
              >
                <option value="0" disabled>Producto</option>
                {products.map(p => (
                  <option key={p.id} value={p.id}>{p.name} ({p.code})</option>
                ))}
              </select>
              <input
                type="number"
                min="1"
                value={line.quantity}
                onChange={e => updateLine(idx, 'quantity', e.target.value)}
                className="border p-1"
                placeholder="Cantidad"
                required
              />
              <input
                type="number"
                step="0.01"
                value={line.unit_price}
                onChange={e => updateLine(idx, 'unit_price', e.target.value)}
                className="border p-1"
                placeholder="Precio unitario"
                readOnly
              />
              <input
                type="number"
                step="0.01"
                value={line.iva_percent}
                onChange={e => updateLine(idx, 'iva_percent', e.target.value)}
                className="border p-1"
                placeholder="IVA %"
                readOnly
              />
              <div className="flex space-x-2">
                <button type="button" onClick={() => removeLine(idx)} className="text-red-600">Eliminar</button>
              </div>
            </div>
          ))}
        </div>
        {/* Totales */}
        <div className="bg-gray-100 p-4 rounded">
          <p><strong>Subtotal:</strong> {subtotal.toFixed(2)}</p>
          <p><strong>IVA Total:</strong> {ivaTotal.toFixed(2)}</p>
          <p><strong>Total:</strong> {total.toFixed(2)}</p>
        </div>
        {/* Submit */}
        <button type="submit" disabled={loading} className="bg-green-600 text-white px-4 py-2 rounded">
          {loading ? 'Generando...' : 'Crear Factura'}
        </button>
      </form>
      {status && <div className="mt-4 p-4 border rounded bg-white">
        {status}
      </div>}
    </div>
  );
}
