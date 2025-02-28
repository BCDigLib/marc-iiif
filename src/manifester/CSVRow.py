from manifester.source_record import SourceRecord
from typing import List, Optional


class CSVRow(SourceRecord):

    row: list[str]

    def __init__(self, row: List[str]):
        self.row = row

    @property
    def identifier(self) -> str:
        return self.row[0]

    @property
    def title(self) -> str:
        return self.row[1]

    @property
    def publication_year(self) -> str:
        return ''

    def attribution(self) -> Optional[str]:
        return self.row[2]

    def citation(self) -> Optional[str]:
        return self.row[3]

    @property
    def manifest_url(self) -> str:
        return super().manifest_url

    @property
    def handle_url(self) -> str:
        return super().handle_url

