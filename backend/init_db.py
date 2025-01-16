import sqlite3 as sql

def init_database(cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS posts (parent_id text, id text, owner_uuid text, owner_username text, date text," 
                "rating integer, title text, contents text, image_id text, comments text, likes integer)") #store comments in json form

    cursor.execute("CREATE TABLE IF NOT EXISTS users (uuid text, username text, name text, bio text, following text,"
                "followers text, post_ids text)") #all lists (followers, posts, etc) stored in json

