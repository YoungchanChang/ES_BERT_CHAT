from django.contrib.auth.models import AbstractUser
from django.db import models
from core import managers as core_managers
# Create your models here.


class User(AbstractUser):


    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )
    avatar = models.ImageField(upload_to="avatars", null=True, blank=True)
    gender = models.CharField(
        choices=GENDER_CHOICES, max_length=10, null=True, blank=True
    )
    bio = models.TextField(default="", blank=True)

    birthdate = models.DateField(null=True)
    birthtime = models.TimeField(default=None, null=True, blank=True)
    objects = core_managers.CustomUserManager()

    def show_pk(self):
        return self.pk