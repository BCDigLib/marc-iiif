from manifester.source_record import SourceRecord
from typing import Optional


class XLSXRow(SourceRecord):
    _manifest_row: tuple

    def __init__(self, manifest_row: tuple):
        self._manifest_row = manifest_row

    @property
    def identifier(self) -> str:
        return self._manifest_row[0].value

    @property
    def handle_url(self) -> str:
        return self._manifest_row[1].value

    @property
    def title(self) -> str:
        return self._manifest_row[2].value

    @property
    def publication_year(self) -> str:
        raise NotImplementedError()

    @property
    def attribution(self) -> Optional[str]:
        return self._manifest_row[3].value

    @property
    def citation(self) -> Optional[str]:
        return self._manifest_row[4].value
