import sqlite3
import pandas as pd
import csv
import os
 
connection = sqlite3.connect("students.db")
cursor = connection.cursor()
 
 
def print_menu():
    print("\n" + "=" * 45)
    print("   Student Course Enrollment System")
    print("=" * 45)
    print("  1.  Display Students by Last Name")
    print("  2.  Search Student by Name")
    print("  3.  Display Students by Major")
    print("  4.  Display Majors by Department")
    print("  5.  Display All Courses")
    print("  6.  Display Courses Enrolled by Student")
    print("  7.  Import Student List from CSV")
    print("  8.  Add New Student")
    print("  9.  Enroll Student in Course")
    print("  10. Remove Student from Course")
    print("  11. Display Enrollment Summary")
    print("  12. Export Results to CSV")
    print("  13. Exit")
    print("=" * 45)
 
 
def no_results():
    print("\n  No records found.\n")
 
 
# Fetches all students sorted alphabetically by last name
def display_students_by_lastname():
    sql = """
        SELECT s.student_lastname, s.student_name, s.student_id,
               s.student_email, s.student_dob, m.major_name
        FROM students s
        LEFT JOIN majors m ON s.major_id = m.major_id
        ORDER BY s.student_lastname
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    if rows:
        df = pd.DataFrame(rows, columns=["Last Name", "First Name", "ID", "Email", "DOB", "Major"])
        print("\n" + df.to_string(index=False))
    else:
        no_results()
 
 
# Searches students by partial first or last name
def search_student_by_name():
    stud_name = input("\n  Enter student name (or partial): ").strip()
    sql = """
        SELECT s.student_id, s.student_name, s.student_lastname,
               s.student_email, s.student_dob, m.major_name
        FROM students s
        LEFT JOIN majors m ON s.major_id = m.major_id
        WHERE s.student_name LIKE ?
           OR s.student_lastname LIKE ?
    """
    cursor.execute(sql, (f"%{stud_name}%", f"%{stud_name}%"))
    rows = cursor.fetchall()
    if rows:
        df = pd.DataFrame(rows, columns=["ID", "First Name", "Last Name", "Email", "DOB", "Major"])
        print("\n" + df.to_string(index=False))
    else:
        no_results()
 
 
# Lists all majors then filters students by the selected major
def display_students_by_major():
    sql = "SELECT major_id, major_name FROM majors ORDER BY major_name"
    cursor.execute(sql)
    rows = cursor.fetchall()
    if rows:
        df = pd.DataFrame(rows, columns=["Major ID", "Major Name"])
        print("\n" + df.to_string(index=False))
    else:
        no_results()
        return
 
    major_id = input("\n  Enter Major ID to see students: ").strip()
    sql = """
        SELECT s.student_id, s.student_name, s.student_lastname, s.student_email
        FROM students s
        WHERE s.major_id = ?
        ORDER BY s.student_lastname
    """
    cursor.execute(sql, (major_id,))
    rows = cursor.fetchall()
    if rows:
        df = pd.DataFrame(rows, columns=["ID", "First Name", "Last Name", "Email"])
        print("\n" + df.to_string(index=False))
        print(f"\n  {len(rows)} student(s) found in Major ID {major_id}")
    else:
        print(f"\n  No students found for Major ID: {major_id}")
 
 
# Lists all departments then shows majors belonging to the selected department
def display_majors_by_department():
    sql = "SELECT dept_id, department_name, department_location, phone FROM departments"
    cursor.execute(sql)
    rows = cursor.fetchall()
    if rows:
        df = pd.DataFrame(rows, columns=["Dept ID", "Department", "Location", "Phone"])
        print("\n" + df.to_string(index=False))
    else:
        no_results()
        return
 
    dept_id = input("\n  Enter Department ID to see its majors: ").strip()
    sql = """
        SELECT m.major_id, m.major_name, d.department_name
        FROM majors m
        JOIN departments d ON m.dept_id = d.dept_id
        WHERE d.dept_id = ?
        ORDER BY m.major_name
    """
    cursor.execute(sql, (dept_id,))
    rows = cursor.fetchall()
    if rows:
        df = pd.DataFrame(rows, columns=["Major ID", "Major Name", "Department"])
        print("\n" + df.to_string(index=False))
    else:
        print(f"\n  No majors found for Department ID: {dept_id}")
 
 
# Displays every course with its department name
def display_all_courses():
    sql = """
        SELECT c.course_id, c.course_number, c.course_name, d.department_name
        FROM courses c
        LEFT JOIN departments d ON c.dept_id = d.dept_id
        ORDER BY c.course_number
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    if rows:
        df = pd.DataFrame(rows, columns=["Course ID", "Course No.", "Course Name", "Department"])
        print("\n" + df.to_string(index=False))
    else:
        no_results()
 
 
# Shows all courses a specific student is enrolled in
def display_student_enrollments():
    student_id = input("\n  Enter Student ID: ").strip()
    cursor.execute("SELECT student_name, student_lastname FROM students WHERE student_id = ?", (student_id,))
    student = cursor.fetchone()
    if not student:
        print(f"\n  No student found with ID: {student_id}")
        return
 
    print(f"\n  Courses enrolled for: {student[0]} {student[1]}")
    sql = """
        SELECT c.course_number, c.course_name, d.department_name,
               e.enrollment_date, e.grade
        FROM enrollments e
        JOIN courses c ON e.course_id = c.course_id
        JOIN departments d ON c.dept_id = d.dept_id
        WHERE e.student_id = ?
        ORDER BY e.enrollment_date
    """
    cursor.execute(sql, (student_id,))
    rows = cursor.fetchall()
    if rows:
        df = pd.DataFrame(rows, columns=["Course No.", "Course Name", "Department", "Enrolled Date", "Grade"])
        print("\n" + df.to_string(index=False))
        print(f"\n  Total courses enrolled: {len(rows)}")
    else:
        print("  This student is not enrolled in any courses.")
 
 
# Reads a CSV file and inserts each row as a new student record
def import_students_from_csv():
    filepath = input("\n  Enter path to CSV file: ").strip()
    if not os.path.exists(filepath):
        print(f"\n  File not found: {filepath}")
        return
 
    imported = 0
    skipped = 0
 
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                cursor.execute("""
                    INSERT OR IGNORE INTO students
                    (student_id, student_name, student_lastname,
                     student_email, student_dob, major_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    row["student_id"],
                    row["student_name"],
                    row["student_lastname"],
                    row.get("student_email", ""),
                    row.get("student_dob", ""),
                    row.get("major_id", ""),
                ))
                if cursor.rowcount > 0:
                    imported += 1
                else:
                    skipped += 1
            except Exception as e:
                print(f"  Skipping row — error: {e}")
                skipped += 1
 
    connection.commit()
    print(f"\n  Import complete: {imported} added, {skipped} skipped.")
 
 
# Prompts for student details and inserts a new record into the database
def add_new_student():
    print("\n  Add New Student")
    sid = input("  Student ID: ").strip()
    first = input("  First Name: ").strip()
    last = input("  Last Name: ").strip()
    email = input("  Email: ").strip()
    dob = input("  Date of Birth (YYYY-MM-DD): ").strip()
    major_id = input("  Major ID: ").strip()
 
    try:
        cursor.execute("""
            INSERT INTO students (student_id, student_name, student_lastname,
                                  student_email, student_dob, major_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (sid, first, last, email, dob, major_id))
        connection.commit()
        print(f"\n  Student {first} {last} added successfully.")
    except sqlite3.IntegrityError:
        print(f"\n  Error: Student ID {sid} already exists.")
    except Exception as e:
        print(f"\n  Error adding student: {e}")
 
 
# Enrolls a student in a course and sets their grade to In Progress
def enroll_student():
    student_id = input("\n  Enter Student ID: ").strip()
    course_id = input("  Enter Course ID: ").strip()
    enroll_date = input("  Enrollment Date (YYYY-MM-DD): ").strip()
 
    try:
        cursor.execute("""
            INSERT INTO enrollments (student_id, course_id, enrollment_date, grade)
            VALUES (?, ?, ?, ?)
        """, (student_id, course_id, enroll_date, "In Progress"))
        connection.commit()
        print(f"\n  Student {student_id} enrolled in Course {course_id}.")
    except sqlite3.IntegrityError:
        print("\n  Error: Student is already enrolled in this course.")
    except Exception as e:
        print(f"\n  Error: {e}")
 
 
# Removes a student from a course by deleting their enrollment record
def remove_enrollment():
    student_id = input("\n  Enter Student ID: ").strip()
    course_id = input("  Enter Course ID to drop: ").strip()
 
    cursor.execute("""
        DELETE FROM enrollments
        WHERE student_id = ? AND course_id = ?
    """, (student_id, course_id))
    connection.commit()
 
    if cursor.rowcount > 0:
        print(f"\n  Removed Student {student_id} from Course {course_id}.")
    else:
        print("\n  No matching enrollment found.")
 
 
# Shows how many students are enrolled in each course
def enrollment_summary():
    sql = """
        SELECT c.course_name, c.course_number,
               COUNT(e.student_id) as enrolled
        FROM courses c
        LEFT JOIN enrollments e ON c.course_id = e.course_id
        GROUP BY c.course_id
        ORDER BY enrolled DESC
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    if rows:
        df = pd.DataFrame(rows, columns=["Course Name", "Course No.", "Students Enrolled"])
        print("\n" + df.to_string(index=False))
        total = sum(r[2] for r in rows)
        print(f"\n  Total enrollments across all courses: {total}")
    else:
        no_results()
 
 
# Exports students, enrollments, or courses to a CSV file
def export_to_csv():
    print("\n  What would you like to export?")
    print("  1. All students")
    print("  2. All enrollments")
    print("  3. All courses")
    choice = input("  Choice: ").strip()
 
    queries = {
        "1": ("SELECT * FROM students", "students_export.csv"),
        "2": ("SELECT * FROM enrollments", "enrollments_export.csv"),
        "3": ("SELECT * FROM courses", "courses_export.csv"),
    }
 
    if choice not in queries:
        print("  Invalid choice.")
        return
 
    sql, filename = queries[choice]
    cursor.execute(sql)
    rows = cursor.fetchall()
    cols = [desc[0] for desc in cursor.description]
 
    df = pd.DataFrame(rows, columns=cols)
    df.to_csv(filename, index=False)
    print(f"\n  Exported {len(rows)} rows to {filename}")
 
 
# Runs the menu loop and routes each selection to its function
def main():
    while True:
        print_menu()
        try:
            choice = int(input("  Select an option: "))
        except ValueError:
            print("\n  Please enter a number.")
            continue
 
        if choice == 1:
            display_students_by_lastname()
        elif choice == 2:
            search_student_by_name()
        elif choice == 3:
            display_students_by_major()
        elif choice == 4:
            display_majors_by_department()
        elif choice == 5:
            display_all_courses()
        elif choice == 6:
            display_student_enrollments()
        elif choice == 7:
            import_students_from_csv()
        elif choice == 8:
            add_new_student()
        elif choice == 9:
            enroll_student()
        elif choice == 10:
            remove_enrollment()
        elif choice == 11:
            enrollment_summary()
        elif choice == 12:
            export_to_csv()
        elif choice == 13:
            print("\n  Goodbye.\n")
            connection.close()
            break
        else:
            print("\n  Invalid choice. Please select 1-13.")
 
 
if __name__ == "__main__":
    main()
 