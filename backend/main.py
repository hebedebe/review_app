import sqlite3 as sql
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler

from init_db import init_database

def verify_user(username: str, uuid: str): #verify user against uuid
    cur.execute("select * FROM users WHERE uuid=?", (uuid,))
    user = cur.fetchone()
    print(user)

def does_entry_exist(table, heading, contents):
    cur.execute(f"SELECT EXISTS(SELECT 1 FROM {table} WHERE {heading}=\"{contents}\")")
    row = cur.fetchone()
    return row != (0,)

def create_user(uuid, username, name=""):
    if (does_entry_exist("users", "username", username) or
        does_entry_exist("users", "uuid", uuid)):
        print("Failed to create user (username or uuid already exists)")
        return False

    cur.execute(f'INSERT INTO users (uuid, username, name) VALUES ("{uuid}", "{username}", "{name}");')
    conn.commit()
    print("Created user.")
    return True


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        print(self.request)
        print(self.requestline)
        print()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"recieved.")

    def do_POST(self):
        args = self.path.split("/")[1:]
        print(args)
        match args[0]:
            case "create_user":
                try:
                    uuid = args[1]
                    username = args[2]
                    name = args[3]
                    user_created = create_user(uuid, username, name)
                    if user_created:
                        self.send_response(201)
                        self.end_headers()
                    else:
                        self.send_response(500)
                        self.end_headers()
                except Exception as e:
                    print(e)
                    self.send_response(400)
                    self.end_headers()

            case "update_user":
                try:
                    uuid = args[1]
                    username = args[2]
                    name = args[3]
                    user_exists = does_entry_exist("users", "uuid", uuid)
                    if user_exists:
                        cur.execute(f'UPDATE users SET username="{username}", name="{name}" WHERE uuid="{uuid}"')
                        conn.commit()
                        self.send_response(200)
                        self.end_headers()
                    else:
                        self.send_response(404)
                        self.end_headers()
                except Exception as e:
                    print(e)
                    self.send_response(500)
                    self.end_headers()

            case _:
                self.send_response(501)
                self.end_headers()

conn = sql.connect("server.db")
cur = conn.cursor()

init_database(cur)

IP, PORT = "0.0.0.0", 65432
httpd = HTTPServer((IP, PORT), SimpleHTTPRequestHandler)
httpd.serve_forever()