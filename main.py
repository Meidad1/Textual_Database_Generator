import sys
import os
from corpus_generator import *
AVAILABLE_LANGUAGES = ["KK", "Khoekhoe"]

CSV_METADATA_TXT_PATH = "meta_csv.txt"
CSV_CONTENT_TXT_PATH = "content_csv.txt"

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
    :return: if input is valid - true, otherwise a msg
    """
    if len(args) != 3 or (args[2] not in AVAILABLE_LANGUAGES):
        print("Invalid input.")
        print("The arguments line must be as follows:\n<KK/LUG URLs file path> <ENG URLs file path> <KK / LUG>")
        return
    elif not does_file_exist(args[0]):
        print("KK/LUG URLs file does not exist.")
    elif not does_file_exist(args[1]):
        print("ENG URLs file does not exist.")
    else:
        return True


def run_corpus_generator():
    args_lst = sys.argv[1:]
    input_validity = check_input_args(args_lst)
    if input_validity is not True:
        return
    kk_urls_file_path = args_lst[0]
    en_urls_file_path = args_lst[1]
    generator = KKCorpusGenerator()
    generator.generate_KK_corpus(kk_urls_file_path, en_urls_file_path)
    generator.export_articles_to_txt_files()
    generator.export_articles_to_excel()


if __name__ == '__main__':
    run_corpus_generator()

