from aiohttp_security.abc import AbstractAuthorizationPolicy

from ..const import *


class AuthPolicy(AbstractAuthorizationPolicy):

    def __init__(self, model):
        self._model = model

    async def authorized_userid(self, identity):
        return identity if await self._model.has_user_id(identity) else None

    async def permits(self, identity, permission, context=None):
        if permission == MB_ROLE_USER:
            return await self._model.has_user_id(identity)
        elif permission == MB_ROLE_ADMIN:
            return await self._model.is_admin(identity)
        else:
            return False
