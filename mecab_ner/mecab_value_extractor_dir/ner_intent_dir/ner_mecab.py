from mecab_ner.mecab_value_extractor_dir import mecab_value_extractor as mve
from mecab_ner.mecab_value_extractor_dir.ner_intent_dir.utility_data import read_txt
BLANK_LIST = []
START_IDX = 0
END_IDX = 1
ONE_WORD = 1
POS_IDX = 1


class EntityMeCab:
    def __init__(self, data_path=''):
        self.entity_list = read_txt(data_path)
        self.mecab_value_extractor = mve.MeCabValueExtractor()

    def get_mecab_list(self, sentence):
        sentence_mecab_list = self.mecab_value_extractor.parse_compound(sentence)
        entity_contain_list = []

        for entity_item in self.entity_list:
            category, reading, mecab_reading = entity_item.split(",")
            if (pattern_list := mve.contain_pattern_list(mecab_reading.split(), sentence_mecab_list)) != BLANK_LIST:
                for pattern_item in pattern_list:
                    entity_contain_list.append((category, reading))
                    for pattern_idx_item in range(pattern_item[START_IDX], pattern_item[END_IDX], ONE_WORD):
                        sentence_mecab_list[pattern_idx_item] = ("*", sentence_mecab_list[pattern_idx_item][POS_IDX])
        return sentence_mecab_list, entity_contain_list


if __name__ == "__main__":
    entity_list_path = "../data_dir/entity_mecab/entity_food_fastfood_mecab.txt"
    e_s = EntityMeCab(entity_list_path)
    e_s_parse_list = e_s.get_mecab_list("흰수라를 먹고 싶어요")
    sentence_mecab_list, entity_contain_list = e_s_parse_list
    restored_val = mve.reverse_compound_parse(sentence_mecab_list)
    print(e_s_parse_list)
    print("추출 엔티티 : ", entity_contain_list)
    print("복구된 값 : ", restored_val)
