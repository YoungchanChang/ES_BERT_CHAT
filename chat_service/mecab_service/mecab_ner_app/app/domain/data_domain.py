import os
from dataclasses import dataclass
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
from peewee import *

mysql_db = MySQLDatabase(os.getenv("RDS_NAME"), user=os.getenv("RDS_USER"), password=os.getenv("RDS_PASSWORD"),
                         host=os.getenv("RDS_HOST"), port=int(os.getenv("RDS_PORT")))


class CategoryIndex(BaseModel):
    large_category: str
    medium_category: str
    small_category: str
    type: str

class MecabWord(BaseModel):
    word: str
    category: int
    type: str



class TimeStampedModel(Model):

    """ TimeStampedModel Model Definition """
    id = PrimaryKeyField()
    created = DateTimeField(default=datetime.now)
    updated = DateTimeField()

    def save(self, *args, **kwargs):
        self.updated = datetime.now()
        return super(TimeStampedModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class AbstractCategory(TimeStampedModel):

    """ Abstract Item """

    large_category = CharField(max_length=80)
    medium_category = CharField(max_length=80)
    small_category = CharField(max_length=80)

    class Meta:
        abstract = True
        database = mysql_db


class EntityCategoryItem(AbstractCategory):
    class Meta:
        table_name = "mecab_ner_entitycategoryitem"


class IntentCategoryItem(AbstractCategory):
    class Meta:
        table_name = "mecab_ner_intentcategoryitem"


class BaseModel(TimeStampedModel):
    class Meta:
        database = mysql_db


class MecabEntityItem(BaseModel):

    """ Item Model Definition """

    word = CharField(max_length=80)
    mecab_word = CharField(max_length=150)
    category = ForeignKeyField(
        EntityCategoryItem, backref='mecab_entities', on_delete='CASCADE'
    )

    class Meta:
        table_name = "mecab_ner_mecabentity"


class MecabIntentItem(BaseModel):

    """ Item Model Definition """

    word = CharField(max_length=80)
    mecab_word = CharField(max_length=150)
    category = ForeignKeyField(
        IntentCategoryItem, backref='mecab_intents', on_delete='CASCADE'
    )

    class Meta:
        table_name = "mecab_ner_mecabintent"
