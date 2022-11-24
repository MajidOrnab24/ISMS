from dataclasses import field
import django_filters
from django.db import models
from admin_app.models import *
from django import forms
from main.admision_models import *
from django.forms.widgets import DateInput


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

class StaffLibFilter(django_filters.FilterSet):
    class Meta:
        model = StaffLibProfile
        fields = {'name' :['exact'],'designation':['exact'] }

        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },

        }
class RoadmapFilter(django_filters.FilterSet):
    class Meta:
        model = RoadMap
        fields = {'event' :['exact'],'date':['exact']}

        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
             models.TextField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },

        }
class FaqFilter(django_filters.FilterSet):
    class Meta:
        model = Faq
        fields = {'question' :['exact'],'answer':['exact']}

        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
             RichTextField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },

        }
class AdmissionQuestionFilter(django_filters.FilterSet):
    class Meta:
        model = QuestionBank
        fields = {'year' :['exact']}

        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },

        }

class semesterQuestionFilter(django_filters.FilterSet):
    class Meta:
        model = SemesterQuestionBank
        fields = {'year' :['exact'],'department' :['exact'],'semester' :['exact']}

        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },

        }

class BooksFilter(django_filters.FilterSet):
    class Meta:
        model = Books
        fields = {'title' :['exact'],'author' :['exact'],'book_code' :['exact'],'category' :['exact'],'shelf_no' :['exact']}

        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },

        }

class BooksStudentFilter(django_filters.FilterSet):
    class Meta:
        model = Books
        fields = {'title' :['exact'],'author' :['exact'],'book_code' :['exact'],'due_date' :['exact'],'student_id__student_ID' :['exact'],'borrow_date' :['exact'],}

        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.DateField: {
                'filter_class': django_filters.DateFilter,
                'extra': lambda f: {
                     'widget': forms.DateInput(attrs={'type' :'date'}),
                    # 'lookup_expr': 'icontains',
                },
            },
            

        }

class MedLogsFilter(django_filters.FilterSet):
    class Meta:
        model = MedLog
        fields = {'student_id__student_ID' :['exact'],'date' :['exact']}

        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
                        models.DateField: {
                'filter_class': django_filters.DateFilter,
                'extra': lambda f: {
                     'widget': forms.DateInput(attrs={'type' :'date'}),
                    # 'lookup_expr': 'icontains',
                },
            },

        }

class CoursesFilter(django_filters.FilterSet):
    class Meta:
        model = Courses
        fields = {'name' :['exact'],'semester' :['exact'],'faculty_id__name' :['exact'],'credit' :['exact']}

        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },

        }

class EnrollmentFilter(django_filters.FilterSet):
    class Meta:
        model = Enrollment
        fields = {'students__name' :['exact'],'courses__name' :['exact'],'courses__semester' :['exact'],'date_joined' :['exact']}

        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.DateField: {
                'filter_class': django_filters.DateFilter,
                'extra': lambda f: {
                     'widget': forms.DateInput(attrs={'type' :'date'}),
                    # 'lookup_expr': 'icontains',
                },
            },

        }

class NoticeFilter(django_filters.FilterSet):
    class Meta:
        model = notice
        fields = {'date' :['exact'],'course__name' :['exact']}

        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.DateField: {
                'filter_class': django_filters.DateFilter,
                'extra': lambda f: {
                     'widget': forms.DateInput(attrs={'type' :'date'}),
                    # 'lookup_expr': 'icontains',
                },
            },

        }

class CRNoticeFilter(django_filters.FilterSet):
    class Meta:
        model = student_notice
        fields = {'date' :['exact']}

        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.DateField: {
                'filter_class': django_filters.DateFilter,
                'extra': lambda f: {
                     'widget': forms.DateInput(attrs={'type' :'date'}),
                    # 'lookup_expr': 'icontains',
                },
            },

        }