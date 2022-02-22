from typing import List, Generator
from pathlib import Path
from app.application.service.mecab_parser import MeCabParser
from app.utility.custom_error import DataException, PathException
from app.utility.data_reader import DataReader


class MecabGenerator:

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

    def validate_path(self, path) -> None:
        """ 경로 검증 """
        if not Path(path).is_dir():
            raise PathException("Please check if directory")

        for file in Path(path).iterdir():
            if len(file.stem.split(self.FORMAT_SPLITER)) != self.FORMAT_LIMIT:
                raise PathException("Please check if format is right")

            if file.suffix != self.FORMAT_SUFFIX:
                raise PathException("Please check if suffix")

    @staticmethod
    def read_category(txt_data: List) -> Generator:
        """ 데이터에서 헤더, 내용 나누어서 값 반환하는 메소드 """
        header, *contents = txt_data
        category_list = []

        if not header.startswith(MecabGenerator.CLASS_BOUNDARY):
            raise DataException("header should starts with #")

        for data_item in contents:
            if MecabGenerator.CLASS_BOUNDARY in data_item:
                yield header, sorted(category_list, key=len, reverse=True)
                header = data_item
                category_list = []
                continue

            if data_item == '':
                continue

            category_list.append(data_item)

        yield header, sorted(category_list, key=len, reverse=True)

    @staticmethod
    def gen_all_mecab_category_data(storage_path, need_parser=False) -> Generator:
        """경로에 있는 데이터 읽은 뒤 카테고리 데이터셋으로 반환"""

        for path_item in Path(storage_path).iterdir():
            large_category, medium_category = path_item.stem.split("_")
            txt_data = DataReader.read_txt(path_item)
            data_dict = {}

            for data_item in MecabGenerator.read_category(txt_data):
                small_category, contents = data_item
                if need_parser:
                    contents = [(x, MeCabParser(x).get_word_from_feature()) for x in contents]
                dict_value = data_dict.get(small_category, None)
                if dict_value is None:
                    data_dict[small_category] = contents
                else:
                    data_dict[small_category].extend(contents)
            yield large_category, medium_category, data_dict

    def write_category(self) -> None:
        """카테고리별로 데이터 저장하는 메소드"""
        for item in self.gen_all_mecab_category_data(storage_path=self.storage_path, need_parser=True):
            large_category, medium_category, data_dict = item
            file_name = large_category + self.FORMAT_SPLITER + medium_category + self.FORMAT_SUFFIX
            mecab_write_path = self.mecab_path.joinpath(file_name)
            for date_key in data_dict.keys():
                DataReader.write_txt(mecab_write_path, [date_key])
                data_item = [str(x[self.ORIGIN_WORD]) + self.ITEM_BOUNDARY + str(x[self.MECAB_WORD]) for x in data_dict[date_key]]
                DataReader.write_txt(mecab_write_path, data_item)
