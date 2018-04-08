from bs4 import BeautifulSoup
import grequests
import argparse
import re
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from models.player import Player
from models.item import Item
from sqlalchemy.orm import sessionmaker


def main():
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.debug('Process starts')
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--from', default=0, type=int)
    parser.add_argument('-t', '--to', type=int, required=True)

    args = dict(parser.parse_args().__dict__)

    # conn = pymysql.connect(host='localhost', user='root', password='new_password', charset='utf8')

    base = declarative_base()
    engine = create_engine('mysql+pymysql://root:new_password@localhost/roswar?charset=utf8mb4')
    base.metadata.bind = engine
    db_session = sessionmaker(bind=engine)
    session = db_session()
    base.metadata.create_all(engine)

    urls = []
    for x in range(args['from'], args['to'] + 1):
        player_url = "http://www.roswar.ru/player/{}/".format(x)
        urls.append(player_url)

    rs = (grequests.get(u) for u in urls)
    complete_requests = grequests.map(rs, size=100)

    for r in complete_requests:
        if r is None:
            logger.warning('empty response')
            continue
        # logger.debug(r.url)
        player_id = int(re.search(r'\d+', r.url).group())
        r.encoding = 'utf-8'
        result = parse_html(html=r.text)
        result['player_id'] = player_id

        if len(result.keys()) < 12:
            logger.debug('{} was not found'.format(player_id))
            continue

        existing_player = session.query(Player).filter(Player.player_id == result['player_id']).first()

        if existing_player is None:
            player_fields = result
            new_items = player_fields.pop('items')
            new_player = Player(**player_fields)
            session.add(new_player)

            for x in range(0, len(new_items)):
                one_item = new_items[x]
                players_new_item = Item(**one_item)
                new_player.items.append(players_new_item)
                session.add(new_player)

            session.commit()
            logger.debug('{} new player added to db'.format(player_id))

        else:
            player_fields = result
            players_items_list = player_fields.pop('items')
            existing_player.update(**player_fields)

            items_from_bd = existing_player.items
            for x in range(0, len(players_items_list)):
                one_existing_item = players_items_list[x]

                for x in range(0, len(items_from_bd)):
                    item_from_bd = items_from_bd[x]
                    if item_from_bd.type == one_existing_item['type']:
                        item_from_bd.update(**one_existing_item)
                    else:
                        x = x+1

            session.commit()

            logger.debug('{} existing player updated'.format(player_id))

        session.close()


def parse_html(html: str):
    out = {}

    soup = BeautifulSoup(html, "html5lib")
    a = soup.find('span', class_="user")
    if a is not None:

        if a.find('i') is not None:
            out['alignment'] = a.find('i')['class'][0]
        else:
            out['alignment'] = None

        out['name'] = a.select_one('a[href^="/player"]').get_text()
        out['level'] = a.find('span').get_text().strip('[]')

        if a.select_one('a[href^="/clan"]') is not None:
            out['clan'] = a.select_one('a[href^="/clan"]').find('img')['title']
        else:
            out['clan'] = ''

        a = soup.find('ul', class_="stats").find_all('li', class_="stat")
        for item in a:
            stat_name = item.attrs.get('data-type')
            stat_value = item.find('span', class_="num").get_text()
            out[stat_name] = stat_value

        out['items'] = []

        for x in range(1, 11):
            a = soup.find('ul', class_="slots").find_all('li', class_='slot{}'.format(x))

            for item in a:
                img = item.find('img')
                item_info = {}

                if img is not None:
                    slot_item_type = img.attrs.get('data-type')
                    slot_item_mf = img.attrs.get('data-mf')
                    slot_item_name = img.attrs.get('src').replace('/@/images/obj/', '').rstrip('png.jpe')
                    item_info['mf'] = slot_item_mf
                    item_info['type'] = slot_item_type
                    item_info['name'] = slot_item_name
                else:
                    item_info['mf'] = '0'
                    item_info['type'] = 'slot{}'.format(x)
                    item_info['name'] = ''
                out['items'].append(item_info)

    print(out)
    return out


if __name__ == '__main__':

    main()
