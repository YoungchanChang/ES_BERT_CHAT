#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from dotenv import load_dotenv
import platform

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':

    os.environ["RDS_NAME"] = "mecab_ner"
    os.environ["RDS_USER"] = "mecab_ner"
    os.environ["RDS_PASSWORD"] = "mecab_ner"
    if platform.system() == "Darwin":
        os.environ["RDS_PORT"] = "3307"
        os.environ["RDS_HOST"] = "127.0.0.1"
        bot_response_url = "localhost"
        mecab_create_index = "localhost"
        mecab_insert_data = "localhost"
    else:
        os.environ["RDS_PORT"] = "3306"
        os.environ["RDS_HOST"] = "mysql_db"
        bot_response_url = "chat_middleware"
        mecab_create_index = "mecab_ner_app"
        mecab_insert_data = "localhost"

    os.environ["bot_response"] = f"http://{bot_response_url}:5000/chat_middleware/response_middleware"
    os.environ["mecab_create_index"] = f"http://{mecab_create_index}:5100/mecab_data/create_index"
    os.environ["mecab_insert_data"] = f"http://{mecab_insert_data}:5100/mecab_data/insert_data"


    main()
