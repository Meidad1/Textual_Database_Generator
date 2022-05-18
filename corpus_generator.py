import os
import shutil
import pandas
from NewEra_KK_scraper import *
from NewEra_KK_parser import *

METADATA_FIELDS = "ID,Title,Date,Author,Khoekhoe Translation URL\n"
CONTENT_TABLE_FIELDS = "TextID,SentenceID,Khoekhoe\n"
CSV_METADATA_TXT_PATH = "meta_csv.txt"
CSV_CONTENT_TXT_PATH = "content_csv.txt"
ARTICLES_SEPARATOR = "\n------------------------------------------------------------------------------------------------------------------------\n\n"
TITLE_IDX_ART = 1
CONTENT_IDX_ART = 5


class KKCorpusGenerator:

    def __init__(self):
        self._articles_list = []                # a list of lists of the parsed articles.
                                                # Each kk_article_list is followed by its equivalent English_article_list

    def generate_KK_corpus(self, kk_urls_file_path, en_urls_file_path):
        """
        Fills _articles_list with content: it contains elements of kk_article, which followed by the equivalent English
        article elements. It creates also text files of the csv tables (only for KK material).
        :param kk_urls_file_path: urls of kk articles
        :param en_urls_file_path: urls of the original English articles. The urls must be in the same order of kk_urls_file_path!
        :return: None
        """
        scraper = NewEraKKScraper()
        parser = NewEraKKParser()
        meta_txt_file = open(CSV_METADATA_TXT_PATH, "w", encoding='utf8')
        meta_txt_file.write(METADATA_FIELDS)
        content_table_txt_file = open(CSV_CONTENT_TXT_PATH, "w", encoding='utf8')
        content_table_txt_file.write(CONTENT_TABLE_FIELDS)
        with open(kk_urls_file_path, 'r') as kk_input_file:
            all_kk_urls = kk_input_file.readlines()       # reading the kk urls to a list
        with open(en_urls_file_path, 'r') as en_input_file:
            all_en_urls = en_input_file.readlines()       # reading the kk urls to a list

        cur_url_idx = 0
        while cur_url_idx < len(all_kk_urls):
            kk_url = all_kk_urls[cur_url_idx].strip()            # cut new line char and other space chars
            en_url = all_en_urls[cur_url_idx].strip()
            kk_raw_text = scraper.retrieve_raw_text_from_single_url(kk_url)
            en_raw_text = scraper.retrieve_raw_text_from_single_url(en_url)
            parsed_kk_text = parser.parse_single_article(kk_raw_text, kk_url)
            parsed_en_text = parser.parse_single_article(en_raw_text, en_url)
            self._articles_list.append(parsed_kk_text)
            self._articles_list.append(parsed_en_text)

            article_id = parsed_kk_text[0]
            cur_meta_str = ",".join(parsed_kk_text[TITLE_IDX_ART+1:CONTENT_IDX_ART]) + "\n"
            cur_meta_str = article_id + ',"' + parsed_kk_text[TITLE_IDX_ART] + '",' + cur_meta_str     # adding quote chars to the title
            meta_txt_file.write(cur_meta_str)                 # writing to the kk metadata_csv txt file

            for i in range(len(parsed_kk_text[CONTENT_IDX_ART:])):
                cur_line_list = [article_id, str(i+1), parsed_kk_text[CONTENT_IDX_ART + i]]
                cur_line_str = ",".join(cur_line_list[:-1]) + ',"' + cur_line_list[-1] + '"\n'
                content_table_txt_file.write(cur_line_str)    # writing to the kk content_csv txt file

            cur_url_idx += 1

        meta_txt_file.close()
        content_table_txt_file.close()

    def export_articles_to_excel(self):
        tables_output_dir_path = "output_tables"
        if os.path.exists(tables_output_dir_path):        # override an existing output directory
            shutil.rmtree(tables_output_dir_path)
        os.makedirs(tables_output_dir_path)

        # Creating the metadata table
        read_file = pandas.read_csv(CSV_METADATA_TXT_PATH)
        # read_file.to_csv(r"output_tables\metadata.csv", index=None)       # if we want, we can create a csv file as well
        read_file.to_excel(r"output_tables\metadata.xlsx", index=None, header=True)

        # Creating the content table
        read_file = pandas.read_csv(CSV_CONTENT_TXT_PATH)
        # read_file.to_csv(r"output_tables\articles_content.csv", index=None)
        read_file.to_excel(r"output_tables\articles_content.xlsx", index=None, header=True)

    def export_articles_to_txt_files(self):
        txt_output_dir_path = "output_txt"
        if os.path.exists(txt_output_dir_path):             # override an existing output directory
            shutil.rmtree(txt_output_dir_path)
        os.makedirs(txt_output_dir_path)

        i = 0
        while i < len(self._articles_list):
            article_id = self._articles_list[i][0]
            with open(txt_output_dir_path + "\\" + article_id + ".txt", 'w', encoding='utf8') as file:
                for item in self._articles_list[i]:             # writing the KK text
                    file.write(item)
                    file.write('\n')
                file.write(ARTICLES_SEPARATOR)
                for item_idx in range(1, len(self._articles_list[i+1])):          # writing the English equivalent text
                    file.write(self._articles_list[i+1][item_idx])                # skipping the first item, which is the article_id
                    file.write('\n')
            i += 2                                            # jumping to the next KK article
