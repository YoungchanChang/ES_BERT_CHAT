import os
import pandas as pd
import numpy as np
import mecab_value_extractor as mve

CATEGORY = 3
MECAB_PARSE = 4
DIR_NAME = 0
FIRST_VAL = 0


def search_tsv():
    dirname = "./entity_dir/entity_original"
    filenames = os.listdir(dirname)
    for filename in filenames:
        full_filename = os.path.join(dirname, filename)
        ext = os.path.splitext(full_filename)[-1]

        category_list = []
        # 1. tsv파일 읽기
        if ext == '.tsv':
            # 1-1. 이름에 따라 대분류, 소분류 구분
            file_name = os.path.splitext(filename)[0]
            entity, large_category, sub_category = file_name.split("_")
            df = pd.read_csv(full_filename, sep='\t', encoding='utf-8-sig')

            # 1-2. 모든 컬럼에 대해 수행
            for df_column_item in df.columns:
                for df_row in df[df_column_item]:
                    if df_row is np.nan:
                        break
                    category_list.append([file_name, large_category, sub_category, df_column_item, df_row])

        yield category_list


def write_txt(dir_name, txt_list):
    with open(f"entity_dir/entity_mecab/{dir_name}_mecab.txt", "w", encoding='UTF8') as file:
        for txt_item in txt_list:
            data = txt_item + "\n"
            file.write(data)


def str_entity_mecab():
    mecab_value_extractor = mve.MeCabValueExtractor()
    txt_list = []

    for search_list in search_tsv():
        for search_list_item in search_list:
            mecab_parsed_value = " ".join([x[mve.IDX_TOKEN] for x in mecab_value_extractor.parse_compound(search_list_item[MECAB_PARSE])])
            txt_list.append(search_list_item[CATEGORY] + "," + search_list_item[MECAB_PARSE] + "," + mecab_parsed_value)
        write_txt(search_list[FIRST_VAL][DIR_NAME], txt_list)


if __name__ == "__main__":
    str_entity_mecab()

