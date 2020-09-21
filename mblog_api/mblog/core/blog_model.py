from datetime import datetime
from typing import Optional, Iterable

from ._db_model import DbModel
from ._auth import AuthLimited
from .verifiers import LimitPreparer, TagsPreparer
from ..vo import PostVO


class BlogModel:

    def __init__(self, db_engine, salt):
        db = DbModel(db_engine)
        self._db = db
        self._auth = AuthLimited(db, salt)
        self._norm_limit = LimitPreparer()
        self._norm_tags = TagsPreparer()

    async def init_db(self, sql):
        await self._db.init_db(sql)

    async def login(self, *args, **kwargs):
        return await self._auth.login(*args, **kwargs)

    async def add_user(self, login, password) -> bool:
        secret = self._auth.calc_secret(login, password)
        return await self._db.add_user(login, secret)

    async def is_admin(self, uid) -> bool:
        return await self._db.is_admin(uid)

    async def has_user_id(self, uid) -> bool:
        return await self._db.has_uid(uid)

    async def add_post(self, uid, text: str, date=None,
                       tags: Optional[Iterable[str]] = None) -> bool:
        return await self._db.add_post(uid, text,
                                       date or datetime.utcnow(),
                                       self._norm_tags(tags))

    async def get_posts(self, uid, *,
                        limit=None,
                        filter_tags=None) -> Optional[Iterable[PostVO]]:
        posts = await self._db.get_posts(uid,
                                         limit=self._norm_limit(limit),
                                         item_cls=PostVO,
                                         filter_tags=self._norm_tags(filter_tags))
        # get tags
        if posts:
            for x in posts:
                x.tags = await self._db.get_tags(x.id)
        return posts

    async def get_all_posts(self, *,
                            limit=None,
                            filter_tags=None) -> Optional[Iterable[PostVO]]:
        posts = await self._db.get_all_posts(limit=self._norm_limit(limit),
                                             item_cls=PostVO,
                                             filter_tags=self._norm_tags(filter_tags))
        # get tags
        if posts:
            for x in posts:
                x.tags = await self._db.get_tags(x.id)
        return posts
