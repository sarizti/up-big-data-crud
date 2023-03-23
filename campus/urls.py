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

    # teachers


]
