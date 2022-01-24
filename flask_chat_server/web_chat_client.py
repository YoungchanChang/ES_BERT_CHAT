# 플라스크 라이브러리
from flask import Flask
from flask import render_template

# 플라스크 소켓 통신을 위한 라이브러리
from flask_socketio import SocketIO

# flask 인스턴스 생성
app = Flask(__name__)

# Socket을 사용하기 위한 SocketIO 에 인자로 플라스크 app 변수를 넘겨 새로운 socketio 변수에 저장합니다.
socketio = SocketIO(app)


# 접속 주소는 / 입니다.
@app.route("/")
def index():
    # templates 폴더의 index.html 파일을 렌더링 해서 출력합니다.
    return render_template("index.html")


# 클라이언트에서 소켓으로 chat 이벤트가 발생하면
@socketio.on("chat")
def event_handler(json):
    # 인자로 넘어온 json 은 기본적으로 latin1 로 인코딩 되어있습니다.
    # 그래서 정상적인 한글을 사용하기 위해선 utf-8로 디코딩 해주어야 합니다.
    json["nickname"] = json["nickname"].encode("latin1").decode("utf-8")
    json["message"] = json["message"].encode("latin1").decode("utf-8")

    # 클라이언트에게 response 이벤트를 발생시킵니다.
    # 전송받은 닉네임과 채팅 메세지를 각각 nickname, message를 키값으로 dict형태로 전송합니다.
    socketio.emit("response", {"nickname": json["nickname"], "message": json["message"]})


# 클라이언트에서 소켓으로 connectd 이벤트가 발생하면
@socketio.on("connected")
def connect_handler():
    # 클라이언트에게 response 이벤트를 발생시킵니다.
    # response 이벤트는 nickname 과 message를 키로 받기 때문에 키 값은 고정으로 두고
    # message 값만 '새로운 유저 입장' 이라고 알려줍니다.
    socketio.emit("response", {"nickname": "", "message": "새로운 유저 입장"})


# py 파일 시작 엔트리 포인트
if __name__ == "__main__":
    # socketio 를 run 합니다.
    # 기본적으로 flask 인스턴스를 run 하는것과 같습니다.
    socketio.run(app, host="0.0.0.0", port=14000, debug=True)