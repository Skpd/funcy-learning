from bs4 import BeautifulSoup
import requests
import argparse
import pymysql.cursors



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--from', default=0, type=int)
    parser.add_argument('-t', '--to', type=int, required=True)

    args = dict(parser.parse_args().__dict__)

    conn = pymysql.connect(host='localhost', user='root', password='new_password', charset='utf8')
    conn.cursor().execute('CREATE DATABASE IF NOT EXISTS RosWar')
    conn.cursor().execute(
        'CREATE TABLE IF NOT EXISTS RosWar.Players '
        '(id INT not null primary key, name VARCHAR(255) COLLATE utf8_unicode_ci DEFAULT NULL, level INT, '
        'alignment VARCHAR(255) DEFAULT NULL, clan VARCHAR(255) COLLATE utf8_unicode_ci DEFAULT NULL, health INT, '
        'strength INT, dexterity INT, resistance INT,  intuition INT, attention INT, charism INT)')

    for x in range(args['from'], args['to'] + 1):
        player_id = "http://www.roswar.ru/player/{}/".format(x)
        r = requests.get(player_id)
        r.encoding = 'utf-8'
        result = parse_html(html=r.text)
        result['id'] = x
        if len(result.keys()) != 12:
            print(x,'was not found')
            continue

        sel_cursor = conn.cursor()
        sel_cursor.execute('SELECT * FROM roswar.players WHERE id = %s', result['id'])
        existing_player = sel_cursor.fetchone()

        if existing_player is None:
            conn.cursor().execute(
                "INSERT INTO roswar.players "
                "(id, name,level, clan, alignment, health, strength, dexterity, resistance, intuition, attention, charism) "
                "VALUES (%(id)s, %(name)s, %(level)s, %(clan)s, %(alignment)s, %(health)s, %(strength)s, %(dexterity)s, "
                "%(resistance)s, %(intuition)s, %(attention)s, %(charism)s)",
                result
            )
            conn.commit()
            print(x, 'existing player')
        else:
            conn.cursor().execute(
                'UPDATE roswar.players '
                'SET level = %(level)s, clan = %(clan)s, health = %(health)s, strength = %(strength)s, dexterity = %(dexterity)s, '
                'resistance = %(resistance)s, intuition = %(intuition)s, attention = %(attention)s, charism = %(charism)s',
                result
            )
            print(x, 'new player added to db')
    conn.close()


def parse_html(html: str):
    out = {}
    soup = BeautifulSoup(html, "html.parser")
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
            out.update({stat_name: stat_value})

    return out


if __name__ == '__main__':
    main()
