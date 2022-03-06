from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import ListView, View
from . import models, forms
# Create your views here.
from mecab_ner.docker_api import create_mecab_index, insert_mecab_data

def index(request):
    return render(request, 'mecab_ner/ner_list.html', {})


class EntityCategoryItemView(ListView):

    """ HomeView Definition """

    model = models.EntityCategoryItem
    paginate_by = 10
    ordering = "created"
    context_object_name = "entity_category_items"
    template_name_suffix = '_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class EntityItemView(ListView):

    """ HomeView Definition """

    model = models.MecabEntity
    ordering = "created"
    paginate_by = 10
    context_object_name = "mecab_entity_items"
    template_name_suffix = '_list'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EntityCategorySearchView(View):

    """ SearchView Definition """

    def get(self, request):

        entity_category = request.GET.get("entity_category")
        page = request.GET.get("page", 1)
        if entity_category:

            form = forms.EntityCategorySearchForm(request.GET)

            if form.is_valid():

                entity_category = form.cleaned_data.get("entity_category")

                filter_args = {}

                if entity_category != "AnyCategory":
                    filter_args["small_category__contains"] = entity_category
                qs = models.EntityCategoryItem.objects.filter(**filter_args).order_by("-created")
                if qs.count() == 0:
                    filter_args = {}
                    filter_args["medium_category__contains"] = entity_category
                    qs = models.EntityCategoryItem.objects.filter(**filter_args).order_by("-created")

                if qs.count() == 0:
                    filter_args = {}
                    filter_args["large_category__contains"] = entity_category
                    qs = models.EntityCategoryItem.objects.filter(**filter_args).order_by("-created")

                paginator = Paginator(qs, 10, orphans=5)



                qs = paginator.get_page(page)

                return render(
                    request, "mecab_ner/entitycategoryitem_search.html", {"form": form, "entity_category_items": qs,
                                                                          "entity_search_item": entity_category}
                )

        else:
            form = forms.EntityCategorySearchForm()

        return render(request, "mecab_ner/entitycategoryitem_search.html", {"form": form})


class EntityCategoryAddView(View):

    """ SearchView Definition """

    def post(self, request):

        form = forms.EntityCategoryAddForm()

        large_category = request.POST.get("large_category")
        medium_category = request.POST.get("medium_category")
        small_category = request.POST.get("small_category")
        json_data = {"large_category": large_category, "medium_category": medium_category,
                     "small_category": small_category, "type": "entity"}

        answer = create_mecab_index(json_data)

        if not answer:
            return render(request, "mecab_ner/entitycategoryitem_add.html", {"form": form})

        return render(request, "mecab_ner/entitycategoryitem_list.html", {"form": form})


    def get(self, request):

        form = forms.EntityCategoryAddForm()


        return render(request, "mecab_ner/entitycategoryitem_add.html", {"form": form})