from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.EntityCategoryItem, models.IntentCategoryItem)
class ItemAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    list_display = ("small_category", "medium_category", "large_category", "used_by")

    list_filter = (
        "small_category",
        "medium_category",
        "large_category",
    )

    def used_by(self, obj):
        return obj.entity.count()



@admin.register(models.MecabEntity)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "word",
        "category",
    )
