class LimitPreparer:

    def __init__(self, default=100, minimum=1, maximum=1000):
        self.default = default
        self.minimum = minimum
        self.maximum = maximum

    def __call__(self, value):
        if not value:
            return self.default
        try:
            ret = int(value)
        except Exception:
            return self.default
        return max(min(ret, self.maximum), self.minimum)


class TagsPreparer:

    def __call__(self, value):
        if isinstance(value, str):
            value = [value]
        return frozenset(str(x).casefold() for x in value) if value else None