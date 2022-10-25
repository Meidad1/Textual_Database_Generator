import sys
import os
import output_files_exporter
from corpus_generator import *
from NewEra_KK_parser import *
from Bukedde_lug_parser import *
AVAILABLE_LANGUAGES = ["KK", "LUG"]
KK_METADATA_FIELDS = "ID,Title,Date,Author,Khoekhoe Translation URL\n"
KK_CONTENT_TABLE_FIELDS = "TextID,SentenceID,Khoekhoe\n"
LUG_METADATA_FIELDS = "ID,Title,Date,Author,Bukedde URL\n"
LUG_CONTENT_TABLE_FIELDS = "TextID,SentenceID,Luganda\n"
CSV_METADATA_TXT_PATH = "meta_csv.txt"
CSV_CONTENT_TXT_PATH = "content_csv.txt"
INVALID_INPUT_MSG = "The input arguments line must be as follows:\n<KK> <NewEra URLs file path> <ENG URLs file path>\nOR\n<LUG> <Bukedde URLs file path>"


def does_file_exist(file_name):
    """
    Checks whether a file exists.
    :param file_name: A string of a file path.
    :return: True - if the file exists, otherwise - False.
    """
    file_exists = True
    if not os.path.isfile(file_name):
        return False
    return file_exists


def check_input_args(args):
    """
    checks the validity of the user arguments
    :param args: a list of the arguments
    :return: if input is valid - true, otherwise a msg is printed
    """
    if args[0] not in AVAILABLE_LANGUAGES:
        print(INVALID_INPUT_MSG)
        return
    if args[0] == "LUG":
        if len(args) != 2:
            print(INVALID_INPUT_MSG)
        elif not does_file_exist(args[1]):
            print("Bukedde URLs file does not exist.")
    elif args[0] == "KK":
        if len(args) != 3:
            print(INVALID_INPUT_MSG)
        elif not does_file_exist(args[1]):
            print("The provided KK URLs file does not exist.")
        elif not does_file_exist(args[2]):
            print("The provided ENG URLs file does not exist.")
        else:
            return True


def run_corpus_generator():
    args_lst = sys.argv[1:]
    if not check_input_args(args_lst):
        return
    articles_list = []
    if args_lst[0] == "KK":
        kk_urls_file_path = args_lst[1]
        en_urls_file_path = args_lst[2]
        generator = CorpusGenerator(NewEraKKParser(), KK_METADATA_FIELDS, KK_CONTENT_TABLE_FIELDS)
        articles_list = generator.generate_corpus(kk_urls_file_path, en_urls_file_path)
    elif args_lst[0] == "LUG":
        lug_urls_file_path = args_lst[1]
        generator = CorpusGenerator(BukeddeLugParser(), LUG_METADATA_FIELDS, LUG_CONTENT_TABLE_FIELDS)
        articles_list = generator.generate_corpus(lug_urls_file_path)

    output_files_exporter.export_kk_articles_to_txt_files(articles_list)
    output_files_exporter.export_articles_to_excel()


if __name__ == '__main__':
    run_corpus_generator()

