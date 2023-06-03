from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.db import connection
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import datetime


from .campus_utils import reports, dict_fetchall, dict_fetchone


def index(request):
    return render(request, 'campus/home.html')


# region: students

def students_index(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, name, last_name, date_of_birth, favorite_number, country_of_origin, active, created_at
            FROM students""")
        students = dict_fetchall(cursor)
    return render(request, 'campus/students/index.html', {'students': students})


def students_detail(request, student_id):
    with connection.cursor() as cursor:
        q = """
            SELECT id, name, last_name, date_of_birth, favorite_number, country_of_origin, active, created_at
            FROM students
            WHERE id = %s"""
        cursor.execute(q, [student_id])
        student = dict_fetchone(cursor)
        q = """
            SELECT
                cl.id as "Class ID",
                cl.school as "School",
                c.semester as "Period",
                e.grade as "Grade"
            FROM enrollments e
            JOIN courses c on c.id = e.course_id
            JOIN classes cl on c.class_id = cl.id
            WHERE e.student_id = %s"""
        cursor.execute(q, [student_id])
        enrollments_rows = cursor.fetchall()
        enrollments_headers = [d[0] for d in cursor.description]

    context = {
        'student': student,
        'enrollments_rows': enrollments_rows,
        'enrollments_headers': enrollments_headers,
    }
    return render(request, 'campus/students/detail.html', context)


def students_add(request):
    student = {'date_of_birth': datetime.date(1999, 1, 1)}
    return render(request, 'campus/students/detail.html', {'student': student, 'create': True})


@csrf_exempt
def students_save(request, student_id):
    posted = {
        'name': request.POST['name'],
        'last_name': request.POST['last_name'],
        'date_of_birth': request.POST['date_of_birth'],
        'favorite_number': request.POST['favorite_number'],
        'country_of_origin': request.POST['country_of_origin'],
        'active': 1 if 'active' in request.POST else 0,
        'id': student_id,
    }
    with connection.cursor() as cursor:
        q = """
            UPDATE students
            SET name=:name, last_name=:last_name, date_of_birth=:date_of_birth,
            favorite_number=:favorite_number, country_of_origin=:country_of_origin, active=:active
            WHERE id=:id"""
        cursor.execute(q, posted)
        connection.commit()
        return HttpResponseRedirect(reverse('campus:students-index'))


@csrf_exempt
def students_create(request):
    posted = {
        'id': request.POST['id'],
        'name': request.POST['name'],
        'last_name': request.POST['last_name'],
        'date_of_birth': request.POST['date_of_birth'],
        'favorite_number': request.POST['favorite_number'],
        'country_of_origin': request.POST['country_of_origin'],
        'active': 1 if 'active' in request.POST else 0
    }
    with connection.cursor() as cursor:
        q = """
            INSERT INTO students (name, last_name, date_of_birth, favorite_number, country_of_origin, active, id)
            VALUES (:name, :last_name, :date_of_birth, :favorite_number, :country_of_origin, :active, :id)"""
        cursor.execute(q, posted)
        connection.commit()
        return HttpResponseRedirect(reverse('campus:students-index'))

# endregion


# region: teachers


def teachers_index(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, name, last_name, date_of_birth, degree, created_at FROM teachers")
        teachers = dict_fetchall(cursor)
    return render(request, 'campus/teachers/index.html', {'teachers': teachers})


def teachers_detail(request, teacher_id):
    with connection.cursor() as cursor:
        q = """
            SELECT id, name, last_name, date_of_birth, degree, created_at
            FROM teachers
            WHERE id = %s"""
        cursor.execute(q, [teacher_id])
        teacher = dict_fetchone(cursor)
    return render(request, 'campus/teachers/detail.html', {'teacher': teacher, 'teacher_id': teacher_id})


def teachers_add(request):
    teacher = {'date_of_birth': datetime.date(1999, 1, 1)}
    context = {'teacher': teacher, 'create': True}
    return render(request, 'campus/teachers/detail.html', context)


@csrf_exempt
def teachers_save(request, teachers_id):
    posted = {
        'id': teachers_id,
        'name': request.POST['name'],
        'last_name': request.POST['last_name'],
        'date_of_birth': request.POST['date_of_birth'],
        'degree': request.POST['degree'],
        'active': 1 if 'active' in request.POST else 0,
    }
    with connection.cursor() as cursor:
        q = """
            UPDATE teachers
            SET name=:name, last_name=:last_name, date_of_birth=:date_of_birth, degree=:degree
            WHERE id=:id"""
        cursor.execute(q, posted)
        connection.commit()
    return HttpResponseRedirect(reverse('campus:teachers-index'))


@csrf_exempt
def teachers_create(request):
    posted = {
        'id': request.POST['id'],
        'name': request.POST['name'],
        'last_name': request.POST['last_name'],
        'date_of_birth': request.POST['date_of_birth'],
        'degree': request.POST['degree'],
        'active': 1 if 'active' in request.POST else 0,
    }
    with connection.cursor() as cursor:
        q = """INSERT INTO teachers (name, last_name, date_of_birth, degree, id)
               VALUES (:name, :last_name, :date_of_birth, :degree, :id)
            """
        cursor.execute(q, posted)
        connection.commit()
        return HttpResponseRedirect(reverse('campus:teachers-index'))

# endregion

# region: classes


def classes_index(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, name, school, created_at FROM classes")
        classes = dict_fetchall(cursor)
    return render(request, 'campus/classes/index.html', {'classes': classes})


def classes_detail(request, classes_id):
    with connection.cursor() as cursor:
        q = """
            SELECT id, name, school, created_at
            FROM classes
            WHERE id = %s"""
        cursor.execute(q, [classes_id])
        classes = dict_fetchone(cursor)
    return render(request, 'campus/classes/detail.html', {'classes': classes, 'classes_id': classes_id})


def classes_add(request):
    classes = dict()
    context = {'classes': classes, 'create': True}
    return render(request, 'campus/classes/detail.html', context)


@csrf_exempt
def classes_save(request, classes_id):
    posted = {
        'id': classes_id,
        'name': request.POST['name'],
        'school': request.POST['school'],
        'active': 1 if 'active' in request.POST else 0,
    }
    with connection.cursor() as cursor:
        q = """
            UPDATE classes
            SET name=:name, school=:school
            WHERE id=:id"""
        cursor.execute(q, posted)
        connection.commit()
    return HttpResponseRedirect(reverse('campus:classes-index'))


@csrf_exempt
def classes_create(request):
    posted = {
        'id': request.POST['id'],
        'name': request.POST['name'],
        'school': request.POST['school'],
        'active': 1 if 'active' in request.POST else 0,
    }
    with connection.cursor() as cursor:
        q = """INSERT INTO classes (name, school, id)
               VALUES (:name, :school, :id)
            """
        cursor.execute(q, posted)
        connection.commit()
        return HttpResponseRedirect(reverse('campus:classes-index'))

# endregion

# region: reports


def report(request, report_id):
    rpt = reports[report_id]
    cursor = connection.cursor()
    result = cursor.execute(rpt['query'])
    context = {
        'rows': result.fetchall(),
        'headers': [d[0] for d in result.description],
        'report_title': rpt['title'],
    }

    if 'download' in request.GET:
        response = HttpResponse(content_type='text/csv')
        pd.DataFrame(context['rows'], columns=context['headers']).set_index(context['headers'][0]).to_csv(response)
        response['Content-Disposition'] = f'attachment; filename={report_id}.csv'
        return response
    else:
        return render(request, 'campus/reports/campus_report.html', context)

# endregion


def common(request):
    return {
        # for tpl html to render menu
        'reports': {r: reports[r]['title'] for r in reports}
    }