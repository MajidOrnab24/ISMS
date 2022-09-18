from django.contrib import admin
from main.models import*

# Register your models here.
admin.site.register(UserAccount)
admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(StaffMed)
admin.site.register(StaffLib)

