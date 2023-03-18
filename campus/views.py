from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.db import connection
from django.urls import reverse


def index(request):
    return render(request, 'campus/home.html')


def students_index(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM students")
        students = dict_fetchall(cursor)
    return render(request, 'campus/students_index.html', {'students': students})


def students_detail(request, student_id):
    with connection.cursor() as cursor:
        q = "SELECT * FROM students WHERE id = %s"
        cursor.execute(q, [student_id])
        student = dict_fetchone(cursor)
    return render(request, 'campus/students_detail.html', {'student': student, 'student_id': student_id})


def students_add(request):
    with connection.cursor() as cursor:
        q = "SELECT * FROM students LIMIT 1"  # any, just to get the columns
        cursor.execute(q)
        student = dict_fetchone(cursor)
        student = {k: '' for k in student}  # no values please
    return render(request, 'campus/students_detail.html', {'student': student, 'student_id': 0})


def students_save(request, student_id):
    the_id = request.POST['student_id'] if student_id == 0 else student_id
    posted = [
        request.POST['name'],
        request.POST['last_name'],
        request.POST['date_of_birth'],
        request.POST['favorite_number'],
        request.POST['country_of_origin'],
        1 if 'active' in request.POST else 0,
        request.POST['student_id'] if student_id == 0 else student_id,
    ]
    with connection.cursor() as cursor:
        if student_id == 0:  # zero means new student
            q = """INSERT INTO students (name, last_name, date_of_birth, favorite_number, country_of_origin, active, id)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
        else:
            q = """UPDATE students SET
                name=%s,
                last_name=%s,
                date_of_birth=%s,
                favorite_number=%s,
                country_of_origin=%s,
                active=%s
                WHERE id=%s
            """
        cursor.execute(q, posted)
        connection.commit()
        return HttpResponseRedirect(reverse('campus:students-detail', args=(the_id,)))


# move to another file:

def dict_fetchall(cursor):
    """Return all rows from a cursor as a list of dicts"""
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def dict_fetchone(cursor):
    """Return one row from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    row = cursor.fetchone()
    return dict(zip(columns, row))
