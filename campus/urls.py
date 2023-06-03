from django.urls import path

from . import views

app_name = 'campus'
urlpatterns = [
    # ex: /campus/
    path('', views.index, name='home'),

    # students

    # ex: /campus/students
    path('students', views.students_index, name='students-index'),
    # ex: /campus/students/5
    path('students/<int:student_id>', views.students_detail, name='students-detail'),
    # ex: /campus/students/add
    path('students/add', views.students_add, name='students-add'),
    # ex: /campus/students/5/save
    path('students/<int:student_id>/save', views.students_save, name='students-save'),
    # ex: /campus/students/create
    path('students/create', views.students_create, name='students-create'),

    # teachers

    # ex: /campus/teachers
    path('teachers', views.teachers_index, name='teachers-index'),
    # ex: /campus/teachers/5
    path('teachers/<int:teacher_id>', views.teachers_detail, name='teachers-detail'),
    # ex: /campus/teachers/add
    path('teachers/add', views.teachers_add, name='teachers-add'),
    # ex: /campus/teacher/5/save
    path('teachers/<int:teacher_id>/save', views.teachers_save, name='teachers-save'),
    # ex: /campus/teachers/create
    path('teachers/create', views.teachers_create, name='teachers-create'),

# classes

    # ex: /campus/classes
    path('classes', views.classes_index, name='classes-index'),
    # ex: /campus/classes/5
    path('classes/<int:classe_id>', views.classes_detail, name='classes-detail'),
    # ex: /campus/classes/add
    path('classes/add', views.classes_add, name='classes-add'),
    # ex: /campus/teacher/5/save
    path('classes/<int:classe_id>/save', views.classes_save, name='classes-save'),
    # ex: /campus/classes/create
    path('classes/create', views.classes_create, name='classes-create'),


    # reports

    # ex: /campus/report/student_enrollments
    path('report/<report_id>', views.report, name='report'),
]
