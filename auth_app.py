# auth_app.py
from flask import Flask, render_template_string, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os, random

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'secret123')
DB = 'family_auth.db'

# --- Initialize DB ---
def init_db():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash TEXT,
            role TEXT CHECK(role IN ('admin','member')),
            family_id TEXT
        )
    """)
    con.commit()
    con.close()

# --- Auto-generate users ---
def auto_generate_users(n=10000, family_count=100):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    roles = ['admin', 'member']
    for i in range(1, n+1):
        username = f"user{i}"
        password_hash = generate_password_hash(f"pass{i}")
        role = random.choice(roles)
        family_id = f"fam{random.randint(1, family_count)}"
        try:
            cur.execute("INSERT INTO users(username,password_hash,role,family_id) VALUES (?,?,?,?)",
                        (username, password_hash, role, family_id))
        except sqlite3.IntegrityError:
            continue
    con.commit()
    con.close()

# --- Flask Routes ---
@app.route('/')
def home():
    if 'user' in session:
        return render_template_string("""
        <h2>Expense and Budget Tracking System with Insights</h2>
        <p>Welcome {{username}} (Role: {{role}})</p>
        <ul>
          <li><a href='/add_expense'>Add Expense</a></li>
          <li><a href='/charts'>View Charts</a></li>
          <li><a href='/logout'>Logout</a></li>
        </ul>
        """, username=session['user'], role=session['role'])
    return redirect('/login')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        u, p, role, fid = request.form['username'], request.form['password'], request.form['role'], request.form['family_id']
        con = sqlite3.connect(DB)
        cur = con.cursor()
        cur.execute("INSERT INTO users(username,password_hash,role,family_id) VALUES (?,?,?,?)",
                    (u, generate_password_hash(p), role, fid))
        con.commit(); con.close()
        return redirect('/login')
    return render_template_string("""
    <h3>Expense and Budget Tracking System with Insights - Register</h3>
    <form method='post'>
      Username: <input name='username'><br>
      Password: <input type='password' name='password'><br>
      Role: <select name='role'><option>admin</option><option>member</option></select><br>
      Family ID: <input name='family_id' value='fam1'><br>
      <input type='submit'>
    </form>
    <p>Already have an account? <a href='/login'>Login</a></p>
    """)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        u, p = request.form['username'], request.form['password']
        con = sqlite3.connect(DB)
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE username=?", (u,))
        user = cur.fetchone(); con.close()
        if user and check_password_hash(user[2], p):
            session['user'], session['role'], session['family_id'] = user[1], user[3], user[4]
            return redirect('/')
        return "Invalid credentials"
    return render_template_string("""
    <h3>Expense and Budget Tracking System with Insights - Login</h3>
    <form method='post'>
      Username: <input name='username'><br>
      Password: <input type='password' name='password'><br>
      <input type='submit'>
    </form>
    <p>Don't have an account? <a href='/register'>Register</a></p>
    """)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
# auth_app.py
from flask import Flask, render_template_string, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os, random

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'secret123')
DB = 'family_auth.db'

# --- Initialize DB ---
def init_db():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash TEXT,
            role TEXT CHECK(role IN ('admin','member')),
            family_id TEXT
        )
    """)
    con.commit()
    con.close()

# --- Auto-generate users ---
def auto_generate_users(n=10000, family_count=100):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    roles = ['admin', 'member']
    for i in range(1, n+1):
        username = f"user{i}"
        password_hash = generate_password_hash(f"pass{i}")
        role = random.choice(roles)
        family_id = f"fam{random.randint(1, family_count)}"
        try:
            cur.execute("INSERT INTO users(username,password_hash,role,family_id) VALUES (?,?,?,?)",
                        (username, password_hash, role, family_id))
        except sqlite3.IntegrityError:
            continue
    con.commit()
    con.close()

# --- Flask Routes ---
@app.route('/')
def home():
    if 'user' in session:
        return render_template_string("""
        <h2>Expense and Budget Tracking System with Insights</h2>
        <p>Welcome {{username}} (Role: {{role}})</p>
        <ul>
          <li><a href='/add_expense'>Add Expense</a></li>
          <li><a href='/charts'>View Charts</a></li>
          <li><a href='/logout'>Logout</a></li>
        </ul>
        """, username=session['user'], role=session['role'])
    return redirect('/login')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        u, p, role, fid = request.form['username'], request.form['password'], request.form['role'], request.form['family_id']
        con = sqlite3.connect(DB)
        cur = con.cursor()
        cur.execute("INSERT INTO users(username,password_hash,role,family_id) VALUES (?,?,?,?)",
                    (u, generate_password_hash(p), role, fid))
        con.commit(); con.close()
        return redirect('/login')
    return render_template_string("""
    <h3>Expense and Budget Tracking System with Insights - Register</h3>
    <form method='post'>
      Username: <input name='username'><br>
      Password: <input type='password' name='password'><br>
      Role: <select name='role'><option>admin</option><option>member</option></select><br>
      Family ID: <input name='family_id' value='fam1'><br>
      <input type='submit'>
    </form>
    <p>Already have an account? <a href='/login'>Login</a></p>
    """)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        u, p = request.form['username'], request.form['password']
        con = sqlite3.connect(DB)
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE username=?", (u,))
        user = cur.fetchone(); con.close()
        if user and check_password_hash(user[2], p):
            session['user'], session['role'], session['family_id'] = user[1], user[3], user[4]
            return redirect('/')
        return "Invalid credentials"
    return render_template_string("""
    <h3>Expense and Budget Tracking System with Insights - Login</h3>
    <form method='post'>
      Username: <input name='username'><br>
      Password: <input type='password' name='password'><br>
      <input type='submit'>
    </form>
    <p>Don't have an account? <a href='/register'>Register</a></p>
    """)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
