import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '@/services/api';
import { useAuth } from '@/context/AuthContext';

export default function Login() {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const { data } = await api.post('/users/login', { email, password });
      login(data.access_token, data.email || null);
      navigate('/dashboard');
    } catch (err: any) {
      const detail = err?.response?.data?.detail;
      const friendlyMsg =
        typeof detail === 'string'
          ? detail
          : Array.isArray(detail)
          ? detail.map((d: any) => d.msg).join(' | ')
          : JSON.stringify(detail);
      setError(
        friendlyMsg ||
          'Error al iniciar sesión. Verifique sus credenciales.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-purple-900 to-slate-800 p-4">
      <div className="w-full max-w-md">
        {/* Logo / Título superior */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-extrabold text-white tracking-tight">
            Mapgenius <span className="text-indigo-400">Solutions</span>
          </h1>
          <p className="text-slate-300 mt-2 text-sm">Inicia sesión y gestiona tus finanzas con IA</p>
        </div>

        {/* Tarjeta principal */}
        <div className="bg-white/95 backdrop-blur-sm rounded-2xl shadow-2xl p-8 space-y-6 border border-white/20">
          <div className="text-center">
            <h2 className="text-2xl font-bold text-gray-900">Iniciar sesión</h2>
            <p className="text-gray-500 text-sm mt-1">Ingresa tus credenciales para continuar</p>
          </div>
          <div className="space-y-3 mt-4">
            <button type="button" onClick={() => window.location.href='http://localhost:8000/api/v1/auth/google'} className="w-full flex items-center justify-center space-x-3 py-2.5 px-4 bg-white border border-gray-300 rounded-xl hover:bg-gray-50 transition shadow-sm">
              <svg width="20" height="20" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill="#EA4335" d="M24 9.5c3.54 0 6.36 1.22 8.23 3.34l-6.23 6.23v-8.57z"/><path fill="#4285F4" d="M24 9.5v8.57l6.23-6.23c-1.87-2.12-4.69-3.34-8.23-3.34z"/><path fill="#FBBC05" d="M24 42c3.24 0 5.95-1.07 7.93-2.9l-6.93-6.93h-1v8.83z"/><path fill="#34A853" d="M24 33.5h1l6.93 6.93C30.95 40.93 28.24 42 24 42v-8.5z"/></svg>
              <span className="text-gray-700 font-medium">Continuar con Google</span>
            </button>
            <button type="button" onClick={() => window.location.href='http://localhost:8000/api/v1/auth/google'} className="w-full flex items-center justify-center space-x-3 py-2.5 px-4 bg-white border border-gray-300 rounded-xl hover:bg-gray-50 transition shadow-sm">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="2" y="2" width="20" height="20" rx="2" fill="#F25022"/><rect x="2" y="2" width="9" height="9" fill="#7FBA00"/><rect x="13" y="2" width="9" height="9" fill="#00A4EF"/><rect x="2" y="13" width="9" height="9" fill="#FFB900"/><rect x="13" y="13" width="9" height="9" fill="#F25022"/></svg>
              <span className="text-gray-700 font-medium">Continuar con Microsoft</span>
            </button>
            <div className="flex items-center my-3">
              <hr className="flex-grow border-t border-gray-300" />
              <span className="mx-3 text-gray-500 text-sm">o</span>
              <hr className="flex-grow border-t border-gray-300" />
            </div>
          </div>

          {error && (
            <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded-r-md">
              <div className="flex items-center">
                <svg className="h-5 w-5 text-red-500 mr-2" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 0 8 8 0 000 16zm0-2a6 6 0 110-12 0 6 6 0 010 12zm-.75-5.25a.75.75 0 01.75-.75h.5a.75.75 0 01.75.75v3.5a.75.75 0 01-.75.75h-.5a.75.75 0 01-.75-.75v-3.5zm.75-3a1 1 0 100-2 0 1 1 0 002 0z" clipRule="evenodd" />
                </svg>
                <p className="text-sm text-red-700">{error}</p>
              </div>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Email */}
            <div className="space-y-1">
              <label className="text-sm font-medium text-gray-700 block">Correo electrónico</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg className="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.932l-7.5 4.33a2.25 2.25 0 01-2.25 0l-7.5-4.33a2.25 2.25 0 01-1.07-1.932V6.75" />
                  </svg>
                </div>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={e => setEmail(e.target.value)}
                  placeholder="tu@email.com"
                  className="pl-10 w-full rounded-xl border-gray-300 bg-gray-50 py-2.5 text-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 focus:outline-none transition"
                />
              </div>
            </div>

            {/* Password */}
            <div className="space-y-1">
              <label className="text-sm font-medium text-gray-700 block">Contraseña</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg className="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-7.5a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v7.5a2.25 2.25 0 002.25 2.25z" />
                  </svg>
                </div>
                <input
                  type="password"
                  required
                  value={password}
                  onChange={e => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="pl-10 w-full rounded-xl border-gray-300 bg-gray-50 py-2.5 text-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 focus:outline-none transition"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 text-white py-3 rounded-xl font-semibold text-sm hover:from-indigo-700 hover:to-purple-700 transition-all duration-300 shadow-lg hover:shadow-xl disabled:opacity-60 disabled:cursor-not-allowed"
            >
              {loading ? (
                <span className="flex items-center justify-center">
                  <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Entrando...
                </span>
              ) : (
                'Iniciar sesión'
              )}
            </button>
          </form>

          <p className="text-center text-sm text-gray-500">
            ¿No tienes cuenta?{' '}
            <Link to="/register" className="font-semibold text-indigo-600 hover:text-indigo-500 transition">
              Regístrate aquí
            </Link>
          </p>
        </div>

        {/* Footer */}
        <p className="text-center text-xs text-slate-400 mt-6">
          © 2026 Mapgenius Solutions. Todos los derechos reservados.
        </p>
      </div>
    </div>
  );
}
