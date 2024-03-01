import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Float, MetaData, TIMESTAMP, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData()
Base = declarative_base(metadata=metadata)

class Bench(Base):
    __tablename__ = 'bench'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    count = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)
    creator_id = Column(Integer, ForeignKey('user.id'))

    creator = relationship('User', back_populates='benches')

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    is_active = Column(Boolean, default=False, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    benches = relationship('Bench', back_populates='creator')