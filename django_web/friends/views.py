from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from friends import models


class HomeView(ListView):

    """ HomeView Definition """

    model = models.Friend
    paginate_by = 3
    ordering = "created"
    context_object_name = "friends"
    template_name_suffix = '_home'

    def first_photo(self):
        print(self)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
