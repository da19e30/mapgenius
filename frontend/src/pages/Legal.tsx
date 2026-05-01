export default function Legal() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-800 p-8">
      <div className="max-w-4xl mx-auto text-white">
        <h1 className="text-4xl font-extrabold mb-6">Legal</h1>
        <p className="text-slate-300 mb-8">Información legal y avisos.</p>
        <div className="bg-white/10 p-8 rounded-xl backdrop-blur-sm space-y-4">
          <h2 className="text-2xl font-bold">Aviso Legal</h2>
          <p className="text-slate-300">Mapgenius Solutions es una marca registrada. Todos los derechos reservados.</p>
          <h2 className="text-2xl font-bold mt-6">Propiedad Intelectual</h2>
          <p className="text-slate-300">El contenido de este sitio está protegido por leyes de propiedad intelectual.</p>
        </div>
      </div>
    </div>
  );
}
