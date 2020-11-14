from django import forms
from django.contrib.auth.models import User
from django.forms import CheckboxSelectMultiple

from .models import Person, Group, Bill, Item


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name',)


# class PersonForm(forms.ModelForm):
#     class Meta:
#         model = Person
#         fields =['money']


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_name', 'price']


class BillForm(forms.ModelForm):

    class Meta:
        model = Bill
        fields = ['bill_name', 'no_items']
