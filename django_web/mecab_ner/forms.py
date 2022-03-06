
from django import forms
from . import models


class EntityCategorySearchForm(forms.Form):

    entity_category = forms.CharField(initial="AnyCategory")


class EntityCategoryAddForm(forms.Form):

    large_category = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Large Category"})
    )
    medium_category = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Medium Category"})
    )
    small_category = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Small Category"})
    )

