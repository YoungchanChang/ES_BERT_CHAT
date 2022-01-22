import os
import csv
import pandas as pd
import numpy as np

FILENAME_ONLY = 0
EXTENSION = -1


def search_tsv(dir_path):
    filenames = os.listdir(dir_path)
    for filename in filenames:
        full_filename = os.path.join(dir_path, filename)

        split_filename = os.path.splitext(filename)
        ext = split_filename[EXTENSION]
        file_name = split_filename[FILENAME_ONLY]


        category_list = []
        # 1. tsv파일 읽기
        if ext == '.tsv':
            # 1-1. 이름에 따라 대분류, 소분류 구분
            entity, large_category, sub_category = file_name.split("_")
            df = pd.read_csv(full_filename, sep='\t', encoding='utf-8-sig')

            # 1-2. 모든 컬럼에 대해 수행
            for df_column_item in df.columns:
                for df_row in df[df_column_item]:
                    if df_row is np.nan:
                        break
                    category_list.append([file_name, large_category, sub_category, df_column_item, df_row])

            yield category_list, file_name


def read_txt(data_path):
    with open(data_path, "r", encoding='utf-8-sig') as file:
        txt_list = file.read().splitlines()
        return sorted(list(txt_list), key=len, reverse=True)


def write_txt(data_path, txt_list, is_sort=False):
    if is_sort:
        txt_list = sorted(list(txt_list), key=len, reverse=True)

    with open(data_path, "w", encoding='UTF8') as file:
        for txt_item in txt_list:
            data = str(txt_item) + "\n"
            file.write(data)


def read_csv(data_dir):
    with open(data_dir, 'r', encoding='utf-8-sig') as reader_csv:
        reader = csv.reader(reader_csv, delimiter=',')
        return list(reader)


def write_csv(data_dir, csv_list):
    with open(data_dir, 'w', encoding='utf-8-sig', newline='') as writer_csv:
        writer = csv.writer(writer_csv, delimiter=',')
        for idx, csv_item in enumerate(csv_list):
            writer.writerow([idx, *csv_item])