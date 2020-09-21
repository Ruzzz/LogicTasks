import logging

APP_ID = 'MBLOG'
URL_PATH_PREFIX = '/api'
COOKIE_NAME = APP_ID + '_SESSION'
SESSION_MAX_AGE = 60 * 60 * 24 * 14  # seconds
# LOG_FORMAT = '%(asctime)s | %(levelname)s | %(filename)s | %(funcName)s() | %(message)s'
LOG_FORMAT = '%(asctime)s | %(levelname)s | %(message)s'
LOG_LEVEL = logging.INFO
AUTH_FAILS_LIMIT_PERIOD = 5 * 60  # seconds
AUTH_FAILS_LIMIT_COUNT = 5  # times
AUTH_FAILS_BAN_TIME = 5 * 60  # seconds
