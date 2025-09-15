import os
import sys

from sqlalchemy import engine_from_config, pool

from alembic import context
from app.core.config import settings
from app.core.database import Base
from app.organisation import models as organisation_models  # noqa: F401
from app.users import models as user_models  # noqa: F401
from app.voting import models as voting_models  # noqa: F401



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# Alembic config
config = context.config
target_metadata = Base.metadata


config.set_main_option("sqlalchemy.url", settings.ASYNC_DATABASE_URL.replace("+asyncpg", ""))


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            render_as_batch=True,
        )

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
