from abc import ABC, abstractmethod
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import PipelineConfiguration
from contextlib import contextmanager


class ConfigurationManager(ABC):
    @abstractmethod
    def get_config(self, key, default=None):
        pass

class RDSConfigurationProvider(ConfigurationManager):
    _instances = {}

    def __new__(cls, pipeline_name, *args, **kwargs):
        if pipeline_name not in cls._instances:
            cls._instances[pipeline_name] = super(RDSConfigurationProvider, cls).__new__(cls)
        return cls._instances[pipeline_name]

    def __init__(self, pipeline_name, db_url):
        if not hasattr(self, '_initialized'):
            self.pipeline_name = pipeline_name
            self.config = {}
            self._initialized = True
            self._load_config(db_url)

    @contextmanager
    def get_session(db_url):
        engine = create_engine(db_url)
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            yield session
        finally:
            session.close()

    def _load_config(self, db_url):
        with self.get_session(db_url) as session:
            results = session.query(PipelineConfiguration).filter_by(pipeline_id=self.pipeline_name).all()
            self.config = {row.key: row.value for row in results}

    def get_config(self, key):
        if key not in self.config:
            raise KeyError(f"Configuration key '{key}' not found.")
        return self.config[key]