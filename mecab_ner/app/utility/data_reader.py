from typing import List


class DataReader:

    CLASS_BOUNDARY = "#"
    ITEM_BOUNDARY = ","

    @staticmethod
    def read_txt(data_path):
        with open(data_path, "r", encoding='utf-8-sig') as file:
            txt_list = file.read().splitlines()
            return txt_list

    @staticmethod
    def read_category(data_list: List):
        header, *other = data_list
        header = header.replace("#", "").strip()
        category_list = []

        for data_item in other:
            if DataReader.CLASS_BOUNDARY in data_item:
                yield header, sorted(category_list, key=len, reverse=True)
                header = data_item.replace("#", "").strip()
                category_list = []

            category_list.append(data_item)

        yield header, sorted(category_list, key=len, reverse=True)
