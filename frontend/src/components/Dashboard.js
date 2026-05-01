// Dashboard.js
// Main overview dashboard showing key financial metrics and charts.

import React from "react";
import { colors, spacing, radii, shadows } from "./DesignSystem";

export default function Dashboard() {
  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Panel de Control</h1>
      {/* Metrics summary */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <MetricCard title="Ingresos" value="$24,560" bg={colors.primary} />
        <MetricCard title="Gastos" value="$8,720" bg={colors.danger} />
        <MetricCard title="Beneficio Neto" value="$15,840" bg={colors.success} />
      </div>
      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <ChartCard title="Ingresos vs Gastos" />
        <ChartCard title="Flujo de Caja" />
      </div>
    </div>
  );
}

function MetricCard({ title, value, bg }) {
  return (
    <div
      className="text-white p-4 rounded-lg shadow"
      style={{ backgroundColor: bg, borderRadius: radii.md }}
    >
      <p className="text-sm opacity-80">{title}</p>
      <p className="text-2xl font-semibold">{value}</p>
    </div>
  );
}

function ChartCard({ title }) {
  // Placeholder for chart – replace with Recharts, Chart.js, etc.
  return (
    <div
      className="bg-white p-4 rounded-lg shadow"
      style={{ borderRadius: radii.md }}
    >
      <h2 className="text-lg font-medium text-gray-700 mb-2">{title}</h2>
      <div className="h-48 flex items-center justify-center text-gray-400">
        {/* Insert chart component here */}
        <span>Gráfico</span>
      </div>
    </div>
  );
}
