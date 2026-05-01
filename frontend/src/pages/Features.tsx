export default function Features() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-800 p-8">
      <div className="max-w-4xl mx-auto text-white">
        <h1 className="text-4xl font-extrabold mb-6">Funcionalidades</h1>
        <p className="text-slate-300 mb-8">Herramientas potenciadas por IA para la gestión financiera.</p>
        <div className="space-y-6">
          {[
            { title: 'OCR de Facturas', desc: 'Extracción automática de datos de PDF, JPG y PNG.' },
            { title: 'Clasificación Automática', desc: 'Categorización inteligente de gastos e ingresos.' },
            { title: 'Predicción de Flujo', desc: 'Proyecciones financieras basadas en datos históricos.' },
            { title: 'Exportación de Datos', desc: 'Descarga tus datos en formato CSV con un clic.' },
          ].map((f) => (
            <div key={f.title} className="bg-white/10 p-6 rounded-xl backdrop-blur-sm">
              <h3 className="text-xl font-semibold mb-2">{f.title}</h3>
              <p className="text-slate-400">{f.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
