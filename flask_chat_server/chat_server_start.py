from flask import Flask
from flask import render_template
from flask_socketio import SocketIO
from utility_dir.docker_net import get_mecab_ner_answer
from engineio.payload import Payload
import logging

app = Flask(__name__)
socketio = SocketIO(app)

Payload.max_decode_packets = 50

@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("chat")
def event_handler(json):
    json["nickname"] = json["nickname"].encode("utf-8").decode("utf-8")
    json_message = json["message"].encode("utf-8").decode("utf-8")
    logging.debug(json_message)
    mecab_bert_answer = get_mecab_ner_answer(json_message)
    logging.debug(mecab_bert_answer)
    socketio.emit("response", {"nickname": "friendbot", "message": mecab_bert_answer})


@socketio.on("connected")
def connect_handler():
    socketio.emit("response", {"nickname": "", "message": "새로운 유저 입장"})


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=9096, debug=True)