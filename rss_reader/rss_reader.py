import hashlib
import json
import shutil
import sys
import argparse
import logging
import requests
import os
import re
import datetime as dt
from bs4 import BeautifulSoup, element
from xhtml2pdf import pisa


def parse_arguments():
    """
    Returns parameters read from the command line.

    :return:
    source : str
        url of source of rss news

    version
        print version info

    json_print : bool
        print result as JSON in stdout

    verbose : bool
        output verbose status message

    limit : int
        limit news topics if this parameter provided

    date : str
        print cached news for specified date

    to_pdf : str
        convert news to pdf and save to specified path

    to_html : str
        convert news to html and save to specified path
    """
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
        version=f"'Version 0.4.1'",
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
        "--to-pdf",
        default=None,
        help="convert news to pdf and save to specified path",
        dest="to_pdf",
    )
    parser.add_argument(
        "--to-html",
        default=None,
        help="convert news to html and save to specified path",
        dest="to_html",
    )
    args = parser.parse_args()
    return args.source, args.json_print, args.verbose, args.limit, args.date, args.to_pdf, args.to_html


def create_logger(verbose: bool) -> logging.Logger:
    """
    Changes the parameters of  the created logger.

    :param verbose : bool
        the 'verbose' parameter from the command line

    :return logger : logging.Logger
        the logger with the updated parameters
    """
    logger = logging.getLogger(__name__)
    if verbose:
        handler = logging.StreamHandler()
        logger.setLevel(logging.DEBUG)
    else:
        handler = logging.FileHandler("file.log", mode="w", encoding="utf-8")
    log_format = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
    handler.setFormatter(log_format)
    logger.addHandler(handler)
    return logger


def is_date_valid(date: str) -> bool:
    """
    Gets the date and checks if the date is correct

    :param date : str
        the 'date' parameter from the command line

    :return 'bool' if the date is correct

    :raise  ValueError
        an error if the specified date is invalid
    """
    log.info("Checking if date is valid")
    try:
        dt.datetime.strptime(date, "%Y%m%d")
        return True
    except ValueError:
        log.error("Exception occurred 'ValueError'")
        raise ValueError(f"'{date}' invalid date input. '%Y%m%d' is required")


def is_response_successful(status_code: int) -> bool:
    """
    Gets the status code and checks if the response status code successful.

    :param status_code : int
        status code of the received response from the server

    :return True
        if the number is greater than 199 and less than 300
    :return False
        if the number is less than 199 and more than 300
    """
    log.info(f"Checking status code '{status_code}'")
    if 199 < status_code < 300:
        return True
    else:
        return False


def get_response(source: str) -> requests.models.Response or None:
    """
    Gets url, send GET request and stores in variable 'response'.

    :param source : str
        the 'source' parameter from the command line

    :return response : requests.models.Response
        retrieved data from the server

    :return None
        if it is impossible to connect to the server

    :return None
        if response status code is not valid

    :raise requests.exceptions.MissingSchema
        an error if 'source' is incorrect url
    """
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
    if not is_response_successful(response.status_code):
        log.error("Exception occurred 'requests.exceptions.HTTPError'")
        print(requests.exceptions.HTTPError(
            f"Request was not successfully processed. Status code = '{response.status_code}'"
        ))
        return
    return response


def get_directory(source: str) -> str:
    """
    Gets url to extract the site name.

    :param source : str
        the 'source' parameter from the command line

    :return str
        site name extracted from url
    """
    log.info("Getting directory name")
    return re.findall(r"(?<=//)\S+?(?=/)", source)[0]


def get_filename(directory: str, date: str) -> str:
    """
    Gets the directory name and date and returns the file name.

    :param directory: str
        the name of the directory of cache files or pdf files or html files
    :param date : str
        the 'date' parameter from the command line

    :return filename : str
        filename which consists of directory name or directory name and date
    """
    log.info("Getting file name")
    if directory and date:
        filename = directory + "_" + date
    else:
        filename = directory
    return filename


def is_file(directory: str, filename: str):
    """
    Gets the directory name and the filename and checks for file existence.

    :param directory : str
        the name of the directory of cache files or pdf files or html files
    :param filename : str
        filename which consists of directory name or directory name and date

    :raise FileNotFoundError
        an error if the file doesn't exist
    """
    log.info(f"Checking if there is cache file '{filename}'")
    if not os.path.exists(os.path.join("cache", directory, f"{filename}.json")):
        log.error("Exception occurred 'FileNotFoundError'")
        raise FileNotFoundError(f"There is no cache news for '{filename}'")


def get_soup(response: requests.models.Response) -> BeautifulSoup:
    """
    Gets the response and create the soup with BeautifulSoup and 'lxml-xml' parser.

    :param response : requests.models.Response
        retrieved data from the server

    :return BeautifulSoup
        an 'BeautifulSoup' object obtained by parsing 'response.text'
    """
    log.info("Creating soup with 'lxml-xml'")
    return BeautifulSoup(response.text, "lxml-xml")


def is_rss(soup: BeautifulSoup) -> bool:
    """
    Gets the 'BeautifulSoup' object and looking for the 'rss' tag.

    :param soup : BeautifulSoup
        an 'BeautifulSoup' object obtained by parsing 'response.text'

    :return True
        if the soup contains 'rss' tag
    :return False
        if the soup does not contain 'rss' tag
    """
    log.info("Checking if soup contains 'RSS'")
    return bool(soup.find("rss"))


def get_items(soup: BeautifulSoup) -> list:
    """
    Gets the 'BeautifulSoup' object and searches all the item tags.

    :param soup : BeautifulSoup
        an 'BeautifulSoup' object obtained by parsing 'response.text'

    :return list
        list of objects 'element.Tag' selected by the 'item' tag
    """
    log.info("Getting items from soup")
    return soup.find_all("item")


class Novelty:
    """
    A class to represent one news item.

    Attributes
    ----------
    item=None : element.Tag
        object 'element.Tag' obtained from the soup by the 'item' tag

    kwargs : dict
        dictionary of one news received from cache

    Methods
    -------
    def scrape_date(self):
        Scrapes the news release date.

    def scrape_title(self):
        Scrapes the news title.

    def scrape_source(self):
        Scrapes the source of news.

    def scrape_category(self):
        Scrapes the news category.

    def scrape_link(self):
        Scrapes the news link.

    def scrape_enclosure(self):
        Scrapes the news enclosure.

    def scrape_description(self):
        Scrapes the news description.

    def scrape_links(self):
        Scrapes the news links.

    def create_dictionary(self):
        Creates a dictionary based on scraped data.
    """
    def __init__(self, item=None, **kwargs):
        """
        Constructs all attributes for the 'Novelty' object
        based on 'element.Tag' object or 'dict' object

        :param item : element.Tag
            object 'element.Tag' obtained from the soup by the 'item' tag

        :param kwargs : dict
            dictionary of one news received from cache
        """
        if item:
            self.item = item
            self.date = self.scrape_date()
            self.title = self.scrape_title()
            self.source = self.scrape_source()
            self.category = self.scrape_category()
            self.link = self.scrape_link()
            self.enclosure = self.scrape_enclosure()
            self.description = self.scrape_description()
            self.links = self.scrape_links()
            self.dictionary = self.create_dictionary()
        elif kwargs:
            self.date = kwargs["date"]
            self.title = kwargs["title"]
            self.source = kwargs["source"]
            self.category = kwargs["category"]
            self.link = kwargs["link"]
            self.enclosure = kwargs["enclosure"]
            self.description = kwargs["description"]
            self.links = kwargs["links"]
            self.dictionary = kwargs

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
        for i, link in enumerate(self.links):
            result += f"\n[{i + 1}]: {link}"
        return result

    def scrape_date(self):
        """
        Scrapes the news release date.

        :return str
            if 'element.Tag' object contain 'pubDate' tag
        :return None
            if 'element.Tag' does not contain 'pubDate' tag
        """
        date = self.item.find("pubDate")
        if date:
            return date.text
        return

    def scrape_title(self):
        """
        Scrapes the news title.

        :return str
            if 'element.Tag' object contain 'title' tag
        :return None
            if 'element.Tag' does not contain 'title' tag
        """
        title = self.item.find("title")
        if title:
            return title.text
        return

    def scrape_source(self):
        """
        Scrapes the source of news.

        :return str
            if 'element.Tag' object contain 'source' tag
        :return None
            if 'element.Tag' does not contain 'source' tag
        """
        source = self.item.find("source")
        if source:
            return source.text
        return

    def scrape_category(self):
        """
        Scrapes the news category.

        :return str
            if 'element.Tag' object contain 'category' tag
        :return None
            if 'element.Tag' does not contain 'category' tag
        """
        category = self.item.find("category")
        if category:
            return category.text
        return

    def scrape_link(self):
        """
        Scrapes the news link.

        :return str
            if 'element.Tag' object contain 'link' tag
        :return None
            if 'element.Tag' does not contain 'link' tag
        """
        link = self.item.find("link")
        if link:
            return link.text
        return

    def scrape_enclosure(self):
        """
        Scrapes the news enclosure.

        :return str
            if 'element.Tag' object contain 'enclosure' tag
            or 'media:content' tag or 'media:thumbnail' tag
        :return None
            if 'element.Tag' object does not contain 'enclosure' tag
            or 'media:content' tag or 'media:thumbnail' tag
        """
        tag_names = ["enclosure", "media:content", "media:thumbnail"]
        for tag in tag_names:
            if self.item.find(tag):
                return self.item.find(tag)["url"]
        return

    def scrape_description(self):
        """
        Scrapes the news description.

        :return str
            if 'element.Tag' object contain 'description' tag
        :return None
            if 'element.Tag' does not contain 'description' tag
        """
        description = self.item.find("description")
        if description:
            description = BeautifulSoup(description.text, "lxml")
            return description.get_text("\n", strip=True)
        return

    def scrape_links(self):
        """
        Scrapes the news links.

        :return links_list : list
            list of urls contained in url parameters
        """
        links_list = [self.link]
        for tag in self.item.find_all(url=True):
            links_list.append(tag["url"])
        return links_list

    def create_dictionary(self):
        """
        Creates a dictionary based on scraped data.

        :return dictionary : dict
            dictionary with all scraped data from the 'element.Tag' object
        """
        dictionary = {
            "date": self.date,
            "title": self.title,
            "source": self.source,
            "category": self.category,
            "link": self.link,
            "enclosure": self.enclosure,
            "description": self.description,
            "links": self.links,
        }
        return dictionary


def create_news(objects_list: list) -> list:
    """
    Gets a list of 'element.Tag' objects and creates a list of 'Novelty' objects.

    :param objects_list : list
        list of novelty objects or a list of cached news dictionaries

    :return news : list
        a list of 'Novelty' objects
    """
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
    log.info(f"Number of created objects: '{len(news)}'")
    return news


def get_news(response: requests.models.Response) -> (None, None) or (list, str):
    """
    Gets a response and calls a function to check the status code and
    calls the function to check if the response contains 'rss' tag.

    :param response : requests.models.Response
        retrieved data from the server

    :return (None, None)
        if the status code is not successful
    :return (None, None)
        if the soup does not contain 'rss'
    :return (list, title : str)
        a list of 'Novelty' objects and string with the title of feed
    """
    log.info("Creating news if the response contains 'RSS' tag")
    soup = get_soup(response)
    if not is_rss(soup):
        log.error("Exception occurred 'requests.exceptions.InvalidURL'")
        print(requests.exceptions.InvalidURL("Source does not contain web feed RSS"))
        return None, None
    items = get_items(soup)
    title = soup.find('title').text
    return create_news(items), title


def get_date_format(one_news: Novelty) -> str:
    """
    Gets a scraped string of news publication date and specifies its format.

    :param one_news : Novelty
        object of class "Novelty"

    :return date_format : str
        if the date format matches one of three known

    :raise ValueError
        an error if the date format does not match one of three known
    """
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


def create_news_dict(news: list) -> dict:
    """
    Creates a dictionary with keys – dates and values – lists of dictionaries Novelty.dictionary.

    :param news : list
        a list of 'Novelty' objects

    :return news_dict : dict
        dictionary of dictionaries sorted by date
    """
    log.info("Creating dictionary with news sorted by date")
    news_dict = {}
    date_format = get_date_format(news[0])
    for one_news in news:
        date = dt.datetime.strptime(one_news.dictionary["date"], date_format)
        try:
            news_dict[date.strftime("%Y%m%d")].append(one_news.dictionary)
        except KeyError:
            news_dict[date.strftime("%Y%m%d")] = [one_news.dictionary]
    return news_dict


def cache_images(news: list, path: str, filename: str) -> list:
    """
    Gets a list of 'Novelty' objects, path to the cache file, and name of the cache file.
    If 'Novelty' object dictionary.["enclosure"] contains url, downloads the image,
    determines its format and caches it. The path in the dictionary.["enclosure"]
    changes to the path of saved file.

    :param news : list
        a list of 'Novelty' objects
    :param path : str
        path to the cache file
    :param filename : str
        filename which consists of directory name or directory name and date

    :return news : list
        a list of 'Novelty' objects with modified paths
    """
    log.info("Caching images")
    for one_news in news:
        if one_news["enclosure"]:
            url = one_news["enclosure"]
            response = requests.get(url)
            image_format = re.findall(r"(?<=image/)\w+", response.headers["Content-Type"])[0]
            image_name = hashlib.md5(bytes(url, encoding="utf-8")).hexdigest()
            directory_path = os.path.join(os.getcwd(), path, "images", filename)
            if not os.path.isdir(directory_path):
                os.makedirs(directory_path)
            file_path = os.path.join(directory_path, f"{image_name}.{image_format}")
            with open(file_path, "wb") as image:
                image.write(response.content)
            one_news["enclosure"] = file_path
    return news


def cache_news(source: str, news: list):
    """
    Gets a list of 'Novelty' objects, creates a directory for cache files.
    Runs a loop that checks if there is no cache file – creates it
    and serializes all dictionaries. If there is a cache file,
    it compares the dictionaries from the cache file and from the dictionary
    by title and adds new ones. If there are no matches, it adds all news dictionaries.

    :param source : str
        the 'source' parameter from the command line

    :param news : list
        a list of 'Novelty' objects
    """
    log.info("Caching news")
    news_dict = create_news_dict(news)
    directory = get_directory(source)
    path = os.path.join("cache", directory)
    if not os.path.isdir(path):
        log.info(f"Creating directory '{path}' for cache")
        os.makedirs(path)
    for date in news_dict:
        filename = get_filename(directory, date)
        if not os.path.exists(os.path.join(path, f"{filename}.json")):
            log.info(f"Creating cache file '{filename}.json' and caching all parsed news")
            with open(os.path.join(path, f"{filename}.json"), "w") as json_file:
                news_dict[date] = cache_images(news_dict[date], path, filename)
                json.dump(news_dict[date], json_file, ensure_ascii=True, indent=4)
        else:
            log.info(f"Opening cache file '{filename}.json' and deserializing it")
            with open(os.path.join(path, f"{filename}.json"), "r+") as json_file:
                news_list = json.load(json_file)
                json_file.seek(0)
                log.info("Checking for new parsed news")
                for index, one_news in enumerate(news_dict[date]):
                    if one_news["title"] == news_list[0]["title"] and index == 0:
                        log.info("No new news")
                        break
                    elif one_news["title"] == news_list[0]["title"] and index != 0:
                        log.info(f"Number of new parsed news – {index}")
                        news_dict[date][:index] = cache_images(news_dict[date][:index], path, filename)
                        updated_news_list = news_dict[date][:index] + news_list
                        json.dump(updated_news_list, json_file, ensure_ascii=True, indent=4)
                        log.info("Writing new data to file")
                        break
                else:
                    log.info("All parsed news are new")
                    news_dict[date] = cache_images(news_dict[date], path, filename)
                    updated_news_list = news_dict[date] + news_list
                    json.dump(updated_news_list, json_file, ensure_ascii=True, indent=4)
                    log.info("Writing new data to file")


def print_json(news: list):
    """
    Gets a list of 'Novelty' objects, creates a list of dictionaries and prints to std as json.

    :param news : list
        a list of 'Novelty' objects
    """
    log.info("Creating list of dictionaries for serialization")
    news_dictionaries = [one_news.dictionary for one_news in news]
    log.info("Printing news as JSON")
    print(json.dumps(news_dictionaries, ensure_ascii=False, indent=4))


def copy_images(news: list, filename: str, path: str) -> list:
    """
    Gets a list of 'Novelty' objects, copies images to the folder
    for html file and changes the path ["enclosure"].

    :param news : list
        a list of 'Novelty' objects
    :param filename : str
        filename which consists of directory name or directory name and date
    :param path : str
        directory path for 'html' files

    :return news : list
        a list of 'Novelty' objects with modified paths
    """
    log.info("Copying images for html file")
    directory_path = os.path.join(path, filename)
    for one_news in news:
        if one_news.dictionary["enclosure"]:
            if os.path.exists(one_news.dictionary["enclosure"]):
                image_name = os.path.basename(one_news.dictionary["enclosure"])
                image_path = os.path.join(directory_path, image_name)
                if not os.path.isdir(directory_path):
                    log.info(f"Creating directory '{filename}' for images")
                    os.makedirs(directory_path)
                shutil.copy(one_news.dictionary["enclosure"], image_path)
                one_news.dictionary["enclosure"] = os.path.join(filename, image_name)
    return news


def create_soup(template: str, news: list, title: str):
    """
    Creates the soup based on a template for conversion to 'html' or 'pdf'.

    :param template : str
        template name 'template_for_pdf.html' or 'template_for_pdf.html'
    :param news : list
        a list of 'Novelty' objects
    :param title : str
        news feed title

    :return soup : BeautifulSoup
        'BeautifulSoup' object based on the template
    """
    log.info("Creating soup based on template")
    soup = BeautifulSoup(template, "lxml")
    soup.title.append(title)
    soup.body.append(soup.new_tag("h1"))
    soup.h1.append(title)
    for i, one_news in enumerate(news):
        soup.body.append(soup.new_tag("div", id=f"news{i}"))
        for key in one_news.dictionary:
            if one_news.dictionary[key] and key == "enclosure":
                soup.find("div", id=f"news{i}").append(soup.new_tag("img", attrs={"class": key}))
            elif one_news.dictionary[key]:
                soup.find("div", id=f"news{i}").append(soup.new_tag("p", attrs={"class": key}))
                soup.find("div", id=f"news{i}").find("p", attrs={"class": key}).append(key.capitalize() + ": ")
        tags = {tag["class"][0]: tag for tag in soup.find("div", id=f"news{i}").contents}
        for key, tag in tags.items():
            if key == "enclosure":
                tag.attrs["src"] = one_news.dictionary["enclosure"]
                tag.attrs["alt"] = one_news.dictionary["enclosure"]
                tag.wrap(soup.new_tag("a", href=one_news.dictionary["link"], target="_blank"))
            elif key == "link":
                tag.append(soup.new_tag("a", href=one_news.dictionary[key], target="_blank"))
                tag.a.append(one_news.dictionary[key])
            elif key == "links":
                for j, link in enumerate(one_news.dictionary[key]):
                    tag.append(soup.new_tag("a", id=f"news{i}link{j}", href=link, target="_blank"))
                    tag.find("a", id=f"news{i}link{j}").append(link)
                    tag.find("a", id=f"news{i}link{j}").wrap(soup.new_tag(
                        "p",
                        attrs={"class": "link list", "id": f"news{i}link{j}wrap"}
                    ))
                    tag.find("p", id=f"news{i}link{j}wrap").insert(0, f"[{j+1}]: ")
            else:
                if "\n" in one_news.dictionary[key]:
                    tag.append(soup.new_tag("br"))
                    for line in one_news.dictionary[key].split("\n"):
                        tag.append(line)
                        tag.append(soup.new_tag("br"))
                else:
                    tag.append(one_news.dictionary[key])
    return soup


def create_pdf(soup: BeautifulSoup, path: str, filename: str, data_path: str):
    """
    Adds fonts and creates a 'pdf' file based on the soup.

    :param soup : BeautifulSoup
        'BeautifulSoup' object based on the template
    :param path : str
        directory path for 'pdf' files
    :param filename : str
        filename which consists of directory name or directory name and date
    :param data_path:
        path to directory with package data
    """
    log.info("Adding fonts to html for pdf creation")
    soup.style.append(
        "@font-face {font-family: 'DejaVuSans'; src: url(" +
        os.path.join(data_path, "fonts", "DejaVuSans.ttf") + ");}"
    )
    soup.style.append(
        "@font-face {font-family: 'DejaVuSans'; src: url(" +
        os.path.join(data_path, "fonts", "DejaVuSans-Bold.ttf") +
        "); font-weight: bold;}"
    )
    log.info(f"Creating '{filename}.pdf' and writing to '/{path}/'")
    with open(os.path.join(path, f"{filename}.pdf"), "w+b") as pdf_file:
        pisa.CreatePDF(soup.prettify(), dest=pdf_file)


def convert_to(path: str, file_format: str, news: list, filename: str, title: str):
    """
    Converts news to 'pdf' or 'html' format

    :param path : str
        directory path for 'pdf' or 'html' files
    :param file_format : str
        name to which format to convert
    :param news : list
        a list of 'Novelty' objects
    :param filename : str
        filename which consists of directory name or directory name and date
    :param title : str
        news feed title
    """
    log.info("Converting news to html format")
    if file_format == "pdf":
        template_name = "template_for_pdf.html"
    else:
        news = copy_images(news, filename, path)
        template_name = "template_for_html.html"
    data_path = os.getcwd()
    if not os.path.isdir("templates"):
        data_path = os.path.join(sys.path[-1], "rss_reader")
    with open(os.path.join(data_path, "templates", template_name), encoding="utf-8") as html_file:
        template = html_file.read()
    soup = create_soup(template, news, title)
    if not os.path.isdir(path):
        log.info(f"Creating directory '{path}' for files)")
        os.makedirs(path)
    if file_format == "pdf":
        create_pdf(soup, path, filename, data_path)
    elif file_format == "html":
        log.info(f"Creating '{filename}.html' and writing to '/{path}/'")
        with open(os.path.join(path, f"{filename}.html"), "w", encoding="utf-8") as html_file:
            html_file.write(soup.prettify())


def get_cached_news(directory: str, filename: str) -> list:
    """
    Deserializes the cache file.

    :param directory : str
        the name of the directory of cache files
    :param filename : str
        filename which consists of directory name or directory name and date

    :return cached_news_dicts : list
        list of deserialized dictionaries from the cache file
    """
    log.info(f"Deserializing '{filename}.json'")
    with open(os.path.join("cache", directory, f"{filename}.json"), "r") as json_file:
        cached_news_dicts = json.load(json_file)
    return cached_news_dicts


def print_news(news: list, title: str):
    """
    Prints news in stdout.

    :param news : list
        a list of 'Novelty' objects
    :param title : str
        news feed title
    """
    log.info("Printing news")
    print(f"\nFeed: {title}")
    for one_news in news:
        print("\n", one_news, "\n", sep="")


def process_output(json_print, to_pdf, to_html, filename, news, title):
    """
    Processes variables for data output.

    :param json_print : bool
        print result as JSON in stdout
    :param to_pdf : str
        contains the path for files converted to 'pdf' format
    :param to_html : str
        contains the path for files converted to 'html' format
    :param filename : str
        filename which consists of directory name or directory name and date
    :param news : list
        a list of 'Novelty' objects
    :param title : str
        news feed title
    """
    if to_pdf or to_html:
        if json_print:
            print_json(news)
        if to_pdf:
            convert_to(to_pdf, "pdf", news, filename, title)
        if to_html:
            convert_to(to_html, "html", news, filename, title)
    elif json_print:
        print_json(news)
    elif not json_print:
        print_news(news, title)


def main():
    """
    The main logic of the program.
    """
    sys.tracebacklimit = 0
    source, json_print, verbose, limit, date, to_pdf, to_html = parse_arguments()
    global log
    log = create_logger(verbose)
    log.debug(f"Program received: {source=} {json_print=} {verbose=} {limit=} {date=} {to_pdf=} {to_html=}")
    if date:
        is_date_valid(date)
    if source:
        response = get_response(source)
        if not response and not date:
            log.error("Exception occurred 'RuntimeError'")
            raise RuntimeError(f"Failed to get news from '{source}'")
        elif response:
            news, title = get_news(response)
        else:
            news, title = None, None
        directory = get_directory(source)
        filename = get_filename(directory, date)
        if news and not date:
            process_output(json_print, to_pdf, to_html, filename, news[:limit], title)
            cache_news(source, news)
        elif date:
            is_file(directory, filename)
            if not news and not title:
                title = filename
            elif news and title:
                cache_news(source, news)
            cached_news_dicts = get_cached_news(directory, filename)
            cached_news = create_news(cached_news_dicts)
            process_output(json_print, to_pdf, to_html, filename, cached_news[:limit], title)
    elif date and source is None:
        log.info("Getting list of cache directories")
        cache_dirs = list(os.walk("cache"))[0][1]
        flag = True
        for directory in cache_dirs:
            filename = get_filename(directory, date)
            title = filename
            if os.path.exists(os.path.join("cache", directory, f"{filename}.json")):
                cached_news_dicts = get_cached_news(directory, filename)
                cached_news = create_news(cached_news_dicts)
                process_output(json_print, to_pdf, to_html, filename, cached_news[:limit], title)
                flag = False
        if flag:
            log.error("Exception occurred 'FileNotFoundError'")
            raise FileNotFoundError(f"No cached news for '{date}' date")


log = create_logger(False)


if __name__ == "__main__":
    main()
