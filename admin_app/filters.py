from dataclasses import field
import django_filters
from django.db import models
from admin_app.models import *


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
class FacultyFilter(django_filters.FilterSet):
    class Meta:
        model = FacultyProfile
        # fields = ['name', 'department']
        fields = {'name' :['exact'],'department':['exact'] }

        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },

        }
class StaffMedFilter(django_filters.FilterSet):
    class Meta:
        model = StaffMedProfile
        fields = {'name' :['exact'],'designation':['exact'] }

        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },

        }