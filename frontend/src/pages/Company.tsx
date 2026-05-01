export default function Company() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-800 p-8">
      <div className="max-w-4xl mx-auto text-white">
        <h1 className="text-4xl font-extrabold mb-6">Empresa</h1>
        <p className="text-slate-300 mb-8">Conoce al equipo detrás de Mapgenius Solutions.</p>
        <div className="bg-white/10 p-8 rounded-xl backdrop-blur-sm">
          <h2 className="text-2xl font-bold mb-4">Nuestra Misión</h2>
          <p className="text-slate-300 mb-6">Transformar la gestión financiera mediante inteligencia artificial accesible para todos.</p>
          <h2 className="text-2xl font-bold mb-4">Visión</h2>
          <p className="text-slate-300">Ser la plataforma líder en automatización financiera para PyMEs en Latinoamérica.</p>
        </div>
      </div>
    </div>
  );
}
