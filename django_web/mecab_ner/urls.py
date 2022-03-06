from django.urls import path
from . import views

app_name = "mecab_ner"

urlpatterns = [path("", views.index, name="list"),
               path("entity_category", views.EntityCategoryItemView.as_view(), name="entity_category"),
               path("entity_category_search/", views.EntityCategorySearchView.as_view(), name="entity_category_search"),
               path("entity_category_add/", views.EntityCategoryAddView.as_view(), name="entity_category_add"),
               path("entity_item/", views.EntityItemView.as_view(), name="entity_item"),
               ]