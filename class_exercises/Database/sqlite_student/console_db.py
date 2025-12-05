import sqlite3

with sqlite3.connect('student.sqlite') as conn:
    cursor = conn.cursor()

    # Change the name of all 'William's to 'Bill'
    update_sql = """
    UPDATE students
    SET firstname ='Bill'
    WHERE firstname = 'William';
    """
    cursor.execute(update_sql)
    conn.commit()

    # Update the last name of student with id = 4
    update_sql = """
    UPDATE students
    SET lastname = ?
    WHERE id = 4;"""

    cursor.execute(update_sql, ('Smith', ))

