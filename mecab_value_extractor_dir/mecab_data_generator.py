import os
import csv
import mecab
import pandas as pd
import numpy as np
import mecab_value_extractor as mve
from mecab_value_extractor_dir.ner_intent_dir import utility_data

USER_SENTENCE = 1
CATEGORY = 3
MECAB_PARSE = 4
DIR_NAME = 0
FIRST_VAL = 0
STRING_NOT_FOUND = -1
ENTITY = 2
FILENAME_ONLY = 0
EXTENSION = -1

mecab = mecab.MeCab()


def get_mecab_value(compound_parse_str):
    for read_item in utility_data.read_txt():
        read_value, mecab_value = read_item.split(",")
        if (pattern_idx := compound_parse_str.find(read_value)) != STRING_NOT_FOUND:
            compound_parse_str = mve.string_replacer(compound_parse_str, read_value, pattern_idx, nofail=False)
            return compound_parse_str, read_value
    return False


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


def str_entity_mecab(dir_path):
    mecab_path = "./data_dir/intent_mecab/"
    mecab_value_extractor = mve.MeCabValueExtractor()
    txt_list = []

    for search_list in search_tsv(dir_path):
        category_list, filename = search_list
        for category_list_item in category_list:
            mecab_parsed_value = " ".join([x[mve.IDX_TOKEN] for x in mecab_value_extractor.parse_compound(category_list_item[MECAB_PARSE])])
            txt_list.append(category_list_item[CATEGORY] + "," + category_list_item[MECAB_PARSE] + "," + mecab_parsed_value)

        mecab_category_path = mecab_path + filename + "_mecab.txt"
        utility_data.write_txt(mecab_category_path, txt_list)


def string_ner():
    mecab_value_extractor = mve.MeCabValueExtractor()
    tmp_list = []

    is_same_cnt = 0
    for idx, csv_item in enumerate(utility_data.read_csv()):
        is_same = False

        # Do function
        compound_parse_list = mecab_value_extractor.parse_compound(csv_item[USER_SENTENCE])
        compound_parse_str = " ".join([x[0] for x in compound_parse_list])
        print(compound_parse_str)
        entity_contain_list = []

        save_data = csv_item[USER_SENTENCE]
        mecab_match_val = True
        while mecab_match_val:
            if mecab_match_val := get_mecab_value(save_data):
                compound_parse, read_value = mecab_match_val
                save_data = compound_parse
                print(idx, compound_parse)
                entity_contain_list.append(read_value)

        entity_contain_list.sort()

        # 2. get saved entity
        csv_entity_list = [x.strip() for x in csv_item[2].split(",")]
        csv_entity_list.sort()

        if all(elem in entity_contain_list for elem in csv_entity_list):
            print(idx, csv_item[USER_SENTENCE])
            is_same_cnt += 1
            is_same = True

        tmp_list.append([csv_item[USER_SENTENCE], csv_item[ENTITY], ", ".join(entity_contain_list), ", ".join(csv_entity_list), is_same])
    print(is_same_cnt, "/", len(utility_data.read_csv()))
    utility_data.write_csv(tmp_list)


if __name__ == "__main__":
    import time
    st = time.time()
    dir_path = "./data_dir/intent_original"
    txt_list = str_entity_mecab(dir_path)
    et = time.time()
    print(et-st)
