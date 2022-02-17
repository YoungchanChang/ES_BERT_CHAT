from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.User)
class CustomUserAdmin(admin.ModelAdmin):

    list_display = ("username", "email", "gender", 'birthdate', 'birthtime')
    list_filter = ("gender", "birthdate", 'birthtime')