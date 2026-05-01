import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth } from '@/context/AuthContext';

interface Product {
  id: number;
  code: string;
  name: string;
  price: number;
  iva_percent: number;
  dian_class?: string;
  unit: string;
}

export default function ProductPage() {
  const { token } = useAuth();
  const [products, setProducts] = useState<Product[]>([]);
  const [editing, setEditing] = useState<Product | null>(null);
  const [form, setForm] = useState<Omit<Product, 'id'>>({
    code: '',
    name: '',
    price: 0,
    iva_percent: 19,
    dian_class: '',
    unit: 'unidad',
  });

  const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
    headers: { Authorization: `Bearer ${token}` },
  });

  const loadProducts = async () => {
    const resp = await api.get('/products');
    setProducts(resp.data);
  };

  useEffect(() => {
    loadProducts();
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setForm(prev => ({ ...prev, [name]: name === 'price' || name === 'iva_percent' ? parseFloat(value) : value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (editing) {
      await api.put(`/products/${editing.id}`, form);
    } else {
      await api.post('/products', form);
    }
    setForm({ code: '', name: '', price: 0, iva_percent: 19, dian_class: '', unit: 'unidad' });
    setEditing(null);
    loadProducts();
  };

  const startEdit = (p: Product) => {
    setEditing(p);
    setForm({ code: p.code, name: p.name, price: p.price, iva_percent: p.iva_percent, dian_class: p.dian_class || '', unit: p.unit });
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('¿Eliminar producto?')) {
      await api.delete(`/products/${id}`);
      loadProducts();
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Gestión de Productos/Servicios</h1>
      <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-4 mb-6">
        <input name="code" placeholder="Código / SKU" value={form.code} onChange={handleChange} className="border p-2" required />
        <input name="name" placeholder="Nombre" value={form.name} onChange={handleChange} className="border p-2" required />
        <input name="price" type="number" step="0.01" placeholder="Precio unitario" value={form.price} onChange={handleChange} className="border p-2" required />
        <input name="iva_percent" type="number" step="0.01" placeholder="IVA %" value={form.iva_percent} onChange={handleChange} className="border p-2" required />
        <input name="dian_class" placeholder="Código DIAN (opcional)" value={form.dian_class} onChange={handleChange} className="border p-2" />
        <input name="unit" placeholder="Unidad de medida" value={form.unit} onChange={handleChange} className="border p-2" required />
        <button type="submit" className="bg-indigo-600 text-white px-4 py-2 rounded col-span-2">
          {editing ? 'Actualizar' : 'Crear'}
        </button>
      </form>
      <table className="min-w-full bg-white border">
        <thead className="bg-gray-100">
          <tr>
            <th className="p-2 text-left">Código</th>
            <th className="p-2 text-left">Nombre</th>
            <th className="p-2 text-left">Precio</th>
            <th className="p-2 text-left">IVA %</th>
            <th className="p-2 text-left">Clase DIAN</th>
            <th className="p-2 text-left">Unidad</th>
            <th className="p-2">Acciones</th>
          </tr>
        </thead>
        <tbody>
          {products.map(p => (
            <tr key={p.id} className="border-t">
              <td className="p-2">{p.code}</td>
              <td className="p-2">{p.name}</td>
              <td className="p-2">{p.price.toFixed(2)}</td>
              <td className="p-2">{p.iva_percent}</td>
              <td className="p-2">{p.dian_class}</td>
              <td className="p-2">{p.unit}</td>
              <td className="p-2 space-x-2">
                <button onClick={() => startEdit(p)} className="text-blue-600">Editar</button>
                <button onClick={() => handleDelete(p.id)} className="text-red-600">Eliminar</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-800 p-8">
      <div className="max-w-4xl mx-auto text-white">
        <h1 className="text-4xl font-extrabold mb-6">Producto</h1>
        <p className="text-slate-300 mb-4">Descubre todas las funcionalidades de Mapgenius Solutions.</p>
        <div className="grid md:grid-cols-3 gap-6 mt-8">
          {['OCR Inteligente', 'Clasificación IA', 'Análisis Financiero'].map((f) => (
            <div key={f} className="bg-white/10 p-6 rounded-xl backdrop-blur-sm">
              <h3 className="text-xl font-semibold mb-2">{f}</h3>
              <p className="text-slate-400 text-sm">Automatización y precisión en el procesamiento de facturas.</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
