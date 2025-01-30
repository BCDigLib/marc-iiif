import os.path

import requests
from typing import Optional


class Image:
    """
    An image file

    Attributes:
        short_name (str): e.g. 'bc-2022-172_0042'
        info_url (str): e.g. 'https://iiif.bc.edu/iiif/2/bc-2022-172_0042.jp2/info.json'
    """
    annotation_url: str
    short_name: str
    info_url: str
    filename: str
    height: Optional[str]
    width: Optional[str]

    def __init__(self, filepath: str, base_url: str = 'https://iiif.bc.edu/iiif/2'):
        """
        Constructor

        :param filepath: the full path to the file on the local machine (e.g. /opt/cantaloupe/images/bc2023-159_0019.jp2)
        :param base_url: str base URL for the IIIF server
        :param lookup: bool should we look up the image dimensions?
        """
        # Get the full filename (e.g. 'bc-2022-172_0042.jp2')
        self.filename = os.path.split(filepath)[1]

        # The image identifier, with no extension (e.g. 'bc-2022-172_0042')
        self.short_name = self.filename[0:self.filename.index('.')]

        # The sequence counter (e.g. '0042')
        self.counter = self.short_name[len(self.short_name) - 4:len(self.short_name)]

        # The image identifier minus the counter (e.g. 'bc-2022-172')
        self.cui = self.short_name[0:len(self.short_name) - 5]

        # The base IIIF URL for the image (e.g. 'https://iiif.bc.edu/iiif/2/bc-2022-172_0042.jp2')
        self.image_url = f'{base_url}/{self.filename}'

        # The IIIF info URL (e.g. 'https://iiif.bc.edu/iiif/2/bc-2022-172_0042.jp2/info.json')
        self.info_url = f'{self.image_url}/info.json'

        # IIIF thumbnail URL (e.g. 'https://iiif.bc.edu/iiif/2/bc-2022-172_0042.jp2/full/!200,200/0/default.jpg')
        self.thumbnail_url = f'{self.image_url}/full/!200,200/0/default.jpg'

        self.annotation_url = f'https://iiif.bc.edu/iiif/2/{self.cui}/{self.counter}/annotation/1'

        self.canvas_url = f'https://iiif.bc.edu/iiif/2/{self.cui}/canvas/{self.counter}'

        counter_index = int(self.counter) - 1
        self.range_url = f'https://iiif.bc.edu/iiif/2/{self.cui}/range/r-{str(counter_index)}'

        self.height = None
        self.width = None
