import sqlite3 as sql
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler

from init_db import init_database

conn = sql.connect("server.db")
cur = conn.cursor()

init_database(cur)

IP, PORT = "0.0.0.0", 65432
httpd = HTTPServer((IP, PORT), SimpleHTTPRequestHandler)
httpd.serve_forever()


def verify_user(username: str, uuid: str): #verify user against uuid
    cur.execute("select * FROM users WHERE uuid=?", (uuid,))
    user = cur.fetchone()
    print(user)

def does_entry_exist(table, heading, contents):
    cur.execute(f"SELECT EXISTS(SELECT 1 FROM ? WHERE ?=\"?\"", (table, heading, contents))
    return cur.fetchone()

def create_user(uuid, username, name=""):
    if (does_entry_exist("users", "username", username) or
        does_entry_exist("users", "uuid", uuid)):
        print("Failed to create user (username or uuid already exists)")
        return False

    cur.execute("INSERT INTO users (?, ?, ?)", (uuid, username, name))
    conn.commit()
    print("Created user.")
    return True


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        create_user("test_username", "test_uuid", "test_name")
        self.wfile.write(b"recieved.")


