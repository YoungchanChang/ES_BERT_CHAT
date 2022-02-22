from typing import List


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