from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.db import connection
from django.urls import reverse
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


def students_save(request, student_id):
    posted = request.POST | {
        'active': 1 if 'active' in request.POST else 0,
        'id': student_id,
    }
    with connection.cursor() as cursor:
        q = """
            UPDATE students
            SET name=%s, last_name=%s, date_of_birth=%s, favorite_number=%s, country_of_origin=%s, active=%s
            WHERE id=%s"""
        cursor.execute(q, posted)
        connection.commit()
        return HttpResponseRedirect(reverse('campus:students-detail', args=(student_id,)))


def students_create(request):
    posted = request.POST | {
        'active': 1 if 'active' in request.POST else 0
    }
    with connection.cursor() as cursor:
        q = """
            INSERT INTO students (name, last_name, date_of_birth, favorite_number, country_of_origin, active, id)
            VALUES (:name, :last_name, :date_of_birth, :favorite_number, :country_of_origin, :active, :id)"""
        cursor.execute(q, posted)
        connection.commit()
        return HttpResponseRedirect(reverse('campus:students-detail', args=(request.POST['id'],)))

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


def teachers_save(request, teacher_id):
    with connection.cursor() as cursor:
        q = """
            UPDATE teachers
            SET name=:name, last_name=:last_name, date_of_birth=:date_of_birth, degree=:degree
            WHERE id=:id"""
        cursor.execute(q, request.POST | {'id': teacher_id})
        connection.commit()
        return HttpResponseRedirect(reverse('campus:teachers-detail', args=(teacher_id,)))


def teachers_create(request):
    with connection.cursor() as cursor:
        q = """INSERT INTO teachers (name, last_name, date_of_birth, degree, id)
               VALUES (:name, :last_name, :date_of_birth, :degree, :id)
            """
        cursor.execute(q, request.POST)
        connection.commit()
        return HttpResponseRedirect(reverse('campus:teachers-detail', args=(request.POST['id'],)))


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
