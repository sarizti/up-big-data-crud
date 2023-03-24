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
    path('teachers/<int:teachers_id>/save', views.teachers_save, name='teachers-save'),
    # ex: /campus/teachers/create
    path('teachers/create', views.teachers_create, name='teachers-create'),

    # reports

    # ex: /campus/student-enrollments
    path('student-enrollments', views.student_enrollments, name='student-enrollments'),
]
