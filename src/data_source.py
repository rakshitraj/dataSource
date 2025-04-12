from abc import ABC, abstractmethod
from config import ConfigurationManager
from typing import Generator

class DataSource(ABC):
    @abstractmethod
    def data_filter(self) -> bool:
        """
        Should return a boolean value indicating whether the data satisfies the filter criteria.
        """
        pass

    @abstractmethod
    def format_data(self, data_object: any) -> any:
        """
        Takes the data object and returns it in the needed format for ingestion.
        """
        pass

    @abstractmethod
    def fetch_data(self, args) -> Generator[tuple[str, any], None, None]:
        """
        Should yield a tuple containing the filename and the file object.
        Generator[tuple[str, any], None, None]: This specifies that the method is a generator.
        -   It yields values of type tuple[str, any] (a tuple containing a string and any type of data).
        -   The first None indicates that the generator does not accept values via send().
        -   The second None indicates that the generator does not return a value when it completes.
        """
        pass