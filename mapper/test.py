from unittest import TestCase
from mapper.events.parser import get_rss, parser

class ParserTestCase(TestCase):

    def test_get_rss(self):
        self.assertIsNotNone(get_rss())
        self.assertIsInstance(get_rss(), str)

    def test_add_data_to_db(self):
        self.assertEqual(parser(), 'the creation of records in the database successfully')

