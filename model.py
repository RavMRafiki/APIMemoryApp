from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class Score(Base):
    __tablename__ = 'score'
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    size = Column(Integer)
    value = Column(Integer)
    time = Column(Integer)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    user_id = Column(Integer, ForeignKey('player.id'))

    user = relationship('User')


class User(Base):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    token = Column(String)
    disabled = Column(Boolean)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())