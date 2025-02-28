from manifester.source_record import SourceRecord
from typing import Optional


class XLSXRow(SourceRecord):
    _manifest_row: tuple
    _identifier: str

    def __init__(self, manifest_row: tuple, identifier: str):
        self._manifest_row = manifest_row
        self._identifier = identifier

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def title(self) -> str:
        return self._manifest_row[1].value

    @property
    def publication_year(self) -> str:
        raise NotImplementedError()

    @property
    def attribution(self) -> Optional[str]:
        return self._manifest_row[2].value

    @property
    def citation(self) -> Optional[str]:
        return self._manifest_row[3].value
