import sqlite3

connection = sqlite3.connect('admin.db')


with open('admin.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO administrator (username, password) VALUES (?, ?)",
            ('admin', '1234')
            )

connection.commit()
connection.close()