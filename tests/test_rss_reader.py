import json
import logging
import unittest
from unittest.mock import Mock, patch
import bs4
import requests
import rss_reader.rss_reader as rss_reader


logging.disable(logging.CRITICAL)


class TestCreateLogger(unittest.TestCase):
    def test_verbose_true(self):
        verbose = True
        result = rss_reader.create_logger(verbose)
        self.assertIsInstance(result.handlers[0], logging.StreamHandler)
        self.assertEqual(result.level, 10)

    def test_verbose_False(self):
        verbose = False
        result = rss_reader.create_logger(verbose)
        self.assertIsInstance(result.handlers[0], logging.FileHandler)
        self.assertEqual(result.level, 0)


class TestIsDateValid(unittest.TestCase):
    def test_valid_date(self):
        date = "20211029"
        result = rss_reader.is_date_valid(date)
        self.assertEqual(result, True)

    def test_invalid_date(self):
        date = "20091944"
        with self.assertRaises(ValueError):
            rss_reader.is_date_valid(date)

    def test_invalid_input(self):
        date = "2g241210"
        with self.assertRaises(ValueError):
            rss_reader.is_date_valid(date)


class TestGetResponse(unittest.TestCase):
    def test_invalid_url(self):
        url = "abc123def456"
        with self.assertRaises(requests.exceptions.MissingSchema):
            rss_reader.get_response(url)


class TestGetDirectory(unittest.TestCase):
    def test_valid_source(self):
        source = "https://news.yahoo.com/rss"
        result = rss_reader.get_directory(source)
        self.assertEqual(result, "news.yahoo.com")


class TestGetFilename(unittest.TestCase):
    def test_two_string_args(self):
        directory = "news.yahoo.com"
        date = "20211030"
        result = rss_reader.get_filename(directory, date)
        self.assertEqual(result, "news.yahoo.com_20211030")

    def test_date_none(self):
        directory = "news.yahoo.com"
        date = None
        result = rss_reader.get_filename(directory, date)
        self.assertEqual(result, "news.yahoo.com")


class TestIsResponseSuccessful(unittest.TestCase):
    def test_successful_status_code(self):
        status_code = 200
        result = rss_reader.is_response_successful(status_code)
        self.assertEqual(result, True)

    def test_not_successful_status_code(self):
        status_code = 404
        result = rss_reader.is_response_successful(status_code)
        self.assertEqual(result, False)


class TestGetSoup(unittest.TestCase):
    def test_html_text(self):
        mock_response = Mock()
        mock_response.text = "<p>Something hilarious</p>"
        result = rss_reader.get_soup(mock_response)
        self.assertIsInstance(result, bs4.BeautifulSoup)


class TestIsRss(unittest.TestCase):
    def test_soup_with_rss(self):
        soup = bs4.BeautifulSoup("<rss version='2.0' xmlns:'atom=http://www.w3.org/2005/Atom'>", "lxml-xml")
        result = rss_reader.is_rss(soup)
        self.assertEqual(result, True)

    def test_soup_without_rss(self):
        soup = bs4.BeautifulSoup("<html lang='ru'>", "lxml-xml")
        result = rss_reader.is_rss(soup)
        self.assertEqual(result, False)


class TestGetItems(unittest.TestCase):
    def test_soup_with_items(self):
        xml_content = "<rss><item>Abc</item>, <item>Def</item>, <item>Ghi</item></rss>"
        soup = bs4.BeautifulSoup(xml_content, "lxml-xml")
        items_list = soup.find_all("item")
        result = rss_reader.get_items(soup)
        self.assertEqual(result, items_list)

    def test_soup_without_items(self):
        xml_content = "<rss><p>Abc</p>, <p>Def</p>, <p>Ghi</p></rss>"
        soup = bs4.BeautifulSoup(xml_content, "lxml-xml")
        items_list = soup.find_all("item")
        result = rss_reader.get_items(soup)
        self.assertEqual(result, items_list)


class TestCreateNews(unittest.TestCase):
    def test_novelty_objects(self):
        xml_content = "<rss><item>Abc</item>, <item>Def</item>, <item>Ghi</item></rss>"
        soup = bs4.BeautifulSoup(xml_content, "lxml-xml")
        items_list = soup.find_all("item")
        result = rss_reader.create_news(items_list)
        self.assertIsInstance(result, list)
        for item in result:
            self.assertIsInstance(item, rss_reader.Novelty)

    def test_dictionary_objects(self):
        dicts_list = []
        for i in range(3):
            dictionary = {
                "date": f"date_item_{i}",
                "title": f"title_item_{i}",
                "source": f"source_item_{i}",
                "category": f"category_item_{i}",
                "link": f"link_item_{i}",
                "enclosure": f"enclosure_item_{i}",
                "description": f"description_item_{i}",
                "links": [
                    f"links_item_{i}",
                    f"links_item_{i+1}",
                    f"links_item_{i+2}",
                ]
            }
            dicts_list.append(dictionary)
        result = rss_reader.create_news(dicts_list)
        self.assertIsInstance(result, list)
        for item in result:
            self.assertIsInstance(item, rss_reader.Novelty)


class TestGetDateFormat(unittest.TestCase):
    def test_valid_date_format(self):
        mock_one_news = Mock()
        dates = {
            "Sat, 30 Oct 2021 09:05:17 +0300": "%a, %d %b %Y %H:%M:%S %z",
            "Sat, 30 Oct 2021 06:12:19 GMT": "%a, %d %b %Y %H:%M:%S %Z",
            "2021-10-27T15:36:51Z": "%Y-%m-%dT%H:%M:%SZ",
        }
        news = []
        for date, date_format in dates.items():
            mock_one_news.dictionary = {"date": f"{date}"}
            result = rss_reader.get_date_format(mock_one_news)
            self.assertEqual(result, date_format)

    def test_invalid_date_format(self):
        mock_one_news = Mock()
        mock_one_news.dictionary = {"date": "30-10-2021"}
        with self.assertRaises(ValueError):
            rss_reader.get_date_format(mock_one_news)


class TestCreateNewsDict(unittest.TestCase):
    def test_news_with_date(self):
        mock_news_1 = Mock()
        mock_news_2 = Mock()
        mock_news_3 = Mock()
        mock_news_1.dictionary = {"date": "Sat, 30 Oct 2021 09:05:17 +0300"}
        mock_news_2.dictionary = {"date": "Sat, 29 Oct 2021 09:05:17 +0300"}
        mock_news_3.dictionary = {"date": "Sat, 28 Oct 2021 09:05:17 +0300"}
        news = [mock_news_1, mock_news_2, mock_news_3]
        dates = ["20211030", "20211029", "20211028"]
        result = rss_reader.create_news_dict(news)
        for date in dates:
            self.assertIn(date, result)


class TestPrintJson(unittest.TestCase):
    @patch("builtins.print")
    def test_objects_news(self, mock_print):
        mock_one_news = Mock
        mock_one_news.dictionary = {
            "date": "date_item",
            "title": "title_item",
            "source": "source_item",
            "category": "category_item",
            "link": "link_item_",
            "enclosure": "enclosure_item",
            "description": "description_item",
            "links": [
                "links_item",
                "links_item",
                "links_item",
            ]
        }
        news = [mock_one_news]
        rss_reader.print_json(news)
        list_dicts = [mock_one_news.dictionary]
        mock_print.assert_called_with(json.dumps(list_dicts, ensure_ascii=False, indent=4))


# class TestPrintNews(unittest.TestCase):
#     @patch("builtins.print")
#     def test_objects_news(self, mock_print):
#         mock_one_news = Mock()
#         # mock_one_news.__class__ = rss_reader.Novelty
#         mock_one_news.date = "date_item"
#         mock_one_news.title = "title_item"
#         mock_one_news.link = "link_item"
#         mock_one_news.links = ["links_item", "links_item", "links_item"]
#         mock_one_news.source = "date_item"
#         mock_one_news.category = "date_item"
#         mock_one_news.enclosure = "date_item"
#         mock_one_news.description = "date_item"
#         mock_one_news.__str__ = (
#             mock_one_news.date + mock_one_news.title + mock_one_news.link + mock_one_news.links[0] +
#             mock_one_news.source + mock_one_news.category + mock_one_news.enclosure + mock_one_news.description
#         )
#         news = [mock_one_news]
#         title = "Test"
#         rss_reader.print_news(news, title)
#         mock_print.assert_called_with("\nFeed: Test\nDate: date_item\nLink: link_item\n\nLinks:\n[1]: links_item\n[2]: links_item\n[3]: links_item")


if __name__ == "__main__":
    unittest.main()
