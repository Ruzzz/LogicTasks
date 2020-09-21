import os

CATSAUCTION_DEVELOPMENT = False
CATSAUCTION_TESTING = False
CATSAUCTION_DB_URI = os.environ.get(
    'CATSAUCTION_DB_URI',
    'postgresql://catsauction:catsauction@localhost:5432/catsauction'
)

CATSAUCTION_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'WARNING',
        'handlers': ['console']
    },
    'formatters': {
        'simple': {
            'format': '%(asctime)s | %(name)s | %(levelname)s | %(message)s'
        },
        'verbose': {
            'format': '%(asctime)s | %(process)d | %(name)s | %(levelname)s | '
                      '%(filename)s:%(lineno)d | %(funcName)s() | %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'catsauction': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'INFO',
        }
    }
}
