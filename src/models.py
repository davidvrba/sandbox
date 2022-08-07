from .db import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float



class FlowRate(Base):
    __tablename__ = "flow_rate"

    id = Column(Integer, primary_key=True, index=True)
    zone = Column(Integer)
    flow_timestamp = Column(DateTime)
    increment = Column(Float)
    total_pulse_count = Column(Integer)
    watter_source = Column(Integer)


class Zone(Base):
    __tablename__ = "zone"

    id = Column(Integer, primary_key=True, index=True)
    zone_name = Column(String)
