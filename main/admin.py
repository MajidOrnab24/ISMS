from django.contrib import admin
from main.models import*
from admin_app.models import*
from main.admision_models import *



# Register your models here.
admin.site.register(UserAccount)
admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(StaffMed)
admin.site.register(StaffLib)
admin.site.register(department)
admin.site.register(StudentProfile)
admin.site.register(FacultyProfile)
admin.site.register(DeptHeadFaculty)
admin.site.register(StaffMedProfile)
admin.site.register(StaffLibProfile)
admin.site.register(Faq)
admin.site.register(RoadMap)