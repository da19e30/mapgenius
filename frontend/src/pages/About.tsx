export default function About() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-800 p-8">
      <div className="max-w-4xl mx-auto text-white">
        <h1 className="text-4xl font-extrabold mb-6">Sobre Nosotros</h1>
        <p className="text-slate-300 mb-8">Historia y valores de Mapgenius Solutions.</p>
        <div className="bg-white/10 p-8 rounded-xl backdrop-blur-sm">
          <p className="text-slate-300 mb-4">Mapgenius nació en 2023 con la visión de democratizar el acceso a herramientas financieras avanzadas.</p>
          <p className="text-slate-300">Nuestro equipo combina experiencia en finanzas e inteligencia artificial para ofrecer soluciones innovadoras.</p>
        </div>
      </div>
    </div>
  );
}
