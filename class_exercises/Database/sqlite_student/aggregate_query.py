import sqlite3

with sqlite3.connect('student.sqlite') as conn:
    cursor = conn.cursor()
    aveage_query = """
    SELECT gender, avg(age)
    FROM students
    GROUP BY gender"""

    average_age_by_gender = cursor.execute(aveage_query).fetchall()

print(average_age_by_gender)