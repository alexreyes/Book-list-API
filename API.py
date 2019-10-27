from flask import Flask, jsonify, g
import os
import psycopg2
import sqlite3

app = Flask(__name__)
app.database = "sample.db"

@app.route("/bookList")
def bookList(): 
    g.db = connect_db()
    cur = g.db.execute('select * from posts')
    posts = [dict(title=row[0], description=row[1]) for row in cur.fetchall()]
    g.db.close()
    print(posts)

    # file = open('bookList.txt', 'r')
    # lines = file.read().split("\n")
    lines = posts

    response = jsonify(lines)
    response.headers.add('Access-Control-Allow-Origin', '*')
    
    file.close()

    return response

def connect_db(): 
    return sqlite3.connect(app.database)