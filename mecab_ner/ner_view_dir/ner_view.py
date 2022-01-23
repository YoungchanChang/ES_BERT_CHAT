import datetime
import json
from flask import Flask, Blueprint, request, render_template, make_response, jsonify, redirect, url_for, session
from ner_control_dir.ner_mgmt import get_entity_intent_dict
from utility_dir.docker_net import get_entity_intent_answer
ner_bp = Blueprint('ner', __name__)


@ner_bp.route('/ner_intent_analyzed', methods=['GET', 'POST'])
def entity_intent_result():
    return_json = {
        "sender" : "youngchan"
    }
    input_json = json.loads(request.get_data().decode('utf-8'))
    query = input_json.get("query")
    try:
        e_i_dict = get_entity_intent_dict(query)
        if e_i_dict:
            return_json.update(e_i_dict)
            return_json["answer"] = get_entity_intent_answer(return_json)
        return make_response(jsonify(return_json), 200)

    except Exception as e:
        return_json["Exception"] = e
        return make_response(jsonify(return_json), 500)
