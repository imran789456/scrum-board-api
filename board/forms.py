import django_filters
from . import models
from django.contrib.auth import get_user_model

User = get_user_model()


class NullFilter(django_filters.BooleanFilter):
    """Filter on a field set as null or not."""

    def filter(self, qs, value):
        if value is not None:
            return qs.filter(**{'%s__isnull' % self.name: value})
            # return qs.filter(**{ self.name__isnull: value })
        
        return qs 


class TaskFilter(django_filters.FilterSet):
    backlog = NullFilter(name='sprint')

    class Meta:
        model = models.Task 
        fields = ('sprint', 'status', 'assigned')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['assigned'].extra.update({
            'to_field_name': User.USERNAME_FIELD,
        })


class SprintFilter(django_filters.FilterSet):
    end_min = django_filters.DateFilter(name='end', lookup_type='gte')
    end_max = django_filters.DateFilter(name='end', lookup_type='lte')

    class Meta:
        model = models.Sprint 
        fields = ('end_min', 'end_max')