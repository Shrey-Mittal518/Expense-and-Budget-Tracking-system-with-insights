
# app_bootstrap_bg.py
from flask import Flask, render_template_string, request, redirect, session, send_from_directory
import auth_app, data_handler, visualize, health_score, ml_predict
import os

app = Flask(__name__)
app.secret_key = 'secret123'

@app.route('/charts/<path:filename>')
def charts(filename):
    return send_from_directory(os.path.join(os.getcwd(), "charts"), filename)

@app.route('/')
def dashboard():
    if 'user' not in session:
        return redirect('/login')

    user = session['user']
    role = session['role']
    family_id = session['family_id']

    visualize.pie_chart_member(user, family_id)
    visualize.bar_chart_family(family_id)

    score = health_score.compute_health_score(family_id)
    predicted = ml_predict.predict_next_month(family_id)

    pie_chart = f"charts/pie_{user}_{family_id}.png"
    bar_chart = f"charts/bar_{family_id}.png"

    html = f"""
    <html>
    <head>
        <title>Expense & Budget Dashboard</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body style="background-color:#e3f2fd;">
        <div class="container mt-4">
            <h1 class="text-primary mb-4">💰 Expense & Budget Tracking System with Insights</h1>
            <h4>Welcome <b>{user}</b> | Role: <b>{role}</b></h4>

            <div class="row mt-4">
                <div class="col-md-4">
                    <div class="card shadow-sm mb-3">
                        <div class="card-body">
                            <h5 class="card-title">Financial Health Score</h5>
                            <p class="card-text"><b>{score}</b></p>
                            <h5 class="card-title">Predicted Next Month Spend</h5>
                            <p class="card-text"><b>₹{predicted}</b></p>
                        </div>
                    </div>
                </div>

                <div class="col-md-4">
                    <div class="card shadow-sm mb-3">
                        <div class="card-body">
                            <h5 class="card-title">Charts</h5>
                            <img src='/{pie_chart}' class="img-fluid mb-2">
                            <img src='/{bar_chart}' class="img-fluid">
                        </div>
                    </div>
                </div>

                <div class="col-md-4">
                    <div class="card shadow-sm mb-3">
                        <div class="card-body">
                            <h5 class="card-title">Add Expense</h5>
                            <form method="post" action="/add_expense">
                                <div class="mb-2">
                                    <input class="form-control" name="category" placeholder="Category">
                                </div>
                                <div class="mb-2">
                                    <input class="form-control" name="amount" placeholder="Amount">
                                </div>
                                <button class="btn btn-primary">Add Expense</button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>

            <a href='/logout' class="btn btn-danger mt-3">Logout</a>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/add_expense', methods=['POST'])
def add_expense():
    if 'user' not in session:
        return redirect('/login')
    member = session['user']
    family_id = session['family_id']
    category = request.form['category']
    amount = request.form['amount']
    data_handler.add_expense(member, category, amount, family_id)
    return redirect('/')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        u, p = request.form['username'], request.form['password']
        con = auth_app.sqlite3.connect(auth_app.DB)
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE username=?", (u,))
        user = cur.fetchone()
        con.close()
        if user and auth_app.check_password_hash(user[2], p):
            session['user'], session['role'], session['family_id'] = user[1], user[3], user[4]
            return redirect('/')
        return "❌ Invalid credentials"
    return render_template_string("""
    <div class="container mt-5">
        <h3>Login</h3>
        <form method='post'>
          <div class="mb-2">
              <input class="form-control" name='username' placeholder="Username">
          </div>
          <div class="mb-2">
              <input type='password' class="form-control" name='password' placeholder="Password">
          </div>
          <button class="btn btn-primary">Login</button>
        </form>
    </div>
    """)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    auth_app.init_db()
    app.run(debug=True)
