from bs4 import BeautifulSoup
import requests
import csv
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--from', default=0, type=int)
    parser.add_argument('-t', '--to', type=int, required=True)
    parser.add_argument('-o', '--output', default='results.csv')

    args = dict(parser.parse_args().__dict__)

    with open(args['output'], 'w') as csvfile:
        resultwriter = csv.writer(csvfile)

        print('Progress:')

        for x in range(args['from'], args['to'] + 1):
            player_id = "http://www.roswar.ru/player/{}/".format(x)
            r = requests.get(player_id)
            result = parse_html(html=r.text)
            if 'name' in result and 'level' in result and 'alignment' in result:
                resultwriter.writerow([x, result['name'], result['level'], result['alignment']])
            print(x, 'done')


def parse_html(html: str):
    out = {}
    soup = BeautifulSoup(html, "html.parser")
    a = soup.find('span', class_="user")
    if a is not None:
        out['alignment'] = a.find('i')['class'][0]
        out['name'] = a.select_one('a[href^="/player"]').get_text().strip()
        out['level'] = a.find('span').get_text().strip('[]')
    return out


if __name__ == '__main__':
    main()
