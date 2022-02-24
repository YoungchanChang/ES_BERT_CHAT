import os
from pathlib import Path

from utility.custom_error import TemplateNotExist

TEMPLATE_SEP = 2


def read_template(template_category):

    TEMPLATE_DIR = Path(__file__).resolve().parent.joinpath("chat_templates", f"template_{template_category}.txt")

    try:

        with open(TEMPLATE_DIR, "r", encoding='utf-8-sig') as file:
            txt_list = file.read().splitlines()
            template_dictionary = [x.split(",") for x in txt_list if x.count(',') == TEMPLATE_SEP]
            return sorted(list(template_dictionary), key=len, reverse=True)

    except FileNotFoundError as fnf:
        raise TemplateNotExist(fnf)