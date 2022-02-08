from mecab_value_extractor_dir.ner_intent_dir.utility_string import string_replacer
from mecab_value_extractor_dir.ner_intent_dir.utility_data import read_txt
STRING_NOT_FOUND = -1


class EntityString:
    def __init__(self, data_path=''):
        self.entity_list = read_txt(data_path)

    def get_sting_entity(self, sentence):
        for entity_item in self.entity_list:
            pattern_idx = sentence.find(entity_item)
            if pattern_idx != STRING_NOT_FOUND:
                sentence = string_replacer(sentence, entity_item, pattern_idx, nofail=False)
                return sentence, entity_item
        return False

    def get_entity_list(self, sentence):
        entity_contain_list = []
        mecab_match_val = True
        while mecab_match_val:
            mecab_match_val = self.get_sting_entity(sentence)
            entity_erased_sentence, entity_item = mecab_match_val
            sentence = entity_erased_sentence
            entity_contain_list.append(entity_item)
        return sentence, entity_contain_list


if __name__ == "__main__":
    entity_list_path = "../data_dir/entity_dump/call_center_entity.txt"
    e_s = EntityString(entity_list_path)
    ner_list = e_s.get_entity_list("약품 이름을 알려주세요")
    print(ner_list)