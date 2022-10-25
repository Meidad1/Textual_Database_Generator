from ArticlesParser import *

DATE_LENGTH = 10
NON_BREAKING_SPACE_UNICODE = u"\u00A0"
SPACE_CHAR = " "
DATE_AND_AUTHOR_TAG = "new-item-date"
TITLE_TAG = "single-title"
ARTICLE_BODY_TAG = "single-content"


class NewEraKKParser(ArticlesParser):
    """
    Inherits from ArticlesParser.
    Web raw text parser of data received from a NewEraKKScraper object.
    Receives a BeautifulSoup object and parse the text in it according to the specific requirements
    of the project.
    """
    def parse_single_article(self, page_raw_text, url):
        """
        parses a single article
        :param page_raw_text: a BeautifulSoup object which contains the raw text of the web page
        :return: a list which contains the title, the date, the author and the body of the article
        :param url: a string of the url to be parsed
        """
        title = page_raw_text.findAll(class_=TITLE_TAG)[0].text.strip()
        title = title.replace(NON_BREAKING_SPACE_UNICODE, SPACE_CHAR)
        title = title.replace(SOFT_HYPHEN, "")
        title = self._clean_quotes(title)
        date_author = page_raw_text.find(class_=DATE_AND_AUTHOR_TAG).text
        date = date_author[:DATE_LENGTH]
        author_name = date_author[DATE_LENGTH:].strip()
        body = page_raw_text.findAll(class_=ARTICLE_BODY_TAG)[0].text

        first_line = page_raw_text.find(class_=ARTICLE_BODY_TAG).find("p").text
        if author_name == 'Staff Reporter' and len(list(first_line)) == 2:      # when the author is written as the first line of the article
            author_name = first_line
            body = body[len(author_name):]                      # cut the name from the body of the article

        body_txt_list = self._sentences_to_lines(body)
        trimming_idx = body_txt_list[-1].find(date)     # trimming the date and author name which appear in the end of the article
        body_txt_list[-1] = body_txt_list[-1][:trimming_idx]
        while body_txt_list[-1] in ["\n", "\r", "", " "]:
            body_txt_list.pop()
        for i in range(len(body_txt_list)):            # cleaning each sentence from unwanted " and '
            body_txt_list[i] = self._clean_quotes(body_txt_list[i])
        article_id = self._create_article_id(title, date)
        return [article_id, title, date, author_name, url, ""] + body_txt_list

    def _create_article_id(self, title, date=None):                         # overriding of the method
        article_id = super()._create_article_id(title)
        date = date[2:].replace("-", "")                # processing the date according to the file naming convention
        return "KK-NEWS-" + date + "-" + article_id
