from typing import List, Generator

from mecab_ner.app.application.service.mecab_generator import MecabGenerator
from mecab_ner.app.application.service.mecab_parser import MeCabParser
from mecab_ner.app.domain.entity import MecabCategory
from mecab_ner.app.utility.mecab_helper import contain_pattern_list
import copy


class MeCabNer:

    MIN_MEANING = 2
    START_IDX = 0
    END_IDX = 1
    ONE_WORD = 1
    MECAB_FEATURE_IDX = 1
    WORD_IDX = 0

    def __init__(self, storage_mecab_path: str, sentence: str):
        self.mecab_parsed_list = list(MeCabParser(sentence=sentence).gen_mecab_compound_token_feature())
        self.gen_all_mecab_category_data = MecabGenerator.gen_all_mecab_category_data\
            (storage_path=storage_mecab_path, need_parser=False)

    def get_category_entity(self) -> Generator:
        """ mecab 저장 데이터와 storage 데이터의 길이가 같은지 확인 """

        for mecab_category_item in self.gen_all_mecab_category_data:
            mecab_parsed_copied = copy.deepcopy(self.mecab_parsed_list)
            large_category, medium_category, mecab_token_data = mecab_category_item

            for small_category in mecab_token_data.keys():

                for small_category_item in mecab_token_data[small_category]:

                    original_data, mecab_data = small_category_item.split(MecabGenerator.ITEM_BOUNDARY)

                    contain_pattern = contain_pattern_list(mecab_data, mecab_parsed_copied)

                    if contain_pattern:
                        for pattern_item in contain_pattern:
                            self.prevent_compound_token(pattern_item, mecab_parsed_copied)
                            yield MecabCategory(large_category=large_category, medium_category=medium_category, small_category=small_category,
                                                start_idx=pattern_item[self.START_IDX], end_idx=pattern_item[self.END_IDX])
                        continue

                    space_token_contain_pattern = contain_pattern_list(original_data, mecab_parsed_copied)

                    if (len(original_data) >= self.MIN_MEANING) and space_token_contain_pattern:
                        for pattern_item in contain_pattern:
                            self.prevent_compound_token(pattern_item, mecab_parsed_copied)
                            yield MecabCategory(large_category=large_category, medium_category=medium_category,
                                                small_category=small_category,
                                                start_idx=pattern_item[self.START_IDX],
                                                end_idx=pattern_item[self.END_IDX])

    def prevent_compound_token(self, pattern_item: List, mc_ps: List) -> None:
        for pattern_idx_item in range(pattern_item[self.START_IDX], pattern_item[self.END_IDX], self.ONE_WORD):
            mc_ps[pattern_idx_item] = ("*", mc_ps[pattern_idx_item][self.MECAB_FEATURE_IDX])

    def get_entity(self, start_idx: int, end_idx: int) -> str:
        for step_idx in range(start_idx, end_idx, self.ONE_WORD):
            yield self.mecab_parsed_list[step_idx][0]

    def infer_entity(self, mecab_category_item: MecabCategory) -> MecabCategory:
        for idx_range in range(mecab_category_item.start_idx - 1, 0, -1):
            if self.mecab_parsed_list[idx_range][1].pos in ["NNG", "NNP"]:
                mecab_category_item.start_idx = self.mecab_parsed_list[idx_range][1].mecab_token_idx
                continue
            break
        return mecab_category_item

