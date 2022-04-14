from django_filters import FilterSet, DateFilter, ChoiceFilter, CharFilter
from .models import Post
from django import forms


class PostFilter(FilterSet):
    time_create = DateFilter(field_name='time_create', lookup_expr='gt', label='Опубликовано после ',
                             widget=forms.DateInput(format='%d.%m.%Y"', attrs={'type': 'date'}))
    header = CharFilter(label='Название', lookup_expr='icontains')

    class Meta:
        model = Post
        fields = ['time_create', 'header', 'author', 'category']
