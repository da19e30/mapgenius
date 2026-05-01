export default function Blog() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-800 p-8">
      <div className="max-w-4xl mx-auto text-white">
        <h1 className="text-4xl font-extrabold mb-6">Blog</h1>
        <p className="text-slate-300 mb-8">Últimas noticias y artículos sobre finanzas e IA.</p>
        <div className="space-y-6">
          {[
            { title: 'Cómo la IA está transformando las finanzas', date: '15 abril 2026' },
            { title: 'Guía para automatizar tus facturas', date: '1 abril 2026' },
            { title: 'Tendencias en OCR para 2026', date: '20 marzo 2026' },
          ].map((post) => (
            <div key={post.title} className="bg-white/10 p-6 rounded-xl backdrop-blur-sm">
              <h3 className="text-xl font-semibold mb-2">{post.title}</h3>
              <p className="text-sm text-slate-400">{post.date}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
