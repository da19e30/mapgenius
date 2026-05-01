export default function Privacy() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-800 p-8">
      <div className="max-w-4xl mx-auto text-white">
        <h1 className="text-4xl font-extrabold mb-6">Política de Privacidad</h1>
        <p className="text-slate-300 mb-8">Cómo protegemos y gestionamos tus datos personales.</p>
        <div className="bg-white/10 p-8 rounded-xl backdrop-blur-sm space-y-4 text-slate-300">
          <h2 className="text-2xl font-bold text-white">Recolección de Datos</h2>
          <p>Recopilamos información necesaria para proveer nuestros servicios, incluyendo datos de facturación y de uso.</p>
          <h2 className="text-2xl font-bold text-white mt-6">Uso de la Información</h2>
          <p>Utilizamos tus datos para procesar facturas, generar análisis y mejorar nuestros servicios.</p>
          <h2 className="text-2xl font-bold text-white mt-6">Compartir Información</h2>
          <p>No vendemos ni compartimos tus datos personales con terceros, salvo requerimiento legal.</p>
          <h2 className="text-2xl font-bold text-white mt-6">Tus Derechos</h2>
          <p>Puedes solicitar acceso, corrección o eliminación de tus datos en cualquier momento.</p>
        </div>
      </div>
    </div>
  );
}
