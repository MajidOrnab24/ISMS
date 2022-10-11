from django.contrib import admin
from main.models import*
from admin_app.models import*

# Register your models here.
admin.site.register(UserAccount)
admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(StaffMed)
admin.site.register(StaffLib)
admin.site.register(department)
admin.site.register(StudentProfile)

