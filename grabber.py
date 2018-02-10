from bs4 import BeautifulSoup
import requests
import csv

def main():
    with open('results/result.csv', 'w') as csvfile:
        resultwriter = csv.writer(csvfile)
        for x in range(100, 120):
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


if __name__ == '__main__':
    main()