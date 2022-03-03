from chat_core.chat_domain import TemplateItemRequestData
from datas.data_reader import read_template, read_template_item
from chat_core.chat_domain import TemplateRequestData
from utility import utility_string

ENTITY_SMALL_CATEGORY = 0
INTENT_SMALL_CATEGORY = 1
TEMPLATE_IDX = 2


def get_template_item(template_item: TemplateItemRequestData):

    """엔티티 대분류, 중분류에 따라 인텐트 템플릿에 넣고 반환하는함수"""

    return read_template_item(template_item=template_item)




def get_template_data(template_request_data: TemplateRequestData):

    """엔티티 대분류, 중분류에 따라 인텐트 템플릿에 넣고 반환하는함수"""

    for data_item in read_template(template_request_data.main_category):
        if data_item[ENTITY_SMALL_CATEGORY] == template_request_data.entity_medium_category and data_item[INTENT_SMALL_CATEGORY] == template_request_data.intent_small_category:
            josa_sbj = utility_string.get_marker(template_request_data.entity, "josa_sbj")
            josa_obj = utility_string.get_marker(template_request_data.entity, "josa_obj")
            hint = data_item[TEMPLATE_IDX].replace("{entity}", template_request_data.entity)
            hint = hint.replace("{josa_sbj}", josa_sbj)
            hint = hint.replace("{josa_obj}", josa_obj)
            return hint
    return False
