class InsufficientSourceMetadataError(Exception):
    def __init__(self, msg='Not enough metadata to build SourceRecord'):
        self.msg = msg
        super().__init__(self.msg)
