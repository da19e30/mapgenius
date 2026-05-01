export default function Terms() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-800 p-8">
      <div className="max-w-4xl mx-auto text-white">
        <h1 className="text-4xl font-extrabold mb-6">Términos y Condiciones</h1>
        <p className="text-slate-300 mb-8">Por favor, lee detenidamente nuestros términos de servicio.</p>
        <div className="bg-white/10 p-8 rounded-xl backdrop-blur-sm space-y-4 text-slate-300">
          <h2 className="text-2xl font-bold text-white">1. Uso del Servicio</h2>
          <p>Al utilizar Mapgenius Solutions, aceptas cumplir con estos términos y condiciones.</p>
          <h2 className="text-2xl font-bold text-white mt-6">2. Propriedad Intelectual</h2>
          <p>Todos los derechos sobre el software y contenido pertenecen a Mapgenius Solutions.</p>
          <h2 className="text-2xl font-bold text-white mt-6">3. Limitación de Responsabilidad</h2>
          <p>Mapgenius no será responsable por daños indirectos derivados del uso del servicio.</p>
          <h2 className="text-2xl font-bold text-white mt-6">4. Modificaciones</h2>
          <p>Nos reservamos el derecho de modificar estos términos en cualquier momento.</p>
        </div>
      </div>
    </div>
  );
}
