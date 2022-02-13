from typing import List, Generator

from mecab_ner.app.application.service.mecab_generator import MecabGenerator
from mecab_ner.app.application.service.mecab_parser import MeCabParser
from mecab_ner.app.domain.entity import MecabCategory
from mecab_ner.app.utility.mecab_helper import contain_pattern_list
import copy


def infer_backward(mecab_parsed_list: List, mecab_category_item: MecabCategory) -> MecabCategory:
    """ pos에 따라 end_index 변경"""

    for idx_range in range(mecab_category_item.end_idx, len(mecab_parsed_list) - 1, 1):
        if mecab_parsed_list[idx_range][MeCabNer.MECAB_FEATURE_IDX].pos in ["NNG", "NNP"]:
            mecab_category_item.end_idx = mecab_parsed_list[idx_range][1].mecab_token_idx + 1
            continue
        elif mecab_parsed_list[idx_range][MeCabNer.MECAB_FEATURE_IDX].pos in ["MM"]:
            mecab_category_item.end_idx = mecab_parsed_list[idx_range][1].mecab_token_idx + 1
            continue
        break
    return mecab_category_item


def infer_entity(mecab_parsed_list: List, mecab_category_item: MecabCategory) -> MecabCategory:
    """ pos에 따라 start_index 변경"""

    for idx_range in range(mecab_category_item.start_idx - 1, 0, -1):
        if mecab_parsed_list[idx_range][MeCabNer.MECAB_FEATURE_IDX].pos in ["NNG", "NNP"]:
            mecab_category_item.start_idx = mecab_parsed_list[idx_range][1].mecab_token_idx
            continue
        break
    return mecab_category_item


class MeCabNer:
    """
    엔티티 추출하는 클래스
    - 앞에 단어 품사를 통한 추론 기능
    - 뒤에 단어 품사를 통한 추론 기능
    """

    MIN_MEANING = 2
    START_IDX = 0
    END_IDX = 1
    ONE_WORD = 1
    MECAB_FEATURE_IDX = 1
    WORD_IDX = 0
    ENTITY = 0
    INFER_FORWARD = 1
    INFER_BACKWARD = 2

    def __init__(self, storage_mecab_path: str):

        self.gen_all_mecab_category_data = MecabGenerator.gen_all_mecab_category_data \
            (storage_path=storage_mecab_path, need_parser=False)

    def get_category_entity(self, sentence: str) -> Generator:
        """ mecab 저장 데이터와 storage 데이터의 길이가 같은지 확인 """
        mecab_parsed_list = list(MeCabParser(sentence=sentence).gen_mecab_compound_token_feature())

        for mecab_category_item in self.gen_all_mecab_category_data:
            mecab_parsed_copied = copy.deepcopy(mecab_parsed_list)
            large_category, medium_category, mecab_token_data = mecab_category_item

            for small_category in mecab_token_data.keys():

                for small_category_item in mecab_token_data[small_category]:

                    original_data, mecab_data = small_category_item.split(MecabGenerator.ITEM_BOUNDARY)

                    contain_pattern = contain_pattern_list(mecab_data, mecab_parsed_copied)

                    if contain_pattern:
                        for pattern_item in contain_pattern:
                            self.prevent_compound_token(pattern_item, mecab_parsed_copied)
                            yield MecabCategory(large_category=large_category, medium_category=medium_category,
                                                small_category=small_category,
                                                start_idx=pattern_item[self.START_IDX],
                                                end_idx=pattern_item[self.END_IDX])
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

    def get_entities(self, sentence: str, status=0):
        mecab_parsed_list = list(MeCabParser(sentence=sentence).gen_mecab_compound_token_feature())
        for category_item in self.get_category_entity(sentence=sentence):
            if status == self.INFER_FORWARD:
                category_item = infer_entity(mecab_parsed_list, category_item)
            elif status == self.INFER_BACKWARD:
                category_item = infer_backward(mecab_parsed_list, category_item)
            entity_list = list(self.get_entity(mecab_parsed_list, category_item.start_idx, category_item.end_idx))
            entity_str = " ".join(entity_list)
            yield MecabCategory(large_category=category_item.large_category,
                                medium_category=category_item.medium_category,
                                small_category=category_item.small_category,
                                start_idx=category_item.start_idx,
                                end_idx=category_item.end_idx,
                                entity=entity_str)

    def get_entity(self, mecab_parsed_list: List, start_idx: int, end_idx: int) -> str:

        """ start_index와 end_index를 바탕으로 리스트에서 해당 값 추출 """

        for step_idx in range(start_idx, end_idx, self.ONE_WORD):
            yield mecab_parsed_list[step_idx][self.WORD_IDX]
