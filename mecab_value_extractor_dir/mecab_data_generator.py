import os
import pandas as pd
import numpy as np
import mecab_value_extractor as mve
import csv
USER_SENTENCE = 1
CATEGORY = 3
MECAB_PARSE = 4
DIR_NAME = 0
FIRST_VAL = 0
STRING_NOT_FOUND = -1
ENTITY = 2

import mecab
mecab = mecab.MeCab()

def read_txt():
    with open("entity_dir/entity_dump/call_center_entity_mecab.txt", "r", encoding='utf-8-sig') as file:
        txt_list = file.read().splitlines()
        return sorted(list(txt_list), key=len, reverse=True)


def get_mecab_value(compound_parse_str):
    for read_item in read_txt():
        read_value, mecab_value = read_item.split(",")
        if (pattern_idx := compound_parse_str.find(read_value)) != STRING_NOT_FOUND:
            compound_parse_str = mve.string_replacer(compound_parse_str, read_value, pattern_idx, nofail=False)
            return compound_parse_str, read_value
    return False


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


def write_txt(dir_name, txt_list):
    with open(f"entity_dir/entity_mecab/{dir_name}_mecab.txt", "w", encoding='UTF8') as file:
        for txt_item in txt_list:
            data = txt_item + "\n"
            file.write(data)


def read_csv():
    with open('./test_file/call_center_data/call_center_entity.csv', 'r', encoding='utf-8-sig') as reader_csv:
        reader = csv.reader(reader_csv, delimiter=',')
        return list(reader)


def write_csv(csv_list):
    with open('./test_file/call_center_entity.csv', 'w', encoding='utf-8-sig', newline='') as writer_csv:
        writer = csv.writer(writer_csv, delimiter=',')
        for idx, csv_item in enumerate(csv_list):
            writer.writerow([idx, *csv_item])


def string_ner():
    mecab_value_extractor = mve.MeCabValueExtractor()
    tmp_list = []

    is_same_cnt = 0
    for idx, csv_item in enumerate(read_csv()):
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
    print(is_same_cnt, "/", len(read_csv()))
    write_csv(tmp_list)


if __name__ == "__main__":
    import time
    st = time.time()
    string_ner()
    et = time.time()
    print(et-st)
