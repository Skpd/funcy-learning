from bs4 import BeautifulSoup
import grequests
import argparse
import pymysql.cursors
import re
import logging
# import sqlalchemy
# from sqlalchemy import create_engine


def main():
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.debug('Process starts')
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--from', default=0, type=int)
    parser.add_argument('-t', '--to', type=int, required=True)

    args = dict(parser.parse_args().__dict__)

    # e = create_engine('mysql://root:new_password:@localhost/foo', , echo=True)

    conn = pymysql.connect(host='localhost', user='root', password='new_password', charset='utf8')

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

        sel_cursor = conn.cursor()
        sel_cursor.execute('SELECT * FROM roswar.players WHERE player_id = %s', result['player_id'])
        existing_player = sel_cursor.fetchone()

        if existing_player is None:
            conn.cursor().execute(
                "INSERT INTO roswar.players "
                "(player_id, name,level, clan, alignment, health, strength, dexterity, resistance, intuition, "
                "attention, charism) VALUES (%(player_id)s, %(name)s, %(level)s, %(clan)s, %(alignment)s, %(health)s, "
                "%(strength)s, %(dexterity)s, %(resistance)s, %(intuition)s, %(attention)s, %(charism)s)",
                {
                    'player_id': result['player_id'],
                    'name': result['name'],
                    'alignment': result['alignment'],
                    'level': result['level'],
                    'clan': result['clan'],
                    'health': result['health'],
                    'strength': result['strength'],
                    'dexterity': result['dexterity'],
                    'resistance': result['resistance'],
                    'intuition': result['intuition'],
                    'attention': result['attention'],
                    'charism': result['charism']

                }

            )

            for x in range(0, len(result['items'])):
                conn.cursor().execute(
                    "INSERT INTO roswar.playersitems "
                    "(player_id, name, type, mf) VALUES (%(player_id)s, %(name)s, %(type)s, %(mf)s)",
                    {
                        'player_id': result['player_id'],
                        'name': result['items'][x]['name'],
                        'type': result['items'][x]['type'],
                        'mf': result['items'][x]['mf'],

                    }

                )
            conn.commit()
            logger.debug('{} new player added to db'.format(player_id))
        else:
            conn.cursor().execute(
                'UPDATE roswar.players '
                'SET level = %(level)s, clan = %(clan)s, health = %(health)s, strength = %(strength)s, '
                'dexterity = %(dexterity)s, resistance = %(resistance)s, intuition = %(intuition)s, '
                'attention = %(attention)s, charism = %(charism)s',
                {
                    'level': result['level'],
                    'clan': result['clan'],
                    'health': result['health'],
                    'strength': result['strength'],
                    'dexterity': result['dexterity'],
                    'resistance': result['resistance'],
                    'intuition': result['intuition'],
                    'attention': result['attention'],
                    'charism': result['charism']

                }

            )

            for x in range(0, len(result['items'])):
                conn.cursor().execute(
                    'UPDATE roswar.playersitems '
                    'SET name = %(name)s, type = %(type)s, mf = %(mf)s',
                    {
                        'name': result['items'][x]['name'],
                        'type': result['items'][x]['type'],
                        'mf': result['items'][x]['mf'],

                    }

                    )
            logger.debug('{} existing player updated'.format(player_id))
    conn.close()


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

        for x in range (1,11):
            a = soup.find('ul', class_="slots").find_all('li', class_ ='slot{}'.format(x))

        # if len(a) == 1:
        #     item = a[0].find('img')
        # else:
        #     item = None
        #
        # if item is None:
        #     continue

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


    return out


if __name__ == '__main__':

    main()
