import { Link } from 'react-router-dom';

export default function Footer({ isAuthenticated = false }: { isAuthenticated?: boolean }) {
  return (
    <footer className="bg-white border-t border-gray-200 py-6 px-4">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-4">
        <p className="text-sm text-gray-500">
          © 2026 Mapgenius Solutions. Todos los derechos reservados.
        </p>
        <div className="flex space-x-4 text-sm">
          <Link to="/terms" className="text-gray-500 hover:text-indigo-600 transition">
            Términos y condiciones
          </Link>
          <Link to="/privacy" className="text-gray-500 hover:text-indigo-600 transition">
            Política de privacidad
          </Link>
          <Link to="/cookies" className="text-gray-500 hover:text-indigo-600 transition">
            Cookies
          </Link>
          {!isAuthenticated && (
            <>
              <Link to="/contact" className="text-gray-500 hover:text-indigo-600 transition">
                Contacto
              </Link>
              <Link to="/about" className="text-gray-500 hover:text-indigo-600 transition">
                Sobre nosotros
              </Link>
            </>
          )}
        </div>
      </div>
    </footer>
  );
}
