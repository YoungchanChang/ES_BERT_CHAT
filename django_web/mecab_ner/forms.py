
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
        required=True, empty_label="Any kind", queryset=models.EntityCategoryItem.objects.all()
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
        required=True, empty_label="Any kind", queryset=models.IntentCategoryItem.objects.all()
    )


class EntityIntentItemTemplateSearchForm(forms.Form):

    entity_intent_item_template = forms.CharField(initial="AnyIntentItem")


entity_category_items = models.EntityCategoryItem.objects.all().distinct().values('large_category')
a = [x['large_category'] for x in entity_category_items]
intent_category_items = models.IntentCategoryItem.objects.filter(large_category__in=a).distinct().values('large_category')
b = [(x['large_category'], x['large_category']) for x in intent_category_items]
class EntityIntentItemTemplateAddForm(forms.Form):

    large_category = forms.ChoiceField(widget=forms.Select, required=True, choices=b)


class EntityIntentItemTemplateAddCategoryForm(forms.Form):

    def __init__(self, *args, **kwargs):
        category = kwargs.pop('category')
        qs_ent = models.MecabEntity.objects.filter(category__large_category=category).values('id', 'word')
        qs_int = models.MecabIntent.objects.filter(category__large_category=category).values('id', 'word')
        qs_int_list = [(x['id'], x['word']) for x in qs_int]
        qs_ent_list = [(x['id'], x['word']) for x in qs_ent]
        super(EntityIntentItemTemplateAddCategoryForm, self).__init__(*args, **kwargs)
        self.fields['entity_word_id'].choices = qs_ent_list
        self.fields['intent_word_id'].choices = qs_int_list


    entity_word_id = forms.ChoiceField(widget=forms.Select, required=True, choices=[])
    intent_word_id = forms.ChoiceField(widget=forms.Select, required=True, choices=[])

    sentence = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Sentence"})
    )

