from abc import ABC, abstractmethod


class SourceRecord(ABC):
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