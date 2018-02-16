import codecs
import unittest
from grabber import parse_html


class TestPlayerParsing(unittest.TestCase):

    def test_noclan(self):
        with open('tests/eng-noclan.rtf', 'r') as f:
            data = f.read()
            r = parse_html(data)
            self.assertEqual('arrived', r['alignment'])
            self.assertEqual('1', r['level'])
            self.assertEqual(' fair-wind', r['name'])

    def test_clan(self):
        with open('tests/eng-clan.rtf', 'r') as f:
            data = f.read()
            r = parse_html(data)
            self.assertEqual('resident', r['alignment'])
            self.assertEqual('14', r['level'])
            self.assertEqual(' Anna I', r['name'])

    def test_rus(self):
        with codecs.open('tests/rus-noclan.htm', 'r') as f:
            data = f.read()
            r = parse_html(data)
            self.assertEqual('resident', r['alignment'])
            self.assertEqual('7', r['level'])
            self.assertEqual(' Евгений11', r['name'])
            self.assertEqual('54', r['health'])
            self.assertEqual('52', r['strength'])
            self.assertEqual('61', r['dexterity'])
            self.assertEqual('47', r['resistance'])
            self.assertEqual('69', r['intuition'])
            self.assertEqual('73', r['attention'])
            self.assertEqual('47', r['charism'])
            self.assertEqual('', r['clan'])

    def test_nodata(self):
        with open('tests/nodata.rtf', 'r') as f:
            data = f.read()
            r = parse_html(data)
            self.assertNotIn('alignment', r)
            self.assertNotIn('level', r)
            self.assertNotIn('name', r)

    def test_noalig(self):
        with open('tests/eng-noalig.htm', 'r') as f:
            data = f.read()
            r = parse_html(data)
            self.assertEqual(None, r['alignment'])

    def test_nolis(self):
        with open('tests/nolis.htm', 'r') as f:
            data = f.read()
            r = parse_html(data)
            self.assertEqual('slot1', r['items'][0]['type'])
            self.assertEqual('', r['items'][0]['name'])
            self.assertEqual('0', r['items'][0]['mf'])

            self.assertEqual('slot2', r['items'][1]['type'])
            self.assertEqual('', r['items'][1]['name'])
            self.assertEqual('0', r['items'][1]['mf'])

            self.assertEqual('slot3', r['items'][2]['type'])
            self.assertEqual('', r['items'][2]['name'])
            self.assertEqual('0', r['items'][2]['mf'])

            self.assertEqual('slot4', r['items'][3]['type'])
            self.assertEqual('', r['items'][3]['name'])
            self.assertEqual('0', r['items'][3]['mf'])

            self.assertEqual('slot5', r['items'][4]['type'])
            self.assertEqual('', r['items'][4]['name'])
            self.assertEqual('0', r['items'][4]['mf'])

            self.assertEqual('tech', r['items'][5]['type'])
            self.assertEqual('tech4', r['items'][5]['name'])
            self.assertEqual('0', r['items'][5]['mf'])

            self.assertEqual('slot7', r['items'][6]['type'])
            self.assertEqual('', r['items'][6]['name'])
            self.assertEqual('0', r['items'][6]['mf'])

            self.assertEqual('slot8', r['items'][7]['type'])
            self.assertEqual('', r['items'][7]['name'])
            self.assertEqual('0', r['items'][7]['mf'])

            self.assertEqual('jewellery', r['items'][8]['type'])
            self.assertEqual('accessory5', r['items'][8]['name'])
            self.assertEqual('17', r['items'][8]['mf'])

            self.assertEqual('cologne', r['items'][9]['type'])
            self.assertEqual('smell5', r['items'][9]['name'])
            self.assertEqual('10', r['items'][9]['mf'])


if __name__ == '__main__':
    unittest.main()
