from web_scraper import *

CSV_METADATA_TXT_PATH = "meta_csv.txt"
CSV_CONTENT_TXT_PATH = "content_csv.txt"
ARTICLES_SEPARATOR = "\n------------------------------------------------------------------------------------------------------------------------\n\n"
TITLE_IDX_ART = 1
CONTENT_IDX_ART = 5


class CorpusGenerator:
    """
    A general corpus generator.
    """
    def __init__(self, parser, metadata_fields, content_table_fields):
        """
        A constructor of CorpusGenerator.
        :param parser: a parser of type (or a child of) ArticlesParser
        """
        self.parser = parser
        self.metadata_fields = metadata_fields
        self.content_table_fields = content_table_fields
        self._articles_list = []                                     # a list of lists of the parsed articles.
        self.scraper = WebScraper()

    def generate_corpus(self, urls_file_path, en_urls_file_path=None):
        """
        Fills _articles_list with content: it contains elements of lug_article, which followed by the equivalent English
        article elements. It creates also text files of the csv tables.
        :param en_urls_file_path: urls of English equivalents articles
        :param urls_file_path: urls of articles
        :return: None
        """
        meta_txt_file = open(CSV_METADATA_TXT_PATH, "w", encoding='utf8')
        meta_txt_file.write(self.metadata_fields)
        content_table_txt_file = open(CSV_CONTENT_TXT_PATH, "w", encoding='utf8')
        content_table_txt_file.write(self.content_table_fields)
        with open(urls_file_path, 'r') as input_file:
            all_urls = input_file.readlines()                        # reading the urls to a list

        if en_urls_file_path is not None:
            with open(en_urls_file_path, 'r') as en_input_file:
                all_en_urls = en_input_file.readlines()  # reading the kk urls to a list

        cur_url_idx = 0
        while cur_url_idx < len(all_urls):
            url = all_urls[cur_url_idx].strip()                  # cut new line char and other space chars
            raw_text = self.scraper.retrieve_raw_text_from_single_url(url)
            parsed_text = self.parser.parse_single_article(raw_text, url)
            self._articles_list.append(parsed_text)

            if en_urls_file_path is not None:                   # if there is an English version
                en_url = all_en_urls[cur_url_idx].strip()
                en_raw_text = self.scraper.retrieve_raw_text_from_single_url(en_url)
                parsed_en_text = self.parser.parse_single_article(en_raw_text, en_url)
                self._articles_list.append(parsed_en_text)

            article_id = parsed_text[0]
            cur_meta_str = ",".join(parsed_text[TITLE_IDX_ART+1:CONTENT_IDX_ART]) + "\n"
            cur_meta_str = article_id + ',"' + parsed_text[TITLE_IDX_ART] + '",' + cur_meta_str     # adding quote chars to the title
            meta_txt_file.write(cur_meta_str)                 # writing to the kk metadata_csv txt file

            first_content_line_list = [article_id, '1', parsed_text[TITLE_IDX_ART]]
            first_line_str = ",".join(first_content_line_list[:-1]) + ',"' + first_content_line_list[-1] + '"\n'
            content_table_txt_file.write(first_line_str)
            for i in range(2, len(parsed_text[CONTENT_IDX_ART:])):
                cur_line_list = [article_id, str(i), parsed_text[CONTENT_IDX_ART + i-1]]
                cur_line_str = ",".join(cur_line_list[:-1]) + ',"' + cur_line_list[-1] + '"\n'

                content_table_txt_file.write(cur_line_str)    # writing to the kk content_csv txt file

            cur_url_idx += 1

        meta_txt_file.close()
        content_table_txt_file.close()

        return self._articles_list
