'''Alembic environment configuration for Mapgenius Solutions.

This file sets up the migration context, loading the SQLAlchemy URL from
environment variables securely. It also configures the target metadata from
the application models and enables "offline" and "online" migration modes.
'''

import os
import sys
from logging.config import fileConfig

from alembic import context

# Add the parent directory of the project to sys.path so that the
# application modules can be imported.
_project_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.append(_project_root)

# Import the MetaData object from the application. It is assumed that the
# SQLAlchemy models live in ``backend.app.models`` and expose ``Base.metadata``.
try:
    from backend.app.models import Base  # Adjust the import path as needed
except Exception as exc:
    raise RuntimeError("Unable to import Base metadata for Alembic migrations") from exc

# this is the Alembic Config object, which provides access to the values
# within the ``alembic.ini`` file.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically the same as ``logging.config.fileConfig``.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ---------------------------------------------------------------------------
# Database URL handling
# ---------------------------------------------------------------------------
# The database URL is not stored in ``alembic.ini`` for security reasons.
# It should be supplied via the environment variable ``DATABASE_URL``.
# Example:
#   export DATABASE_URL="postgresql+psycopg2://user:password@db-host:5432/mapgenius"
#
# Alembic will raise a clear error if the variable is missing.
# ---------------------------------------------------------------------------

def get_url() -> str:
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError(
            "DATABASE_URL environment variable is not set. "
            "Set it before running alembic commands."
        )
    return url

# ---------------------------------------------------------------------------
# Run migrations in "offline" mode.
# ---------------------------------------------------------------------------
def run_migrations_offline():
    """Run migrations in 'offline' mode.

    In this mode Alembic generates the SQL statements as strings without
    connecting to the database. This is useful for CI pipelines where a DB
    connection is not available.
    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=Base.metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

# ---------------------------------------------------------------------------
# Run migrations in "online" mode.
# ---------------------------------------------------------------------------
def run_migrations_online():
    """Run migrations in 'online' mode.

    Here we create an Engine and a connection, then pass the connection to
    Alembic's MigrationContext. This is the typical path used by developers.
    """
    from sqlalchemy import engine_from_config, pool

    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = get_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=Base.metadata,
            compare_type=True,  # Detect column type changes
            compare_server_default=True,
        )
        with context.begin_transaction():
            context.run_migrations()

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
