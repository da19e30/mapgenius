import { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, LineChart, Line, CartesianGrid, Legend, PieChart, Pie, Cell } from 'recharts';
import { Link } from 'react-router-dom';
import api from '@/services/api';

interface HealthData {
  status: string;
  message: string;
}

export default function Dashboard() {
  const [categoryData, setCategoryData] = useState<any[]>([]);
  const [monthlyTrend, setMonthlyTrend] = useState<any[]>([]);
  const [aiInsights, setAiInsights] = useState<any[]>([]);
  const [insightsLoading, setInsightsLoading] = useState(true);
  const [insightsError, setInsightsError] = useState<string | null>(null);
  const [health, setHealth] = useState<HealthData | null>(null);
  const [invoices, setInvoices] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Detect route changes (e.g., after upload) to refresh data
  const location = useLocation();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [{ data: healthData }, { data: invoicesData }] = await Promise.all([
          api.get('/health'),
          api.get('/invoices/list'),
        ]);
        setHealth(healthData);
        setInvoices(invoicesData);
        computeCategoryData(invoicesData);
        computeMonthlyTrend(invoicesData);
      } catch (err: any) {
        const detail = err?.response?.data?.detail;
        const friendlyMsg =
          typeof detail === 'string'
            ? detail
            : Array.isArray(detail)
            ? detail.map((d: any) => d.msg).join(' | ')
            : JSON.stringify(detail);
        setError(friendlyMsg || 'Error al cargar datos');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  useEffect(() => {
    const fetchInsights = async () => {
      try {
        setInsightsLoading(true);
        const res = await api.get('/ai/insights');
        setAiInsights(res.data.insights || []);
      } catch (err: any) {
        setInsightsError(err?.response?.data?.detail || 'No se pudieron cargar los insights');
      } finally {
        setInsightsLoading(false);
      }
    };
    fetchInsights();
  }, []);

  function computeCategoryData(invoices: any[]) {
    const categoryMap: Record<string, number> = {};
    invoices.forEach((inv: any) => {
      // Use vendor or filename as category fallback
      const cat = inv.vendor || 'Otros';
      const amount = inv.total_amount || 0;
      categoryMap[cat] = (categoryMap[cat] || 0) + amount;
    });
    const data = Object.entries(categoryMap).map(([name, value]) => ({ name, value }));
    // sort descending
    data.sort((a: any, b: any) => b.value - a.value);
    setCategoryData(data.slice(0, 10)); // top 10
  }

  function computeMonthlyTrend(invoices: any[]) {
    const monthMap: Record<string, number> = {};
    invoices.forEach((inv: any) => {
      const date = new Date(inv.uploaded_at);
      const key = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
      monthMap[key] = (monthMap[key] || 0) + (inv.total_amount || 0);
    });
    const data = Object.entries(monthMap)
      .map(([month, amount]) => ({ month, amount }))
      .sort((a: any, b: any) => a.month.localeCompare(b.month));
    setMonthlyTrend(data);
  }

  const totalInvoices = invoices.length;
  const pendingInvoices = invoices.filter(i => i.status === 'pending').length;
  const processedInvoices = invoices.filter(i => i.processed_at).length;

  return (
      <div className="p-6">
        <h1 className="text-2xl font-bold mb-6">Dashboard - Mapgenius Solutions</h1>

        {error && (
          <div className="bg-red-100 text-red-700 p-4 rounded mb-4">{error}</div>
        )}

        {loading && !error && (
          <div className="text-center py-4">Cargando datos...</div>
        )}

        {/* If no invoices, show friendly placeholder */}
        {!loading && !error && invoices.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-600 mb-4">Aún no tienes facturas registradas.</p>
            <Link
              to="/upload-invoice"
              className="inline-block px-6 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 transition"
            >
              Subir tu primera factura
            </Link>
          </div>
        )}

        {/* When invoices exist, render full dashboard */}
        {!loading && !error && invoices.length > 0 && (
          <>

              {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="bg-white p-6 rounded shadow">
              <h3 className="text-lg font-semibold">Facturas Totales</h3>
              <p className="text-2xl font-bold mt-2">{totalInvoices}</p>
            </div>
            <div className="bg-white p-6 rounded shadow">
              <h3 className="text-lg font-semibold">Facturas Procesadas</h3>
              <p className="text-2xl font-bold mt-2">{processedInvoices}</p>
            </div>
            <div className="bg-white p-6 rounded shadow">
              <h3 className="text-lg font-semibold">Pendientes</h3>
              <p className="text-2xl font-bold mt-2">{pendingInvoices}</p>
            </div>
            {/* Total gasto */}
            <div className="bg-white p-6 rounded shadow">
              <h3 className="text-lg font-semibold">Gasto total</h3>
              <p className="text-2xl font-bold mt-2">
                {invoices.reduce((sum, inv) => sum + (inv.total_amount || 0), 0).toLocaleString('es-ES', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
              </p>
            </div>
          </div>

          {/* Health Status */}
          {health && (
            <div className="bg-white p-6 rounded shadow-md max-w-lg mb-6">
              <h2 className="text-xl font-semibold mb-4">Estado del Sistema</h2>
              <div className="space-y-2">
                <p><strong>Estado:</strong> {health.status}</p>
                <p><strong>Mensaje:</strong> {health.message}</p>
              </div>
            </div>
          )}

          {/* Quick Actions */}
          <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            <Link
              to="/upload-invoice"
              className="block p-4 bg-indigo-600 text-white rounded shadow hover:bg-indigo-700 transition"
            >
              <h3 className="text-lg font-semibold">Subir Factura</h3>
              <p>Procesa tus facturas con OCR e IA</p>
            </Link>
            <Link
              to="/transactions"
              className="block p-4 bg-white rounded shadow hover:bg-gray-50 transition"
            >
              <h3 className="text-lg font-semibold">Transacciones</h3>
              <p className="text-gray-600">Ver tus ingresos y gastos</p>
            </Link>
            {/* Export Buttons */}
            <button
              onClick={() => {
                // descarga facturas CSV
                const link = document.createElement('a');
                link.href = `${import.meta.env.VITE_API_URL ?? '/api/v1'}/export/invoices`;
                link.download = 'invoices.csv';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
              }}
              className="block p-4 bg-green-600 text-white rounded shadow hover:bg-green-700 transition"
            >
              <h3 className="text-lg font-semibold">Exportar Facturas</h3>
            </button>
            <button
              onClick={() => {
                const link = document.createElement('a');
                link.href = `${import.meta.env.VITE_API_URL ?? '/api/v1'}/export/financial-data`;
                link.download = 'financial_data.csv';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
              }}
              className="block p-4 bg-green-600 text-white rounded shadow hover:bg-green-700 transition"
            >
              <h3 className="text-lg font-semibold">Exportar Datos Financieros</h3>
            </button>
          </div>

          {/* Recent Invoices */}
          {/* Spending by Category Chart */}
          <div className="bg-white p-6 rounded shadow mb-6">
            <h2 className="text-xl font-semibold mb-4">Gasto por Categoría</h2>
            {categoryData.length === 0 ? (
              <p className="text-gray-500">Sin datos de gasto.</p>
            ) : (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={categoryData} layout="vertical" margin={{ top: 20, right: 30, left: 80, bottom: 20 }}>
                  <XAxis type="number" />
                  <YAxis dataKey="name" type="category" width={100} />
                  <Tooltip />
                  <Bar dataKey="value" fill="#6366F1" />
                </BarChart>
              </ResponsiveContainer>
            )}
          </div>

          {/* Category Distribution Pie Chart */}
          {categoryData.length > 0 && (
            <div className="bg-white p-6 rounded shadow mb-6">
              <h2 className="text-xl font-semibold mb-4">Distribución por Categoría</h2>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={categoryData}
                    dataKey="value"
                    nameKey="name"
                    cx="50%"
                    cy="50%"
                    outerRadius={100}
                    fill="#8884d8"
                    label
                  >
                    {categoryData.map((_entry, index) => (
                      <Cell key={`cell-${index}`} fill={['#6366F1', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899', '#14B8A6', '#F97316'][index % 8]} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>
          )}

          {/* Monthly Trend Line Chart */}
          <div className="bg-white p-6 rounded shadow mb-6">
            <h2 className="text-xl font-semibold mb-4">Tendencia Mensual</h2>
            {monthlyTrend.length === 0 ? (
              <p className="text-gray-500">Sin datos de tendencia.</p>
            ) : (
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={monthlyTrend} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="amount" stroke="#10B981" />
                </LineChart>
              </ResponsiveContainer>
            )}
          </div>

          {/* Recent Activity Feed */}
          <div className="bg-white p-6 rounded shadow mb-6">
            <h2 className="text-xl font-semibold mb-4">Actividad Reciente</h2>
            <ul className="space-y-2">
              {invoices.slice(0, 5).map((inv) => (
                <li key={inv.id} className="border-b pb-2">
                  <p className="font-medium">Factura {inv.filename}</p>
                  <p className="text-sm text-gray-600">
                    Estado: {inv.status} | Subida: {new Date(inv.uploaded_at).toLocaleDateString()}
                  </p>
                </li>
              ))}
              {invoices.length === 0 && (
                <p className="text-gray-500">No hay actividad reciente.</p>
              )}
            </ul>
          </div>

          {/* AI Insights */}
          <div className="bg-white p-6 rounded shadow mb-6">
            <h2 className="text-xl font-semibold mb-4">AI Insights</h2>
            {insightsLoading ? (
              <p className="text-gray-500">Cargando insights...</p>
            ) : insightsError ? (
              <p className="text-red-500">{insightsError}</p>
            ) : aiInsights.length === 0 ? (
              <p className="text-gray-500">Sin insights disponibles.</p>
            ) : (
              <ul className="space-y-2">
                {aiInsights.map((ins: any, idx: number) => (
                  <li key={idx} className="border-b pb-2">
                    <p className="font-medium">{ins.title || `Insight ${idx + 1}`}</p>
                    <p className="text-sm text-gray-600">{ins.description}</p>
                  </li>
                ))}
              </ul>
            )}
          </div>

          {/* Recent Invoices */}
          <div className="bg-white p-6 rounded shadow">
            <h2 className="text-xl font-semibold mb-4">Últimas Facturas</h2>
            {invoices.slice(0, 5).map((inv) => (
              <div key={inv.id} className="border-b py-2">
                <p className="font-medium">{inv.filename}</p>
                <p className="text-sm text-gray-600">
                  Estado: {inv.status} | Subida: {new Date(inv.uploaded_at).toLocaleDateString()}
                </p>
              </div>
            ))}
            {invoices.length === 0 && (
              <p className="text-gray-500">No hay facturas recientes.</p>
            )}
          </div>
        </>
      )}
    </div>
  );
}
