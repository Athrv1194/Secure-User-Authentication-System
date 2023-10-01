import sqlite3
import socket
import threading
import bcrypt
import time

failed_login_attempts = {}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
server.listen()

MAX_LOGIN_ATTEMPTS = 3
TIME_PERIOD = 60


def handle_connection(c):
    attempts_left = MAX_LOGIN_ATTEMPTS

    while attempts_left > 0:
        c.send("Username: ".encode())
        username = c.recv(1024).decode()
        c.send("Password: ".encode())
        password = c.recv(1024).decode()

        # Validate login credentials against the database
        conn = sqlite3.connect("userdata.db")
        cur = conn.cursor()

        cur.execute("SELECT password, salt FROM userdata WHERE username=?", (username,))
        user_data = cur.fetchone()

        if user_data:
            stored_password, salt = user_data
            # Encode password and salt to bytes before hashing
            encoded_password = (password + salt).encode('utf-8')
            encoded_salt = salt.encode('utf-8')
            hashed_password = bcrypt.hashpw(encoded_password, encoded_salt)
            if hashed_password == stored_password:
                c.send("Login successful".encode())
                failed_login_attempts.pop(username, None)  # Reset login attempts if successful
                conn.close()
                return
            else:
                attempts_left -= 1  # Decrease attempts left on failed attempt
                c.send("Invalid username or password. Attempts left: {} \n".format(attempts_left).encode())

                if attempts_left <= 0:
                    c.send(f"Too many failed login attempts. Try again after {TIME_PERIOD} seconds.\n".encode())
                    time.sleep(TIME_PERIOD)  # Introduce a delay before allowing another login attempt


while True:
    client, adr = server.accept()
    threading.Thread(target=handle_connection, args=(client,)).start()