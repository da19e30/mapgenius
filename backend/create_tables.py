"""
Script para crear todas las tablas del proyecto Mapgenius Solutions en la base de datos.

Ejecuta este archivo una sola vez (o cada vez que añadas nuevos modelos) con:
    python create_tables.py

El script:
1. Carga la configuración del ``.env`` (DATABASE_URL, etc.).
2. Importa *todos* los modelos para que SQLAlchemy los registre.
3. Llama a ``Base.metadata.create_all`` para crear las tablas si no existen.

Está pensado para usarse con PostgreSQL o con SQL Server (mssql+pyodbc).
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env (ubicado en la raíz del proyecto)
load_dotenv(dotenv_path=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env")))

# Importar la configuración de la base de datos (engine, Base, init_db)
from app.database import engine, Base, init_db

# Importar explícitamente todos los modelos del proyecto para que SQLAlchemy los registre.
# Si añades nuevos modelos, simplemente añádelos aquí.
from app.models.user import User  # noqa: F401
from app.models.invoice import Invoice  # noqa: F401
from app.models.financial_data import FinancialData  # noqa: F401

def main() -> None:
    """Crea las tablas en la base de datos configurada.

    Si la base de datos ya contiene las tablas, la llamada es idempotente y no hará nada.
    """
    try:
        # init_db ya llama a ``Base.metadata.create_all``
        init_db()
        print("✅  Todas las tablas fueron creadas (o ya existían) en la base de datos.")
    except Exception as exc:
        print("❌  Error al crear las tablas:")
        print(exc)

if __name__ == "__main__":
    main()
