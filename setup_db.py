import sqlite3
import os

# Reads create_tables.sql and runs it against students.db
def setup():
    if not os.path.exists("create_tables.sql"):
        print("Error: create_tables.sql not found in this folder.")
        return

    with open("create_tables.sql", "r") as f:
        sql = f.read()

    connection = sqlite3.connect("students.db")
    cursor = connection.cursor()
    cursor.executescript(sql)
    connection.commit()
    connection.close()
    print("students.db created and populated successfully.")
    print("You can now run: python enrollment_system.py")

if __name__ == "__main__":
    setup()
