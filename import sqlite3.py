import sqlite3
import pandas as pd

# define connections

connection = sqlite3.connect("students.db")

# define cursor

cursor = connection.cursor()

while True:
    print("Welcome to the student course enrollment system")
    print("1. Display Students by Last Name")
    print("2. Search Student by Name")
    print("3. Display Students by Major")
    print("4. Display Majors by Departments")
    print("5. Display all Courses")
    print("6. Display courses enrolled by students")
    print("7. Import student list")
    print("8. Exit the program")
    choice = int(input("Please select your choice:"))
    if choice == 1:
        sql = """SELECT student_lastname, student_name, student_id, student_email, student_dob,
        major_id From students ORDER BY student_lastname"""
        cursor.execute(sql)
        rows = cursor.fetchall()

        df = pd.DataFrame(rows, columns = ['Last Name', 'Name', 'ID', 'Email', 'DOB', 'Major ID'])

        print(df)
    elif choice == 2:

        stud_name = input("Enter student's name: ")
        sql = "SELECT * FROM students WHERE student_name LIKE ? "
        cursor.execute(sql, (stud_name,))
        rows = cursor.fetchall()
        if len(rows) > 0:
            df = pd.DataFrame(rows, columns = ['ID', 'Name', 'Last Name', 'Email', 'DOB', 'Major ID'])
            print()
            print(df)
            print()
        else:
            print("\nNo record is found")

    elif choice == 3:

        sql = " SELECT major_id, major_name FROM majors"
        cursor.execute(sql)
        rows = cursor.fetchall()
        if len(rows) > 0:
            df = pd.DataFrame(rows, columns = ['Major ID', 'Major Name'])
            print(df)
            print()

        major_id = input("Please enter a Major ID: ")
        sql = "SELECT major_id, student_name, student_lastname FROM students" #still needs work it shows all students
        cursor.execute(sql,)
        rows = cursor.fetchall()
        if len(rows) > 0:
            df = pd.DataFrame(rows, columns = ['Major', 'ID' 'Name', 'Last Name'])
            print(df)
            print()
    elif choice == 4:

        sql = "SELECT * FROM departments"
        cursor.execute(sql)
        rows = cursor.fetchall()
        if len(rows) > 0:
            df = pd.DataFrame(rows, columns = ['Dept. ID', 'Department', 'Dept. Location', 'Phone'])
            print(df)
            print()

        department_id = input('Enter Major ID: ') #Confused comeback later/ Picture and task are different
        sql = """SELECT department_name, department_location FROM departments"""
        if len(rows) > 0:
            df = pd.DataFrame(rows, columns = ['Dept. ID', 'Department', 'Dept. Location', 'Phone'])
            print(df)
            print()


    elif choice == 5:

        sql = "SELECT * FROM courses"
        cursor.execute(sql)
        rows = cursor.fetchall()

        df = pd.DataFrame(rows, columns=['Course ID', 'Course Number', 'Course Name', 'Department ID'])
        print(df)
        print()
    elif choice == 6:

        sql = "SELECT * FROM students"
        cursor.execute(sql)
        rows = cursor.fetchall()
        if len(rows) > 0:
            df = pd.DataFrame(rows, columns = [])
            print(df)
            print()

    elif choice == 7:
        print()

    elif choice == 8:
        print("Program exited")
        break
    else:
        print("Invalid choice. Try a different option.")
