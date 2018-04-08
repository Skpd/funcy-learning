from sqlalchemy import String, Integer, Column, ForeignKey
from sqlalchemy.orm import relationship
from models import Base


class Item(Base):
    __tablename__ = 'PlayersItems'

    item_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    type = Column(String, default=None)
    name = Column(String, default=None)
    mf = Column(Integer)
    player_id = Column(Integer, ForeignKey('players.player_id'))

    player = relationship("Player")


    def update (self, **kwargs):
        for k, v in kwargs.items():
            if getattr(self, k, None):
                setattr(self, k, v)

