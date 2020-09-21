import hashlib
from datetime import datetime, timedelta
from typing import Tuple, Optional

from ..const import *
from .. import config


class Auth:

    def __init__(self, db_model, salt):
        self._db = db_model
        self._salt = salt

    def calc_secret(self, login, password):
        secret = login + password
        if self._salt:
            secret = secret + self._salt
        return hashlib.md5(secret.encode()).hexdigest()

    async def login(self, login, password, **kwargs) -> Tuple[Optional[int], bool]:
        uid, secret = await self._db.get_secret(login)
        if (uid is not None) and (secret is not None):
            authorized = secret == self.calc_secret(login, password)
            return uid, authorized
        else:
            return None, False


class AuthLimiter:

    def __init__(self, db_model, limit_period, limit_count, ban_time):
        assert limit_count > 0
        assert limit_period > 0
        assert ban_time > 0
        self._db = db_model
        self.limit_period = limit_period
        self.limit_count = limit_count
        self.ban_time = ban_time

    async def is_banned(self, uid, device_id) -> bool:
        date_start = datetime.utcnow()
        date_end = date_start + timedelta(seconds=self.ban_time)
        count = await self._db.count_incidents(
            uid,
            date_start,
            date_end,
            device_id,
            MB_INCIDENT_BAN)
        if count > 0:
            return True

        date_end = datetime.utcnow()
        date_start = date_end - timedelta(seconds=self.limit_period)
        count = await self._db.count_incidents(
            uid,
            date_start,
            date_end,
            device_id,
            MB_INCIDENT_AUTH_FAIL)
        ret = count >= self.limit_count - 1
        if ret:
            await self.add_ban(uid, device_id)
        return ret

    async def add_fail(self, uid, device_id):
        await self._db.add_incident(
            uid,
            datetime.utcnow(),
            device_id,
            MB_INCIDENT_AUTH_FAIL)
        await self._cleanup_bans(uid, device_id)

    async def add_ban(self, uid, device_id):
        date = datetime.utcnow() + timedelta(seconds=self.ban_time)
        await self._db.add_incident(
            uid,
            date,
            device_id,
            MB_INCIDENT_BAN)
        await self._cleanup_fails(uid, device_id)

    async def unban(self, uid, device_id):
        await self._cleanup_fails(uid, device_id)
        await self._cleanup_bans(uid, device_id)

    async def _cleanup_fails(self, uid, device_id):
        await self._db.remove_incidents(
            uid,
            device_id,
            MB_INCIDENT_AUTH_FAIL)

    async def _cleanup_bans(self, uid, device_id):
        await self._db.remove_incidents(
            uid,
            device_id,
            MB_INCIDENT_BAN)


class AuthLimited(Auth):
    # Hash device_id

    def __init__(self, db_model, salt):
        super().__init__(db_model, salt)
        self._limiter = AuthLimiter(
            db_model,
            config.AUTH_FAILS_LIMIT_PERIOD,
            config.AUTH_FAILS_LIMIT_COUNT,
            config.AUTH_FAILS_BAN_TIME)

    async def login(self, login, password, **kwargs) -> Tuple[Optional[int], bool]:
        device_id = kwargs.get('device_id')
        if not device_id:
            return None, False

        uid, secret = await self._db.get_secret(login)
        if (uid is not None) and (secret is not None):
            if await self._limiter.is_banned(uid, device_id):
                return uid, False
            authorized = secret == self.calc_secret(login, password)
            if not authorized:
                await self._limiter.add_fail(uid, device_id)
            else:
                await self._limiter.unban(uid, device_id)
            return uid, authorized
        else:
            return None, False
