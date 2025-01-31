from abc import ABC, abstractmethod


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
    @abstractmethod
    def citation(self) -> str:
        pass

    @property
    def manifest_url(self) -> str:
        return f'https://library.bc.edu/iiif/manifests/{self.identifier}.json'

    @property
    def handle_url(self) -> str:
        return f'http://hdl.handle.net/2345.2/{self.identifier}'
