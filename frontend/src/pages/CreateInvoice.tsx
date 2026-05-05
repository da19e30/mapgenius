import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

interface ClientOption { id: number; nit: string; name: string; }
interface ProductOption { id: number; code: string; name: string; price: number; iva_percent: number; }

interface LineItem {
  product_id: number;
  quantity: number;
  unit_price: number;
  iva_percent: number;
}

const CreateInvoice = () => {
  const navigate = useNavigate();
  const [clients, setClients] = useState<ClientOption[]>([]);
  const [products, setProducts] = useState<ProductOption[]>([]);
  const [clientId, setClientId] = useState<number | "">("");
  const [lines, setLines] = useState<LineItem[]>([
    { product_id: 0, quantity: 1, unit_price: 0, iva_percent: 19 },
  ]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [clientsRes, productsRes] = await Promise.all([
          api.get("/clients"),
          api.get("/products"),
        ]);
        setClients(clientsRes.data);
        setProducts(productsRes.data);
      } catch {
        setError("Error al cargar clientes o productos");
      }
    };
    fetchData();
  }, []);

  const addLine = () => {
    setLines([...lines, { product_id: 0, quantity: 1, unit_price: 0, iva_percent: 19 }]);
  };

  const updateLine = (index: number, field: keyof LineItem, value: number) => {
    setLines(lines.map((l, i) => (i === index ? { ...l, [field]: value } : l)));
  };

  const removeLine = (index: number) => {
    setLines(lines.filter((_, i) => i !== index));
  };

  const subtotal = lines.reduce((s, l) => s + l.quantity * l.unit_price, 0);
  const ivaTotal = lines.reduce((s, l) => s + l.quantity * l.unit_price * l.iva_percent / 100, 0);
  const total = subtotal + ivaTotal;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    if (!clientId) { setError("Seleccione un cliente"); return; }
    if (lines.some(l => !l.product_id)) { setError("Seleccione un producto en cada línea"); return; }

    setLoading(true);
    try {
      await api.post("/invoices/", {
        client_id: clientId,
        line_items: lines.map(l => ({
          product_id: l.product_id,
          quantity: l.quantity,
          unit_price: l.unit_price,
          iva_percent: l.iva_percent,
        })),
      });
      alert("Factura creada con éxito");
      navigate("/");
    } catch (err: any) {
      const detail = err?.response?.data?.detail;
      setError(typeof detail === "string" ? detail : JSON.stringify(detail));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto">
      <h2 className="text-2xl font-semibold mb-6">Crear Nueva Factura</h2>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-sm p-6 space-y-6">
        {/* Cliente */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Cliente *</label>
          <select
            value={clientId}
            onChange={e => setClientId(Number(e.target.value) || "")}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
            required
          >
            <option value="">-- Seleccionar cliente --</option>
            {clients.map(c => (
              <option key={c.id} value={c.id}>{c.nit} - {c.name}</option>
            ))}
          </select>
        </div>

        {/* Líneas */}
        <div>
          <h3 className="text-lg font-medium mb-2">Líneas de detalle</h3>
          {lines.map((line, idx) => (
            <div key={idx} className="grid grid-cols-1 md:grid-cols-5 gap-3 mb-3 items-end">
              <div className="md:col-span-2">
                <label className="block text-xs text-gray-500">Producto</label>
                <select
                  value={line.product_id || ""}
                  onChange={e => {
                    const pid = Number(e.target.value);
                    const prod = products.find(p => p.id === pid);
                    updateLine(idx, "product_id", pid);
                    if (prod) {
                      updateLine(idx, "unit_price", prod.price);
                      updateLine(idx, "iva_percent", prod.iva_percent);
                    }
                  }}
                  className="w-full px-2 py-1 border border-gray-300 rounded"
                  required
                >
                  <option value="">-- Producto --</option>
                  {products.map(p => (
                    <option key={p.id} value={p.id}>{p.code} - {p.name}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-xs text-gray-500">Cant.</label>
                <input type="number" step="0.01" value={line.quantity}
                  onChange={e => updateLine(idx, "quantity", Number(e.target.value))}
                  className="w-full px-2 py-1 border border-gray-300 rounded" required />
              </div>
              <div>
                <label className="block text-xs text-gray-500">Precio Unit.</label>
                <input type="number" step="0.01" value={line.unit_price}
                  onChange={e => updateLine(idx, "unit_price", Number(e.target.value))}
                  className="w-full px-2 py-1 border border-gray-300 rounded" required />
              </div>
              <div className="flex items-center gap-2">
                <div className="flex-1">
                  <label className="block text-xs text-gray-500">IVA %</label>
                  <input type="number" step="0.01" value={line.iva_percent}
                    onChange={e => updateLine(idx, "iva_percent", Number(e.target.value))}
                    className="w-full px-2 py-1 border border-gray-300 rounded" required />
                </div>
                {lines.length > 1 && (
                  <button type="button" onClick={() => removeLine(idx)}
                    className="text-red-500 text-sm mt-5">✕</button>
                )}
              </div>
            </div>
          ))}
          <button type="button" onClick={addLine}
            className="text-indigo-600 text-sm hover:underline">+ Agregar línea</button>
        </div>

        {/* Totales */}
        <div className="bg-gray-50 p-4 rounded">
          <div className="flex justify-between"><span>Subtotal:</span><span>${subtotal.toFixed(2)}</span></div>
          <div className="flex justify-between"><span>IVA:</span><span>${ivaTotal.toFixed(2)}</span></div>
          <div className="flex justify-between font-bold text-lg"><span>Total:</span><span>${total.toFixed(2)}</span></div>
        </div>

        <div className="flex gap-4">
          <button type="submit" disabled={loading}
            className="flex-1 bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 disabled:opacity-50">
            {loading ? "Creando..." : "Crear Factura"}
          </button>
          <button type="button" onClick={() => navigate("/")}
            className="flex-1 bg-gray-200 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-300">
            Cancelar
          </button>
        </div>
      </form>
    </div>
  );
};

export default CreateInvoice;
