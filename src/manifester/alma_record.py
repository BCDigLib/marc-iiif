from pymarc import Record

from manifester.citation import burns_citation, law_citation
from manifester.source_record import SourceRecord


class AlmaRecord(SourceRecord):
    """
    A bibliographic record from Alma

    Built off of a MARC record, but uses some Alma-specific features (e.g. MMS id).
    """
    record: Record

    def __init__(self, record: Record):
        """
        Constructor

        :type record: Record the MARC record exported from Alma
        :param record:
        """
        self.record = record

    @property
    def identifier(self) -> str:
        """
        Get identifier (MMS)

        When dealing with our MARC records, we usually use Alma's MMS as the identifier. That ID is found at the
        beginning of the

        :return: str
        """
        long_identifier = str(record['001'])
        return long_identifier[6:len(long_identifier)]

    @property
    def title(self) -> str:
        """
        Get title

        :return: str
        """
        return str(self.record.title)

    @property
    def publication_year(self) -> str:
        """
        Publication year

        :return: str
        """
        return str(self.record.pubyear or "")

    @property
    def citation(self) -> str:
        """
        Citation for this item

        :return: str a formatted citation
        """

        # No 510 (source location)? It's at Burns.
        if self.record['510'] is None or self.record['510']['a'] is None:
            return burns_citation(self.title, self.publication_year, self.identifier)

        # 510 doesn't say it's at Law? It's at Burns
        if 'BCLL RBR' not in self.record['510']['a']:
            return burns_citation(self.title, self.publication_year, self.identifier)

        # If it's at Law and doesn't have a sublocation, just return the room it's in.
        room = str(self.record['510']['a'])
        if self.record['510']['c'] is None:
            return law_citation(self.title, self.publication_year, self.room, self.identifier)

        # If it does have a location, add that to the citation.
        location = self.record['510']['c']
        return law_citation(self.title, self.publication_year, f'{room} {location}', self.identifier)