import json
import sys
import argparse
import logging
import requests
from bs4 import BeautifulSoup


def parse_arguments():
    parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.")
    parser.add_argument(
        "source",
        help="RSS URL"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"'Version 0.2.0'",
        help="print version info"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        default=False,
        help="print result as JSON in stdout",
        dest="json_converting"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=False,
        help="outputs verbose status message",
        dest="verbose"
    )
    parser.add_argument(
        "--limit",
        default=None,
        type=int,
        help="limit news topics if this parameter provided",
        dest="limit"
    )
    args = parser.parse_args()
    return args.source, args.json_converting, args.verbose, args.limit


def create_logger(verbose):
    logger = logging.getLogger(__name__)
    if verbose:
        handler = logging.StreamHandler()
        logger.setLevel(logging.DEBUG)
    else:
        handler = logging.FileHandler("file.log", mode="w")
    log_format = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
    handler.setFormatter(log_format)
    logger.addHandler(handler)
    return logger


def get_response(source):
    log.info(f"Getting data from '{source}'")
    try:
        response = requests.get(source)
    except requests.exceptions.MissingSchema as exc:
        log.error("Exception occurred 'requests.exceptions.MissingSchema'")
        raise exc
    except requests.ConnectionError:
        log.error("Exception occurred 'requests.ConnectionError'")
        raise requests.ConnectionError(f"URL '{source}' does not exist")  # выводит слишком крупное сообщение
    return response


def is_successful_response(status_code):
    log.info(f"Checking status code '{status_code}'")
    if 199 < status_code < 300:
        return True


def get_soup(response):
    log.info("Making the soup with 'lxml-xml'")
    return BeautifulSoup(response.text, "lxml-xml")


def is_rss(soup):
    log.info("Checking if the soup contains 'RSS'")
    return bool(soup.find("rss"))


def get_items(soup):
    log.info("Getting items from soup")
    return soup.find_all("item")


def create_news(items):
    log.info("Creating a news list")
    news_list = []
    for item in items:
        one_news = Novelty(item)
        news_list.append(one_news)
    log.info(f"News added: '{len(news_list)}'")
    return news_list


class Novelty:
    def __init__(self, soup_news):
        self.soup_news = soup_news
        self.title = self.scrape_title()
        self.category = self.scrape_category()
        self.date = self.scrape_date()
        self.source = self.scrape_source()
        self.link = self.scrape_link()
        self.description = self.scrape_description()
        self.urls = self.scrape_urls()
        self.dictionary = self.create_dictionary()

    def __str__(self):
        result = f"Title: {self.title}"
        if self.source:
            result += f"\nSource: {self.source}"
        result += f"\nDate: {self.date}\nLink: {self.link}"
        if self.category:
            result += f"\nCategory: {self.category}"
        if self.description:
            result += f"\n\nDescription: {self.description}"
        result += f"\n\nLinks:"
        for i, link in enumerate(self.urls):
            result += f"\n[{i + 1}]: {link}"
        return result

    def scrape_title(self):
        title = self.soup_news.find("title")
        if title:
            return title.text
        return

    def scrape_category(self):
        category = self.soup_news.find("category")
        if category:
            return category.text
        return

    def scrape_date(self):
        date = self.soup_news.find("pubDate")
        if date:
            return date.text
        return

    def scrape_source(self):
        source = self.soup_news.find("source")
        if source:
            return source.text
        return

    def scrape_link(self):
        link = self.soup_news.find("link")
        if link:
            return link.text
        return

    def scrape_description(self):
        description = self.soup_news.find("description")
        if description:
            description = BeautifulSoup(description.text, "lxml")
            return description.get_text(" ")
        return

    def scrape_urls(self):
        urls_list = [self.link]
        for tag in self.soup_news.find_all(url=True):
            urls_list.append(tag["url"])
        # for tag in self.soup_news.find_all(href=True):  # doesn't work. потытка вынять ссылки из описания гугл
        #     urls_list.append(tag["href"])
        return urls_list

    def create_dictionary(self):
        dictionary = {
            "title": self.title,
            "date": self.date,
            "link": self.link,
            "links": self.urls,
        }
        if self.source:
            dictionary["source"] = self.source
        if self.category:
            dictionary["category"] = self.category
        if self.description:
            dictionary["description"] = self.description
        return dictionary


def create_json(news_list, limit):
    log.info("Converting news to JSON")
    news_dictionaries = [one_news.dictionary for one_news in news_list]
    return json.dumps(news_dictionaries[:limit], ensure_ascii=False, indent=4)


def print_news(news, limit, soup):
    log.info(f"Printing news: '{limit}'")
    print(f"\nFeed: {soup.find('title').text}")
    for one_news in news[:limit]:
        print("\n", one_news, "\n", sep="")


def main():
    sys.tracebacklimit = 0
    source, json_converting, verbose, limit = parse_arguments()
    global log
    log = create_logger(verbose)
    log.debug(f"Program received: {source=} {json_converting=} {verbose=} {limit=}")
    response = get_response(source)
    if not is_successful_response(response.status_code):
        log.error("Exception occurred 'requests.exceptions.HTTPError'")
        raise requests.exceptions.HTTPError(
            f"Request was not successfully processed. Status code = {response.status_code}"
        )
    soup = get_soup(response)
    if not is_rss(soup):
        log.error("Exception occurred 'requests.exceptions.InvalidURL'")
        raise requests.exceptions.InvalidURL(f"'{source}' does not contain web feed RSS")
    items = get_items(soup)
    news_list = create_news(items)
    if json_converting:
        json_news = create_json(news_list, limit)
        log.info("Print news as JSON")
        print(json_news)
    else:
        print_news(news_list, limit, soup)


if __name__ == "__main__":
    log = create_logger(False)
    main()
