-- report of enrolments with student names
SELECT
    students.name || ' ' || students.last_name AS "Estudiante",
    enrollments.grade AS "Calificación",
    courses.semester AS "Semestre",
    iif(t.degree = 'doctorate', 'Dr.', iif(t.degree = 'masters', 'Mtro.', 'Lic.'))
        || ' ' || t.name || ' ' || t.last_name
        AS "Professor",
    classes.name || ' (' || classes.school || ')' AS "Clase"
FROM enrollments
INNER JOIN students ON enrollments.student_id = students.id
INNER JOIN courses ON enrollments.course_id = courses.id
INNER JOIN teachers AS t ON courses.teacher_id = t.id
INNER JOIN classes ON courses.class_id = classes.id;
