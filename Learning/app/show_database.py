import sqlite3

# connect to database file
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# run a query to show all the tables
cursor.execute("SELECT * FROM user")

rows = cursor.fetchall()


print("This is the data that is find from the database")


for row in rows:
    print(row)

conn.close()
