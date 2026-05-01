import { Link } from 'react-router-dom';

const features = [
  {
    icon: (
      <svg className="h-8 w-8 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
      </svg>
    ),
    title: 'OCR Inteligente',
    description: 'Extracción automática de datos de facturas en PDF, JPG y PNG con precisión de nivel empresarial.',
  },
  {
    icon: (
      <svg className="h-8 w-8 text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714a2.25 2.25 0 00.659 1.591L19 14.5M14.25 3.104c.251.023.501.05.75.082M19 14.5l-1.26 3.78a2.25 2.25 0 01-2.13 1.47H8.39a2.25 2.25 0 01-2.13-1.47L5 14.5m14 0H5" />
      </svg>
    ),
    title: 'Clasificación con IA',
    description: 'Categorización automática de gastos e ingresos usando modelos avanzados de inteligencia artificial.',
  },
  {
    icon: (
      <svg className="h-8 w-8 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z" />
      </svg>
    ),
    title: 'Analítica Financiera',
    description: 'Visualiza tendencias, genera reportes y obtén insights accionables de tus finanzas.',
  },
  {
    icon: (
      <svg className="h-8 w-8 text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" />
      </svg>
    ),
    title: 'Seguridad Garantizada',
    description: 'Tus datos están protegidos con encriptación de extremo a extremo y cumplimiento normativo.',
  },
];

const steps = [
  {
    number: '1',
    title: 'Sube tu factura',
    description: 'Arrastra y suelta tus facturas en cualquier formato: PDF, JPG, PNG o XML.',
    icon: (
      <svg className="h-10 w-10 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5" />
      </svg>
    ),
  },
  {
    number: '2',
    title: 'IA procesa',
    description: 'Nuestra IA extrae datos, clasifica gastos e identifica patrones automáticamente.',
    icon: (
      <svg className="h-10 w-10 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.455 2.456L21.75 6l-1.036.259a3.375 3.375 0 00-2.455 2.456z" />
      </svg>
    ),
  },
  {
    number: '3',
    title: 'Visualiza resultados',
    description: 'Accede a dashboards interactivos, reportes y análisis financieros en tiempo real.',
    icon: (
      <svg className="h-10 w-10 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7.5 3.75H6A2.25 2.25 0 003.75 6v1.5M16.5 3.75H18A2.25 2.25 0 0120.25 6v1.5m0 9V18A2.25 2.25 0 0118 20.25h-1.5m-9 0H6A2.25 2.25 0 013.75 18v-1.5M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
      </svg>
    ),
  },
];

export default function Landing() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-800">
      {/* Navigation */}
      <nav className="absolute top-0 left-0 right-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <span className="text-2xl font-extrabold text-white tracking-tight">
                Mapgenius <span className="text-indigo-400">Solutions</span>
              </span>
            </div>
            <div className="flex items-center space-x-4">
              <Link
                to="/login"
                className="text-slate-300 hover:text-white text-sm font-medium transition"
              >
                Iniciar sesión
              </Link>
              <Link
                to="/register"
                className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700 transition"
              >
                Comenzar gratis
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative pt-32 pb-20 px-4 sm:px-6 lg:px-8 overflow-hidden">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-4xl md:text-6xl font-extrabold text-white tracking-tight">
            Automatiza tus finanzas
            <br />
            <span className="text-indigo-400">con Inteligencia Artificial</span>
          </h1>
          <p className="mt-6 text-lg md:text-xl text-slate-300 max-w-3xl mx-auto">
            Procesa facturas, clasifica gastos y obtén insights financieros automáticamente
          </p>
          <div className="mt-10 flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/register"
              className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-8 py-4 rounded-xl font-semibold text-lg hover:from-indigo-700 hover:to-purple-700 transition-all duration-300 shadow-lg hover:shadow-xl"
            >
              Comenzar gratis
            </Link>
            <Link
              to="/login"
              className="bg-white/10 backdrop-blur-sm text-white px-8 py-4 rounded-xl font-semibold text-lg hover:bg-white/20 transition-all duration-300 border border-white/20"
            >
              Iniciar sesión
            </Link>
          </div>

          {/* Stats */}
          <div className="mt-16 grid grid-cols-3 gap-8 max-w-2xl mx-auto">
            <div className="text-center">
              <div className="text-3xl md:text-4xl font-bold text-indigo-400">10K+</div>
              <div className="text-sm text-slate-400 mt-1">Facturas procesadas</div>
            </div>
            <div className="text-center">
              <div className="text-3xl md:text-4xl font-bold text-purple-400">99%</div>
              <div className="text-sm text-slate-400 mt-1">Precisión OCR</div>
            </div>
            <div className="text-center">
              <div className="text-3xl md:text-4xl font-bold text-indigo-400">500+</div>
              <div className="text-sm text-slate-400 mt-1">Usuarios activos</div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-white">
              Todo lo que necesitas para gestionar tus finanzas
            </h2>
            <p className="mt-4 text-lg text-slate-300">
              Herramientas potentes impulsadas por inteligencia artificial
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature, idx) => (
              <div
                key={idx}
                className="bg-white/95 backdrop-blur-sm rounded-2xl p-6 shadow-xl border border-white/20 hover:shadow-2xl transition-all duration-300"
              >
                <div className="mb-4">{feature.icon}</div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">{feature.title}</h3>
                <p className="text-sm text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How it Works Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-purple-900/50 to-transparent">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-white">
              Cómo funciona
            </h2>
            <p className="mt-4 text-lg text-slate-300">
              Comienza en minutos, no en horas
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            {steps.map((step, idx) => (
              <div key={idx} className="relative text-center">
                {/* Connector line */}
                {idx < steps.length - 1 && (
                  <div className="hidden md:block absolute top-10 left-1/2 w-full h-0.5 bg-indigo-500/30" />
                )}

                <div className="relative">
                  <div className="w-20 h-20 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-lg">
                    {step.icon}
                  </div>
                  <div className="absolute -top-2 -right-2 w-8 h-8 bg-indigo-500 rounded-full flex items-center justify-center text-white font-bold text-sm">
                    {step.number}
                  </div>
                </div>
                <h3 className="text-xl font-semibold text-white mb-2">{step.title}</h3>
                <p className="text-slate-300 text-sm">{step.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center">
          <div className="bg-white/95 backdrop-blur-sm rounded-3xl p-10 md:p-16 shadow-2xl border border-white/20">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              ¿Listo para automatizar tus finanzas?
            </h2>
            <p className="text-lg text-gray-600 mb-8">
              Únete a cientos de usuarios que ya transformaron su gestión financiera
            </p>
            <Link
              to="/register"
              className="inline-block bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-10 py-4 rounded-xl font-semibold text-lg hover:from-indigo-700 hover:to-purple-700 transition-all duration-300 shadow-lg hover:shadow-xl"
            >
              Comenzar gratis ahora
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/10 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            <div>
              <h3 className="text-xl font-bold text-white mb-4">
                Mapgenius <span className="text-indigo-400">Solutions</span>
              </h3>
              <p className="text-sm text-slate-400">
                Automatiza tus finanzas con el poder de la inteligencia artificial.
              </p>
            </div>
            <div>
              <h4 className="text-sm font-semibold text-white mb-4">Producto</h4>
              <ul className="space-y-2">
                <li><Link to="/features" className="text-sm text-slate-400 hover:text-white transition">Funcionalidades</Link></li>
                <li><Link to="/pricing" className="text-sm text-slate-400 hover:text-white transition">Precios</Link></li>
                <li><Link to="/integrations" className="text-sm text-slate-400 hover:text-white transition">Integraciones</Link></li>
                <li><Link to="/security" className="text-sm text-slate-400 hover:text-white transition">Seguridad</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="text-sm font-semibold text-white mb-4">Empresa</h4>
              <ul className="space-y-2">
                <li><Link to="/about" className="text-sm text-slate-400 hover:text-white transition">Sobre nosotros</Link></li>
                <li><Link to="/blog" className="text-sm text-slate-400 hover:text-white transition">Blog</Link></li>
                <li><Link to="/careers" className="text-sm text-slate-400 hover:text-white transition">Carreras</Link></li>
                <li><Link to="/contact" className="text-sm text-slate-400 hover:text-white transition">Contacto</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="text-sm font-semibold text-white mb-4">Legal</h4>
              <ul className="space-y-2">
                <li><Link to="/terms" className="text-sm text-slate-400 hover:text-white transition">Términos y condiciones</Link></li>
                <li><Link to="/privacy" className="text-sm text-slate-400 hover:text-white transition">Política de privacidad</Link></li>
                <li><Link to="/cookies" className="text-sm text-slate-400 hover:text-white transition">Cookies</Link></li>
              </ul>
            </div>
          </div>
          <div className="pt-8 border-t border-white/10 text-center">
            <p className="text-sm text-slate-400">
              © 2026 Mapgenius Solutions. Todos los derechos reservados.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
