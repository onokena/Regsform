from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import hashlib
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

db_params = {
    'dbname': 'XXXXXXXXXXXXX',
    'user': 'XXXXXXXXXXXXX',
    'password': 'XXXXXXXXXXXXX',
    'host': 'localhost',
    'port': '5432',
}

create_table_query = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(64) NOT NULL
);
"""

with psycopg2.connect(**db_params) as conn, conn.cursor() as cur:
    cur.execute(create_table_query)
    conn.commit()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    #SHA-256 HASHING
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    insert_user_query = "INSERT INTO users (username, password_hash) VALUES (%s, %s);"
    with psycopg2.connect(**db_params) as conn, conn.cursor() as cur:
        cur.execute(insert_user_query, (username, hashed_password))
        conn.commit()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=8000)
