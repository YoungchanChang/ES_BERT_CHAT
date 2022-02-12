

class DataReader:

    @staticmethod
    def read_txt(data_path):
        with open(data_path, "r", encoding='utf-8-sig') as file:
            txt_list = file.read().splitlines()
            return txt_list

    @staticmethod
    def write_txt(data_path, txt_list, is_sort=False):
        if is_sort:
            txt_list = sorted(list(txt_list), key=len, reverse=True)

        with open(data_path, "a", encoding='UTF8') as file:
            for txt_item in txt_list:
                data = str(txt_item) + "\n"
                file.write(data)