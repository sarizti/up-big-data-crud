DROP TABLE IF EXISTS students;
CREATE TABLE students(
    id INT PRIMARY KEY, -- e.g. 0105123
    name VARCHAR(100),
    last_name VARCHAR(100),
    date_of_birth DATE, -- e.g. 1989-07-27
    favorite_number INT CHECK(favorite_number >= 0), -- e.g. 1.5
    country_of_origin CHAR(3) CHECK(country_of_origin IN ('MEX', 'USA', 'CAN', 'BOL')),
    active INT CHECK(active IN (TRUE, FALSE)) DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

DROP TABLE IF EXISTS classes;
CREATE TABLE classes (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    school VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

DROP TABLE IF EXISTS teachers;
CREATE TABLE teachers(
    id INT PRIMARY KEY,
    name VARCHAR(100),
    last_name VARCHAR(100),
    date_of_birth DATE, -- e.g. 1989-07-27
    degree TEXT CHECK(degree IN ('bachelors', 'masters', 'doctorate')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

DROP TABLE IF EXISTS courses;
CREATE TABLE courses (
    id INT PRIMARY KEY,
    class_id INT,
    teacher_id INT REFERENCES teachers(id),
    semester CHAR(6), -- e.g. 2023-2
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

DROP TABLE IF EXISTS enrollments;
CREATE TABLE enrollments (
    id INT PRIMARY KEY,
    course_id INT REFERENCES courses(id),
    student_id INT REFERENCES students(id),
    grade INT CHECK(grade between 0 and 100), -- e.g. 95
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

DROP TABLE IF EXISTS attendance;
CREATE TABLE attendance (
    id INT PRIMARY KEY,
    enrollment_id INT REFERENCES enrollments(id),
    class_nr INT, -- e.g. 1, 2, 3
    attended TEXT CHECK(attended IN ('yes', 'late', 'no')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);
