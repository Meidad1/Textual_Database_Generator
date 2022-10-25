import os
import shutil
import pandas

CSV_METADATA_TXT_PATH = "meta_csv.txt"
CSV_CONTENT_TXT_PATH = "content_csv.txt"
ARTICLES_SEPARATOR = "\n------------------------------------------------------------------------------------------------------------------------\n\n"


def export_articles_to_excel():
    tables_output_dir_path = "output_tables"
    if os.path.exists(tables_output_dir_path):  # override an existing output directory
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


def export_kk_articles_to_txt_files(articles_list):
    txt_output_dir_path = "output_txt"
    if os.path.exists(txt_output_dir_path):                  # override an existing output directory
        shutil.rmtree(txt_output_dir_path)
    os.makedirs(txt_output_dir_path)

    i = 0
    while i < len(articles_list):
        article_id = articles_list[i][0]
        with open(txt_output_dir_path + "\\" + article_id + ".txt", 'w', encoding='utf8') as file:
            for item in articles_list[i]:                         # writing the KK text
                file.write(item)
                file.write('\n')
            file.write(ARTICLES_SEPARATOR)
            for item_idx in range(1, len(articles_list[i + 1])):  # writing the English equivalent text
                file.write(articles_list[i + 1][item_idx])  # skipping the first item, which is the article_id
                file.write('\n')
        i += 2  # jumping to the next KK article


def export_lug_articles_to_txt_files(articles_list):
    pass
