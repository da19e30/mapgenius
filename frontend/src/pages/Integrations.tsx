export default function Integrations() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-800 p-8">
      <div className="max-w-4xl mx-auto text-white">
        <h1 className="text-4xl font-extrabold mb-6">Integraciones</h1>
        <p className="text-slate-300 mb-8">Conecta con tus herramientas favoritas.</p>
        <div className="grid md:grid-cols-4 gap-6">
          {['QuickBooks', 'Xero', 'SAP', 'Salesforce'].map((i) => (
            <div key={i} className="bg-white/10 p-6 rounded-xl backdrop-blur-sm text-center">
              <div className="h-16 flex items-center justify-center mb-4 bg-white/5 rounded-lg">
                <span className="text-2xl">🔗</span>
              </div>
              <h3 className="font-semibold">{i}</h3>
              <p className="text-sm text-slate-400 mt-2">Próximamente</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
