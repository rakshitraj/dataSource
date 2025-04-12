from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import PrimaryKeyConstraint

Base = declarative_base()

class PipelineConfiguration(Base):
    __tablename__ = 'pipeline_configuration'
    __table_args__ = (
        # PrimaryKeyConstraint('pipeline_id', 'key_conf', 'value_conf'),
        {'schema': 'data_store'}
    )

    pipeline_id = Column(String, nullable=False)
    key_conf = Column(String, nullable=False)
    value_conf = Column(String, nullable=False)
    created_time = Column(DateTime, nullable=True)
    updated_time = Column(DateTime, nullable=True)
    active_from = Column(DateTime, nullable=True)
    active_until = Column(DateTime, nullable=True)