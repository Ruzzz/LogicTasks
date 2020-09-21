from alembic import context
from logging.config import fileConfig

from sqlalchemy import create_engine

import catsauction.models.models

from catsauction import conf
from catsauction.models.meta import db

config = context.config
target_metadata = db
fileConfig(config.config_file_name)


def run_migrations():
    with create_engine(conf.CATSAUCTION_DB_URI).connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_server_default=True,
        )
        with context.begin_transaction():
            context.run_migrations()


run_migrations()
