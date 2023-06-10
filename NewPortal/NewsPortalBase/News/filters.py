#from django.shortcuts import render
import django_filters
#from django_filters import ModelChoiceFilter
from django import forms
from .models import *


class PostFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(field_name="datetime", widget=forms.DateInput(attrs={'type': "date"}),
                                     label='Дата', lookup_expr='date')

    class Meta:
        model = Post
        fields = {
            'author': ['exact'],
            'heading': ['icontains'],
            'category': ['exact'],
        }
