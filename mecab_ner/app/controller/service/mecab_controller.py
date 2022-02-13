import os
from dataclasses import asdict
import numpy as np
from app.application.service.mecab_ner import MeCabNer
from app.application.service.mecab_storage import MeCabStorage
from app.domain.entity import MecabCategory, MeCabEntityIntent, MeCabEntity, MeCabIntent


class MeCabController:

    EMPTY_WORD = 0
    FULL_WORD = 1

    def __init__(self):
        entity_storage_path = os.getenv("entity_storage_path")
        self.mecab_entity_ner = MeCabNer(storage_mecab_path=entity_storage_path)
        entity_storage_path = os.getenv("intent_storage_path")
        self.mecab_intent_ner = MeCabNer(storage_mecab_path=entity_storage_path)

    def gen_entity_intent(self, sentence):

        entity_gen = self.mecab_entity_ner.gen_integrated_entities(sentence, status=MeCabNer.INFER_FORWARD)
        entity_list = list(entity_gen)
        intent_gen = self.mecab_intent_ner.gen_integrated_entities(sentence, status=MeCabNer.ENTITY)
        intent_list = list(intent_gen)

        if len(entity_list) == 0:
            for intent_item in intent_list:
                yield MeCabIntent(intent=intent_item)
        elif len(intent_list) == 0:
            for entity_item in entity_list:
                yield MeCabEntity(entity=entity_item)
        else:
            for intent_item in intent_list:
                tmp_dis = np.inf
                mc_en_int = None
                for entity_item in entity_list:
                    if entity_item.large_category == intent_item.large_category:
                        e_i_dis = abs(intent_item.start_idx - entity_item.start_idx)
                        if e_i_dis <= tmp_dis:
                            mc_en_int = MeCabEntityIntent(entity_item, intent_item)
                yield mc_en_int


def get_data(sentence):
    return_val = []
    for mecab_item in MeCabController().gen_entity_intent(sentence=sentence):
        if mecab_item:
            return_val.append(asdict(mecab_item))

    return return_val