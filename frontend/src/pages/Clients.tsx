import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth } from '@/context/AuthContext';

interface Client {
  id: number;
  nit: string;
  name: string;
  email: string;
  address?: string;
  tax_regime: string;
}

export default function Clients() {
  const { token } = useAuth();
  const [clients, setClients] = useState<Client[]>([]);
  const [editing, setEditing] = useState<Client | null>(null);
  const [form, setForm] = useState<Omit<Client, 'id'>>({
    nit: '',
    name: '',
    email: '',
    address: '',
    tax_regime: '',
  });

  const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
    headers: { Authorization: `Bearer ${token}` },
  });

  const loadClients = async () => {
    const resp = await api.get('/clients');
    setClients(resp.data);
  };

  useEffect(() => {
    loadClients();
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (editing) {
      await api.put(`/clients/${editing.id}`, form);
    } else {
      await api.post('/clients', form);
    }
    setForm({ nit: '', name: '', email: '', address: '', tax_regime: '' });
    setEditing(null);
    loadClients();
  };

  const startEdit = (c: Client) => {
    setEditing(c);
    setForm({ nit: c.nit, name: c.name, email: c.email, address: c.address || '', tax_regime: c.tax_regime });
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('¿Eliminar cliente?')) {
      await api.delete(`/clients/${id}`);
      loadClients();
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Gestión de Clientes</h1>
      <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-4 mb-6">
        <input name="nit" placeholder="NIT" value={form.nit} onChange={handleChange} className="border p-2" required />
        <input name="name" placeholder="Nombre / Razón Social" value={form.name} onChange={handleChange} className="border p-2" required />
        <input name="email" placeholder="Email" value={form.email} onChange={handleChange} className="border p-2" required />
        <input name="address" placeholder="Dirección" value={form.address} onChange={handleChange} className="border p-2" />
        <input name="tax_regime" placeholder="Régimen tributario" value={form.tax_regime} onChange={handleChange} className="border p-2" required />
        <button type="submit" className="bg-indigo-600 text-white px-4 py-2 rounded">
          {editing ? 'Actualizar' : 'Crear'}
        </button>
      </form>
      <table className="min-w-full bg-white border">
        <thead className="bg-gray-100">
          <tr>
            <th className="p-2 text-left">NIT</th>
            <th className="p-2 text-left">Nombre</th>
            <th className="p-2 text-left">Email</th>
            <th className="p-2 text-left">Dirección</th>
            <th className="p-2 text-left">Regimen</th>
            <th className="p-2">Acciones</th>
          </tr>
        </thead>
        <tbody>
          {clients.map(c => (
            <tr key={c.id} className="border-t">
              <td className="p-2">{c.nit}</td>
              <td className="p-2">{c.name}</td>
              <td className="p-2">{c.email}</td>
              <td className="p-2">{c.address}</td>
              <td className="p-2">{c.tax_regime}</td>
              <td className="p-2 space-x-2">
                <button onClick={() => startEdit(c)} className="text-blue-600">Editar</button>
                <button onClick={() => handleDelete(c.id)} className="text-red-600">Eliminar</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
