export default function Cookies() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-800 p-8">
      <div className="max-w-4xl mx-auto text-white">
        <h1 className="text-4xl font-extrabold mb-6">Política de Cookies</h1>
        <p className="text-slate-300 mb-8">Información sobre el uso de cookies en nuestro sitio.</p>
        <div className="bg-white/10 p-8 rounded-xl backdrop-blur-sm space-y-4 text-slate-300">
          <h2 className="text-2xl font-bold text-white">Qué son las Cookies</h2>
          <p>Las cookies son pequeños archivos de texto que se almacenan en tu dispositivo para mejorar tu experiencia.</p>
          <h2 className="text-2xl font-bold text-white mt-6">Tipos de Cookies</h2>
          <p>Utilizamos cookies esenciales, de rendimiento y funcionales para operar el servicio.</p>
          <h2 className="text-2xl font-bold text-white mt-6">Control de Cookies</h2>
          <p>Puedes configurar tu navegador para rechazar cookies, aunque esto puede afectar la funcionalidad.</p>
        </div>
      </div>
    </div>
  );
}
