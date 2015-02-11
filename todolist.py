from flask import Flask, session, redirect, url_for, escape, request, render_template
import sys
import sqlite3
app = Flask(__name__)
DB_FILENAME = 'todo.db'

@app.route('/add_task', methods=["POST"])
def add_task():
    if 'username' in session:
        enter_task(category, priority, description, username)
    return redirect(url_for('index'))

@app.route('/')
def index():
    if 'username' in session:
        tasks = get_user_tasks(request.form['username'])
        return render_template('layout.html')#, tasks=tasks)

    return 'You are not logged in'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        # check if user in db
        if (user_in_db(request.form['username'])):
            # check password
            if (password_matches_user(request.form['username'], request.form['password'])):
                return redirect(url_for('index'))
            else:
                # bad password
                return render_template('login.html', access_denied=True)
        else:
            # if user no in db add them with the password given
            add_user(request.form['username'], request.form['password'])
            return redirect(url_for('index'))

        return redirect(url_for('index'))

    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

def enter_task(category, priority, description, username):
    try:
        conn = sqlite3.connect(DB_FILENAME)
        c = conn.cursor()
        c.execute("INSERT into task(category, priority, description, username) VALUES(?, ?, ?, ?)", (category, priority, description, username))
        conn.commit()
    except sqlite3.Error as e:
        print "Error %s:" % e.args[0]
        sys.exit(1)
    finally:
        if c:
            c.close()

def get_user_tasks(username):
    try:
        conn = sqlite3.connect(DB_FILENAME)
        c = conn.cursor()
        c.execute("SELECT * from task where username=?", (username,))
        tasks = c.fetall()
        return tasks
    except sqlite3.Error as e:
        print "Error %s:" % e.args[0]
        sys.exit(1)
    finally:
        if c:
            c.close()

def password_matches_user(username, password):
    try:
        conn = sqlite3.connect(DB_FILENAME)
        c = conn.cursor()
        c.execute("SELECT * from user where username=?", (username,))
        user = c.fetchone()
        if user[1] == password:
            return True
        else:
            return False
    except sqlite3.Error as e:
        print "Error %s:" % e.args[0]
        sys.exit(1)
    finally:
        if c:
            c.close()

def user_in_db(username):
    try:
        conn = sqlite3.connect(DB_FILENAME)
        c = conn.cursor()
        c.execute("SELECT * from user where username=?", (username,))
        user = c.fetchone()
        if user:
            return True
        else:
            return False
    except sqlite3.Error as e:
        print "Error %s:" % e.args[0]
        sys.exit(1)
    finally:
        if c:
            c.close()

def add_user(username, password):
    try:
        conn = sqlite3.connect(DB_FILENAME)
        c = conn.cursor()
        c.execute("INSERT into user(username, password) VALUES(?, ?)", (username, password))
        conn.commit()
    except sqlite3.Error, e:
        print "Error %s:" % e.args[0]
        sys.exit(1)
    finally:
        if c:
            c.close()

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

