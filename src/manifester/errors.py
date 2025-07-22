class InsufficientSourceMetadataError(Exception):
    def __init__(self, msg='Not enough metadata to build SourceRecord'):
        self.msg = msg
        super().__init__(self.msg)


class BadImageInfoURLError(Exception):
    def __init__(self, msg='404 when looking up image info.json file'):
        self.msg = msg
        super().__init__(self.msg)
