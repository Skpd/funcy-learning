

from bs4 import BeautifulSoup
import requests
import csv
import argparse


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-st','--start', default=0 , type=int)
    parser.add_argument('-en', '--end', type=int, required = True)
    parser.add_argument('-out', '--output', default = 'results.csv')

    args = parser.parse_args()

    with open( args.output , 'w') as csvfile:
        resultwriter = csv.writer(csvfile)

        print('Progress:')

        for x in range (args.start, args.end + 1):
            player_id = "http://www.roswar.ru/player/{}/".format(x)
            r = requests.get(player_id)
            soup = BeautifulSoup(r.text, "html.parser")
            a = soup.find('span', class_="user")
            if a is None:
                print(x, 'not found')
            else:
                alignment = a.find('i')['class'][0]
                name = a.select_one('a[href^="/player"]').get_text().strip()
                level = a.find('span').get_text().strip('[]')
                resultwriter.writerow([x, name, level, alignment])
                print(x, 'done')

if __name__ == '__main__':
    main()