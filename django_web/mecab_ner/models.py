from django.db import models
from core import models as core_models
# Create your models here.
from mecab_ner.docker_api import create_mecab_index, insert_mecab_data


class AbstractItem(core_models.TimeStampedModel):

    """ Abstract Item """

    large_category = models.CharField(max_length=80)
    medium_category = models.CharField(max_length=80)
    small_category = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def show_pk(self):
        return self.pk


class EntityCategoryItem(AbstractItem):

    class Meta:
        verbose_name_plural = "entity_categories"

    def save(self, *args, **kwargs):
        json_data = {"large_category": self.large_category, "medium_category": self.medium_category,
                     "small_category": self.small_category, "type": "entity"}

        answer = create_mecab_index(json_data)

        if not answer:
            return

    def delete(self, using=None, keep_parents=False):
        """ Temporary disable """
        pass

class IntentCategoryItem(AbstractItem):

    class Meta:
        verbose_name_plural = "intent_categories"

    def save(self, *args, **kwargs):
        json_data = {'large_category': self.large_category, "medium_category": self.medium_category,
                     "small_category": self.small_category, "type": "intent"}

        answer = create_mecab_index(json_data)

        if not answer:
            return

    def delete(self, using=None, keep_parents=False):
        """ Temporary disable """
        pass

class MecabEntity(core_models.TimeStampedModel):

    """ Item Model Definition """

    word = models.CharField(max_length=80)
    mecab_word = models.CharField(max_length=150)
    category = models.ForeignKey(
        "EntityCategoryItem", related_name="entity", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = "mecab_entities"

    def show_pk(self):
        return self.pk

    def save(self, *args, **kwargs):
        json_data = {'word': self.word, "category": self.category_id,
                     "type": "entity"}

        answer = insert_mecab_data(json_data)

        if not answer:
            return

    def delete(self, using=None, keep_parents=False):
        """ Temporary disable """
        pass

class MecabIntent(core_models.TimeStampedModel):

    """ Item Model Definition """

    word = models.CharField(max_length=80)
    mecab_word = models.CharField(max_length=150)
    category = models.ForeignKey(
        "IntentCategoryItem", related_name="intent", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = "mecab_intents"

    def show_pk(self):
        return self.pk

    def save(self, *args, **kwargs):
        json_data = {'word': self.word, "category": self.category_id,
                     "type": "intent"}

        answer = insert_mecab_data(json_data)

        if not answer:
            return

    def delete(self, using=None, keep_parents=False):
        """ Temporary disable """
        pass