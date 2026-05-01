export default function Security() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-800 p-8">
      <div className="max-w-4xl mx-auto text-white">
        <h1 className="text-4xl font-extrabold mb-6">Seguridad</h1>
        <p className="text-slate-300 mb-8">Tus datos protegidos con los más altos estándares.</p>
        <div className="space-y-6">
          {[
            { title: 'Encriptación AES-256', desc: 'Todos los datos se encriptan en tránsito y reposo.' },
            { title: 'Autenticación JWT', desc: 'Tokens seguros con expiración configurable.' },
            { title: 'Auditoría de Accesos', desc: 'Registro detallado de todas las actividades.' },
          ].map((s) => (
            <div key={s.title} className="bg-white/10 p-6 rounded-xl backdrop-blur-sm">
              <h3 className="text-xl font-semibold mb-2">🔒 {s.title}</h3>
              <p className="text-slate-400">{s.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
