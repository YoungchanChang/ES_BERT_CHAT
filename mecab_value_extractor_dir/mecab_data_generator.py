import mecab
import mecab_value_extractor as mve
from mecab_value_extractor_dir.ner_intent_dir import utility_data, utility_string

USER_SENTENCE = 1
CATEGORY = 3
MECAB_PARSE = 4
DIR_NAME = 0
FIRST_VAL = 0
STRING_NOT_FOUND = -1
ENTITY = 2
TITLE = 0
SPECIFIC_WORD = 4
DATA_CATEGORY = 1

mecab = mecab.MeCab()





def str_entity_mecab(dir_path):
    mecab_path = "./data_dir/intent_mecab/"
    mecab_value_extractor = mve.MeCabValueExtractor()
    txt_list = []

    for search_list in utility_data.search_tsv(dir_path):
        category_list, filename = search_list
        for category_list_item in category_list:
            mecab_parsed_value = " ".join([x[mve.IDX_TOKEN] for x in mecab_value_extractor.parse_compound(category_list_item[MECAB_PARSE])])
            txt_list.append(category_list_item[CATEGORY] + "," + category_list_item[MECAB_PARSE] + "," + mecab_parsed_value)

        mecab_category_path = mecab_path + filename + "_mecab.txt"
        utility_data.write_txt(mecab_category_path, txt_list)

def main():
    import time
    st = time.time()
    dir_path = "./data_dir/intent_original"
    txt_list = str_entity_mecab(dir_path)
    et = time.time()
    print(et-st)


def test_sentence_generator():
    entity_dir_path = "./data_dir/entity_original"
    intent_dir_path = "./data_dir/intent_original"

    example_data_gen = []
    for entity_search_list in utility_data.search_tsv(entity_dir_path):
        entity_category_list, filename = entity_search_list
        for entity_category_item in entity_category_list:
            entity_list = entity_category_item[TITLE].split("_")
            print(entity_category_item)

            for intent_search_list in utility_data.search_tsv(intent_dir_path):
                intent_category_list, filename = intent_search_list
                for intent_category_item in intent_category_list:
                    intent_list = intent_category_item[TITLE].split("_")
                    if entity_list[DATA_CATEGORY] == intent_list[DATA_CATEGORY]:
                        josa_sbj = utility_string.get_marker(entity_category_item[SPECIFIC_WORD], "josa_sbj")
                        example_data_gen.append(str(entity_category_item[SPECIFIC_WORD]) + str(josa_sbj) + " " + str(intent_category_item[SPECIFIC_WORD]))
                        print(intent_category_item)

    with open("test_dir/text_write.txt", "w", encoding='UTF8') as file:
        for test in example_data_gen:
            data = test + "\n"
            file.write(data)

if __name__ == "__main__":
    # main()
    test_sentence_generator()