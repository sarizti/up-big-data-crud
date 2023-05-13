DROP TABLE IF EXISTS students;
CREATE TABLE students(
    id INTEGER PRIMARY KEY, -- e.g. 0105123
    name VARCHAR(100),
    last_name VARCHAR(100),
    date_of_birth DATE, -- e.g. 1989-07-27
    favorite_number INTEGER CHECK(favorite_number >= 0), -- e.g. 1.5
    country_of_origin CHAR(3) CHECK(country_of_origin IN ('MEX', 'USA', 'CAN', 'BOL')),
    active INTEGER CHECK(active IN (TRUE, FALSE)) DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

DROP TABLE IF EXISTS classes;
CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    school VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

DROP TABLE IF EXISTS teachers;
CREATE TABLE teachers(
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    last_name VARCHAR(100),
    date_of_birth DATE, -- e.g. 1989-07-27
    degree TEXT CHECK(degree IN ('bachelors', 'masters', 'doctorate')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

DROP TABLE IF EXISTS courses;
CREATE TABLE courses (
    id INTEGER PRIMARY KEY,
    class_id INTEGER REFERENCES classes(id),
    teacher_id INTEGER REFERENCES teachers(id),
    semester CHAR(6), -- e.g. 2023-2
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

DROP TABLE IF EXISTS enrollments;
CREATE TABLE enrollments (
    id INTEGER PRIMARY KEY,
    course_id INTEGER REFERENCES courses(id),
    student_id INTEGER REFERENCES students(id),
    grade INTEGER CHECK(grade between 0 and 100), -- e.g. 95
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

DROP TABLE IF EXISTS attendance;
CREATE TABLE attendance (
    id INTEGER PRIMARY KEY,
    enrollment_id INTEGER REFERENCES enrollments(id),
    class_nr INTEGER, -- e.g. 1, 2, 3
    attended TEXT CHECK(attended IN ('yes', 'late', 'no')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);
