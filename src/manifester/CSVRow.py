from manifester.source_record import SourceRecord
from typing import List

class CSVRow(SourceRecord):

    row: object

    def __init__(self, row: List[str]):
        self.row = row

    @property
    def identifier(self) -> str:
        pass

    @property
    def title(self) -> str:
        pass

    @property
    def publication_year(self) -> str:
        pass