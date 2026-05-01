// TransactionTable.js
// Financial transaction table with sorting and status indicators.

import React, { useState } from "react";
import { colors, spacing, radii, shadows } from "./DesignSystem";

const sampleTransactions = [
  { id: 1, date: "2026-04-01", description: "Pago cliente A", amount: 3200, type: "income" },
  { id: 2, date: "2026-04-03", description: "Suscripción software", amount: 120, type: "expense" },
  { id: 3, date: "2026-04-05", description: "Pago cliente B", amount: 4500, type: "income" },
  { id: 4, date: "2026-04-07", description: "Alquiler oficina", amount: 800, type: "expense" },
];

export default function TransactionTable() {
  const [sortKey, setSortKey] = useState("date");
  const [sortDir, setSortDir] = useState("desc");

  const sorted = [...sampleTransactions].sort((a, b) => {
    const dir = sortDir === "asc" ? 1 : -1;
    if (a[sortKey] < b[sortKey]) return -1 * dir;
    if (a[sortKey] > b[sortKey]) return 1 * dir;
    return 0;
  });

  const toggleSort = (key) => {
    if (sortKey === key) {
      setSortDir((prev) => (prev === "asc" ? "desc" : "asc"));
    } else {
      setSortKey(key);
      setSortDir("asc");
    }
  };

  return (
    <div className="overflow-x-auto bg-white rounded-lg shadow p-4" style={{ borderRadius: radii.md }}>
      <h2 className="text-lg font-semibold text-gray-700 mb-4">Transacciones Recientes</h2>
      <table className="min-w-full text-sm text-left">
        <thead className="bg-gray-50">
          <tr>
            <SortHeader label="Fecha" field="date" current={sortKey} dir={sortDir} onClick={toggleSort} />
            <SortHeader label="Descripción" field="description" current={sortKey} dir={sortDir} onClick={toggleSort} />
            <SortHeader label="Monto" field="amount" current={sortKey} dir={sortDir} onClick={toggleSort} />
            <th className="px-4 py-2 text-gray-600">Tipo</th>
          </tr>
        </thead>
        <tbody>
          {sorted.map((tx) => (
            <tr key={tx.id} className="border-t hover:bg-gray-50">
              <td className="px-4 py-2">{tx.date}</td>
              <td className="px-4 py-2">{tx.description}</td>
              <td className="px-4 py-2 font-medium">
                ${tx.amount.toLocaleString()}
              </td>
              <td className="px-4 py-2">
                <span
                  className={`px-2 py-1 rounded text-xs font-medium ${
                    tx.type === "income" ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"
                  }`}
                  style={{ borderRadius: radii.sm }}
                >
                  {tx.type === "income" ? "Ingreso" : "Gasto"}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function SortHeader({ label, field, current, dir, onClick }) {
  const isActive = current === field;
  return (
    <th
      className="px-4 py-2 cursor-pointer select-none text-gray-600 hover:text-gray-900"
      onClick={() => onClick(field)}
      aria-sort={isActive ? (dir === "asc" ? "ascending" : "descending") : "none"}
    >
      {label}
      {isActive && <span className="ml-1">{dir === "asc" ? "▲" : "▼"}</span>}
    </th>
  );
}
