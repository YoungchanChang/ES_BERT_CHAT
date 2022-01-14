"""
call_center data source : https://aihub.or.kr/aidata/30716
"""
import os
import json
import csv
import mecab_value_extractor as mve
USER_SENTENCE = 1

def get_sentence_entities():
    for (path, dir, files) in os.walk("./"):
        for filename in files:
            ext = os.path.splitext(filename)[-1]
            if ext == '.json':
                print("%s/%s" % (path, filename))
                with open(path + "/" + filename, 'r', encoding='cp949') as f:
                    json_data_list = json.load(f)
                    question_list = [json_data_item for json_data_item in json_data_list if json_data_item.get('QA') == "Q"]
                    question_values = [((question_item.get('고객질문(요청)').strip() or question_item.get('상담사질문(요청)').strip()), question_item.get('개체명 ')) for question_item in question_list if question_item.get('개체명 ') != '']

    return question_values


def write_csv(csv_list):
    with open('./test_file/call_center_function_check.csv', 'w', encoding='utf-8-sig', newline='') as writer_csv:
        writer = csv.writer(writer_csv, delimiter=',')
        for idx, csv_item in enumerate(csv_list):
            writer.writerow([idx, *csv_item])

def read_csv():
    with open('./test_file/call_center_restore_test.csv', 'r', encoding='utf-8-sig') as reader_csv:
        reader = csv.reader(reader_csv, delimiter=',')
        return list(reader)

def mecab_function_test():
    mecab_value_extractor = mve.MeCabValueExtractor()
    tmp_list = []
    is_same = False

    for csv_item in read_csv():
        # Do function
        compound_parse_list = mecab_value_extractor.parse_compound(csv_item[USER_SENTENCE])
        restore_sentence = mve.reverse_compound_parse(compound_parse_list)

        if csv_item[USER_SENTENCE] != restore_sentence:
            is_same = True

        tmp_list.append([csv_item[USER_SENTENCE], restore_sentence, is_same])
    write_csv(tmp_list)

if __name__ == "__main__":
    mecab_function_test()