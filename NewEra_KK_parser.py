import re

DATE_LENGTH = 10
NON_BREAKING_SPACE_UNICODE = u"\u00A0"
SPACE_CHAR = " "
SENTENCE_PATTERN_REGEX = "(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!|\")\s"
PROBLEMATIC_CHARS = ["ǂ", "ǁ", "ǀ", "ǃ", "!", "?", "/", "\\", '"', "*", ":", "<", ">", "|"]
DATE_AND_AUTHOR_TAG = "new-item-date"
TITLE_TAG = "single-title"
ARTICLE_BODY_TAG = "single-content"


class NewEraKKParser:
    """
    Web raw text parser of data received from a NewEraKKScraper object.
    Receives a BeautifulSoup object and parse the text in it according to the specific requirements
    of the project.
    """
    def parse_single_article(self, page_raw_text, url):
        """
        parses a single article
        :param page_raw_text: a BeautifulSoup object which contains the raw text of the web page
        :return: a list which contains the title, the date, the author and the body of the article
        """
        title = page_raw_text.findAll(class_=TITLE_TAG)[0].text.strip()
        title = title.replace(NON_BREAKING_SPACE_UNICODE, SPACE_CHAR)
        title = self._clean_quotes(title)
        date_author = page_raw_text.find(class_=DATE_AND_AUTHOR_TAG).text
        date = date_author[:DATE_LENGTH]
        author_name = date_author[DATE_LENGTH:].strip()
        body = page_raw_text.findAll(class_=ARTICLE_BODY_TAG)[0].text
        body_txt_list = self._sentences_to_lines(body)
        trimming_idx = body_txt_list[-1].find(date)     # trimming the date and author name which appear in the end of the article
        body_txt_list[-1] = body_txt_list[-1][:trimming_idx]
        while body_txt_list[-1] in ["\n", "\r", "", " "]:
            body_txt_list.pop()
        for i in range(len(body_txt_list)):          # cleaning each sentence from unwanted " and '
            body_txt_list[i] = self._clean_quotes(body_txt_list[i])
        article_id = self._create_article_id(title, date)
        return [article_id, title, date, author_name, url] + body_txt_list

    def _create_article_id(self, title, date):
        first_word = title.split()[0]
        for char in PROBLEMATIC_CHARS:
            if char in first_word:
                first_word = first_word.replace(char, "")
        date = date[2:].replace("-", "")            # processing the date according to the file naming convention
        return "KK-NEWS-" + date + "-" + first_word

    def _sentences_to_lines(self, txt_str):
        """
        :param txt_str: txt of an article
        :return: the required separated str
        """
        article_txt = txt_str.replace(NON_BREAKING_SPACE_UNICODE, SPACE_CHAR)
        sentences_list = re.split(SENTENCE_PATTERN_REGEX, article_txt)
        for sentence in sentences_list:
            sentence.strip()                            # cut all unnecessary spaces
        return sentences_list

    def _clean_quotes(self, str_to_clean):
        str_to_clean = str_to_clean.replace('"', '“')
        return str_to_clean.replace("'", "’")