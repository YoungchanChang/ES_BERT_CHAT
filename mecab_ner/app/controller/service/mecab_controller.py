from dataclasses import asdict
from typing import List, Generator
import numpy as np

from mecab_ner.app.application.service.mecab_ner import MeCabNer
from mecab_ner.app.application.service.mecab_storage import MeCabStorage
from mecab_ner.app.domain.entity import MecabCategory, MeCabEntityIntent


class MeCabController:

    EMPTY_WORD = 0
    FULL_WORD = 1

    def __init__(self):
        entity_storage_path = "/Users/youngchan/Desktop/ES_BERT_CHAT/mecab_ner/datas/entities/mecab_storage"
        self.mecab_entity_ner = MeCabNer(storage_mecab_path=entity_storage_path)
        entity_storage_path = "/Users/youngchan/Desktop/ES_BERT_CHAT/mecab_ner/datas/intents/mecab_storage"
        self.mecab_intent_ner = MeCabNer(storage_mecab_path=entity_storage_path)

    def gen_entity_intent(self, sentence):

        entity_gen = self.mecab_entity_ner.gen_integrated_entities(sentence, status=MeCabNer.INFER_FORWARD)
        entity_list = list(entity_gen)
        intent_gen = self.mecab_intent_ner.gen_integrated_entities(sentence, status=MeCabNer.ENTITY)
        intent_list = list(intent_gen)

        if len(entity_list) == 0:
            for intent_item in intent_list:
                yield intent_item
        elif len(intent_list) == 0:
            for entity_item in entity_list:
                yield entity_item

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


def get_data(sentence):
    return_val = []
    for mecab_item in MeCabController().gen_entity_intent(sentence=sentence):
        return_val.append(asdict(mecab_item))

    return return_val