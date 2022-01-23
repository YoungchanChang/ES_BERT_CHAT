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
    entity_large_category = input_json.get("entity_large_category")
    entity_small_category = input_json.get("entity_small_category")
    entity = input_json.get("entity")
    intent_small_category = input_json.get("intent_small_category")

    try:
        template_data = get_template_data(entity_large_category, entity_small_category, entity, intent_small_category)
        return_json["answer"] = template_data
        return make_response(jsonify(return_json), 200)

    except Exception as e:
        return_json["Exception"] = e
        return make_response(jsonify(return_json), 500)
