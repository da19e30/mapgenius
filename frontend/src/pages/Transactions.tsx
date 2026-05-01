import { useEffect, useState } from 'react';
import api from '@/services/api';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

interface Transaction {
  id: number;
  category: string;
  amount: string;
  currency: string;
  transaction_date: string | null;
  rfc_emisor: string | null;
  invoice_id: number;
  created_at: string;
}

export default function Transactions() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [categoryFilter, setCategoryFilter] = useState('');
  const [dateFrom, setDateFrom] = useState('');
  const [dateTo, setDateTo] = useState('');

  useEffect(() => {
    const fetchTransactions = async () => {
      try {
        const { data } = await api.get('/financial-data/list');
        setTransactions(data);
      } catch (err: any) {
        setError(err?.response?.data?.detail || 'Error al cargar transacciones');
      } finally {
        setLoading(false);
      }
    };
    fetchTransactions();
  }, []);

  const filtered = transactions.filter((t) => {
    const matchCategory = categoryFilter ? t.category === categoryFilter : true;
    const txDate = t.transaction_date ? new Date(t.transaction_date) : null;
    const matchFrom = dateFrom ? txDate && txDate >= new Date(dateFrom) : true;
    const matchTo = dateTo ? txDate && txDate <= new Date(dateTo) : true;
    return matchCategory && matchFrom && matchTo;
  });

  const totalAmount = filtered.reduce((sum, t) => sum + parseFloat(t.amount || '0'), 0);

  // Extract unique categories for filter dropdown
  const categories = Array.from(new Set(transactions.map((t) => t.category)));

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6 text-gray-800">Transacciones</h1>

      {error && (
        <div className="bg-red-100 text-red-700 p-4 rounded mb-4">{error}</div>
      )}

      {/* Filters card */}
      <div className="bg-white p-6 rounded shadow mb-6">
        <h2 className="text-lg font-semibold mb-4">Filtros</h2>
        <div className="flex flex-col md:flex-row md:items-center md:space-x-4">
          <select
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
            className="border border-gray-300 rounded p-2 mb-2 md:mb-0 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="">Todas las categorías</option>
            {categories.map((cat) => (
              <option key={cat} value={cat}>
                {cat}
              </option>
            ))}
          </select>
          <input
            type="date"
            value={dateFrom}
            onChange={(e) => setDateFrom(e.target.value)}
            placeholder="Desde"
            className="border border-gray-300 rounded p-2 mb-2 md:mb-0 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
          <input
            type="date"
            value={dateTo}
            onChange={(e) => setDateTo(e.target.value)}
            placeholder="Hasta"
            className="border border-gray-300 rounded p-2 mb-2 md:mb-0 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
          <button
            onClick={() => {
              setCategoryFilter('');
              setDateFrom('');
              setDateTo('');
            }}
            className="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700 transition"
          >
            Resetear
          </button>
        </div>
      </div>

      {/* Chart by category */}
      {!loading && filtered.length > 0 && (
        <div className="bg-white p-6 rounded shadow mb-6">
          <h2 className="text-lg font-semibold mb-4">Gasto por Categoría</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={Object.entries(
                filtered.reduce((acc, t) => {
                  acc[t.category] = (acc[t.category] || 0) + parseFloat(t.amount || '0');
                  return acc;
                }, {} as Record<string, number>)
              ).map(([name, value]) => ({ name, value }))}>
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#6366F1" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Transactions table card */}
      <div className="bg-white rounded shadow overflow-hidden">
        {loading ? (
          <div className="text-center py-8 text-gray-500">Cargando transacciones...</div>
        ) : filtered.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            {transactions.length === 0
              ? 'No hay transacciones registradas.'
              : 'No hay transacciones que coincidan con los filtros.'}
          </div>
        ) : (
          <>
            <div className="overflow-x-auto">
              <table className="min-w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="p-3 text-left text-sm font-medium text-gray-700">Fecha</th>
                    <th className="p-3 text-left text-sm font-medium text-gray-700">Categoría</th>
                    <th className="p-3 text-left text-sm font-medium text-gray-700">Monto</th>
                    <th className="p-3 text-left text-sm font-medium text-gray-700">Moneda</th>
                    <th className="p-3 text-left text-sm font-medium text-gray-700">RFC Emisor</th>
                    <th className="p-3 text-left text-sm font-medium text-gray-700">Factura</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {filtered.map((t) => (
                    <tr key={t.id} className="hover:bg-gray-50">
                      <td className="p-3 text-sm">
                        {t.transaction_date
                          ? new Date(t.transaction_date).toLocaleDateString()
                          : '—'}
                      </td>
                      <td className="p-3 text-sm">{t.category}</td>
                      <td className="p-3 text-sm font-medium">{t.amount}</td>
                      <td className="p-3 text-sm">{t.currency}</td>
                      <td className="p-3 text-sm">{t.rfc_emisor || '—'}</td>
                      <td className="p-3 text-sm text-indigo-600">
                        #{t.invoice_id}
                      </td>
                    </tr>
                  ))}
                </tbody>
                <tfoot className="bg-indigo-50">
                  <tr>
                    <td className="p-3 font-semibold text-gray-800" colSpan={2}>
                      Total ({filtered.length} transacciones)
                    </td>
                    <td className="p-3 font-bold text-indigo-700" colSpan={4}>
                      ${totalAmount.toFixed(2)}
                    </td>
                  </tr>
                </tfoot>
              </table>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
