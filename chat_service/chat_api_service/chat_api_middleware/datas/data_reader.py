import os
from pathlib import Path

from chat_service.chat_core.chat_domain import TemplateItemRequestData
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


def read_template_item(template_item: TemplateItemRequestData):

    TEMPLATE_DIR = Path(__file__).resolve().parent.joinpath(f"template_item.txt")

    try:

        with open(TEMPLATE_DIR, "r", encoding='utf-8-sig') as file:
            txt_list = file.read().splitlines()
            for txt_item in txt_list:
                if txt_item.count(',') == TEMPLATE_SEP:
                    entity, intent, template = txt_item.split(",")
                    if (entity == template_item.entity) and (intent == template_item.intent):
                        return template
        return False
    except FileNotFoundError as fnf:
        raise TemplateNotExist(fnf)