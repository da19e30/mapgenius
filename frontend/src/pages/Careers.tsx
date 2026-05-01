export default function Careers() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-800 p-8">
      <div className="max-w-4xl mx-auto text-white">
        <h1 className="text-4xl font-extrabold mb-6">Carreras</h1>
        <p className="text-slate-300 mb-8">Únete a nuestro equipo y ayuda a transformar las finanzas.</p>
        <div className="bg-white/10 p-8 rounded-xl backdrop-blur-sm">
          <h2 className="text-2xl font-bold mb-4">Posiciones Abiertas</h2>
          <p className="text-slate-300 mb-4">Actualmente no tenemos vacantes abiertas, pero puedes enviar tu CV para futuras oportunidades.</p>
          <button className="bg-indigo-600 text-white px-6 py-2 rounded hover:bg-indigo-700 transition">
            Enviar CV
          </button>
        </div>
      </div>
    </div>
  );
}
