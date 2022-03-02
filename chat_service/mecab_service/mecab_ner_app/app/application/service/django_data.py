from pathlib import Path
from typing import List

from app.application.service.mecab_parser import MecabParser
from app.domain.data_domain import CategoryIndex, MecabWord, MecabEntityItem, EntityCategoryItem, MecabIntentItem, \
    IntentCategoryItem


class DataReader:

    @staticmethod
    def read_txt(data_path):
        with open(data_path, "r", encoding='utf-8-sig') as file:
            txt_list = file.read().splitlines()
            return txt_list

    @staticmethod
    def write_txt(data_path: str, txt_list: List, is_sort=False):
        if is_sort:
            txt_list = sorted(list(txt_list), key=len, reverse=True)

        with open(data_path, "a", encoding='UTF8') as file:
            for idx, txt_item in enumerate(txt_list):
                if len(txt_list) == idx+1:
                    data = str(txt_item)
                else:
                    data = str(txt_item) + "\n"
                file.write(data)

class DjangoDataController:
    BASE_DIR_PATH = Path(__file__).resolve().parent.parent.parent.parent.joinpath("data")

    @classmethod
    def create_index(cls, category_index: CategoryIndex):
        """
        인덱스 생성
        :param category_index: 생성할 카테고리 인덱스 정보
        :return: 성공시 True
        """
        category_name = category_index.large_category + "_" + category_index.medium_category + ".txt"
        small_category_name = "#"+category_index.small_category

        BASE_DIR_PATH = ""
        if category_index.type == "entity":
            BASE_DIR_PATH = cls.BASE_DIR_PATH.joinpath("entities", "entity_data").joinpath(category_name)

        elif category_index.type == "intent":
            BASE_DIR_PATH = cls.BASE_DIR_PATH.joinpath("intents", "intent_data").joinpath(category_name)

        if not BASE_DIR_PATH.exists():
            DataReader.write_txt(str(BASE_DIR_PATH), [small_category_name])

        if BASE_DIR_PATH.exists():
            return True

        return False

    @classmethod
    def insert_data(cls, mecab_word: MecabWord):

        """
        엔티티 데이터 삽입
        :param mecab_word:
        :return:
        """

        saving_word = mecab_word.word
        parsed_word = MecabParser(saving_word).get_word_from_mecab_compound()

        if mecab_word.type == "entity":
            mecab_entity_data = MecabEntityItem.get_or_none(MecabEntityItem.category == mecab_word.category,
                                                        MecabEntityItem.word == saving_word)
            if mecab_entity_data is not None:
                return False

            value = EntityCategoryItem.get_or_none(mecab_word.category)
            small_category = "\n" + "#" + value.small_category
            category_name = value.large_category + "_" + value.medium_category + ".txt"

            BASE_DIR_PATH = cls.BASE_DIR_PATH.joinpath("entities", "storage").joinpath(category_name)

            DataReader.write_txt(str(BASE_DIR_PATH), [small_category, saving_word])

            BASE_DIR_PATH = cls.BASE_DIR_PATH.joinpath("entities", "mecab_storage").joinpath(category_name)

            DataReader.write_txt(str(BASE_DIR_PATH), [small_category, saving_word + "," + parsed_word])

            mecab_entity = MecabEntityItem.create(word=mecab_word.word, mecab_word=parsed_word, category=value)
            if mecab_entity.id:
                return True

        if mecab_word.type == "intent":
            mecab_intent_data = MecabIntentItem.get_or_none(MecabIntentItem.category == mecab_word.category,
                                                        MecabIntentItem.word == saving_word)
            if mecab_intent_data is not None:
                return False

            value = IntentCategoryItem.get_or_none(mecab_word.category)
            small_category = "\n" + "#" + value.small_category
            category_name = value.large_category + "_" + value.medium_category + ".txt"

            BASE_DIR_PATH = cls.BASE_DIR_PATH.joinpath("intents", "storage").joinpath(category_name)

            DataReader.write_txt(str(BASE_DIR_PATH), [small_category, saving_word])

            BASE_DIR_PATH = cls.BASE_DIR_PATH.joinpath("intents", "mecab_storage").joinpath(category_name)

            DataReader.write_txt(str(BASE_DIR_PATH), [small_category, saving_word + "," + parsed_word])

            mecab_intent = MecabIntentItem.create(word=mecab_word.word, mecab_word=parsed_word, category=value)
            if mecab_intent.id:
                return True

        return False