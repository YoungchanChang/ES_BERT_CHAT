import os
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()
from peewee import *
# mysql에서 데이터 읽어온다.
# Path에서 크로스 체킹한다.

mysql_db = MySQLDatabase(os.getenv("RDS_NAME"), user=os.getenv("RDS_USER"), password=os.getenv("RDS_PASSWORD"),
                         host=os.getenv("RDS_HOST"), port=int(os.getenv("RDS_PORT")))


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
        table_name = "entity_category"


class IntentCategoryItem(AbstractCategory):
    class Meta:
        table_name = "intent_category"


class BaseModel(TimeStampedModel):
    class Meta:
        database = mysql_db


class MecabEntity(BaseModel):

    """ Item Model Definition """

    word = CharField(max_length=80)
    mecab_word = CharField(max_length=150)
    category = ForeignKeyField(
        EntityCategoryItem, related_name="entity", on_delete='CASCADE'
    )

    class Meta:
        table_name = "entity_vocab"
