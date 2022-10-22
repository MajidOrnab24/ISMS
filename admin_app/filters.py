from dataclasses import field
import django_filters
from django.db import models
from admin_app.models import StudentProfile


class StudentFilter(django_filters.FilterSet):
    class Meta:
        model = StudentProfile
        # fields = ['name', 'department','semester']
        fields = {'name' :['exact'],'department':['exact'],'semester':['exact'] }

        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },

        }