import asyncio
import logging

from aiohttp import web
from aiohttp.web_runner import GracefulExit

from catsauction import conf
from catsauction.app import make_app

_logger = logging.getLogger('catsauction.app')


class TCPAppRunner:
    runner: web.AppRunner

    def __init__(self, app, port, host='0'):
        self.app = app
        self.port = port
        self.host = host

    async def setup(self):
        self.runner = web.AppRunner(self.app, handle_signals=True)
        await self.runner.setup()

    async def start(self):
        site = web.TCPSite(self.runner, self.host, self.port)
        await site.start()

    async def end(self):
        await self.app.shutdown()
        await self.app.cleanup()


def serve():
    loop = asyncio.get_event_loop()
    app_runner = TCPAppRunner(make_app(), port=8080)

    _logger.info('starting')
    loop.run_until_complete(app_runner.setup())
    loop.create_task(app_runner.start())
    try:
        loop.run_forever()
    except (KeyboardInterrupt, GracefulExit):
        pass
    except Exception as err:
        _logger.critical(str(err))
    finally:
        _logger.info('shutting down')
        loop.run_until_complete(app_runner.end())

    loop.close()


if __name__ == '__main__':
    serve()
