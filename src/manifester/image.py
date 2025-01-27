import os.path
import requests
from typing import Optional


class Image:
    """
    An image file
    """
    info_url: str
    filename: str
    height: Optional[str]
    width: Optional[str]

    def __init__(self, filepath: str, base_url: str = 'https://iiif.bc.edu/iiif/2'):
        """
        Constructor

        :param filepath: the full path to the file on the local machine (e.g. /Volumes/Digital-Library/current-projects/Mirador-workflow/bc-2023-159/jp2/bc2023-159_0019.jp2)
        :param base_url: str base URL for the IIIF server
        """
        # Get the full filename (e.g. 'bc-2022-172_0042.jp2')
        self.filename = os.path.split(filepath)[1]

        # The image identifier, with no extension (e.g. 'bc-2022-172_0042')
        self.short_name = self.filename[0:self.filename.index('.')]

        # The sequence counter (e.g. '0042')
        self.counter = self.short_name[len(self.short_name) - 4:len(self.short_name)]

        # The image identifier minus the counter (e.g. 'bc-2022-172')
        self.cui = self.short_name[0:len(self.short_name) - 5]

        # The IIIF info URL
        self.info_url = f'{base_url}/{self.filename}/info.json'

        # Dimensions will be filled after image lookup
        self.height = None
        self.width = None

    def lookup(self) -> None:
        """
        Lookup the image info on the IIIF server

        We can use the image's info.json on the IIIF server to get dimensions.
        """
        call = requests.get(self.info_url)
        info = call.json()
        self.height = info['height']
        self.width = info['width']
