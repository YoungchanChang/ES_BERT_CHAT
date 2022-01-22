import os
from mecab_value_extractor_dir.ner_intent_dir import ner_string, ner_mecab, utility_data

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

USER_SENTENCE = 1
ENTITY = 2


def test_ner_string():
    entity_list_path = PARENT_DIR + "/entity_dir/entity_dump/call_center_entity.txt"
    csv_dir = PARENT_DIR + "/test_dir/call_center_data/call_center.csv"
    write_dir = "tmp.csv"

    e_s = ner_string.EntityString(entity_list_path)
    is_same_cnt = 0
    tmp_list = []

    for idx, csv_item in enumerate(utility_data.read_csv(csv_dir)):
        is_same = False
        ner_list = e_s.get_entity_list(csv_item[USER_SENTENCE])
        sentence, entity_contain_list = ner_list
        entity_contain_list.sort()

        csv_entity_list = [x.strip() for x in csv_item[2].split(",")]
        csv_entity_list.sort()

        if all(elem in entity_contain_list for elem in csv_entity_list):
            print(idx, csv_item[USER_SENTENCE])
            is_same_cnt += 1
            is_same = True

        tmp_list.append([csv_item[USER_SENTENCE], csv_item[ENTITY], ", ".join(entity_contain_list), ", ".join(csv_entity_list), is_same])
    print(is_same_cnt, "/", len(utility_data.read_csv(csv_dir)))
    utility_data.write_csv(write_dir, tmp_list)


def test_ner_mecab():
    entity_list_path = PARENT_DIR + "/entity_dir/entity_dump/call_center_entity_mecab.txt"
    csv_dir = PARENT_DIR + "/test_dir/call_center_data/call_center.csv"
    write_dir = "tmp_mecab.csv"

    e_m = ner_mecab.EntityMeCab(entity_list_path)
    is_same_cnt = 0
    tmp_list = []

    for idx, csv_item in enumerate(utility_data.read_csv(csv_dir)):
        is_same = False
        ner_list = e_m.get_mecab_list(csv_item[USER_SENTENCE])
        sentence, entity_contain_list = ner_list
        entity_contain_list.sort()

        csv_entity_list = [x.strip() for x in csv_item[2].split(",")]
        csv_entity_list.sort()

        if all(elem in entity_contain_list for elem in csv_entity_list):
            print(idx, csv_item[USER_SENTENCE])
            is_same_cnt += 1
            is_same = True

        tmp_list.append([csv_item[USER_SENTENCE], csv_item[ENTITY], ", ".join(entity_contain_list), ", ".join(csv_entity_list), is_same])
    print(is_same_cnt, "/", len(utility_data.read_csv(csv_dir)))
    utility_data.write_csv(write_dir, tmp_list)


def ner_intent_match():
    example_data = "./entity_intent_example.txt"
    entity_dir_path = PARENT_DIR + "/data_dir/entity_mecab"
    intent_dir_path = PARENT_DIR + "/data_dir/intent_mecab"
    write_dir = "tmp_mecab.csv"
    filenames = os.listdir(entity_dir_path)

    for data_item in utility_data.read_txt(example_data):
        print(data_item)

        for entity_search_list in filenames:
            entity_data_path = os.path.join(entity_dir_path, entity_search_list)
            e_m = ner_mecab.EntityMeCab(entity_data_path)
            sentence_mecab_list, entity_contain_list = e_m.get_mecab_list(data_item)
            print(sentence_mecab_list, entity_contain_list)

        # is_same_cnt = 0
        # tmp_list = []
        #
        # for entity_category_item in entity_category_list:
        #     entity_list = entity_category_item[TITLE].split("_")
        #
        #     for intent_search_list in utility_data.search_tsv(intent_dir_path):
        #         intent_category_list, filename = intent_search_list
        #         for intent_category_item in intent_category_list:
        #             intent_list = intent_category_item[TITLE].split("_")
        #             if entity_list[DATA_CATEGORY] == intent_list[DATA_CATEGORY]:
        #                 josa_sbj = utility_string.get_marker(entity_category_item[SPECIFIC_WORD], "josa_sbj")
        #                 example_data_gen.append(str(entity_category_item[SPECIFIC_WORD]) + str(josa_sbj) + " " + str(intent_category_item[SPECIFIC_WORD]))
        #                 print(intent_category_item)
        #

if __name__ == "__main__":
    import time
    st = time.time()
    ner_intent_match()
    et = time.time()
    print(et-st)