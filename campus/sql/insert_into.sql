
INSERT INTO students (id, name, last_name, date_of_birth, favorite_number, country_of_origin)
VALUES (0105123, 'Santiago', 'Arizti', '1989-07-27', 1.5, 'MEX'),
       (0214020, 'andrea', 'escoto', '2000-03-10', 42,'MEX'),
       (0216072,'Andrea','Perez','1999-11-18',8,'USA'),
       (0248440,'Raul','Estrada','1997-05-24',24,'MEX'),
       (0215080,'Natalia','Villalpando','2000-08-01',7,'MEX'),
       (0167763,'Eduardo','Díaz','1995-11-28',20,'MEX'),
       (0213865,'Juan Manuel','Valdivia','2000-06-04',6,'BOL'),
       (0214611, 'judith', 'macias' ,'1999-05-17', 15,'MEX'),
       (0205608,'Javier','Orozco','1999-06-09',44,'MEX'),
       (0214177, 'Armando', 'Arroyo', '2000-12-28', 1122,'MEX')
ON CONFLICT DO UPDATE SET
  name=excluded.name,
  last_name=excluded.last_name,
  date_of_birth=excluded.date_of_birth,
  favorite_number=excluded.favorite_number,
  country_of_origin=excluded.country_of_origin,
  active=1;

INSERT INTO classes (id, name, school)
VALUES (1001, 'Big Data', 'ECID'),
       (1002, 'Auditoría de Proyectos', 'EIGP');

INSERT INTO teachers (id, name, last_name, date_of_birth, degree)
VALUES (105123, 'Santiago', 'Arizti', '1989-07-27', 'masters'),
       (101010, 'Elon', 'Musk', '1971-06-28', 'doctorate');

INSERT INTO courses (id, class_id, teacher_id, semester)
VALUES (123, 1001, 105123, '2023-2'),
       (456, 1002, 101010, '2022-1');

INSERT INTO enrollments (id, course_id, student_id, grade)
VALUES (172121, 123, 0214020, 93),
       (172122, 123, 0216072, 82),
       (172123, 123, 0248440, 94),
       (172124, 123, 0215080, 93),
       (172125, 123, 0167763, 97),
       (172126, 123, 0213865, 93),
       (172127, 123, 0214611, 73),
       (172128, 123, 0205608, 93),
       (172129, 123, 0214177, 98);

INSERT INTO attendance (id, enrollment_id, class_nr, attended)
VALUES
(9101, 172121, 1, 'yes'),
(9102, 172122, 1, 'yes'),
(9103, 172123, 1, 'yes'),
(9104, 172124, 1, 'yes'),
(9105, 172125, 1, 'yes'),
(9106, 172126, 1, 'yes'),
(9107, 172127, 1, 'yes'),
(9108, 172128, 1, 'yes'),
(9109, 172129, 1, 'yes'),
(9111, 172121, 2, 'yes'),
(9112, 172122, 2, 'yes'),
(9113, 172123, 2, 'late'),
(9114, 172124, 2, 'yes'),
(9115, 172125, 2, 'yes'),
(9116, 172126, 2, 'yes'),
(9117, 172127, 2, 'yes'),
(9118, 172128, 2, 'no'),
(9119, 172129, 2, 'yes'),
(9121, 172121, 3, 'yes'),
(9122, 172122, 3, 'yes'),
(9123, 172123, 3, 'yes'),
(9124, 172124, 3, 'yes'),
(9125, 172125, 3, 'no'),
(9126, 172126, 3, 'yes'),
(9127, 172127, 3, 'yes'),
(9128, 172128, 3, 'yes'),
(9129, 172129, 3, 'yes');
