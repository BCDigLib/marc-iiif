from typing import Optional
import urllib.parse
import os.path

from manifester.errors import InsufficientSourceMetadataError
from manifester.source_record import SourceRecord


class ASpaceLookup(SourceRecord):
    _identifier: Optional[str]
    api_response: dict

    def __init__(self, api_response: dict, identifier=None):
        """
        Constructor
        """
        self._identifier = identifier
        self.api_response = api_response

    @property
    def identifier(self) -> str:
        # Did the caller specify an identifier? Use that.
        if self._identifier:
            return self._identifier

        # If an EAD location is set, it is probably a handle and the identifier should be the last
        # part.
        if 'ead_location' in self.api_response:
            ead_handle = self.api_response['ead_location']
            ead_path = urllib.parse.urlparse(ead_handle).path
            return os.path.split(ead_path)[-1]

        # Otherwise, throw an error
        raise InsufficientSourceMetadataError('Did not find an identifier for record')


    @property
    def title(self) -> str:
        return self.api_response['title']

    @property
    def publication_year(self) -> str:
        if len(self.api_response['dates']) < 0:
            raise InsufficientSourceMetadataError('Record has no associated dates')

        for date in self.api_response['dates']:
            if date['label'] == 'creation:':



        return self.api_response['']

    @property
    def citation(self) -> Optional[str]:
        """
        Return the text of the preferred citation

        :return: Optional[str]
        """
        for note in self.api_response['notes']:
            if note['type'] == 'prefercite':
                return note['subnotes'][0]['content']
        return None

    @property
    def attribution(self) -> Optional[str]:
        """
        Return the text of the usage restriction note

        :return: Optional[str] text of the usage restriction, or None if it doesn't exist
        """
        for note in self.api_response['notes']:
            if note['type'] == 'userestrict':
                return note['subnotes'][0]['content']
        return None