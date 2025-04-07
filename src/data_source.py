from abc import ABC, abstractmethod

class DataSource(ABC):
    @abstractmethod
    def fetch_data(self):
        pass

class APISource(DataSource):
    @abstractmethod
    def generate_api_request(self):
        pass

    @abstractmethod
    def fetch_data(self):
        pass

class ClientSource(DataSource):
    @abstractmethod
    def create_connector(self):
        pass

    @abstractmethod
    def fetch_data(self):
        pass