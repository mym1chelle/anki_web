import django_filters
from django_filters import filters
from django.forms import CheckboxInput
from django.db.models import Value
from django.db.models.functions import Concat
from anki_web.cards.models import Cards


class FilterForTasks(django_filters.FilterSet):
    class Meta:
        model = Cards
        fields = ['question']

    question = filters.CharFilter(field_name='question')