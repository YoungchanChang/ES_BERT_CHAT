import os
from dataclasses import asdict
from pathlib import Path

import numpy as np

from app.application.service.mecab_generator import MecabGenerator
from app.application.service.mecab_ner import MeCabNer
from app.application.service.mecab_storage import MeCabStorage
from app.domain.entity import MecabCategory, MeCabEntityIntent, MeCabEntity, MeCabIntent, CategoryItem
from app.utility.data_reader import DataReader


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

class MecabDataController:
    BASE_DIR_PATH = Path(__file__).resolve().parent.parent.parent.parent.joinpath("datas")

    def create_index(self, category_item: CategoryItem):

        category_name = category_item.large_category + "_" + category_item.medium_category + ".txt"
        small_category_name = "#"+category_item.small_category

        BASE_DIR_PATH = ""
        if category_item.type == "entity":
            BASE_DIR_PATH = self.BASE_DIR_PATH.joinpath("entities", "storage").joinpath(category_name)

        elif category_item.type == "intent":
            BASE_DIR_PATH = self.BASE_DIR_PATH.joinpath("intents")

        if not BASE_DIR_PATH.exists():
            DataReader.write_txt(str(BASE_DIR_PATH), [small_category_name])

        if BASE_DIR_PATH.exists():
            return True
        return False
    # storage_path = "/Users/youngchan/Desktop/ES_BERT_CHAT/mecab_ner/datas/intents/mecab_storage"
    # m_g = MecabGenerator(storage_path=storage_path)
    # for path_item in Path(m_g.mecab_path).iterdir():
    #     Path(path_item).unlink()
    # Path(m_g.mecab_path).rmdir()
    #
    # # init data
    # m_g = MecabGenerator(storage_path=storage_path)