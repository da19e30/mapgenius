import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import InvoiceList from "./pages/InvoiceList";
import CreateInvoice from "./pages/CreateInvoice";

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <header className="bg-indigo-600 text-white p-4 shadow-md">
          <h1 className="text-2xl font-bold">Mapgenius Invoice System</h1>
          <nav className="mt-2">
            <Link className="mr-4 hover:underline" to="/">Lista de Facturas</Link>
            <Link className="hover:underline" to="/create">Crear Factura</Link>
          </nav>
        </header>
        <main className="p-6">
          <Routes>
            <Route path="/" element={<InvoiceList />} />
            <Route path="/create" element={<CreateInvoice />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
