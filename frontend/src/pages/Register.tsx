import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '@/services/api';

export default function Register() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    acceptTerms: false,
  });
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const handleChange =
    (field: keyof typeof form) => (e: React.ChangeEvent<HTMLInputElement>) => {
      const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
      setForm(prev => ({ ...prev, [field]: value }));
    };

  const getPasswordStrength = (pass: string): { score: number; label: string; color: string } => {
    let score = 0;
    if (pass.length >= 8) score++;
    if (/[A-Z]/.test(pass)) score++;
    if (/[0-9]/.test(pass)) score++;
    if (/[^A-Za-z0-9]/.test(pass)) score++;
    if (pass.length >= 12) score++;
    const labels = ['Muy débil', 'Débil', 'Regular', 'Fuerte', 'Muy fuerte'];
    const colors = ['bg-red-500', 'bg-orange-500', 'bg-yellow-500', 'bg-green-500', 'bg-emerald-600'];
    return { score, label: labels[Math.min(score, 4)], color: colors[Math.min(score, 4)] };
  };

  const passwordStrength = getPasswordStrength(form.password);

  const passwordEmoji = (score: number): string => {
    const emojis = ['💀', '😢', '😐', '🙂', '💪'];
    return emojis[Math.min(score, 4)];
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    if (form.password !== form.confirmPassword) {
      setError('Las contraseñas no coinciden.');
      return;
    }
    if (form.password.length < 8) {
      setError('La contraseña debe tener al menos 8 caracteres.');
      return;
    }
    if (!form.acceptTerms) {
      setError('Debes aceptar los términos y condiciones.');
      return;
    }

    setLoading(true);
    try {
      await api.post('/users/register', {
        username: form.username,
        email: form.email,
        password: form.password,
      });
      setSuccess('¡Cuenta creada exitosamente! Ya puedes iniciar sesión.');
      setTimeout(() => navigate('/login'), 2500);
    } catch (err: any) {
      setError(
        err?.response?.data?.detail ||
          'Error al registrar. Por favor, inténtalo de nuevo.'
      );
    } finally {
      setLoading(false);
    }
  };

  const eyeIcon = (
    <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
    </svg>
  );

  const eyeOffIcon = (
    <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.243 4.243l-4.242-4.243" />
    </svg>
  );

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-purple-900 to-slate-800 p-4">
      {/* Animation keyframes and custom styles */}
      <style>{`
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .animate-fadeIn {
          animation: fadeIn 0.5s ease-out forwards;
        }
        @keyframes scaleCheck {
          0% { transform: scale(0); opacity: 0; }
          50% { transform: scale(1.2); }
          100% { transform: scale(1); opacity: 1; }
        }
        .animate-scaleCheck {
          animation: scaleCheck 0.5s ease-out forwards;
        }
        .floating-label-group {
          position: relative;
        }
        .floating-label-group label.floating-label {
          position: absolute;
          left: 2.5rem;
          top: 50%;
          transform: translateY(-50%);
          transition: all 0.2s ease-out;
          pointer-events: none;
          color: #6b7280;
          font-size: 0.875rem;
        }
        .floating-label-group input:focus ~ label.floating-label,
        .floating-label-group input:not(:placeholder-shown) ~ label.floating-label {
          top: 0;
          transform: translateY(-100%);
          font-size: 0.75rem;
          color: #4f46e5;
        }
        .input-glow:focus {
          box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.4);
        }
      `}</style>

      <div className="w-full max-w-4xl grid md:grid-cols-2 gap-8 items-center">
        {/* Left side - Benefits */}
        <div className="hidden md:block text-white space-y-6 animate-fadeIn">
          <h2 className="text-3xl font-bold">Únete a Mapgenius</h2>
          <p className="text-slate-300">Transforma la gestión de tus facturas con inteligencia artificial.</p>
          <div className="space-y-4">
            {[
              { icon: '📄', title: 'OCR Inteligente', desc: 'Extracción automática de datos de facturas PDF, JPG y PNG' },
              { icon: '🤖', title: 'Clasificación IA', desc: 'Categorización automática de gastos e ingresos' },
              { icon: '📊', title: 'Análisis Financiero', desc: 'Visualiza tendencias y obtén insights de tus finanzas' },
              { icon: '🔒', title: 'Seguro y Privado', desc: 'Tus datos están protegidos con encriptación' },
            ].map((item, idx) => (
              <div key={idx} className="flex items-start space-x-3">
                <span className="text-2xl">{item.icon}</span>
                <div>
                  <h3 className="font-semibold">{item.title}</h3>
                  <p className="text-sm text-slate-400">{item.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Right side - Form */}
        <div className="w-full animate-fadeIn" style={{ animationDelay: '0.1s' }}>
          {/* Logo */}
          <div className="text-center mb-6">
            <h1 className="text-3xl font-extrabold text-white tracking-tight">
              Mapgenius <span className="text-indigo-400">Solutions</span>
            </h1>
          </div>

          {/* Card */}
          <div className="bg-white/95 backdrop-blur-sm rounded-2xl shadow-2xl p-8 space-y-6 border border-white/20 animate-fadeIn" style={{ animationDelay: '0.2s' }}>
            <div className="text-center">
              <h2 className="text-2xl font-bold text-gray-900">Crear cuenta</h2>
              <p className="text-gray-500 text-sm mt-1">Completa tus datos para comenzar</p>
            </div>
            <div className="space-y-3 mt-4">
              <button type="button" onClick={() => alert('Próximamente')} className="w-full flex items-center justify-center space-x-3 py-2.5 px-4 bg-white border border-gray-300 rounded-xl hover:bg-gray-50 transition shadow-sm">
                <svg width="20" height="20" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill="#EA4335" d="M24 9.5c3.54 0 6.36 1.22 8.23 3.34l-6.23 6.23v-8.57z"/><path fill="#4285F4" d="M24 9.5v8.57l6.23-6.23c-1.87-2.12-4.69-3.34-8.23-3.34z"/><path fill="#FBBC05" d="M24 42c3.24 0 5.95-1.07 7.93-2.9l-6.93-6.93h-1v8.83z"/><path fill="#34A853" d="M24 33.5h1l6.93 6.93C30.95 40.93 28.24 42 24 42v-8.5z"/></svg>
                <span className="text-gray-700 font-medium">Continuar con Google</span>
              </button>
              <button type="button" onClick={() => alert('Próximamente')} className="w-full flex items-center justify-center space-x-3 py-2.5 px-4 bg-white border border-gray-300 rounded-xl hover:bg-gray-50 transition shadow-sm">
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

            {success && (
              <div className="bg-emerald-50 border-l-4 border-emerald-500 p-4 rounded-r-md animate-scaleCheck">
                <div className="flex items-center">
                  <svg className="h-6 w-6 text-emerald-500 mr-2 animate-scaleCheck" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 0 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <p className="text-sm text-emerald-700">{success}</p>
                </div>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              {/* Username */}
              <div className="floating-label-group">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg className="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0115 0 7.5 7.5 0 01-15 0z" />
                  </svg>
                </div>
                <input
                  id="username"
                  type="text"
                  required
                  minLength={3}
                  value={form.username}
                  onChange={handleChange('username')}
                  placeholder=" "
                  className="peer pl-10 pr-12 w-full rounded-xl border-gray-300 bg-gray-50 py-2.5 text-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 focus:outline-none transition input-glow"
                />
                <label htmlFor="username" className="floating-label">Nombre de usuario</label>
              </div>

              {/* Email */}
              <div className="floating-label-group">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg className="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.932l-7.5 4.33a2.25 2.25 0 01-2.25 0l-7.5-4.33a2.25 2.25 0 01-1.07-1.932V6.75" />
                  </svg>
                </div>
                <input
                  id="email"
                  type="email"
                  required
                  value={form.email}
                  onChange={handleChange('email')}
                  placeholder=" "
                  className="peer pl-10 pr-12 w-full rounded-xl border-gray-300 bg-gray-50 py-2.5 text-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 focus:outline-none transition input-glow"
                />
                <label htmlFor="email" className="floating-label">Correo electrónico</label>
              </div>

              {/* Password */}
              <div className="floating-label-group">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg className="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-7.5a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v7.5a2.25 2.25 0 002.25 2.25z" />
                  </svg>
                </div>
                <input
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  required
                  minLength={8}
                  value={form.password}
                  onChange={handleChange('password')}
                  placeholder=" "
                  className="peer pl-10 pr-12 w-full rounded-xl border-gray-300 bg-gray-50 py-2.5 text-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 focus:outline-none transition input-glow"
                />
                <label htmlFor="password" className="floating-label">Contraseña</label>
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 focus:outline-none transition-colors"
                  tabIndex={-1}
                >
                  {showPassword ? eyeOffIcon : eyeIcon}
                </button>
              </div>

              {/* Password strength indicator */}
              {form.password && (
                <div className="space-y-1 ml-10">
                  <div className="flex items-center space-x-1">
                    <span className="text-sm mr-1">{passwordEmoji(passwordStrength.score)}</span>
                    <div className="flex-1 flex space-x-1">
                      {[0, 1, 2, 3, 4].map((i) => (
                        <div
                          key={i}
                          className={`h-1.5 flex-1 rounded-full transition-all duration-300 ${i < passwordStrength.score ? passwordStrength.color : 'bg-gray-200'}`}
                          style={{ transitionDelay: `${i * 50}ms` }}
                        />
                      ))}
                    </div>
                    <span className="text-xs text-gray-500 ml-1">{passwordStrength.label}</span>
                  </div>
                </div>
              )}

              {/* Confirm Password */}
              <div className="floating-label-group">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg className="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-7.5a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v7.5a2.25 2.25 0 002.25 2.25z" />
                  </svg>
                </div>
                <input
                  id="confirmPassword"
                  type={showConfirmPassword ? 'text' : 'password'}
                  required
                  value={form.confirmPassword}
                  onChange={handleChange('confirmPassword')}
                  placeholder=" "
                  className="peer pl-10 pr-12 w-full rounded-xl border-gray-300 bg-gray-50 py-2.5 text-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 focus:outline-none transition input-glow"
                />
                <label htmlFor="confirmPassword" className="floating-label">Confirmar contraseña</label>
                <button
                  type="button"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 focus:outline-none transition-colors"
                  tabIndex={-1}
                >
                  {showConfirmPassword ? eyeOffIcon : eyeIcon}
                </button>
              </div>

              {form.confirmPassword && form.password !== form.confirmPassword && (
                <p className="text-xs text-red-500 ml-10">Las contraseñas no coinciden</p>
              )}
              {form.confirmPassword && form.password === form.confirmPassword && (
                <p className="text-xs text-emerald-500 ml-10">✓ Las contraseñas coinciden</p>
              )}

              {/* Terms checkbox */}
              <div className="flex items-center">
                <input
                  id="terms"
                  type="checkbox"
                  checked={form.acceptTerms}
                  onChange={handleChange('acceptTerms')}
                  className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                />
                <label htmlFor="terms" className="ml-2 block text-sm text-gray-700">
                  Acepto los <a href="#" className="text-indigo-600 hover:text-indigo-500">términos y condiciones</a>
                </label>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 text-white py-3 rounded-xl font-semibold text-sm hover:from-indigo-700 hover:to-purple-700 transition-all duration-300 shadow-lg hover:shadow-xl disabled:opacity-60 disabled:cursor-not-allowed transform hover:scale-[1.02] active:scale-[0.98]"
              >
                {loading ? (
                  <span className="flex items-center justify-center">
                    <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Registrando...
                  </span>
                ) : (
                  'Crear cuenta'
                )}
              </button>
            </form>

            <p className="text-center text-sm text-gray-500">
              ¿Ya tienes cuenta?{' '}
              <Link to="/login" className="font-semibold text-indigo-600 hover:text-indigo-500 transition">
                Inicia sesión
              </Link>
            </p>
          </div>

          {/* Footer */}
          <p className="text-center text-xs text-slate-400 mt-6">
            © 2026 Mapgenius Solutions. Todos los derechos reservados.
          </p>
        </div>
      </div>
    </div>
  );
}
