export default function Pricing() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-800 p-8">
      <div className="max-w-4xl mx-auto text-white">
        <h1 className="text-4xl font-extrabold mb-6">Precios</h1>
        <p className="text-slate-300 mb-8">Planes diseñados para cada necesidad.</p>
        <div className="grid md:grid-cols-3 gap-6">
          {[
            { plan: 'Básico', price: 'Gratis', features: ['5 facturas/mes', 'OCR limitado', 'Soporte por email'] },
            { plan: 'Pro', price: '$19/mes', features: ['100 facturas/mes', 'OCR completo', 'Clasificación IA', 'Soporte prioritario'] },
            { plan: 'Enterprise', price: 'Contacto', features: ['Facturas ilimitadas', 'Modelos IA personalizados', 'API dedicada', 'Soporte 24/7'] },
          ].map((p) => (
            <div key={p.plan} className="bg-white/10 p-6 rounded-xl backdrop-blur-sm border border-white/20">
              <h3 className="text-2xl font-bold mb-2">{p.plan}</h3>
              <p className="text-3xl font-extrabold text-indigo-400 mb-4">{p.price}</p>
              <ul className="space-y-2 text-slate-300">
                {p.features.map((f) => <li key={f}>✓ {f}</li>)}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
