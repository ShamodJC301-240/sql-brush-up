-- Run this once to set up the students.db database
-- Usage: python setup_db.py

CREATE TABLE IF NOT EXISTS departments (
    dept_id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_name TEXT NOT NULL,
    department_location TEXT,
    phone TEXT
);

CREATE TABLE IF NOT EXISTS majors (
    major_id INTEGER PRIMARY KEY AUTOINCREMENT,
    major_name TEXT NOT NULL,
    dept_id INTEGER,
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);

CREATE TABLE IF NOT EXISTS students (
    student_id TEXT PRIMARY KEY,
    student_name TEXT NOT NULL,
    student_lastname TEXT NOT NULL,
    student_email TEXT,
    student_dob TEXT,
    major_id INTEGER,
    FOREIGN KEY (major_id) REFERENCES majors(major_id)
);

CREATE TABLE IF NOT EXISTS courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_number TEXT NOT NULL,
    course_name TEXT NOT NULL,
    dept_id INTEGER,
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);

CREATE TABLE IF NOT EXISTS enrollments (
    enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    course_id INTEGER NOT NULL,
    enrollment_date TEXT,
    grade TEXT DEFAULT 'In Progress',
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    UNIQUE (student_id, course_id)
);

-- Sample departments
INSERT OR IGNORE INTO departments (dept_id, department_name, department_location, phone) VALUES
(1, 'Computer Science', 'Building A, Room 101', '555-1001'),
(2, 'Business',         'Building B, Room 202', '555-1002'),
(3, 'Mathematics',      'Building C, Room 303', '555-1003'),
(4, 'Health Sciences',  'Building D, Room 404', '555-1004');

-- Sample majors
INSERT OR IGNORE INTO majors (major_id, major_name, dept_id) VALUES
(1, 'Software Engineering',     1),
(2, 'Cybersecurity',            1),
(3, 'Data Science',             1),
(4, 'Business Administration',  2),
(5, 'Accounting',               2),
(6, 'Applied Mathematics',      3),
(7, 'Nursing',                  4),
(8, 'Health Information',       4);

-- Sample courses
INSERT OR IGNORE INTO courses (course_id, course_number, course_name, dept_id) VALUES
(1,  'CS101',  'Introduction to Programming',    1),
(2,  'CS201',  'Data Structures',                1),
(3,  'CS301',  'Database Systems',               1),
(4,  'CS401',  'Software Engineering',           1),
(5,  'CS450',  'Cybersecurity Fundamentals',     1),
(6,  'BUS101', 'Introduction to Business',       2),
(7,  'BUS201', 'Principles of Accounting',       2),
(8,  'BUS301', 'Business Law',                   2),
(9,  'MTH101', 'College Algebra',                3),
(10, 'MTH201', 'Calculus I',                     3),
(11, 'MTH301', 'Statistics',                     3),
(12, 'HLT101', 'Introduction to Health Science', 4),
(13, 'HLT201', 'Medical Terminology',            4),
(14, 'HLT301', 'Anatomy and Physiology',         4);

-- Sample students
INSERT OR IGNORE INTO students (student_id, student_name, student_lastname, student_email, student_dob, major_id) VALUES
('S001', 'James',   'Anderson', 'j.anderson@school.edu', '2001-03-15', 1),
('S002', 'Maria',   'Garcia',   'm.garcia@school.edu',   '2002-07-22', 3),
('S003', 'Tyler',   'Thompson', 't.thompson@school.edu', '2000-11-08', 4),
('S004', 'Aisha',   'Williams', 'a.williams@school.edu', '2003-01-30', 7),
('S005', 'Kevin',   'Martinez', 'k.martinez@school.edu', '2001-09-14', 2),
('S006', 'Brianna', 'Johnson',  'b.johnson@school.edu',  '2002-05-19', 5),
('S007', 'Devon',   'Lee',      'd.lee@school.edu',      '2000-08-03', 6),
('S008', 'Sofia',   'Brown',    's.brown@school.edu',    '2003-12-11', 1),
('S009', 'Marcus',  'Davis',    'm.davis@school.edu',    '2001-04-27', 8),
('S010', 'Priya',   'Patel',    'p.patel@school.edu',    '2002-10-05', 3);

-- Sample enrollments
INSERT OR IGNORE INTO enrollments (student_id, course_id, enrollment_date, grade) VALUES
('S001', 1,  '2024-01-15', 'A'),
('S001', 2,  '2024-01-15', 'B+'),
('S001', 9,  '2024-01-15', 'In Progress'),
('S002', 1,  '2024-01-15', 'A-'),
('S002', 3,  '2024-01-15', 'In Progress'),
('S002', 11, '2024-01-15', 'B'),
('S003', 6,  '2024-01-15', 'B+'),
('S003', 7,  '2024-01-15', 'A'),
('S003', 8,  '2024-01-15', 'In Progress'),
('S004', 12, '2024-01-15', 'A'),
('S004', 13, '2024-01-15', 'A-'),
('S004', 14, '2024-01-15', 'In Progress'),
('S005', 1,  '2024-01-15', 'B'),
('S005', 5,  '2024-01-15', 'In Progress'),
('S005', 9,  '2024-01-15', 'A'),
('S006', 6,  '2024-01-15', 'B+'),
('S006', 7,  '2024-01-15', 'In Progress'),
('S007', 9,  '2024-01-15', 'A-'),
('S007', 10, '2024-01-15', 'B+'),
('S007', 11, '2024-01-15', 'In Progress'),
('S008', 1,  '2024-01-15', 'In Progress'),
('S008', 4,  '2024-01-15', 'In Progress'),
('S009', 12, '2024-01-15', 'B'),
('S009', 13, '2024-01-15', 'In Progress'),
('S010', 1,  '2024-01-15', 'A'),
('S010', 3,  '2024-01-15', 'In Progress'),
('S010', 11, '2024-01-15', 'A-');
