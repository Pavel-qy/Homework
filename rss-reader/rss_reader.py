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
        default="0.1",
        help="print version info"  # doesn't work
    )
    parser.add_argument(
        "--json",
        action="store_true",
        default=False,
        help="print result as JSON in stdout",
        dest="json_output"
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
    return args.source, args.json_output, args.verbose, args.limit


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
    log.info(f"Start getting data from '{source}'")
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
    log.info("Start checking status code")
    if 199 < status_code < 300:
        return True


def get_soup(response):
    log.info("Start making the soup with 'lxml-xml'")
    return BeautifulSoup(response.text, "lxml-xml")


def is_rss(soup):
    return bool(soup.find("rss"))


def get_items(soup):
    return soup.find_all("item")


def news_creation(items):
    news_list = []
    for item in items:
        one_news = Novelty(item)
        news_list.append(one_news)
    return news_list


class Novelty:
    def __init__(self, soup_news):
        self.soup_news = soup_news
        self.title = self.scraping_title()
        self.category = self.scraping_category()
        self.date = self.scraping_date()
        self.source = self.scraping_source()
        self.link = self.scraping_link()
        self.description = self.scraping_description()
        self.urls = self.scraping_urls()

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

    def scraping_title(self):
        return self.soup_news.find("title").text

    def scraping_category(self):
        result = self.soup_news.find("category")
        if result:
            return result.text
        return

    def scraping_date(self):
        return self.soup_news.find("pubDate").text

    def scraping_source(self):
        result = self.soup_news.find("source")
        if result:
            return result.text
        return

    def scraping_link(self):
        return self.soup_news.find("link").text

    def scraping_description(self):
        description = self.soup_news.find("description")
        if description:
            description = BeautifulSoup(description.text, "lxml")
            return description.get_text(" ")
        return

    def scraping_urls(self):
        urls_list = [self.link]
        for tag in self.soup_news.find_all(url=True):
            urls_list.append(tag["url"])
        # for tag in self.soup_news.find_all(href=True):  # doesn't work. потытка вынять ссылки из описания гугл
        #     urls_list.append(tag["href"])
        return urls_list


def print_news(news, limit):
    for one_news in news[:limit]:
        print("\n", one_news, "\n", sep="")


def main():
    sys.tracebacklimit = 0
    source, json_output, verbose, limit = parse_arguments()
    global log
    log = create_logger(verbose)
    log.debug(f"Program received: {source=} {json_output=} {verbose=} {limit=}")
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
    news_list = news_creation(items)
    print(f"Feed: {soup.find('title').text}")
    print_news(news_list, limit)


if __name__ == "__main__":
    log = create_logger(False)
    main()
