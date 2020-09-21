import rapidjson
from aiohttp import web
from aiohttp_security import (
    check_authorized,
    check_permission,
    forget,
    remember,
    authorized_userid)

from ..const import *
from .. import config


# Helpers


def _json_response(data, **kwargs):
    return web.json_response(data, dumps=rapidjson.dumps, **kwargs)


async def _json_request(request) -> dict:
    if request.content_type != 'application/json':
        raise web.HTTPBadRequest()
    try:
        content = await request.text()
        return rapidjson.loads(content)
    except Exception:
        raise web.HTTPBadRequest()


# Routers


async def login(request):
    uid = await authorized_userid(request)
    if uid is not None:
        raise web.HTTPOk(body='Already authorized')

    data = await _json_request(request)
    try:
        user = data['login']
        password = data['password']
    except KeyError:
        raise web.HTTPBadRequest(body='Specify login and password')

    mblog = request.config_dict['mblog']
    device_id = request.remote + request.headers['User-Agent']
    uid, authorized = await mblog.login(user, password, device_id=device_id)
    if (uid is not None) and authorized:
        await remember(request, None, str(uid))
        raise web.HTTPOk()
    else:
        raise web.HTTPUnauthorized(body='Invalid login or password, or user is disabled')


async def logout(request):
    await check_authorized(request)
    await forget(request, None)
    raise web.HTTPOk(body='You have been logged out')


async def users_add(request):
    await check_permission(request, MB_ROLE_ADMIN)
    data = await _json_request(request)
    try:
        user = data['login']
        password = data['password']
    except KeyError:
        raise web.HTTPBadRequest()

    mblog = request.config_dict['mblog']
    if await mblog.add_user(user, password):
        raise web.HTTPOk()
    else:
        raise web.HTTPInternalServerError()


async def posts_add(request):
    uid = await check_authorized(request)
    data = await _json_request(request)
    try:
        text = data['text']
        tags = data.get('tags')
    except KeyError:
        raise web.HTTPBadRequest()

    mblog = request.config_dict['mblog']
    if await mblog.add_post(uid, text, tags=tags):
        raise web.HTTPOk()
    else:
        raise web.HTTPInternalServerError()


async def posts_my(request):
    uid = await check_authorized(request)
    params = request.rel_url.query
    limit = params.get('limit')
    filter_tags = params.getall('tags', None)
    mblog = request.config_dict['mblog']
    posts = await mblog.get_posts(uid,
                                  limit=limit,
                                  filter_tags=filter_tags)
    posts = [x.to_json() for x in posts] if posts else []
    return _json_response(posts)


async def posts_all(request):
    params = request.rel_url.query
    limit = params.get('limit')
    filter_tags = params.getall('tags', None)
    mblog = request.config_dict['mblog']
    posts = await mblog.get_all_posts(limit=limit,
                                      filter_tags=filter_tags)
    posts = [x.to_json() for x in posts] if posts else []
    return _json_response(posts)


def setup(app):
    app.add_routes([
        web.post(config.URL_PATH_PREFIX + '/login', login, name='login'),
        web.post(config.URL_PATH_PREFIX + '/logout', logout, name='logout'),
        web.post(config.URL_PATH_PREFIX + '/users/add', users_add, name='users_add'),
        web.post(config.URL_PATH_PREFIX + '/posts/add', posts_add, name='posts_add'),
        web.get(config.URL_PATH_PREFIX + '/posts/my', posts_my, name='posts_my'),
        web.get(config.URL_PATH_PREFIX + '/posts/all', posts_all, name='posts_all'),
    ])
