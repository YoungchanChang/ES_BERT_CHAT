from flask import Flask
from ner_view_dir import ner_view

app = Flask(__name__)
app.register_blueprint(ner_view.ner_bp, url_prefix='/mecab_ner')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)
