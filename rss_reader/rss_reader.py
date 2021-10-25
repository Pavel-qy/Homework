import json
import sys
import argparse
import logging
import requests
import os
import re
import datetime as dt
from bs4 import BeautifulSoup, element
from fpdf import FPDF


def parse_arguments():
    parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.")
    parser.add_argument(
        "source",
        nargs="?",
        default=None,
        help="RSS URL",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"'Version 0.3.0'",
        help="print version info",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        default=False,
        help="print result as JSON in stdout",
        dest="json_print",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=False,
        help="output verbose status message",
        dest="verbose",
    )
    parser.add_argument(
        "--limit",
        default=None,
        type=int,
        help="limit news topics if this parameter provided",
        dest="limit",
    )
    parser.add_argument(
        "--date",
        default=None,
        help="print cached news for specified date",
    )
    parser.add_argument(
        "--to-html",
        default=None,
        help="convert news to html and save to specified path",
        dest="to_html",
    )
    parser.add_argument(
        "--to-pdf",
        default=None,
        help="convert news to pdf and save to specified path",
        dest="to_pdf",
    )
    args = parser.parse_args()
    return args.source, args.json_print, args.verbose, args.limit, args.date, args.to_html, args.to_pdf


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


def is_date_valid(date):
    log.info("Date validation")
    try:
        dt.datetime.strptime(date, "%Y%m%d")
        return True
    except ValueError:
        return False


def get_path(source):
    log.info("Getting path of directory")
    return os.path.join("cache", re.findall(r"(?<=//)\S+?(?=/)", source)[0])


def is_date(source, date):
    log.info(f"Checking for cached news for '{date}' date")
    if source:
        path = get_path(source)
        return os.path.exists(os.path.join(path, f"{date}.json"))
    elif source is None:
        if not os.path.isdir("cache"):
            return False
        cache_dirs = list(os.walk("cache"))[0][1]
        for directory in cache_dirs:
            if os.path.exists(os.path.join("cache", directory, f"{date}.json")):
                return True
        else:
            return False


def get_response(source):
    log.info(f"Getting data from '{source}'")
    try:
        response = requests.get(source)
    except requests.exceptions.MissingSchema as exc:
        log.error("Exception occurred 'requests.exceptions.MissingSchema'")
        raise exc
    except requests.exceptions.ConnectionError:
        log.error("Exception occurred 'requests.exceptions.ConnectionError'")
        print(requests.exceptions.ConnectionError("Failed to establish connection"))
        return
    return response


def is_response_successful(status_code):
    log.info(f"Checking status code '{status_code}'")
    if 199 < status_code < 300:
        return True


def get_soup(response):
    log.info("Making soup with 'lxml-xml'")
    return BeautifulSoup(response.text, "lxml-xml")


def is_rss(soup):
    log.info("Checking if soup contains 'RSS'")
    return bool(soup.find("rss"))


def get_items(soup):
    log.info("Getting items from soup")
    return soup.find_all("item")


def create_news(objects_list):
    log.info("Creating list of Novelty objects")
    news = []
    if isinstance(objects_list[0], element.Tag):
        for item in objects_list:
            one_news = Novelty(item)
            news.append(one_news)
    elif isinstance(objects_list[0], dict):
        for dct in objects_list:
            one_news = Novelty(**dct)
            news.append(one_news)
    log.info(f"Number of objects: '{len(news)}'")
    return news


def get_news(response):
    if not is_response_successful(response.status_code):
        log.error("Exception occurred 'requests.exceptions.HTTPError'")
        print(requests.exceptions.HTTPError(
            f"Request was not successfully processed. Status code = {response.status_code}"
        ))
        return None, None
    soup = get_soup(response)
    if not is_rss(soup):
        log.error("Exception occurred 'requests.exceptions.InvalidURL'")
        print(requests.exceptions.InvalidURL("Source does not contain web feed RSS"))
        return None, None
    items = get_items(soup)
    title = soup.find('title').text
    return create_news(items), title


class Novelty:
    def __init__(self, item=None, **kwargs):
        if item:
            self.item = item
            self.title = self.scrape_title()
            self.link = self.scrape_link()
            self.description = self.scrape_description()
            self.category = self.scrape_category()
            self.date = self.scrape_date()
            self.source = self.scrape_source()
            self.enclosure = self.scrape_enclosure()
            self.urls = self.scrape_urls()
            self.dictionary = self.create_dictionary()
        elif kwargs:
            self.title = kwargs["title"]
            self.link = kwargs["link"]
            self.description = kwargs["description"]
            self.category = kwargs["category"]
            self.date = kwargs["date"]
            self.source = kwargs["source"]
            self.enclosure = kwargs["enclosure"]
            self.urls = kwargs["links"]

    def __str__(self):
        result = f"Title: {self.title}"
        if self.source:
            result += f"\nSource: {self.source}"
        if self.date:
            result += f"\nDate: {self.date}"
        result += f"\nLink: {self.link}"
        if self.category:
            result += f"\nCategory: {self.category}"
        if self.description:
            result += f"\n\nDescription: {self.description}"
        result += "\n\nLinks:"
        for i, link in enumerate(self.urls):
            result += f"\n[{i + 1}]: {link}"
        return result

    def scrape_title(self):
        title = self.item.find("title")
        if title:
            return title.text
        return

    def scrape_link(self):
        link = self.item.find("link")
        if link:
            return link.text
        return

    def scrape_description(self):
        description = self.item.find("description")
        if description:
            description = BeautifulSoup(description.text, "lxml")
            return description.get_text("\n", strip=True)
        return

    def scrape_category(self):
        category = self.item.find("category")
        if category:
            return category.text
        return

    def scrape_date(self):
        date = self.item.find("pubDate")
        if date:
            return date.text
        return

    def scrape_source(self):
        source = self.item.find("source")
        if source:
            return source.text
        return

    def scrape_enclosure(self):
        tag_names = ["enclosure", "media:content", "media:thumbnail"]
        for tag in tag_names:
            if self.item.find(tag):
                return self.item.find(tag)["url"]
        return

    def scrape_urls(self):
        urls_list = [self.link]
        for tag in self.item.find_all(url=True):
            urls_list.append(tag["url"])
        return urls_list

    def create_dictionary(self):
        dictionary = {
            "title": self.title,
            "link": self.link,
            "description": self.description,
            "category": self.category,
            "date": self.date,
            "source": self.source,
            "enclosure": self.enclosure,
            "links": self.urls,
        }
        return dictionary


def print_json(news, limit):
    log.info("Converting news to JSON")
    news_dictionaries = [one_news.dictionary for one_news in news]
    log.info("Printing news as JSON")
    print(json.dumps(news_dictionaries[:limit], ensure_ascii=False, indent=4))


def get_date_format(one_news):
    log.info("Defining date format of news")
    date_string = one_news.dictionary["date"]
    try:
        date_format = "%a, %d %b %Y %H:%M:%S %z"
        dt.datetime.strptime(date_string, date_format)
        return date_format
    except ValueError:
        pass
    try:
        date_format = "%a, %d %b %Y %H:%M:%S %Z"
        dt.datetime.strptime(date_string, date_format)
        return date_format
    except ValueError:
        pass
    try:
        date_format = "%Y-%m-%dT%H:%M:%SZ"
        dt.datetime.strptime(date_string, date_format)
        return date_format
    except ValueError as exc:
        log.error("Exception occurred 'ValueError'")
        raise exc


def create_dict_by_date(news):
    log.info("Creating dictionary with news sorted by date")
    dict_news_by_date = {}
    date_format = get_date_format(news[0])
    for one_news in news:
        date_string = one_news.dictionary["date"]
        date = dt.datetime.strptime(date_string, date_format)
        try:
            dict_news_by_date[date.strftime("%Y%m%d")].append(one_news.dictionary)
        except KeyError:
            dict_news_by_date[date.strftime("%Y%m%d")] = [one_news.dictionary]
    return dict_news_by_date


def cache_news(source, news):
    log.info("News caching by source and date")
    dict_news_by_date = create_dict_by_date(news)
    path = get_path(source)
    if not os.path.isdir(path):
        log.info(f"Creating directory '{path}' for cache")
        os.makedirs(path)
    for date in dict_news_by_date:
        if not os.path.exists(os.path.join(path, f"{date}.json")):
            log.info(f"Creating cache file '{date}.json' and caching all parsed news")
            with open(os.path.join(path, f"{date}.json"), "w") as json_file:
                json.dump(dict_news_by_date[date], json_file, ensure_ascii=True, indent=4)
        else:
            log.info(f"Opening cache file '{date}.json' and deserializing it")
            with open(os.path.join(path, f"{date}.json"), "r+") as json_file:
                news_list_from_json = json.load(json_file)
                json_file.seek(0)
                log.info("Checking for new parsed news")
                for index, one_news in enumerate(dict_news_by_date[date]):
                    if one_news["title"] == news_list_from_json[0]["title"] and index == 0:
                        log.info("No new news")
                        break
                    elif one_news["title"] == news_list_from_json[0]["title"] and index != 0:
                        log.info(f"Number of new parsed news – {index}. Adding them to cache")
                        updated_news_list = dict_news_by_date[date][:index] + news_list_from_json
                        json.dump(updated_news_list, json_file, ensure_ascii=True, indent=4)
                        break
                else:
                    log.info("All parsed news are new. Adding them to cache")
                    updated_news_list = dict_news_by_date[date] + news_list_from_json
                    json.dump(updated_news_list, json_file, ensure_ascii=True, indent=4)


def get_image(url):  # asdf############################################################################################
    log.info("Getting image and file format")
    response = get_response(url)
    if response:
        file_format = response.headers["Content-Type"].split("/")[1]
        with open("temp", "wb") as image:
            image.write(response.content)
        return file_format
    return


def get_filename(source, date):
    log.info("Getting name for file")
    if date:
        filename = re.findall(r"(?<=//)\S+?(?=/)", source)[0].replace(".", "_") + "_" + date
    else:
        filename = re.findall(r"(?<=//)\S+?(?=/)", source)[0].replace(".", "_")
    return filename


def convert_to_html(path, news, limit, title, source, date=None):
    log.info("Converting news to html format")
    with open(os.path.join("templates", "template.html"), encoding="utf-8") as template:
        html_template = template.read()
    soup = BeautifulSoup(html_template, "lxml")
    soup.title.append(title)
    soup.body.append(soup.new_tag("h1"))
    soup.h1.append(title)
    for i, one_news in enumerate(news[:limit]):
        soup.body.append(soup.new_tag("div", id=i))
        if one_news.dictionary["enclosure"]:
            soup.find("div", id=i).append(soup.new_tag("img", attrs={
                "class": "enclosure",
                "src": one_news.dictionary["enclosure"],
            }))
            soup.find("div", id=i).img.wrap(soup.new_tag("a", href=one_news.dictionary["link"], target="_blank"))
        if one_news.dictionary["title"]:
            soup.find("div", id=i).append(soup.new_tag("p", attrs={"class": "title"}))
            soup.find("div", id=i).find("p", attrs={"class": "title"}).append(one_news.dictionary["title"])
        if one_news.dictionary["date"]:
            soup.find("div", id=i).append(soup.new_tag("p", attrs={"class": "date"}))
            soup.find("div", id=i).find("p", attrs={"class": "date"}).append(one_news.dictionary["date"])
        if one_news.dictionary["category"]:
            soup.find("div", id=i).append(soup.new_tag("p", attrs={"class": "category"}))
            soup.find("div", id=i).find("p", attrs={"class": "category"}).append(one_news.dictionary["category"])
        if one_news.dictionary["source"]:
            soup.find("div", id=i).append(soup.new_tag("p", attrs={"class": "source"}))
            soup.find("div", id=i).find("p", attrs={"class": "source"}).append(one_news.dictionary["source"])
        if one_news.dictionary["link"]:
            soup.find("div", id=i).append(soup.new_tag("p", attrs={"class": "link"}))
            soup.find("div", id=i).find("p", attrs={"class": "link"}).append(one_news.dictionary["link"])
            soup.find("div", id=i).find("p", attrs={"class": "link"}).wrap(soup.new_tag("a", href=one_news.dictionary["link"], target="_blank"))
        if one_news.dictionary["description"]:
            soup.find("div", id=i).append(soup.new_tag("p", attrs={"class": "description"}))
            soup.find("div", id=i).find("p", attrs={"class": "description"}).append(
                one_news.dictionary["description"]
            )
        if one_news.dictionary["links"]:
            soup.find("div", id=i).append(soup.new_tag("p", attrs={"class": "links"}))
            for j, link in enumerate(one_news.dictionary["links"]):
                soup.find("div", id=i).find("p", attrs={"class": "links"}).append(soup.new_tag("a", id=j, href=link, target="_blank"))
                soup.find("div", id=i).find("p", attrs={"class": "links"}).find("a", id=j).append(link)
                soup.find("div", id=i).find("p", attrs={"class": "links"}).append(soup.new_tag("br"))

        # for key in one_news.dictionary:
        #     if key == "enclosure":
        #         soup.find("div", id=index).append(soup.new_tag("img", attrs={"class": key}))
        #     elif one_news.dictionary[key]:
        #         soup.find("div", id=index).append(soup.new_tag("p", attrs={"class": key}))
        # tags = soup.find("div", id=index).contents
        # for tag in tags:
        #     if tag["class"][0] == "enclosure":
        #         tag.attrs["src"] = one_news.dictionary["enclosure"]
        #     elif isinstance(one_news.dictionary[tag["class"][0]], list):
        #         for value in one_news.dictionary[tag["class"][0]]:
        #             tag.append(value)
        #             tag.append(soup.new_tag("br"))
        #     else:
        #         tag.append(one_news.dictionary[tag["class"][0]])

    if not os.path.isdir(path):
        log.info(f"Creating directory '{path}' for html files)")
        os.makedirs(path)
    filename = get_filename(source, date)
    with open(os.path.join(path, f"{filename}.html"), "w", encoding="utf-8") as html_file:
        html_file.write(soup.prettify())


# def convert_to_pdf(path, news, limit, title, source, date=None):
#     log.info("Converting news to pdf format")
#     if not os.path.isdir(path):
#         log.info(f"Creating directory '{path}' for pdf files")
#         os.makedirs(path)
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.add_font("Arial", fname=os.path.join("fonts", "arial.ttf"), uni=True)
#     pdf.set_font("Arial", size=14)
#     pdf.write(h=16, txt=title, link=source)
#     pdf.cell(0, 8)
#     for one_news in news[:limit]:
#         if one_news.dictionary["enclosure"]:
#             file_format = get_image(one_news.dictionary["enclosure"])
#             if file_format:
#                 pdf.image("temp", h=60, type=file_format, link=one_news.dictionary["enclosure"])
#             elif file_format is None:
#                 pdf.write(0, txt=one_news.dictionary["enclosure"][:50] + "...", link=one_news.dictionary["enclosure"])
#         if one_news.dictionary["title"]:
#             pdf.write(0, txt=one_news.dictionary["title"])
#         if one_news.dictionary["source"]:
#             pdf.write(0, txt=one_news.dictionary["source"])
#         if one_news.dictionary["date"]:
#             pdf.write(0, txt=one_news.dictionary["date"])
#         if one_news.dictionary["link"]:
#             pdf.write(0, txt=one_news.dictionary["link"])
#         if one_news.dictionary["category"]:
#             pdf.write(0, txt=one_news.dictionary["category"])
#         if one_news.dictionary["description"]:
#             pdf.write(0, txt=one_news.dictionary["description"])
#         if one_news.dictionary["links"]:
#             for i, link in enumerate(one_news.dictionary["links"]):
#                 pdf.write(0, txt=f"[{i + 1}] {link[:50]}", link=link)
#     filename = get_filename(source, date)
#     log.info(f"Saving pdf file to '{path}'")
#     pdf.output(name=os.path.join(path, f"{filename}.pdf"), dest="F")
#     if os.path.exists("temp"):
#         log.info("Delete temporary image file")
#         os.remove("temp")


def deserialize_json(source, date):
    log.info(f"Deserializing {date}.json")
    if "/" in source:
        path = get_path(source)
    else:
        path = os.path.join("cache", source)
    with open(os.path.join(path, f"{date}.json"), "r") as json_file:
        news_list_from_json = json.load(json_file)
    return news_list_from_json


def print_news(news, limit, title):
    log.info("Printing news")
    print(f"\nFeed: {title}")
    for one_news in news[:limit]:
        print("\n", one_news, "\n", sep="")


def main():
    # sys.tracebacklimit = 0
    source, json_print, verbose, limit, date, to_html, to_pdf = parse_arguments()
    global log
    log = create_logger(verbose)
    log.debug(f"Program received: {source=} {json_print=} {verbose=} {limit=} {date=}")
    if date:
        if not is_date_valid(date):
            log.error("Exception occurred 'ValueError'")
            raise ValueError(f"'{date}' invalid date input. '%Y%m%d' is required")
        if not is_date(source, date):
            log.error("Exception occurred 'FileNotFoundError'")
            raise FileNotFoundError(f"No cached news for '{date}' date")
    if source:
        response = get_response(source)
        if response:
            news, title = get_news(response)
            if news and not date:
                cache_news(source, news)
                if to_html:
                    if json_print:
                        print_json(news, limit)
                    convert_to_html(to_html, news, limit, title, source, date)
                elif json_print:
                    print_json(news, limit)
                elif not json_print:
                    print_news(news, limit, title)
            elif news and date:
                cache_news(source, news)
                list_of_news_dict = deserialize_json(source, date)
                cached_news = create_news(list_of_news_dict)
                if json_print:
                    print_json(cached_news, limit)
                elif not json_print:
                    print_news(cached_news, limit, title)
        elif date and response is None:
            list_of_news_dict = deserialize_json(source, date)
            cached_news = create_news(list_of_news_dict)
            if json_print:
                print_json(cached_news, limit)
            elif not json_print:
                print_news(cached_news, limit, source)
    elif date and source is None:
        cache_dirs = list(os.walk("cache"))[0][1]
        for directory in cache_dirs:
            if os.path.exists(os.path.join("cache", directory, f"{date}.json")):
                list_of_news_dict = deserialize_json(directory, date)
                cached_news = create_news(list_of_news_dict)
                if json_print:
                    print_json(cached_news, limit)
                elif not json_print:
                    print_news(cached_news, limit, directory)


if __name__ == "__main__":
    log = create_logger(False)
    main()
