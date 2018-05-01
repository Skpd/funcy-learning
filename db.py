from pprint import pprint

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from models.player import Player
from models.item import Item
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select

Base = declarative_base()

engine = create_engine('mysql+pymysql://root:new_password@localhost/roswar')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

Base.metadata.create_all(engine)

# new_player = Player(player_id=7775, name='zdes imya')
# session.add(new_player)
# session.commit()

# sel_cursor = conn.cursor()
# sel_cursor.execute('SELECT * FROM roswar.players WHERE player_id = %s', result['player_id'])
# existing_player = sel_cursor.fetchone()


# s = select([]).where(player_id == '0007776')
#existing_player = conn.execute(s).fetchone()
# print(s)

# (ret, ), = Session.query(exists().where(player_id = '0007775')
result = {'player_id': 7775}
existing_player = session.query(Player).filter(Player.player_id == result['player_id']).first()
pprint(existing_player.name)


slot = Item (item_id = 999, player_id = 7775)
existing_player = Player()
existing_player.items.append(slot)

for item in existing_player.items:
    existing_item.update (item_id = 996)




print(existing_player.items)
# existing_player.update(name='qwe', level=2, qweqweqwe=123 )
# session.save(existing_player)
session.commit()

