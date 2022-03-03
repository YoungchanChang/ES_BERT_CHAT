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
        verbose_name_plural = "Entity Category"

    def save(self, *args, **kwargs):
        json_data = {"large_category": self.large_category, "medium_category": self.medium_category,
                     "small_category": self.small_category, "type": "entity"}

        answer = create_mecab_index(json_data)

        if not answer:
            return

    def __str__(self):
        return self.large_category + "_" + self.medium_category + "_" + self.small_category

    def delete(self, using=None, keep_parents=False):
        """ Temporary disable """
        pass

class IntentCategoryItem(AbstractItem):

    class Meta:
        verbose_name_plural = "Intent Category"

    def save(self, *args, **kwargs):
        json_data = {'large_category': self.large_category, "medium_category": self.medium_category,
                     "small_category": self.small_category, "type": "intent"}

        answer = create_mecab_index(json_data)

        if not answer:
            return

    def __str__(self):
        return self.large_category + "_" + self.medium_category + "_" + self.small_category

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
        verbose_name_plural = "Entity"

    def __str__(self):
        return self.word

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
        verbose_name_plural = "Intent"

    def show_pk(self):
        return self.pk

    def __str__(self):
        return self.word

    def save(self, *args, **kwargs):
        json_data = {'word': self.word, "category": self.category_id,
                     "type": "intent"}

        answer = insert_mecab_data(json_data)

        if not answer:
            return

    def delete(self, using=None, keep_parents=False):
        """ Temporary disable """
        pass


class EntityIntentCategoryTemplate(core_models.TimeStampedModel):

    """ 카테고리로 데이터 관리 """

    bind_category = models.CharField(max_length=80, default="")
    entity_category = models.CharField(max_length=100, default="")
    intent_category = models.CharField(max_length=100, default="")
    template = models.TextField(blank=True, default="")



    class Meta:
        verbose_name_plural = "template"

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


class EntityIntentItemTemplate(core_models.TimeStampedModel):

    """ 카테고리로 데이터 관리 """

    entity_item = models.ForeignKey(
        "MecabEntity", related_name="entity_template", on_delete=models.CASCADE
    )

    intent_item = models.ForeignKey(
        "MecabIntent", related_name="intent_template", on_delete=models.CASCADE
    )

    template = models.TextField(blank=True, default="")



    class Meta:
        verbose_name_plural = "item_template"

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