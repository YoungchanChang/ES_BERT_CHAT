import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

TEMPLATE_SEP = 2


def read_txt(template_category):
    TEMPLATE_DIR = CURRENT_DIR + "/template_data/template_" + template_category +".txt"
    with open(TEMPLATE_DIR, "r", encoding='utf-8-sig') as file:
        txt_list = file.read().splitlines()
        template_dictionary = [x.split(",") for x in txt_list if x.count(',') == TEMPLATE_SEP]
        return sorted(list(template_dictionary), key=len, reverse=True)