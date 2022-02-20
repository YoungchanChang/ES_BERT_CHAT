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
class MecabEntityAdmin(admin.ModelAdmin):

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("word",)}
        ),
        ("Last Details", {"fields": ("category",)}),
    )
    list_display = (
        "word",
        "mecab_word",
        "show_small_category",
        "show_medium_category",
        'show_large_category',
    )

    def show_small_category(self, obj):
        return obj.category.small_category

    def show_medium_category(self, obj):
        return obj.category.medium_category

    def show_large_category(self, obj):
        return obj.category.large_category

    search_fields = ("word", )
    raw_id_fields = ("category",)

    list_filter = (
        "category__large_category",
        "category__medium_category",
        "category__small_category",
    )
