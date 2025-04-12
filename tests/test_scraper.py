import unittest
from scraper.main import Scraper

class TestScraper(unittest.TestCase):

    def setUp(self):
        self.scraper = Scraper()

    def test_login(self):
        result = self.scraper.login('test_user', 'test_password')
        self.assertTrue(result)

    def test_scrape_information(self):
        self.scraper.login('test_user', 'test_password')
        data = self.scraper.scrape_information()
        self.assertIsNotNone(data)
        self.assertIsInstance(data, dict)

    def test_handle_invalid_login(self):
        result = self.scraper.login('invalid_user', 'invalid_password')
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()