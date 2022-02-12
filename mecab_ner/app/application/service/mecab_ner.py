from typing import List, Generator

from mecab_ner.app.application.service.mecab_generator import MecabGenerator
from mecab_ner.app.application.service.mecab_parser import MeCabParser
from mecab_ner.app.domain.entity import MecabCategory
from mecab_ner.app.utility.mecab_helper import contain_pattern_list


class MeCabNer:

    MIN_MEANING = 2
    START_IDX = 0
    END_IDX = 1
    ONE_WORD = 1
    MECAB_FEATURE_IDX = 1
    WORD_IDX = 0

    def __init__(self):

        storage_path = "/Users/youngchan/Desktop/ES_BERT_CHAT/mecab_ner/datas/entities/storage"

        self.mecab_generator = MecabGenerator(storage_path=storage_path)
        self.gen_all_mecab_category_data = self.mecab_generator.gen_all_mecab_category_data(storage_path=self.mecab_generator.mecab_path, need_parser=False)

    def get_category_entity(self, sentence: str) -> Generator:
        """ mecab 저장 데이터와 storage 데이터의 길이가 같은지 확인 """

        mecab_parsed_list = list(MeCabParser(sentence=sentence).gen_mecab_compound_token_feature())

        for mecab_category_item in self.gen_all_mecab_category_data:
            large_category, medium_category, mecab_token_data = mecab_category_item

            for small_category in mecab_token_data.keys():

                for small_category_item in mecab_token_data[small_category]:

                    original_data, mecab_data = small_category_item.split(MecabGenerator.ITEM_BOUNDARY)

                    contain_pattern = contain_pattern_list(mecab_data, mecab_parsed_list)

                    if contain_pattern:
                        for pattern_item in contain_pattern:
                            entity_token = self.get_pattern_item(pattern_item, mecab_parsed_list)
                            yield MecabCategory(large_category=large_category, medium_category=medium_category, small_category=small_category, entity=entity_token)
                        continue

                    space_token_contain_pattern = contain_pattern_list(original_data, mecab_parsed_list)

                    if (len(original_data) >= self.MIN_MEANING) and space_token_contain_pattern:
                        for pattern_item in contain_pattern:
                            entity_token = self.get_pattern_item(pattern_item, mecab_parsed_list)
                            yield MecabCategory(large_category=large_category, medium_category=medium_category, small_category=small_category, entity=entity_token)

    def get_pattern_item(self, pattern_item: List, mc_ps: List) -> str:
        pattern_list = []
        for pattern_idx_item in range(pattern_item[self.START_IDX], pattern_item[self.END_IDX], self.ONE_WORD):
            pattern_list.append(mc_ps[pattern_idx_item][self.WORD_IDX])
            mc_ps[pattern_idx_item] = ("*", mc_ps[pattern_idx_item][self.MECAB_FEATURE_IDX])

        return " ".join(pattern_list)