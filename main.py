import sqlite3
import hashlib

conn = sqlite3.connect("userdata.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS userdata (
    id  INTEGER PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    salt VARCHAR(255) NOT NULL
)
""")

username1, password1 = "Atharva123", "atharvapassword"
username2, password2 = "John", "john234"
username3, password3 = "jake", "jakey545"
username4, password4 = "syth", "cybersyth1"


salt1 = hashlib.sha256(username1.encode()).hexdigest()[:16]
salt2 = hashlib.sha256(username2.encode()).hexdigest()[:16]
salt3 = hashlib.sha256(username3.encode()).hexdigest()[:16]
salt4 = hashlib.sha256(username4.encode()).hexdigest()[:16]


hashed_password1 = hashlib.sha256((password1 + salt1).encode()).hexdigest()
hashed_password2 = hashlib.sha256((password2 + salt2).encode()).hexdigest()
hashed_password3 = hashlib.sha256((password3 + salt3).encode()).hexdigest()
hashed_password4 = hashlib.sha256((password4 + salt4).encode()).hexdigest()


cur.execute("INSERT INTO userdata (username, password, salt) VALUES (?, ?, ?)", (username1, hashed_password1, salt1))
cur.execute("INSERT INTO userdata (username, password, salt) VALUES (?, ?, ?)", (username2, hashed_password2, salt2))
cur.execute("INSERT INTO userdata (username, password, salt) VALUES (?, ?, ?)", (username3, hashed_password3, salt3))
cur.execute("INSERT INTO userdata (username, password, salt) VALUES (?, ?, ?)", (username4, hashed_password4, salt4))

conn.commit()
