from flask import json
from sqlalchemy import String, Integer, Column, Enum, ForeignKey
from sqlalchemy.orm import relationship
from models import Base


class Player(Base):
    __tablename__ = 'players'

    player_id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, default=None)
    level = Column(Integer)
    alignment = Column(Enum('arrived','resident'), default=None)
    clan_name = Column(String, default=None)
    clan_id = Column(Integer, ForeignKey('clans.clan_id'))
    health = Column(Integer, default=None)
    strength = Column(Integer, default=None)
    dexterity = Column(Integer, default=None)
    resistance = Column(Integer, default=None)
    intuition = Column(Integer, default=None)
    attention = Column(Integer, default=None)
    charism = Column(Integer, default=None)

    items = relationship("Item")
    clan = relationship("Clan")



    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def update(self, **kwargs):
        for k, v in kwargs.items():
            if getattr(self, k, None):
                setattr(self, k, v)

