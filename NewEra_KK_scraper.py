from bs4 import BeautifulSoup
import requests


class NewEraKKScraper:
    """
    A class which represents a scraper of web pages written in Khoekhoe from the official website
    of New Era news (NEPC).
    """
    def retrieve_raw_text_from_single_url(self, url):
        """
        Retrieves html txt from a certain url (a KK newspaper web) and write the data to a text file.
        :param url: A string of the requested URL
        :return: an object of BeautifulSoup which consists of the raw text of the page
        """
        request = requests.get(url, timeout=(5, 20))
        return BeautifulSoup(request.content, "html.parser")
