import sqlite3

db = 'democratData.db'

conn = sqlite3.connect(db)
c = conn.cursor()

c.execute("SELECT * from tweets")
result = c.fetchall()

print(str(result[:10]))