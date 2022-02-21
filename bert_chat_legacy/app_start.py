from flask import Flask
from bert_view_dir import bert_view

app = Flask(__name__)
app.register_blueprint(bert_view.bert_chat, url_prefix='/bert_chat')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9092)
