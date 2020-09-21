import hashlib
import logging
import sys
from typing import Union

import rapidjson


def create_logger(name: str, fmt: str, level):
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(fmt))
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger


def init_logger(logger, fmt: str, level):
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(fmt))
    logger.addHandler(handler)
    logger.setLevel(level)


def init_async_loop():
    import asyncio
    if sys.platform != 'win32':
        try:
            import uvloop
            asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        except ImportError:
            pass


def digest_str(data: str) -> str:
    return hashlib.md5(data.encode()).hexdigest()


def digest_data(data: Union[dict, tuple, list]) -> str:
    return hashlib.md5(rapidjson.dumps(data).encode()).hexdigest()


def date_as_rfc3339(date):
    return date.strftime('%Y-%m-%dT%H:%M:%SZ')
