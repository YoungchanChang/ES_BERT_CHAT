from typing import List, Generator

from mecab_ner.app.application.service.mecab_ner import MeCabNer
from mecab_ner.app.application.service.mecab_storage import MeCabStorage
from mecab_ner.app.domain.entity import MecabCategory




def integrate_many_entity_index(mecab_entity_category_list: List, mecab_list_length: int) -> List:
    """인덱스 값에 엔티티가 있는 경우, 없는 경우 구분"""
    blank = [MeCabController.EMPTY_WORD] * mecab_list_length
    for mecab_entity_category_item in mecab_entity_category_list:
        for i in range(mecab_entity_category_item.start_idx, mecab_entity_category_item.end_idx, 1):
            blank[i] = MeCabController.FULL_WORD
    return blank

class MeCabController:

    EMPTY_WORD = 0
    FULL_WORD = 1

    def __init__(self, sentence):
        entity_storage_path = "/Users/youngchan/Desktop/ES_BERT_CHAT/mecab_ner/datas/entities/mecab_storage"
        self.mecab_ner = MeCabNer(storage_mecab_path=entity_storage_path, sentence=sentence)

    def integrate_many_entity_index(self, mecab_entity_category_list: List) -> List:
        """인덱스 값에 엔티티가 있는 경우, 없는 경우 구분"""
        blank = [self.EMPTY_WORD] * len(self.mecab_ner.mecab_parsed_list)
        for mecab_entity_category_item in mecab_entity_category_list:
            for i in range(mecab_entity_category_item.start_idx, mecab_entity_category_item.end_idx, 1):
                blank[i] = self.FULL_WORD
        return blank

    def gen_entity(self):

        mecab_entity_category_list = [self.mecab_ner.infer_entity(x) for x in self.mecab_ner.get_category_entity()]

        many_entity_index_list = self.integrate_many_entity_index(mecab_entity_category_list)

        for integrated_entity_item in gen_integrated_entity(many_entity_index_list):

            end_idx = integrated_entity_item[1] + 1
            start_idx = integrated_entity_item[0]
            mecab_parsed_list = self.mecab_ner.mecab_parsed_list[start_idx:end_idx]
            restore_tokens = MeCabStorage().reverse_compound_tokens(mecab_parsed_list)
            restore_sentence = " ".join(restore_tokens)
            for entity_category_item in mecab_entity_category_list:
                if entity_category_item.end_idx == end_idx:
                    yield MecabCategory(large_category=entity_category_item.large_category,
                                        medium_category=entity_category_item.medium_category,
                                        small_category=entity_category_item.small_category,
                                        entity=restore_sentence)

    def gen_integrated_entity(self, blank_list: List) -> Generator:
        start_idx = None
        end_idx = None
        switch_on = True
        for idx, item in enumerate(blank_list):
            if item == MeCabController.FULL_WORD:
                end_idx = idx

                if switch_on:
                    start_idx = idx

                switch_on = False

                if idx != len(blank_list)-1:
                    continue

            if (switch_on is False) and end_idx:
                yield start_idx, end_idx
                start_idx = None
                end_idx = None
                switch_on = True