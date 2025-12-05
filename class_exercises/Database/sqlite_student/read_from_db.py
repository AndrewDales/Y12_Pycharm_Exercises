import sqlite3
conn = sqlite3.connect('student.sqlite')
cursor = conn.cursor()

select_students = """
SELECT id, firstname, lastname, age
FROM students  
WHERE age >= 15;
"""

cursor.execute(select_students)
students = cursor.fetchall()
conn.close()