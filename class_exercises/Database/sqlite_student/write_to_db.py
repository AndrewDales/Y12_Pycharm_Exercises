import sqlite3
conn = sqlite3.connect('student.sqlite')
cursor = conn.cursor()
paramterised_insert_query = """
INSERT INTO students (firstname, lastname, age, gender)
VALUES (?, ?, ?, ?);
"""

cursor.execute(paramterised_insert_query, ("Aadit", "Lamba", 16, "male"))
conn.commit()
conn.close()