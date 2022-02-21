import os
from dataclasses import asdict
from pathlib import Path

import numpy as np

from app.application.service.mecab_generator import MecabGenerator
from app.application.service.mecab_ner import MeCabNer
from app.application.service.mecab_parser import MeCabParser
from app.application.service.mecab_storage import MeCabStorage
from app.domain.endpoint import MecabNerAttribute
from app.domain.entity import MecabCategory, MeCabEntityIntent, MeCabEntity, MeCabIntent, CategoryItem, MecabWord
from app.infrastructure.network.api_endpoint import get_bert_confirm_response
from app.utility.data_reader import DataReader
from scripts.db_info import EntityCategoryItem, MecabEntity, MecabIntent, IntentCategoryItem


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
            if mecab_item.entity.large_category != mecab_item.intent.large_category:
                continue
            m_n_attr = MecabNerAttribute(category_sentence=sentence, main_category=mecab_item.entity.large_category,
                              entity=mecab_item.entity.entity, entity_medium_category=mecab_item.entity.medium_category,
                              entity_small_category=mecab_item.entity.small_category,
                              intent=mecab_item.intent.entity, intent_medium_category=mecab_item.intent.medium_category,
                              intent_small_category=mecab_item.intent.medium_category)
            bert_answer = get_bert_confirm_response(m_n_attr.json())
            m_n_attr.bert_confirm = bert_answer
            return_val.append(m_n_attr)
    return return_val


class MecabDataController:
    BASE_DIR_PATH = Path(__file__).resolve().parent.parent.parent.parent.joinpath("datas")

    @staticmethod
    def create_index(category_item: CategoryItem):

        category_name = category_item.large_category + "_" + category_item.medium_category + ".txt"
        small_category_name = "#"+category_item.small_category

        BASE_DIR_PATH = ""
        if category_item.type == "entity":
            BASE_DIR_PATH = MecabDataController.BASE_DIR_PATH.joinpath("entities", "storage").joinpath(category_name)

        elif category_item.type == "intent":
            BASE_DIR_PATH = MecabDataController.BASE_DIR_PATH.joinpath("intents", "storage").joinpath(category_name)

        if not BASE_DIR_PATH.exists():
            DataReader.write_txt(str(BASE_DIR_PATH), [small_category_name])

        if BASE_DIR_PATH.exists():
            return True

        return False

    @staticmethod
    def insert_data(mecab_word: MecabWord):

        saving_word = mecab_word.word
        parsed_word = MeCabParser(saving_word).get_word_from_feature()

        if mecab_word.type == "entity":
            mecab_entity_data = MecabEntity.get_or_none(MecabEntity.category == mecab_word.category,
                                                        MecabEntity.word == saving_word)
            if mecab_entity_data is not None:
                return False

            value = EntityCategoryItem.get_or_none(mecab_word.category)
            small_category = "\n" + "#" + value.small_category
            category_name = value.large_category + "_" + value.medium_category + ".txt"

            BASE_DIR_PATH = MecabDataController.BASE_DIR_PATH.joinpath("entities", "storage").joinpath(category_name)

            DataReader.write_txt(str(BASE_DIR_PATH), [small_category, saving_word])

            BASE_DIR_PATH = MecabDataController.BASE_DIR_PATH.joinpath("entities", "mecab_storage").joinpath(category_name)

            DataReader.write_txt(str(BASE_DIR_PATH), [small_category, saving_word + "," + parsed_word])

            mecab_entity = MecabEntity.create(word=mecab_word.word, mecab_word=parsed_word, category=value)
            if mecab_entity.id:
                return True

        if mecab_word.type == "intent":
            mecab_intent_data = MecabIntent.get_or_none(MecabIntent.category == mecab_word.category,
                                                        MecabIntent.word == saving_word)
            if mecab_intent_data is not None:
                return False

            value = IntentCategoryItem.get_or_none(mecab_word.category)
            small_category = "\n" + "#" + value.small_category
            category_name = value.large_category + "_" + value.medium_category + ".txt"

            BASE_DIR_PATH = MecabDataController.BASE_DIR_PATH.joinpath("intents", "storage").joinpath(category_name)

            DataReader.write_txt(str(BASE_DIR_PATH), [small_category, saving_word])

            BASE_DIR_PATH = MecabDataController.BASE_DIR_PATH.joinpath("intents", "mecab_storage").joinpath(category_name)

            DataReader.write_txt(str(BASE_DIR_PATH), [small_category, saving_word + "," + parsed_word])

            mecab_intent = MecabIntent.create(word=mecab_word.word, mecab_word=parsed_word, category=value)
            if mecab_intent.id:
                return True

        return False