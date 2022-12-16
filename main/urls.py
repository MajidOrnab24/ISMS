from unicodedata import name
from django.urls import path
from . import views
from main import studentViews as student_view
from main import facultyViews as faculty_view
from main import staff_medViews as staff_med_view
from main import staff_libViews as staff_lib_view

from unicodedata import name
from django.urls import path
from . import views
from admin_app import views as admin_view

urlpatterns = [
    path('',views.home, name='home'),
    path('general login',views.general_login, name='general_login'),
    path('viewSemesterPDF/<str:id>', views.viewSemesterPDF, name='viewSemesterPDF'),
    path('viewAdmissionPDF/<str:id>', views.viewAdmissionPDF, name='viewAdmissionPDF'),



    # Admission urls
    path('admission',views.admission, name='admission'),
    path('about',views.about, name='about'),
    path('faq',views.faq, name='faq'),
    path('questionBank',views.questionBank, name='questionBank'),
    path('roadMap',views.roadMap, name='roadMap'),


    # Admission urls of admin
    path('admin_roadmap',admin_view.admin_roadmap,name='admin_roadmap'),
    path('roadmap_add',admin_view.roadmap_add,name='roadmap_add'),
    path('delete_roadmap/<int:id>', admin_view.delete_roadmap, name='delete_roadmap'),
    path('update_roadmap/<int:id>', admin_view.update_roadmap, name='update_roadmap'),
    path('admin_faq',admin_view.admin_faq,name='admin_faq'),
    path('faq_add',admin_view.faq_add,name='faq_add'),
    path('delete_faq/<int:id>', admin_view.delete_faq, name='delete_faq'),
    path('update_faq/<int:id>', admin_view.update_faq, name='update_faq'),





    # Login urls
    path('signinStudent',views.signinStudent, name='signinStudent'),
    path('signinFaculty',views.signinFaculty, name='signinFaculty'),
    path('signinStaff',views.signinStaff, name='signinStaff'),
    path('logout',views.logout_request, name='logout'),
    path('logError',views.logError, name='logError'),


    # student urls
    path('studentPage',student_view.studentPage, name='studentPage'),
    path('changePasswordStudent',student_view.changePasswordStudent, name='changePasswordStudent'),
    path('studentCR_notice',student_view.studentCR_notice, name='studentCR_notice'),
    path('studentCR_notice_add',student_view.studentCR_notice_add, name='studentCR_notice_add'),
    path('studentCR_notice_delete/<int:id>',student_view.studentCR_notice_delete, name='studentCR_notice_delete'),
    path('studentCR_notice_update/<int:id>',student_view.studentCR_notice_update, name='studentCR_notice_update'),
    path('academic_notice',student_view.academic_notice, name='academic_notice'),
    path('official_notice',student_view.official_notice, name='official_notice'),
    path('medical_logs',student_view.medical_logs, name='medical_logs'),
    path('library_book_status',student_view.library_book_status, name='library_book_status'),
    path('teacher_info',student_view.teacher_info, name='teacher_info'),
    path('student_result',student_view.student_result, name='student_result'),



    

















    # faculty urls
    path('facultyPage',faculty_view.facultyPage, name='facultyPage'),
    path('changePasswordFaculty',faculty_view.changePasswordFaculty, name='changePasswordFaculty'),
    path('courses',faculty_view.courses, name='courses'),
    path('courses_add',faculty_view.courses_add, name='courses_add'),
    path('courses_update/<int:id>', faculty_view.courses_update, name='courses_update'),
    path('courses_delete/<int:id>', faculty_view.courses_delete, name='courses_delete'),
    path('assigned_courses',faculty_view.assigned_courses, name='assigned_courses'),
    path('update_profile',faculty_view.update_profile, name='update_profile'),
    path('result',faculty_view.result, name='result'),
    path('update_result/<int:id>',faculty_view.update_result, name='update_result'),
    path('faculty_notice',faculty_view.faculty_notice, name='faculty_notice'),
    path('faculty_notice_add',faculty_view.faculty_notice_add, name='faculty_notice_add'),
    path('faculty_notice_delete/<int:id>', faculty_view.faculty_notice_delete, name='faculty_notice_delete'),
    path('faculty_notice_update/<int:id>', faculty_view.faculty_notice_update, name='faculty_notice_update'),
    path('courses_assigner_page',faculty_view.courses_assigner_page, name='courses_assigner_page'),
    path('courses_assigner_add',faculty_view.courses_assigner_add, name='courses_assigner_add'),
    path('courses_assigner_delete/<int:id>', faculty_view.courses_assigner_delete, name='courses_assigner_delete'),
    path('forward_semester',faculty_view.forward_semester, name='forward_semester'),



    












    










    # Med staff urls
    path('staffMedPage',staff_med_view.staffMedPage, name='staffMedPage'),
    path('changePasswordStaff_med',staff_med_view.changePasswordStaff_med, name='changePasswordStaff_med'),
    path('medlogs',staff_med_view.medlogs, name='medlogs'),
    path('medlogs_add',staff_med_view.medlogs_add, name='medlogs_add'),
    path('medlogs_update/<int:id>', staff_med_view.medlogs_update, name='medlogs_update'),
    path('medlogs_delete/<int:id>', staff_med_view.medlogs_delete, name='medlogs_delete'),












    # Lib staff urls
    path('staffLibPage',staff_lib_view.staffLibPage, name='staffLibPage'),
    path('changePasswordStaff_lib',staff_lib_view.changePasswordStaff_lib, name='changePasswordStaff_lib'),
    path('admissionQuestion',staff_lib_view.admissionQuestion, name='admissionQuestion'),
    path('admissionQuestion_add',staff_lib_view.admissionQuestion_add, name='admissionQuestion_add'),
    path('admissionQuestion_update/<int:id>', staff_lib_view.admissionQuestion_update, name='admissionQuestion_update'),
    path('admissionQuestion_delete/<int:id>', staff_lib_view.admissionQuestion_delete, name='admissionQuestion_delete'),
    path('semesterQuestion',staff_lib_view.semesterQuestion, name='semesterQuestion'),
    path('semesterQuestion_add',staff_lib_view.semesterQuestion_add, name='semesterQuestion_add'),
    path('semesterQuestion_update/<int:id>', staff_lib_view.semesterQuestion_update, name='semesterQuestion_update'),
    path('semesterQuestion_delete/<int:id>', staff_lib_view.semesterQuestion_delete, name='semesterQuestion_delete'),
    path('lib_books',staff_lib_view.lib_books, name='lib_books'),
    path('lib_books_add',staff_lib_view.lib_books_add, name='lib_books_add'),
    path('lib_books_delete/<int:id>',staff_lib_view.lib_books_delete, name='lib_books_delete'),
    path('lib_books_update/<int:id>', staff_lib_view.lib_books_update, name='lib_books_update'),
    path('books_student',staff_lib_view.books_student, name='books_student'),
    path('books_student_delete/<int:id>',staff_lib_view.books_student_delete, name='books_student_delete'),
    path('books_student_update/<int:id>',staff_lib_view.books_student_update, name='books_student_update'),
    path('books_student_add',staff_lib_view.books_student_add, name='books_student_add'),



    





    # admin urls 
    path('adminHome',admin_view.adminHome,name='adminHome'),
     path('changePasswordAdmin',admin_view.changePasswordAdmin, name='changePasswordAdmin'),

    # Admin Students urls
    path('adminStudent',admin_view.adminStudent,name='adminStudent'),
    path('studentregister',admin_view.studentregister,name='studentregister'),
    path('deleteStudent/<int:id>', admin_view.deleteStudent, name='deleteStudent'),
    path('studentUpdate/<int:id>', admin_view.studentUpdate, name='studentUpdate'),
    path('studentChangePass/<int:id>', admin_view.studentChangePass, name='studentChangePass'),

    # Admin Faculty urls
    path('adminFaculty',admin_view.adminFaculty,name='adminFaculty'),
    path('facultyregister',admin_view.facultyregister,name='facultyregister'),
    path('deleteFaculty/<int:id>', admin_view.deleteFaculty, name='deleteFaculty'),
    path('facultyUpdate/<int:id>', admin_view.facultyUpdate, name='facultyUpdate'),
    path('facultyChangePass/<int:id>', admin_view.facultyChangePass, name='facultyChangePass'),

    # Admin Medical Staff urls
    path('adminStaff_med',admin_view.adminStaff_med,name='adminStaff_med'),
    path('staff_med_register',admin_view.staff_med_register,name='staff_med_register'),
    path('deleteStaffMed/<int:id>', admin_view.deleteStaffMed, name='deleteStaffMed'),
    path('staff_medChangePass/<int:id>', admin_view.staff_medChangePass, name='staff_medChangePass'),
    path('staff_medUpdate/<int:id>', admin_view.staff_medUpdate, name='staff_medUpdate'),

    # Admin Library Staff urls
    path('adminStaff_lib',admin_view.adminStaff_lib,name='adminStaff_lib'),
    path('staff_lib_register',admin_view.staff_lib_register,name='staff_lib_register'),
    path('staff_libUpdate/<int:id>', admin_view.staff_libUpdate, name='staff_libUpdate'),
    path('deleteStaffLib/<int:id>', admin_view.deleteStaffLib, name='deleteStaffLib'),
    path('staff_libChangePass/<int:id>', admin_view.staff_libChangePass, name='staff_libChangePass'),

    ]