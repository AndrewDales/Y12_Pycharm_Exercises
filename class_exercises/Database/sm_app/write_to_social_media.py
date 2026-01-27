import sqlite3

user_data = [('James', 25, 'male', 'USA'),
            ('Leila', 32, 'female', 'France'),
            ('Brigitte', 35, 'female', 'England'),
            ('Mike', 40, 'male', 'Denmark'),
            ('Elizabeth', 21, 'female', 'Canada'),
            ]

post_data = [('Happy', 'I am feeling very happy today', 1),
            ('Hot Weather', 'The weather is very hot today', 2),
            ('Help', 'I need some help with my work', 2),
            ('Great News', 'I am getting married', 1),
            ('Interesting Game', 'It was a fantastic game of tennis', 5),
            ('Party', 'Anyone up for a late-night party today?', 3),
            ]

comment_data = [('Count me in', 1, 6),
                ('What sort of help?', 5, 3),
                ('Congrats buddy', 2, 4),
                ('I was rooting for Nadal though', 4, 5),
                ('Help with your thesis?', 2, 3),
                ('Many congratulations', 5, 4),
                ]

like_data = [(1, 6),
            (2, 3),
            (1, 5),
            (5, 4),
            (2, 4),
            (4, 2),
            (3, 6)
            ]

insert_user_sql = """
INSERT INTO
users (name, age, gender, nationality)
VALUES 
(?,?,?,?)
"""

insert_post_sql = """
INSERT INTO
posts (title, description, user_id)
VALUES 
(?,?,?)
"""

insert_comments_sql = """
INSERT INTO
comments (comment, user_id, post_id)
VALUES 
(?,?,?)
"""

insert_likes_sql = """
INSERT INTO
likes (user_id, post_id)
VALUES 
(?,?)
"""

with sqlite3.connect('sm_app.sqlite') as conn:
    cur = conn.cursor()
    cur.executemany(insert_user_sql, user_data)
    cur.executemany(insert_post_sql, post_data)
    cur.executemany(insert_comments_sql, comment_data)
    cur.executemany(insert_likes_sql, like_data)

    conn.commit()