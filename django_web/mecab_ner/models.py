from django.db import models
from core import models as core_models
# Create your models here.


class AbstractItem(core_models.TimeStampedModel):

    """ Abstract Item """

    large_category = models.CharField(max_length=80)
    medium_category = models.CharField(max_length=80)
    small_category = models.CharField(max_length=80)

    class Meta:
        abstract = True


class EntityCategoryItem(AbstractItem):

    class Meta:
        verbose_name_plural = "entity_categories"


class IntentCategoryItem(AbstractItem):

    class Meta:
        verbose_name_plural = "intent_categories"


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