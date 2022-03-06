from django.urls import path
from . import views

app_name = "mecab_ner"

urlpatterns = [path("", views.index, name="list"),
               path("entity_category", views.EntityCategoryItemView.as_view(), name="entity_category"),
               path("entity_category_search/", views.EntityCategorySearchView.as_view(), name="entity_category_search"),
               path("entity_category_add/", views.EntityCategoryAddView.as_view(), name="entity_category_add"),
               path("entity_item/", views.EntityItemView.as_view(), name="entity_item"),
               path("entity_item_search/", views.EntityItemSearchView.as_view(), name="entity_item_search"),
               path("entity_item_add/", views.EntityItemAddView.as_view(), name="entity_item_add"),

               path("intent_category", views.IntentCategoryItemView.as_view(), name="intent_category"),
               path("intent_category_search/", views.IntentCategorySearchView.as_view(), name="intent_category_search"),
               path("intent_category_add/", views.IntentCategoryAddView.as_view(), name="intent_category_add"),
               path("intent_item/", views.IntentItemView.as_view(), name="intent_item"),
               path("intent_item_search/", views.IntentItemSearchView.as_view(), name="intent_item_search"),
               path("intent_item_add/", views.IntentItemAddView.as_view(), name="intent_item_add"),
               ]