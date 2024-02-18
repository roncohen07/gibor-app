from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'As45@ldcm1sd^&^fd3221'  # Change this to a random secret key

# SQLite database connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize the database
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    user_table_exists = cursor.fetchone()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tweets'")
    tweets_table_exists = cursor.fetchone()
    if user_table_exists and tweets_table_exists:
        conn.close()
        return
    with app.open_resource('schema.sql', mode='r') as f:
        cursor.executescript(f.read())
    conn.commit()
    conn.close()

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            conn = get_db_connection()
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except IntegrityError:
            # Redirect to user_exists.html if username already exists
            return render_template('user_exists.html')
    return render_template('registration.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()
        if user:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('homepage'))
    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))

# Homepage route
@app.route('/')
def homepage():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    tweets = conn.execute('SELECT * FROM tweets').fetchall()
    conn.close()
    return render_template('homepage.html', tweets=tweets)

# Add tweet route
@app.route('/add_tweet', methods=['POST'])
def add_tweet():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    tweet_text = request.form['tweet_text']
    conn = get_db_connection()
    conn.execute('INSERT INTO tweets (username, tweet_text) VALUES (?, ?)', (session['username'], tweet_text))
    conn.commit()
    conn.close()
    return redirect(url_for('homepage'))

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
