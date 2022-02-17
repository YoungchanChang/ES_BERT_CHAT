from django.db import models
from core import models as core_models
# Create your models here.


class Friend(core_models.TimeStampedModel):

    """ Item Model Definition """

    name = models.CharField(max_length=100)
    talk = models.TextField(blank=True, default="")

