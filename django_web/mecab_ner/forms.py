
from django import forms
from . import models


class EntityCategorySearchForm(forms.Form):

    entity_category = forms.CharField(initial="AnyCategory")


class EntityCategoryAddForm(forms.Form):

    large_category = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Entity Large Category"})
    )
    medium_category = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Entity Medium Category"})
    )
    small_category = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Entity Small Category"})
    )


class EntityItemSearchForm(forms.Form):

    entity_item = forms.CharField(initial="AnyEntityItem")


class EntityItemAddForm(forms.Form):

    word = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Word"})
    )

    category_id = forms.ModelChoiceField(
        required=False, empty_label="Any kind", queryset=models.EntityCategoryItem.objects.all()
    )


class IntentCategorySearchForm(forms.Form):

    intent_category = forms.CharField(initial="AnyCategory")


class IntentCategoryAddForm(forms.Form):

    large_category = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Intent Large Category"})
    )
    medium_category = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Intent Medium Category"})
    )
    small_category = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Intent Small Category"})
    )


class IntentItemSearchForm(forms.Form):

    intent_item = forms.CharField(initial="AnyIntentItem")


class IntentItemAddForm(forms.Form):

    word = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Word"})
    )

    category_id = forms.ModelChoiceField(
        required=False, empty_label="Any kind", queryset=models.IntentCategoryItem.objects.all()
    )


class EntityIntentItemTemplateSearchForm(forms.Form):

    entity_intent_item_template = forms.CharField(initial="AnyIntentItem")


class EntityIntentItemTemplateAddForm(forms.Form):

    word = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Sentence"})
    )

    category_id = forms.ModelChoiceField(
        required=False, empty_label="Any kind", queryset=models.EntityIntentCategoryTemplate.objects.all()
    )