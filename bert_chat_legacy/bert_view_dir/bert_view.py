import datetime
import json
from flask import Flask, Blueprint, request, render_template, make_response, jsonify, redirect, url_for, session
from bert_control_dir.bert_mgmt import get_template_data

bert_chat = Blueprint('bert_chat', __name__)


@bert_chat.route('/bert_template', methods=['GET', 'POST'])
def entity_intent_result():
    return_json = {
        "sender" : "youngchan"
    }
    input_json = json.loads(request.get_data().decode('utf-8'))
    answer = input_json.get("answer")
    answer_list = []
    for answer_item in answer:
        entity = answer_item.get("entity")
        intent = answer_item.get("intent")
        template_answer = get_template_data(entity.get('large_category'), entity.get('medium_category'), entity.get('entity'), intent.get('medium_category'))
        answer_list.append(template_answer)

    try:
        return_json["answer"] = answer_list
        return make_response(jsonify(return_json), 200)

    except Exception as e:
        return_json["Exception"] = e
        return make_response(jsonify(return_json), 500)
