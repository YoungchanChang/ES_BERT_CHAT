from flask import Flask
from flask import render_template
from flask_socketio import SocketIO
from utility_dir.docker_net import get_mecab_ner_answer
app = Flask(__name__)
socketio = SocketIO(app)


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("chat")
def event_handler(json):
    json["nickname"] = json["nickname"].encode("latin1").decode("utf-8")
    json_message = json["message"].encode("latin1").decode("utf-8")
    mecab_bert_answer = get_mecab_ner_answer(json_message)
    socketio.emit("response", {"nickname": "friendbot", "message": mecab_bert_answer})


@socketio.on("connected")
def connect_handler():
    socketio.emit("response", {"nickname": "", "message": "새로운 유저 입장"})

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=14000, debug=True)