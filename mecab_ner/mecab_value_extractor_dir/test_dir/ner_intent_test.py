import os
from mecab_value_extractor_dir.ner_intent_dir import utility_data, ner_string, ner_mecab

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

entity_dir_path = PARENT_DIR + "/data_dir/entity_mecab"
intent_dir_path = PARENT_DIR + "/data_dir/intent_mecab"

entity_filenames = os.listdir(entity_dir_path)
intent_filenames = os.listdir(intent_dir_path)

FILENAME_ONLY = 0
USER_SENTENCE = 1
ENTITY = 2
LARGE_CATEGORY = 1
SMALL_CATEGORY = 2
ENTITY_INTENT_CLASS = 0
ONLY_ONE_VALUE = 0
CATEGORY = 0
VALUE = 1
BLANK_LIST = []


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


def get_entity_intent(sentence):
    entity_list = []
    intent_list = []

    # 1. 엔티티 매칭데이터 확인하기
    for entity_search_list in entity_filenames:
        data_copy = sentence
        entity_data_path = os.path.join(entity_dir_path, entity_search_list)
        e_m = ner_mecab.EntityMeCab(entity_data_path)
        sentence_mecab_list, entity_contain_list = e_m.get_mecab_list(data_copy)

        # 1-1.카테고리에 해당되는 엔티티가 있을 때 저장
        if entity_contain_list != BLANK_LIST:
            split_filename = os.path.splitext(entity_search_list)
            file_name = split_filename[FILENAME_ONLY]
            file_split_list = file_name.split("_")
            entity_list.append(
                [file_split_list[ENTITY_INTENT_CLASS], file_split_list[LARGE_CATEGORY], file_split_list[SMALL_CATEGORY],
                 entity_contain_list[ONLY_ONE_VALUE][VALUE]])

    # 2. 인텐트 매칭 데이터 확인하기
    for intent_search_list in intent_filenames:
        data_copy = sentence
        intent_data_path = os.path.join(intent_dir_path, intent_search_list)
        i_m = ner_mecab.EntityMeCab(intent_data_path)
        sentence_mecab_list, intent_contain_list = i_m.get_mecab_list(data_copy)

        # 2-1.카테고리에 해당되는 엔티티가 있을 때 저장
        if intent_contain_list != BLANK_LIST:
            split_filename = os.path.splitext(intent_search_list)
            file_name = split_filename[FILENAME_ONLY]
            file_split_list = file_name.split("_")
            intent_list.append([file_split_list[ENTITY_INTENT_CLASS], file_split_list[LARGE_CATEGORY], file_split_list[SMALL_CATEGORY],
                 intent_contain_list[ONLY_ONE_VALUE][CATEGORY]])

    # 3. 같은 카테고리에 있는 엔티티 인텐트 매칭하기
    for entity_item in entity_list:
        for intent_item in intent_list:
            if entity_item[LARGE_CATEGORY] == intent_item[LARGE_CATEGORY]:
                yield sentence, *entity_item, *intent_item


def test_ner_intent():
    example_data = "./entity_intent_example.txt"
    data_parse_list = []
    # 1. 예시 데이터 불러오기
    for data_item in utility_data.read_txt(example_data)[:5]:
        data_parse_list.append(get_entity_intent(data_item))

    utility_data.write_csv("tmp.csv", data_parse_list)


if __name__ == "__main__":
    import time
    st = time.time()
    test_ner_intent()
    et = time.time()
    print(et-st)