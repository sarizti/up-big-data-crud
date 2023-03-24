
reports = {
    'student_enrollments': {
        'title': 'Student Enrollments',
        'query': """
            SELECT
                students.id as "ID",
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
            INNER JOIN classes ON courses.class_id = classes.id
            """
    },
    'course_enrollments': {
        'title': 'Course Enrollments',
        'query': """
            SELECT
                iif(t.degree = 'doctorate', 'Dr.', iif(t.degree = 'masters', 'Mtro.', 'Lic.'))
                    || ' ' || t.name || ' ' || t.last_name
                    AS "Teacher",
                c2.name || '(' || c2.school || ')' as "Class",
                c.semester as "Period",
                (SELECT count(id) FROM enrollments e where e.course_id = c.id) as "Enrollment Count"
            FROM courses c
            JOIN classes c2 on c.class_id = c2.id
            JOIN teachers t on c.teacher_id = t.id
            """
    }
}


def dict_fetchall(cursor):
    """Return all rows from a cursor as a list of dicts"""
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def dict_fetchone(cursor):
    """Return one row from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    row = cursor.fetchone()
    return dict(zip(columns, row))
