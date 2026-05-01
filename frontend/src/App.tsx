import { Routes, Route, Navigate } from 'react-router-dom';
import HealthCheck from '@/pages/HealthCheck';
import Layout from '@/components/Layout';
import Login from '@/pages/Login';
import Register from '@/pages/Register';
import Dashboard from '@/pages/Dashboard';
import Landing from '@/pages/Landing';
import UploadInvoice from '@/pages/UploadInvoice';
import Transactions from '@/pages/Transactions';
import Product from '@/pages/Product';
import Clients from '@/pages/Clients';
import InvoiceWizard from '@/pages/InvoiceWizard';
import Features from '@/pages/Features';
import Pricing from '@/pages/Pricing';
import Integrations from '@/pages/Integrations';
import Security from '@/pages/Security';
import Company from '@/pages/Company';
import About from '@/pages/About';
import Blog from '@/pages/Blog';
import Careers from '@/pages/Careers';
import Contact from '@/pages/Contact';
import Legal from '@/pages/Legal';
import Terms from '@/pages/Terms';
import Privacy from '@/pages/Privacy';
import Cookies from '@/pages/Cookies';
import { useAuth } from '@/context/AuthContext';

function PrivateRoute({ children }: { children: JSX.Element }) {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? children : <Navigate to="/login" replace />;
}

import { ThemeProvider } from '@/context/ThemeContext';
import { ToastProvider } from '@/components/ui/ToastProvider';
export default function App() {
  return (
    <ThemeProvider>
      <ToastProvider>
        <Routes>
      {/* Public routes */}
      <Route path="/" element={<Landing />} />
          <Route path="/health" element={<HealthCheck />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/product" element={<Product />} />
            <Route path="/clients" element={<Clients />} />
            <Route path="/invoice-wizard" element={<InvoiceWizard />} />
      <Route path="/features" element={<Features />} />
      <Route path="/pricing" element={<Pricing />} />
      <Route path="/integrations" element={<Integrations />} />
      <Route path="/security" element={<Security />} />
      <Route path="/company" element={<Company />} />
      <Route path="/about" element={<About />} />
      <Route path="/blog" element={<Blog />} />
      <Route path="/careers" element={<Careers />} />
      <Route path="/contact" element={<Contact />} />
      <Route path="/legal" element={<Legal />} />
      <Route path="/terms" element={<Terms />} />
      <Route path="/privacy" element={<Privacy />} />
      <Route path="/cookies" element={<Cookies />} />

      {/* Protected routes */}
      <Route
        element={
          <PrivateRoute>
            <Layout />
          </PrivateRoute>
        }
      >
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/upload-invoice" element={<UploadInvoice />} />
        <Route path="/transactions" element={<Transactions />} />
      </Route>

      {/* Catch-all */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
      </ToastProvider>
    </ThemeProvider>
  );
}
