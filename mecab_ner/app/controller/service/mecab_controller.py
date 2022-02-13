from typing import List, Generator
import numpy as np

from mecab_ner.app.application.service.mecab_ner import MeCabNer
from mecab_ner.app.application.service.mecab_storage import MeCabStorage
from mecab_ner.app.domain.entity import MecabCategory, MeCabEntityIntent


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

    def __init__(self):
        entity_storage_path = "/Users/youngchan/Desktop/ES_BERT_CHAT/mecab_ner/datas/entities/mecab_storage"
        self.mecab_entity_ner = MeCabNer(storage_mecab_path=entity_storage_path)
        entity_storage_path = "/Users/youngchan/Desktop/ES_BERT_CHAT/mecab_ner/datas/intents/mecab_storage"
        self.mecab_intent_ner = MeCabNer(storage_mecab_path=entity_storage_path)

    def gen_entity_intent(self, sentence):

        entity_list = self.mecab_entity_ner.gen_integrated_entities(sentence, status=MeCabNer.INFER_FORWARD)
        entity_list = list(entity_list)

        intent_list = self.mecab_intent_ner.gen_integrated_entities(sentence, status=MeCabNer.ENTITY)
        intent_list = list(intent_list)

        if len(intent_list) == 0:
            yield entity_list
        elif len(entity_list) == 0:
            yield intent_list
        else:
            for intent_item in intent_list:
                tmp_dis = np.inf
                mc_en_int = None
                for entity_item in entity_list:
                    if entity_item.large_category == intent_item.large_category:
                        print(entity_item)
                        print(intent_item)
                        e_i_dis = abs(intent_item.start_idx - entity_item.start_idx)
                        if e_i_dis <= tmp_dis:
                            mc_en_int = MeCabEntityIntent(entity_item, intent_item)
                yield mc_en_int
