from typing import Set, Any

from mblog.utils import date_as_rfc3339


class PostVO:
    __slots__ = 'id', 'uid', 'login', 'date', 'text', 'tags'

    def __init__(self, id_: Any = None,
                 uid: Any = None,
                 login: str = None,
                 date: Any = None,
                 text: str = None,
                 tags: Set[str] = None):
        self.id = id_
        self.uid = uid
        self.login = login
        self.date = date
        self.text = text
        self.tags = tags

    def to_json(self) -> dict:
        ret = {}
        if self.login:
            ret['user'] = self.login
        if self.date:
            ret['date'] = date_as_rfc3339(self.date)
        if self.text:
            ret['text'] = self.text
        if self.tags:
            ret['tags'] = sorted(self.tags)
        return ret
