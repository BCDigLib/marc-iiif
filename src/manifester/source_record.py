from abc import ABC, abstractmethod
from typing import Optional


class SourceRecord(ABC):
    """
    Abstract source record
    """
    @property
    @abstractmethod
    def identifier(self) -> str:
        pass

    @property
    @abstractmethod
    def title(self) -> str:
        pass

    @property
    @abstractmethod
    def publication_year(self) -> str:
        pass

    @property
    def citation(self) -> Optional[str]:
        return None

    @property
    def attribution(self) -> Optional[str]:
        return None

    @property
    def manifest_url(self) -> str:
        return f'https://library.bc.edu/iiif/manifests/{self.identifier}.json'

    @property
    def handle_url(self) -> str:
        return f'http://hdl.handle.net/2345.2/{self.identifier}'
