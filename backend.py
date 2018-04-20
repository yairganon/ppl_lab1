import sqlite3
import csv


def create_ratings_table():
    conn = sqlite3.connect('lite.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS ratings (userId TEXT,movieId TEXT,rating REAL)")
    cur.execute("SELECT count(1) FROM ratings;")
    rows = cur.fetchall()
    if rows[0][0] == 0:
        with open("ratings.csv") as f_obj:
            reader = csv.reader(f_obj)
            reader.next()
            for row in reader:
                cur.execute("INSERT INTO ratings VALUES (?,?,?);", (row[0], row[1], row[2]))
    conn.commit()
    conn.close()


def create_movies_table():
    conn = sqlite3.connect('lite.db')
    cur = conn.cursor()
    #cur.execute("DROP TABLE movies")
    cur.execute("CREATE TABLE IF NOT EXISTS movies (movieId TEXT PRIMARY KEY,title TEXT,genre TEXT)")
    cur.execute("SELECT count(1) FROM movies;")
    rows = cur.fetchall()
    if rows[0][0] == 0:
        with open("movies.csv") as f_obj:
            reader = csv.reader(f_obj)
            reader.next()
            for row in reader:
                cur.execute("INSERT INTO movies VALUES (?,?,?);",
                            (unicode(row[0], "utf-8"),
                             unicode(row[1], "utf-8"),
                             unicode(row[2], "utf-8").split("|")[0]))
    conn.commit()
    conn.close()


def get_movie(movie_id, title="", genre=""):
    conn = sqlite3.connect('lite.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM movies WHERE (movieId=? or ?='') AND (title LIKE ?||'%' or ?='') AND (genre LIKE ? or ?='');",
                (movie_id,movie_id,title,title,genre,genre))
    rows = cur.fetchall()
    return rows


def insert(movie_id, title, genre):
    conn = sqlite3.connect('lite.db')
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO movies  VALUES (?,?,?);", (movie_id,title,genre))
        conn.commit()
        conn.close()
        return 0
    except:
        return 1



def delete(movie_id):
    conn = sqlite3.connect('lite.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM movies WHERE movieId=?", (movie_id,))
    conn.commit()
    conn.close()


def update(movie_id,title,genre):
    conn = sqlite3.connect('lite.db')
    cur = conn.cursor()
    cur.execute("UPDATE movies SET title=?, genre=? WHERE movieId=?;", (title, genre, movie_id))
    conn.commit()
    conn.close()


def get_all_ratings():
    conn = sqlite3.connect('lite.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM ratings;")
    rows = cur.fetchall()
    return list(rows)



# create_ratings_table()
# create_movies_table()
