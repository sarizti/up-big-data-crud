from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db import connection
from django.urls import reverse
import datetime


def index(request):
    return render(request, 'campus/home.html')


# region: students

def students_index(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, name, last_name, date_of_birth, favorite_number, country_of_origin, active, created_at
            FROM students""")
        students = dict_fetchall(cursor)
    return render(request, 'campus/students_index.html', {'students': students})


def students_detail(request, student_id):
    with connection.cursor() as cursor:
        q = """
            SELECT id, name, last_name, date_of_birth, favorite_number, country_of_origin, active, created_at
            FROM students
            WHERE id = %s"""
        cursor.execute(q, [student_id])
        student = dict_fetchone(cursor)
    return render(request, 'campus/students_detail.html', {'student': student, 'student_id': student_id})


def students_add(request):
    dob = datetime.date(1999, 1, 1)
    student = dict(id='', name='', last_name='', date_of_birth=dob, favorite_number='', country_of_origin='',
                   active='', created_at='')
    return render(request, 'campus/students_detail.html', {'student': student, 'create': True})


def students_save(request, student_id):
    posted = [
        request.POST['name'],
        request.POST['last_name'],
        request.POST['date_of_birth'],
        request.POST['favorite_number'],
        request.POST['country_of_origin'],
        1 if 'active' in request.POST else 0,
        student_id,
    ]
    with connection.cursor() as cursor:
        q = """
            UPDATE students
            SET name=%s, last_name=%s, date_of_birth=%s, favorite_number=%s, country_of_origin=%s, active=%s
            WHERE id=%s"""
        cursor.execute(q, posted)
        connection.commit()
        return HttpResponseRedirect(reverse('campus:students-detail', args=(student_id,)))


def students_create(request):
    posted = [
        request.POST['name'],
        request.POST['last_name'],
        request.POST['date_of_birth'],
        request.POST['favorite_number'],
        request.POST['country_of_origin'],
        1 if 'active' in request.POST else 0,
        request.POST['id'],
    ]
    with connection.cursor() as cursor:
        q = """
            INSERT INTO students (name, last_name, date_of_birth, favorite_number, country_of_origin, active, id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(q, posted)
        connection.commit()
        return HttpResponseRedirect(reverse('campus:students-detail', args=(request.POST['id'],)))

# endregion


# region: teachers

def teachers_index(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, name, last_name, date_of_birth, degree, created_at FROM teachers")
        teachers = dict_fetchall(cursor)
    return render(request, 'campus/teachers_index.html', {'teachers': teachers})


def teachers_detail(request, teacher_id):
    with connection.cursor() as cursor:
        q = "SELECT id, name, last_name, date_of_birth, degree, created_at FROM teachers WHERE id = %s"
        cursor.execute(q, [teacher_id])
        teacher = dict_fetchone(cursor)
    return render(request, 'campus/teachers_detail.html', {'teacher': teacher, 'teacher_id': teacher_id})


def teachers_add(request):
    dob = datetime.date(1999, 1, 1)
    teacher = dict(id='', name='', last_name='', date_of_birth=dob, degree='', created_at='')
    return render(request, 'campus/teachers_detail.html', {'teacher': teacher, 'create': True})


def teachers_save(request, teacher_id):
    posted = [
        request.POST['name'],
        request.POST['last_name'],
        request.POST['date_of_birth'],
        request.POST['degree'],
        teacher_id,
    ]
    with connection.cursor() as cursor:
        q = "UPDATE teachers SET name=%s, last_name=%s, date_of_birth=%s, degree=%s WHERE id=%s"
        cursor.execute(q, posted)
        connection.commit()
        return HttpResponseRedirect(reverse('campus:teachers-detail', args=(teacher_id,)))


def teachers_create(request):
    posted = [
        request.POST['name'],
        request.POST['last_name'],
        request.POST['date_of_birth'],
        request.POST['degree'],
        request.POST['id'],
    ]
    with connection.cursor() as cursor:
        q = """INSERT INTO teachers (name, last_name, date_of_birth, degree, id)
               VALUES (%s, %s, %s, %s, %s)
            """
        cursor.execute(q, posted)
        connection.commit()
        return HttpResponseRedirect(reverse('campus:teachers-detail', args=(request.POST['id'],)))


# region: reports

def student_enrollments(request):
    query = """
    -- este es un comentario dentro de sql
    SELECT
        students.name || ' ' || students.last_name AS "Estudiante",
        enrollments.grade AS "Calificación",
        courses.semester AS "Semestre",
        iif(t.degree = 'doctorate', 'Dr.', iif(t.degree = 'masters', 'Mtro.', 'Lic.'))
            || ' ' || t.name || ' ' || t.last_name
            AS "Profesor",
        classes.name || ' (' || classes.school || ')' AS "Clase"
    FROM enrollments
    INNER JOIN students ON enrollments.student_id = students.id
    INNER JOIN courses ON enrollments.course_id = courses.id
    INNER JOIN teachers AS t ON courses.teacher_id = t.id
    INNER JOIN classes ON courses.class_id = classes.id;
    """

    cursor = connection.cursor()
    result = cursor.execute(query)
    rows = result.fetchall()
    headers = [d[0] for d in result.description]
    context = {
        'rows': rows,
        'headers': headers
    }

    return render(request, 'campus/student_enrollments.html', context)

# endregion


# region: utils (move to another file)

def dict_fetchall(cursor):
    """Return all rows from a cursor as a list of dicts"""
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def dict_fetchone(cursor):
    """Return one row from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    row = cursor.fetchone()
    return dict(zip(columns, row))

# endregion
