import django_filters
from django.db.models import JSONField
from django_filters import CharFilter
from django_filters.rest_framework import FilterSet
from .models import Cafe

class CafeFilter(FilterSet):
    services = CharFilter(method='filter_services')
    class Meta:
        model = Cafe
        fields = {
            'opening_hours': ['exact', 'icontains'],  # Normal field filter
        }

        filter_overrides = {
            JSONField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',  # Allows filtering JSONField as text
                },
            },
        }
    def filter_services(self, queryset, name, value):
        return queryset.filter(services__icontains=value) 