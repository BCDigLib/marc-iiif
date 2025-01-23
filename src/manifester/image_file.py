import os

class ImageFile:

    def __init__(self, full_path: str):
        parts = os.path.split(full_path)
        self.dir = parts[0]
        self.filename = parts[1]
        self.full_path = full_path