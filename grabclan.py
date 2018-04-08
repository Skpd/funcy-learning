from bs4 import BeautifulSoup
import grequests
import argparse
import re
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from models.clans import Clan
from sqlalchemy.orm import sessionmaker


def main():
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.debug('Process starts')
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--from', default=0, type=int)
    parser.add_argument('-t', '--to', type=int, required=True)

    args = dict(parser.parse_args().__dict__)

    base = declarative_base()
    engine = create_engine('mysql+pymysql://root:new_password@localhost/roswar?charset=utf8')
    base.metadata.bind = engine
    db_session = sessionmaker(bind=engine)
    session = db_session()
    base.metadata.create_all(engine)

    urls = []
    for x in range(args['from'], args['to'] + 1):
        clan_url = "http://www.roswar.ru/clan/{}/".format(x)
        print(clan_url)
        urls.append(clan_url)

    rs = (grequests.get(u, allow_redirects=False) for u in urls)
    complete_requests = grequests.map(rs, size=100)

    for r in complete_requests:
        if r is None:
            logger.warning('empty response')
            continue

        r.encoding = 'utf-8'
        clan_id = int(re.search(r'\d+', r.url).group())

        print(r.status_code)
        if r.status_code != 200:
            logger.debug('{} was not found'.format(clan_id))
            continue

        result = parse_html(html=r.text)
        if not result:
            logger.debug('{} empty clan'.format(clan_id))
            continue
        result['clan_id'] = clan_id

        existing_clan = session.query(Clan).filter(Clan.clan_id == result['clan_id']).first()

        if existing_clan is None:
            new_clan = Clan(**result)
            session.add(new_clan)
            session.commit()
            logger.debug('{} new clan added to db'.format(clan_id))

        else:
            existing_clan.update(**result)
            session.commit()
            logger.debug('{} existing clan updated'.format(clan_id))

    session.close()


def parse_html(html: str):
    out = {}

    soup = BeautifulSoup(html, "html5lib")
    a = soup.find('table', class_='forms').find_all('tr')

    for tr in a:
        td1_text = tr.find('td', class_='label').get_text()

        if td1_text == 'Название:':
            a = soup.select_one(".clan-info .clan-name")
            out['alignment'] = a.find('i')['class'][0] if a.find('i') else None

            name = a.select_one('a[href^="/clan"]')
            if name:
                out['name'] = name.get_text()
            else:
                return None
            out['level'] = a.find('span').get_text()[1:].strip('[]')
        elif td1_text == 'Девиз:':
            out['motto'] = tr.find('td', class_='input').get_text()
        elif td1_text == 'Рейтинг:':
            out['rank'] = tr.find('td', class_='input').get_text()[1:]
        elif td1_text == 'Казна:':
            out['tugriki'] = soup.find('span', class_='tugriki').get_text().replace(',', '')
            out['ore'] = soup.find('span', class_='ruda').get_text().replace(',', '')
            out['honey'] = soup.find('span', class_='med').get_text().replace(',', '')
            out['oil'] = soup.find('span', class_='neft').get_text().replace(',', '')
            out['tooth_white'] = soup.find('span', class_='tooth-white').get_text().replace(',', '')
            out['tooth_gold'] = soup.find('span', class_='tooth-golden').get_text().replace(',', '')
        elif td1_text == 'Глава:':
            head = tr.find('span', class_='user')
            if head is not None:
                head_text = head.select_one('a[href^="/player"]')
                out['head_id'] = head_text['href'].strip('/player')
        elif td1_text == 'Кланеры:':
            population = tr.find('td', class_='input').get_text().splitlines()
            out['population'] = population[0]
        elif td1_text == 'Атака:':
            out['attack'] = tr.find('td', class_='input').find('b').get_text()
        elif td1_text == 'Защита:':
            out['defence'] = tr.find('td', class_='input').find('b').get_text()
        elif td1_text == 'Время ненападения:':
            out['nonaggression_time'] = tr.find('td', class_='input').get_text()
        elif td1_text == 'Дипломатия:':
            relative_clans = tr.find_all('li')
            if relative_clans is not None:

                if len(relative_clans) > 0:
                    a = ''
                    for x in relative_clans:
                        # relative_clan_id = l.select_one('a[href^="/clan"]')
                        relative_clan = x.get_text().strip()
                        a = a + ', ' + relative_clan
                        out['relations'] = a
                else:
                    out['relations'] = None

    return out


if __name__ == '__main__':

    main()
