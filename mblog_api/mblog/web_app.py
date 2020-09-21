import hashlib
import os

import aiopg.sa
import rapidjson
from aiohttp import web
from aiohttp.log import access_logger
from aiohttp_security import setup as setup_security, SessionIdentityPolicy
from aiohttp_session import setup as setup_session
from aiohttp_session.log import log as sessions_log
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from . import config
from .utils import init_async_loop, create_logger, init_logger
from .core.blog_model import BlogModel
from .web.auth_policy import AuthPolicy
from .web.routes import setup as setup_routes


_logger = create_logger(config.APP_ID, config.LOG_FORMAT, config.LOG_LEVEL)


async def _init_app(app):
    options = app['lazy_options']
    try:
        db_engine = await aiopg.sa.create_engine(**options['db_credentials'])
    except Exception as err:  # TODO: psycopg2.OperationalError
        _logger.critical('DB connection error: %s', str(err))
        raise SystemExit(1)

    mblog = BlogModel(db_engine, options['salt'])
    init_sql = options.get('init_sql')
    if init_sql:
        await mblog.init_db(init_sql)
    app['mblog'] = mblog
    app['lazy_options'] = None

    setup_security(app, SessionIdentityPolicy(), AuthPolicy(mblog))


async def _cleanup_app(app):
    app['db'].close()
    await app['db'].wait_closed()


def start_web_app(host, port,
                  db_host, db_port, db, db_user, db_password,
                  secret=None,
                  init_sql=None):
    _logger.info('starting..')
    _logger.info('config: host = %s', host)
    _logger.info('config: host = %d', port)
    _logger.info('config: db_host = %s', db_host)
    _logger.info('config: db_port = %d', db_port)
    _logger.info('config: db = %s', db)
    _logger.info('config: db_user = %s', db_user)

    # log
    init_async_loop()
    access_logger.setLevel(config.LOG_LEVEL)
    init_logger(sessions_log, config.LOG_FORMAT, config.LOG_LEVEL)

    # app
    app = web.Application()

    # sessions
    if not secret:
        session_secret = os.urandom(32)
    else:
        session_secret = hashlib.sha256(bytes('session_' + secret, 'utf-8')).digest()
    storage = EncryptedCookieStorage(session_secret,
                                     max_age=config.SESSION_MAX_AGE,
                                     cookie_name=config.COOKIE_NAME,
                                     encoder=rapidjson.dumps,
                                     decoder=rapidjson.loads)
    setup_session(app, storage)

    # routes
    setup_routes(app)

    # db
    app['lazy_options'] = {
        'db_credentials': {
            'host': db_host,
            'port': db_port,
            'database': db,
            'user': db_user,
            'password': db_password,
        },
        'salt': secret,
        'init_sql': init_sql
    }
    app.on_startup.append(_init_app)
    app.on_cleanup.append(_cleanup_app)

    web.run_app(app, host=host, port=port, access_log=access_logger)
