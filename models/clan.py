from sqlalchemy import String, Integer, Column
from sqlalchemy.orm import relationship
from models import Base



class Clan(Base):
    __tablename__ = 'clans'

    clan_id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, default=None)
    alignment = Column (String)
    level = Column(Integer)
    motto = Column (String, default=None)
    rank = Column(Integer)
    tugriki = Column(Integer)
    ore = Column(Integer)
    honey = Column(Integer)
    oil = Column(Integer)
    tooth_white = Column(Integer)
    tooth_gold = Column(Integer)
    head_id = Column(Integer)
    population = Column(String)
    attack = Column(Integer)
    defence = Column(Integer)
    nonaggression_time = Column(String)
    relations = Column(String)

    players = relationship("Player")

    def update(self, **kwargs):
        for k, v in kwargs.items():
            if getattr(self, k, None):
                setattr(self, k, v)

