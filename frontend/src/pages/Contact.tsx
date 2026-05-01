import { useState } from 'react';

export default function Contact() {
  const [form, setForm] = useState({ name: '', email: '', message: '' });
  const [sent, setSent] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSent(true);
    setTimeout(() => setSent(false), 3000);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-800 p-8">
      <div className="max-w-2xl mx-auto text-white">
        <h1 className="text-4xl font-extrabold mb-6">Contacto</h1>
        <p className="text-slate-300 mb-8">¿Tienes preguntas? Escríbenos y te responderemos pronto.</p>
        <form onSubmit={handleSubmit} className="bg-white/10 p-8 rounded-xl backdrop-blur-sm space-y-4">
          <div>
            <label className="block text-sm mb-1">Nombre</label>
            <input
              type="text"
              required
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
              className="w-full p-2 rounded bg-white/5 border border-white/20 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              placeholder="Tu nombre"
            />
          </div>
          <div>
            <label className="block text-sm mb-1">Email</label>
            <input
              type="email"
              required
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
              className="w-full p-2 rounded bg-white/5 border border-white/20 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              placeholder="tu@email.com"
            />
          </div>
          <div>
            <label className="block text-sm mb-1">Mensaje</label>
            <textarea
              required
              rows={4}
              value={form.message}
              onChange={(e) => setForm({ ...form, message: e.target.value })}
              className="w-full p-2 rounded bg-white/5 border border-white/20 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              placeholder="Tu mensaje..."
            />
          </div>
          <button
            type="submit"
            className="w-full bg-indigo-600 text-white py-2 rounded hover:bg-indigo-700 transition"
          >
            {sent ? '¡Mensaje enviado!' : 'Enviar Mensaje'}
          </button>
        </form>
      </div>
    </div>
  );
}
