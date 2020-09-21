from typing import Optional, AbstractSet

import sqlalchemy as sa

from . import _db_meta


class DbModel:

    def __init__(self, db_engine):
        self._db_engine = db_engine

    async def init_db(self, sql):
        async with self._db_engine.acquire() as conn:
            await conn.execute(sql)

    async def add_incident(self, uid, date, device_id, kind: int) -> bool:
        try:
            uid = int(uid)
        except ValueError:
            return False

        async with self._db_engine.acquire() as conn:
            query = _db_meta.incidents.insert()\
                .values(uid=uid,
                        date=date,
                        device_id=device_id,
                        kind=kind)
            try:
                await conn.execute(query)
            except Exception:
                return False
            return True

    async def remove_incidents(self, uid, device_id, kind: int) -> bool:
        try:
            uid = int(uid)
        except ValueError:
            return False

        async with self._db_engine.acquire() as conn:
            where = sa.and_(_db_meta.incidents.c.uid == uid,
                            _db_meta.incidents.c.device_id == device_id,
                            _db_meta.incidents.c.kind == kind)
            query = _db_meta.incidents.delete().where(where)
            try:
                await conn.execute(query)
            except Exception:
                return False
            return True

    async def count_incidents(self, uid, date_from, date_end, device_id, kind: int) -> int:
        try:
            uid = int(uid)
        except ValueError:
            return 0

        async with self._db_engine.acquire() as conn:
            where = sa.and_(_db_meta.incidents.c.uid == uid,
                            _db_meta.incidents.c.date >= date_from,
                            _db_meta.incidents.c.date <= date_end,
                            _db_meta.incidents.c.device_id == device_id,
                            _db_meta.incidents.c.kind == kind)
            query = _db_meta.incidents.count().where(where)
            return int(await conn.scalar(query))

    async def add_user(self, login, secret) -> bool:
        async with self._db_engine.acquire() as conn:
            query = _db_meta.users.insert()\
                .values(login=login,
                        secret=secret)
            try:
                await conn.execute(query)
            except Exception:
                return False
            return True

    async def is_admin(self, uid) -> bool:
        try:
            uid = int(uid)
        except ValueError:
            return False

        async with self._db_engine.acquire() as conn:
            query = sa.select([_db_meta.users.c.admin])\
                .where(_db_meta.users.c.id == uid)
            ret = await conn.execute(query)
            data = await ret.fetchone()
            if data is not None:
                return bool(data[0])
            else:
                return False

    async def get_secret(self, login):
        async with self._db_engine.acquire() as conn:
            query = sa.select([_db_meta.users.c.id,
                               _db_meta.users.c.secret])\
                .where(_db_meta.users.c.login == login)
            ret = await conn.execute(query)
            data = await ret.fetchone()
            if data is not None:
                return data[0], data[1]
            else:
                return None, None

    async def has_uid(self, uid) -> bool:
        try:
            uid = int(uid)
        except ValueError:
            return False

        async with self._db_engine.acquire() as conn:
            query = _db_meta.users.count()\
                .where(_db_meta.users.c.id == uid)
            return bool(await conn.scalar(query))

    async def add_post(self, uid, text: str, date,
                       tags: Optional[AbstractSet[str]] = None) -> bool:
        try:
            uid = int(uid)
        except ValueError:
            return False

        async with self._db_engine.acquire() as conn:
            async with conn.begin() as _:
                query = _db_meta.posts.insert()\
                    .values(uid=int(uid),
                            date=date,
                            text=text)
                ret = await conn.execute(query)

                if tags:
                    pid = await ret.fetchone()  # .inserted_primary_key
                    if pid:
                        pid = pid[0]
                        values = [{'tag': x, 'pid': pid} for x in tags]
                        query = _db_meta.tags.insert()\
                            .values(values)
                        await conn.execute(query)

        return True

    async def get_posts(self, uid, *, limit, item_cls,
                        filter_tags=None):
        try:
            uid = int(uid)
        except ValueError:
            return None

        async with self._db_engine.acquire() as conn:
            where = _db_meta.posts.c.uid == uid
            where = self._gen_filter_tags_where(where, filter_tags)
            query = sa.select([_db_meta.posts.c.date,
                               _db_meta.posts.c.text,
                               _db_meta.posts.c.id])\
                .where(where)\
                .order_by(_db_meta.posts.c.date)\
                .limit(limit)

            ret = await conn.execute(query)
            posts = await ret.fetchall()
            if posts is not None:
                return [item_cls(
                    date=x[0],
                    text=x[1],
                    id_=x[2],
                ) for x in posts]
        return None

    async def get_all_posts(self, *, limit, item_cls,
                            filter_tags=None):
        async with self._db_engine.acquire() as conn:
            where = _db_meta.users.c.id == _db_meta.posts.c.uid
            where = self._gen_filter_tags_where(where, filter_tags)
            query = sa.select([_db_meta.users.c.login,
                               _db_meta.posts.c.date,
                               _db_meta.posts.c.text,
                               _db_meta.posts.c.id])\
                .where(where)\
                .order_by(_db_meta.users.c.login,
                          _db_meta.posts.c.date)\
                .limit(limit)

            ret = await conn.execute(query)
            posts = await ret.fetchall()
            if posts is not None:
                return [item_cls(
                    login=x[0],
                    date=x[1],
                    text=x[2],
                    id_=x[3],
                ) for x in posts]
        return None

    async def get_tags(self, pid):
        try:
            pid = int(pid)
        except ValueError:
            return None

        async with self._db_engine.acquire() as conn:
            query = sa.select([_db_meta.tags.c.tag])\
                .where(_db_meta.tags.c.pid == pid)\
                .order_by(_db_meta.tags.c.tag)
            ret = await conn.execute(query)
            tags = await ret.fetchall()
            if tags is not None:
                return frozenset(x[0] for x in tags)
        return None

    # private

    @classmethod
    def _gen_filter_tags_where(cls, where, filter_tags):
        if filter_tags:
            tags_count = _db_meta.tags.count().where(
                sa.and_(_db_meta.posts.c.id == _db_meta.tags.c.pid,
                        _db_meta.tags.c.tag.in_(filter_tags))).as_scalar()
            where = sa.and_(where,
                            tags_count == len(filter_tags))
        return where
