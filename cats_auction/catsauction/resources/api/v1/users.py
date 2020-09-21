import logging
from json import JSONDecodeError

from aiohttp import web
from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError

# TODO: process asyncpg.exceptions in service

from catsauction.app import routes

logger = logging.getLogger(__name__)

# TODO: Get user_id from auth data
#       And re-organize rest paths


@routes.post(r'/v1/user/{user_id:\d+}/add-lot')
async def post_add_lot(request):
    user_id = int(request.match_info['user_id'])
    try:
        params = await request.json()
    except JSONDecodeError as err:
        logging.error(str(err))
        raise web.HTTPBadRequest()

    try:
        lot_id = await request.app['auction_service'].add_lot(
            params['price'],
            params['animal_id'],
            user_id
        )
    except (ValueError, ForeignKeyViolationError, UniqueViolationError) as err:
        logging.error(str(err))
        raise web.HTTPBadRequest()
    return web.json_response({'lot_id': lot_id})


@routes.post(r'/v1/user/{user_id:\d+}/add-bet')
async def post_add_bet(request):
    user_id = int(request.match_info['user_id'])
    try:
        params = await request.json()
    except JSONDecodeError as err:
        logging.error(str(err))
        raise web.HTTPBadRequest()

    try:
        bet_id = await request.app['auction_service'].add_bet(
            params['value'],
            params['lot_id'],
            user_id
        )
    except (ValueError, ForeignKeyViolationError, UniqueViolationError) as err:
        logging.error(str(err))
        raise web.HTTPBadRequest()
    return web.json_response({'bet_id': bet_id})


@routes.post(r'/v1/user/{user_id:\d+}/takes-bet')
async def post_takes_bet(request):
    user_id = int(request.match_info['user_id'])
    try:
        params = await request.json()
    except JSONDecodeError as err:
        logging.error(str(err))
        raise web.HTTPBadRequest()

    try:
        await request.app['auction_service'].takes_bet(
            params['bet_id'],
            user_id
        )
    except (ValueError, ForeignKeyViolationError, UniqueViolationError) as err:
        logging.error(str(err))
        raise web.HTTPBadRequest()
    return web.json_response({'result': 'ok'})
