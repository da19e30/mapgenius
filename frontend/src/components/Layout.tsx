import { Outlet, NavLink, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import { useAuth } from '@/context/AuthContext';
import Footer from '@/components/Footer';

import { Moon, Sun, Menu, X, Home, BarChart2, Upload, CreditCard, LogOut } from 'lucide-react';
import ThemeToggle from '@/components/ThemeToggle';
import { useToast } from '@/components/ui/ToastProvider';
export default function Layout() {
  const { isAuthenticated, logout, email } = useAuth();
  const [showMenu, setShowMenu] = useState(false);
  const navigate = useNavigate();

  const { addToast } = useToast();
  const handleLogout = () => {
    logout();
    addToast('Sesión cerrada', 'info');
    navigate('/login');
  };

  // Redirect to landing if not authenticated (should not happen due to PrivateRoute, but safety)
  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <p className="text-gray-500">Redirigiendo...</p>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar - only for authenticated users */}
      {isAuthenticated && (
        <aside className="w-64 bg-white dark:bg-gray-800 shadow-md transition-colors duration-200">
          <nav className="flex flex-col p-4 space-y-2">
                <NavLink
                  to="/dashboard"
                  className={({ isActive }) =>
                    `flex items-center p-2 rounded hover:bg-gray-200 dark:hover:bg-gray-700 ${isActive ? 'bg-gray-200 dark:bg-gray-700 font-medium' : ''}`
                  }
                >
                  <BarChart2 className="mr-2 w-5 h-5" />
                  Dashboard
                </NavLink>
                <NavLink
                  to="/upload-invoice"
                  className={({ isActive }) =>
                    `flex items-center p-2 rounded hover:bg-gray-200 dark:hover:bg-gray-700 ${isActive ? 'bg-gray-200 dark:bg-gray-700 font-medium' : ''}`
                  }
                >
                  <Upload className="mr-2 w-5 h-5" />
                  Subir Factura
                </NavLink>
                <NavLink
                  to="/transactions"
                  className={({ isActive }) =>
                    `flex items-center p-2 rounded hover:bg-gray-200 dark:hover:bg-gray-700 ${isActive ? 'bg-gray-200 dark:bg-gray-700 font-medium' : ''}`
                  }
                >
                  <CreditCard className="mr-2 w-5 h-5" />
                  Transacciones
                </NavLink>
                <NavLink
                  to="/"
                  className={({ isActive }) =>
                    `flex items-center p-2 rounded hover:bg-gray-200 dark:hover:bg-gray-700 ${isActive ? 'bg-gray-200 dark:bg-gray-700 font-medium' : ''}`
                  }
                >
                  <Home className="mr-2 w-5 h-5" />
                  Volver al inicio
                </NavLink>
                        <button
              onClick={handleLogout}
              className="mt-4 p-2 text-left w-full hover:bg-gray-200 rounded"
            >
              Cerrar sesión
            </button>
          </nav>
        </aside>
      )}

      {/* Main area */}
      <main className="flex-1 overflow-y-auto">
        {/* Top bar */}
        <header className="bg-white dark:bg-gray-800 shadow p-4 flex justify-between items-center">
                <button className="md:hidden p-2" onClick={() => setShowMenu(!showMenu)}>
                  <Menu className="w-6 h-6" />
                </button>
          <div className="flex items-center space-x-2">
            <h1 className="text-xl font-semibold">Mapgenius Solutions</h1>
            <ThemeToggle />
          </div>
          <div className="relative inline-block text-left">
            <button onClick={() => setShowMenu(!showMenu)} className="flex items-center space-x-2 focus:outline-none">
              <span className="inline-block w-8 h-8 bg-indigo-500 rounded-full text-white flex items-center justify-center">
                {email ? email.charAt(0).toUpperCase() : '?'}
              </span>
              <span className="text-sm text-gray-700">{email || 'Usuario'}</span>
            </button>
            {showMenu && (
              <div className="origin-top-right absolute right-0 mt-2 w-40 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5">
                <div className="py-1">
                  <button onClick={handleLogout} className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Cerrar sesión</button>
                </div>
              </div>
            )}
          </div>
        </header>

        {/* Page content */}
        <section className="p-6 flex-1">
          <Outlet />
        </section>
        <Footer isAuthenticated={true} />
      </main>
    </div>
  );
}
