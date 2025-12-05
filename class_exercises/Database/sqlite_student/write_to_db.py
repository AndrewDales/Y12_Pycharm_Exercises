import sqlite3
import random
from faker import Faker

conn = sqlite3.connect('student.sqlite')
cursor = conn.cursor()
paramterised_insert_query = """
INSERT INTO students (firstname, lastname, age, gender)
VALUES (?, ?, ?, ?);
"""

fake = Faker('en_GB')
fake.random.seed(42)
random.seed(42)

student_data = []
for _ in range(100):
    gender = random.choice(('Male', 'Female'))
    if gender == 'Male':
        f_name = fake.first_name_male()
        l_name = fake.last_name_male()
    else:
        f_name = fake.first_name_female()
        l_name = fake.last_name_female()
    age = random.randint(11, 18)
    student_data.append([f_name, l_name, age, gender])


cursor.executemany(paramterised_insert_query, student_data)
conn.commit()
conn.close()