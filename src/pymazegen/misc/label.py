class Label:
    class Break(Exception):
        def __init__(self, ctx):
            self.ctx = ctx

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        return isinstance(exc_value, self.Break) and exc_value.ctx is self

    def break_(self):
        raise self.Break(self)

    