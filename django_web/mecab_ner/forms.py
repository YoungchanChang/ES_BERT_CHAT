
from django import forms
from . import models


class EntityCategorySearchForm(forms.Form):

    entity_category = forms.CharField(initial="AnyCategory")


class EntityItemSearchForm(forms.Form):

    entity_item = forms.CharField(initial="AnyEntityItem")


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

class EntityItemAddForm(forms.Form):

    word = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Word"})
    )

    category_id = forms.ModelChoiceField(
        required=False, empty_label="Any kind", queryset=models.EntityCategoryItem.objects.all()
    )
