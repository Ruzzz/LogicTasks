import os

from ._base import *
__conf = os.environ.get('CATSAUCTION_CONF')
if __conf == 'dev':
    from ._dev import *
elif __conf == 'test':
    from ._test import *


def __init():
    import logging.config  # pylint: disable=import-outside-toplevel
    logging.config.dictConfig(CATSAUCTION_LOGGING)


__init()
