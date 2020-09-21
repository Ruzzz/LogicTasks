import asyncio
import logging

from aiohttp import web

from catsauction import conf
from catsauction.models.meta import db
from catsauction.models.models import Animals, User
from catsauction.services.auction import auction_service

logger = logging.getLogger(__name__)
routes = web.RouteTableDef()

from catsauction.resources.api.v1 import users


async def set_bind(_app):
    await db.set_bind(conf.CATSAUCTION_DB_URI)

    # TODO:
    if await User.get(1) is None:
        await User.create(id=1, balance=1000)
    if await User.get(2) is None:
        await User.create(id=2, balance=1000)
    if await User.get(3) is None:
        await User.create(id=3, balance=1000)

    if await Animals.get(1) is None:
        await Animals.create(id=1, breed='egik', alias='tuman', owner_id=1)
    if await Animals.get(2) is None:
        await Animals.create(id=2, breed='kot', alias='murzik', owner_id=2)


async def app_shutdown(_app):
    for task in asyncio.Task.all_tasks():
        if task is not asyncio.tasks.Task.current_task():
            task.cancel()
            await task


def make_app():
    app = web.Application()
    app.add_routes(routes)
    app.on_startup.extend([set_bind])
    app.on_shutdown.extend([app_shutdown])
    app['auction_service'] = auction_service
    return app
