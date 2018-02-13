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

    def test_nodata(self):
        with open('tests/nodata.rtf', 'r') as f:
            data = f.read()
            r = parse_html(data)
            self.assertNotIn('alignment', r)
            self.assertNotIn('level', r)
            self.assertNotIn('name', r)


if __name__ == '__main__':
    unittest.main()