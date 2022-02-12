from typing import List
from pathlib import Path
from mecab_ner.app.application.service.mecab_parser import MeCabParser
from mecab_ner.app.utility.custom_error import DataException, PathException
from mecab_ner.app.utility.data_reader import DataReader


class MecabGenerator:

    FIRST_WORD = 0
    ORIGIN_WORD = 0
    MECAB_WORD = 1
    FORMAT_LIMIT = 2

    FORMAT_SPLITER = "_"
    FORMAT_SUFFIX = ".txt"
    CLASS_BOUNDARY = "#"
    ITEM_BOUNDARY = ","
    MECAB_STORAGE = "mecab_storage"

    def __init__(self, storage_path, mecab_path=None):
        self.validate_path(storage_path)

        if mecab_path is None:
            mecab_path = Path(storage_path).parent.joinpath(self.MECAB_STORAGE)
            if not Path(mecab_path).exists():
                Path(mecab_path).mkdir()
        else:
            self.validate_path(mecab_path)

        self.storage_path = storage_path
        self.mecab_path = mecab_path

    def read_category(self, data_list: List):

        """ 카테고리에서 데이터 읽는 메소드 """

        header, *other = data_list

        if not header.startswith(self.CLASS_BOUNDARY):
            raise DataException("header should starts with #")

        category_list = []

        for data_item in other:
            if self.CLASS_BOUNDARY in data_item:
                yield header, sorted(category_list, key=len, reverse=True)
                header = data_item
                category_list = []
                continue

            category_list.append(data_item)

        yield header, sorted(category_list, key=len, reverse=True)

    def validate_path(self, path):
        """ 경로 검증 """
        if not Path(path).is_dir():
            raise PathException("Please check if directory")

        for file in Path(path).iterdir():
            if len(file.stem.split(self.FORMAT_SPLITER)) != self.FORMAT_LIMIT:
                raise PathException("Please check if format is right")

            if file.suffix != self.FORMAT_SUFFIX:
                raise PathException("Please check if suffix")

    def get_word_from_feature(self, mecab_word):
        """ 메캅 특성에서 단어만 검출"""
        return " ".join([x[self.FIRST_WORD] for x in list(MeCabParser(mecab_word).gen_mecab_compound_token_feature())])

    def gen_data_input(self):
        for path_item in Path(self.storage_path).iterdir():
            large_category, medium_category = path_item.stem.split("_")
            txt_data = DataReader.read_txt(path_item)
            data_dict = {}

            for data_item in self.read_category(txt_data):
                small_category, contents = data_item
                mecab_parsed = [(x, self.get_word_from_feature(x)) for x in contents]
                data_dict[small_category] = mecab_parsed

            yield large_category, medium_category, data_dict

    def write_category(self):
        for item in self.gen_data_input():
            large_category, medium_category, data_dict = item
            file_name = large_category + self.FORMAT_SPLITER + medium_category + self.FORMAT_SUFFIX
            mecab_write_path = self.mecab_path.joinpath(file_name)
            for date_key in data_dict.keys():
                DataReader.write_txt(mecab_write_path, [date_key])
                data_item = [str(x[self.ORIGIN_WORD]) + self.ITEM_BOUNDARY + str(x[self.MECAB_WORD]) for x in data_dict[date_key]]
                DataReader.write_txt(mecab_write_path, data_item)
