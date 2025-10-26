# app.py
from flask import Flask, render_template_string, request, redirect, session, send_from_directory
import auth_app, data_handler, visualize, health_score, ml_predict
import benchmarking
import challenges
import os

app = Flask(__name__)
app.secret_key = 'secret123'

@app.route('/charts/<path:filename>')
def charts(filename):
    return send_from_directory(os.path.join(os.getcwd(), "charts"), filename)

@app.route('/welcome')
def welcome():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Welcome - Expense Tracker</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                margin: 0;
                padding: 20px;
            }
            .container {
                background: white;
                padding: 50px;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                width: 100%;
                max-width: 500px;
                text-align: center;
            }
            h1 {
                color: #333;
                margin-bottom: 10px;
                font-size: 32px;
            }
            .logo {
                font-size: 60px;
                margin-bottom: 20px;
            }
            .subtitle {
                color: #666;
                margin-bottom: 40px;
                font-size: 16px;
            }
            .button-group {
                display: flex;
                flex-direction: column;
                gap: 15px;
            }
            .btn {
                padding: 15px 30px;
                border: none;
                border-radius: 10px;
                font-size: 18px;
                cursor: pointer;
                transition: all 0.3s ease;
                text-decoration: none;
                display: block;
            }
            .btn-primary {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .btn-primary:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
            }
            .btn-secondary {
                background: white;
                color: #667eea;
                border: 2px solid #667eea;
            }
            .btn-secondary:hover {
                background: #f0f0f0;
                transform: translateY(-2px);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">💰</div>
            <h1>Welcome!</h1>
            <p class="subtitle">Track your expenses and manage your budget smartly</p>
            
            <div class="button-group">
                <a href="/login" class="btn btn-primary">
                    🔐 Existing User - Login
                </a>
                <a href="/register" class="btn btn-secondary">
                    ✨ New User - Register
                </a>
            </div>
        </div>
    </body>
    </html>
    ''')

@app.route('/')
def dashboard():
    if 'user' not in session:
        return redirect('/welcome')
    
    user = session['user']
    role = session['role']
    family_id = session['family_id']
    
    # Generate visualizations - Only family-focused charts
    visualize.pie_chart_member(user, family_id)
    visualize.bar_chart_family_members(family_id)
    visualize.bar_chart_category_member_comparison(user, family_id)
    
    # Get scores and predictions
    score = health_score.compute_health_score(family_id)
    predicted = ml_predict.predict_next_month(family_id)
    
    # Get benchmarking data (month-to-month comparison)
    comparison = benchmarking.get_spending_comparison(family_id)
    
    # Get user challenges
    user_challenges = challenges.get_user_challenges(user)
    completed = challenges.check_challenge_progress(user, family_id)
    
    pie_chart = f"charts/pie_{user}_{family_id}.png"
    family_members_chart = f"charts/bar_family_members_{family_id}.png"
    category_member_chart = f"charts/bar_category_member_{family_id}.png"
    
    # Build comparison HTML (month-to-month)
    comparison_html = ""
    if comparison:
        status_colors = {
            'success': '#28a745',
            'warning': '#ffc107',
            'info': '#17a2b8'
        }
        status_color = status_colors.get(comparison['status'], '#17a2b8')
        
        comparison_html = f'''
        <div class="card" style="border-left: 4px solid {status_color};">
            <h3>📊 Month-to-Month Comparison</h3>
            <p style="font-size: 18px; font-weight: bold; color: {status_color};">
                {comparison['message']}
            </p>
        '''
        
        if 'current_total' in comparison and 'previous_total' in comparison:
            comparison_html += f'''
            <div style="margin: 15px 0; padding: 10px; background: #f8f9fa; border-radius: 5px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span><strong>Current Month:</strong></span>
                    <span style="font-size: 18px; color: #333;">₹{comparison['current_total']:,.0f}</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span><strong>Previous Month:</strong></span>
                    <span style="font-size: 18px; color: #666;">₹{comparison['previous_total']:,.0f}</span>
                </div>
            </div>
            '''
        
        if comparison['details']:
            comparison_html += '<div style="margin-top: 15px;"><h4>Category Breakdown:</h4>'
            
            for cat, data in list(comparison['details'].items())[:5]:
                diff_color = "#28a745" if data['diff_percent'] < 0 else "#dc3545"
                arrow = "↓" if data['diff_percent'] < 0 else "↑"
                
                comparison_html += f'''
                    <div style="margin-bottom: 10px; padding: 10px; background: #f8f9fa; border-radius: 5px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <strong>{cat}:</strong>
                            <div>
                                <span>₹{data['current']:,.0f}</span>
                                <span style="color: {diff_color}; margin-left: 10px;">
                                    {arrow} {abs(data['diff_percent']):.1f}%
                                </span>
                            </div>
                        </div>
                        <small style="color: #666;">
                            Last month: ₹{data['previous']:,.0f} 
                            (Difference: ₹{data['diff_amount']:+,.0f})
                        </small>
                    </div>
                '''
            
            comparison_html += '</div>'
        
        comparison_html += '</div>'
    
    # Build challenges HTML
    challenges_html = '''
    <div class="card">
        <h3>🎯 Active Challenges</h3>
    '''
    
    if user_challenges['active_challenges']:
        for challenge in user_challenges['active_challenges']:
            progress_percent = min(100, (challenge['progress'] / challenge['target']) * 100)
            challenges_html += f'''
            <div style="margin-bottom: 20px; padding: 15px; background: #f8f9fa; border-radius: 8px;">
                <h4 style="margin: 0 0 10px 0;">{challenge['name']}</h4>
                <p style="color: #666; margin: 5px 0;">{challenge['description']}</p>
                <div style="background: #e9ecef; height: 20px; border-radius: 10px; overflow: hidden; margin: 10px 0;">
                    <div style="background: linear-gradient(90deg, #667eea, #764ba2); height: 100%; width: {progress_percent}%;"></div>
                </div>
                <p><strong>Progress:</strong> {challenge['progress']}/{challenge['target']}</p>
                <p><strong>Reward:</strong> {challenge['reward']} ({challenge['points']} points)</p>
            </div>
            '''
    else:
        challenges_html += '<p>No active challenges. <a href="/activate_challenge">Start a new challenge</a></p>'
    
    challenges_html += f'''
        <div style="margin-top: 20px; padding: 15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 8px; text-align: center;">
            <h3 style="margin: 0;">Total Points: {user_challenges['total_points']}</h3>
            <p style="margin: 5px 0 0 0;">Completed: {len(user_challenges['completed_challenges'])} challenges</p>
        </div>
    </div>
    '''
    
    # Show completed challenges notification
    completed_notification = ""
    if completed:
        for c in completed:
            completed_notification += f'''
            <div style="background: #d4edda; border: 1px solid #c3e6cb; color: #155724; padding: 15px; border-radius: 5px; margin-bottom: 15px;">
                🎉 <strong>Challenge Completed!</strong> {c['name']} - You earned {c['reward']} and {c['points']} points!
            </div>
            '''
    
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Expense & Budget Dashboard</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f6f8;
                color: #333;
                margin: 20px;
            }}
            h1 {{ color: #2c3e50; }}
            h3 {{ color: #34495e; }}
            h4 {{ color: #555; margin-top: 15px; }}
            .dashboard {{
                display: flex;
                flex-wrap: wrap;
                gap: 20px;
            }}
            .card {{
                background-color: #fff;
                padding: 15px;
                border-radius: 8px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                flex: 1 1 300px;
            }}
            input, select {{
                width: 100%;
                padding: 10px;
                margin: 5px 0;
                border: 1px solid #ccc;
                border-radius: 4px;
            }}
            button {{
                padding: 10px 20px;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }}
            button:hover {{ background-color: #2980b9; }}
            img {{
                max-width: 100%;
                height: auto;
                border-radius: 8px;
                margin-top: 10px;
            }}
        </style>
    </head>
    <body>
        <h1>💰 Expense & Budget Tracking System with Insights</h1>
        <p>Welcome <strong>{user}</strong> | Role: <strong>{role}</strong></p>
        
        {completed_notification}
        
        <div class="dashboard">
            <div class="card">
                <h3>Financial Health Score</h3>
                <h2>{score}</h2>
            </div>
            
            <div class="card">
                <h3>Predicted Next Month Spend</h3>
                <h2>₹{predicted}</h2>
            </div>
            
            {comparison_html}
            
            {challenges_html}
            
            <div class="card">
                <h3>Charts & Analysis</h3>
                
                <h4>{user} Spending by Category</h4>
                <img src="{pie_chart}" alt="Pie Chart">
                
                <h4>Your Family Members Spending Comparison</h4>
                <p style="color: #666; font-size: 14px;">Compare spending among all members in your family</p>
                <img src="{family_members_chart}" alt="Family Members Chart">
                
                <h4>Category-wise Spending Across Family</h4>
                <p style="color: #666; font-size: 14px;">See how different family members spend in each category</p>
                <img src="{category_member_chart}" alt="Category Member Comparison">
            </div>
            
            <div class="card">
                <h3>Add Expense</h3>
                <form method="POST" action="/add_expense">
                    <label>Category:</label>
                    <select name="category" required>
                        <option value="Food">Food</option>
                        <option value="Rent">Rent</option>
                        <option value="Clothes">Clothes</option>
                        <option value="Travel">Travel</option>
                        <option value="Entertainment">Entertainment</option>
                        <option value="Bills">Bills</option>
                        <option value="Medical">Medical</option>
                        <option value="Education">Education</option>
                        <option value="Others">Others</option>
                    </select>
                    
                    <label>Amount:</label>
                    <input type="number" name="amount" placeholder="Enter amount" required>
                    
                    <button type="submit">Add Expense</button>
                </form>
            </div>
        </div>
        
        <br>
        <a href="/logout"><button>Logout</button></a>
    </body>
    </html>
    '''
    
    return render_template_string(html)

@app.route('/add_expense', methods=['POST'])
def add_expense():
    if 'user' not in session:
        return redirect('/welcome')
    
    member = session['user']
    family_id = session['family_id']
    category = request.form['category']
    amount = request.form['amount']
    
    data_handler.add_expense(member, category, amount, family_id)
    return redirect('/')

@app.route('/activate_challenge')
def activate_challenge_page():
    if 'user' not in session:
        return redirect('/welcome')
    
    user = session['user']
    
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Activate Challenge</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                background-color: #f4f6f8; 
                padding: 20px; 
            }
            .container { 
                max-width: 800px; 
                margin: 0 auto; 
            }
            .challenge-card { 
                background: white; 
                padding: 20px; 
                margin: 15px 0; 
                border-radius: 10px; 
                box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
            }
            button { 
                padding: 10px 20px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; 
                border: none; 
                border-radius: 5px; 
                cursor: pointer; 
            }
            button:hover { opacity: 0.9; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎯 Available Challenges</h1>
            <p>Choose a challenge to start:</p>
    '''
    
    for challenge_id, challenge in challenges.AVAILABLE_CHALLENGES.items():
        html += f'''
        <div class="challenge-card">
            <h3>{challenge['name']}</h3>
            <p>{challenge['description']}</p>
            <p><strong>Target:</strong> {challenge['target']}</p>
            <p><strong>Reward:</strong> {challenge['reward']}</p>
            <p><strong>Points:</strong> {challenge['points']}</p>
            <form method="POST" action="/activate_challenge/{challenge_id}">
                <button type="submit">Activate This Challenge</button>
            </form>
        </div>
        '''
    
    html += '''
            <br>
            <a href="/"><button>Back to Dashboard</button></a>
        </div>
    </body>
    </html>
    '''
    
    return render_template_string(html)

@app.route('/activate_challenge/<challenge_id>', methods=['POST'])
def activate_challenge_action(challenge_id):
    if 'user' not in session:
        return redirect('/welcome')
    
    user = session['user']
    challenges.activate_challenge(user, challenge_id)
    
    return redirect('/')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form.get('role', 'member')
        family_id = request.form['family_id']
        
        con = auth_app.sqlite3.connect(auth_app.DB)
        cur = con.cursor()
        try:
            cur.execute("INSERT INTO users(username,password_hash,role,family_id) VALUES (?,?,?,?)",
                       (username, auth_app.generate_password_hash(password), role, family_id))
            con.commit()
            con.close()
            return redirect('/login')
        except auth_app.sqlite3.IntegrityError:
            con.close()
            return render_template_string('''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Register</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        min-height: 100vh;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        padding: 20px;
                    }
                    .container {
                        background: white;
                        padding: 40px;
                        border-radius: 10px;
                        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                        width: 100%;
                        max-width: 400px;
                    }
                    h2 { text-align: center; color: #333; margin-bottom: 20px; }
                    .error {
                        background: #fee;
                        color: #c33;
                        padding: 10px;
                        border-radius: 5px;
                        margin-bottom: 15px;
                        text-align: center;
                    }
                    label {
                        display: block;
                        margin-top: 15px;
                        margin-bottom: 5px;
                        color: #555;
                        font-weight: 500;
                    }
                    input, select {
                        width: 100%;
                        padding: 12px;
                        margin: 5px 0;
                        border: 2px solid #ddd;
                        border-radius: 5px;
                        font-size: 16px;
                    }
                    button {
                        width: 100%;
                        padding: 12px;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        border: none;
                        border-radius: 5px;
                        font-size: 16px;
                        cursor: pointer;
                        margin-top: 20px;
                    }
                    .back-link {
                        text-align: center;
                        margin-top: 15px;
                    }
                    .back-link a {
                        color: #667eea;
                        text-decoration: none;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h2>✨ Register</h2>
                    <div class="error">Username already exists! Please choose another.</div>
                    <form method="POST">
                        <label for="username">Username</label>
                        <input type="text" id="username" name="username" placeholder="Choose a username" required>
                        
                        <label for="password">Password</label>
                        <input type="password" id="password" name="password" placeholder="Create a password" required>
                        
                        <label for="role">Role</label>
                        <select id="role" name="role">
                            <option value="member">Member</option>
                            <option value="admin">Admin</option>
                        </select>
                        
                        <label for="family_id">Family ID</label>
                        <input type="text" id="family_id" name="family_id" placeholder="e.g., fam1, fam2" required>
                        
                        <button type="submit">Create Account</button>
                    </form>
                    <div class="back-link">
                        <a href="/welcome">← Back to Welcome</a> | 
                        <a href="/login">Already have an account? Login</a>
                    </div>
                </div>
            </body>
            </html>
            ''')
    
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Register</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                width: 100%;
                max-width: 400px;
            }
            h2 { text-align: center; color: #333; margin-bottom: 20px; }
            label {
                display: block;
                margin-top: 15px;
                margin-bottom: 5px;
                color: #555;
                font-weight: 500;
            }
            input, select {
                width: 100%;
                padding: 12px;
                margin: 5px 0;
                border: 2px solid #ddd;
                border-radius: 5px;
                font-size: 16px;
            }
            input:focus, select:focus {
                outline: none;
                border-color: #667eea;
            }
            button {
                width: 100%;
                padding: 12px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
                margin-top: 20px;
            }
            button:hover {
                opacity: 0.9;
            }
            .back-link {
                text-align: center;
                margin-top: 15px;
            }
            .back-link a {
                color: #667eea;
                text-decoration: none;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>✨ Register New Account</h2>
            <form method="POST">
                <label for="username">Username</label>
                <input type="text" id="username" name="username" placeholder="Choose a username" required>
                
                <label for="password">Password</label>
                <input type="password" id="password" name="password" placeholder="Create a password" required>
                
                <label for="role">Role</label>
                <select id="role" name="role">
                    <option value="member">Member</option>
                    <option value="admin">Admin</option>
                </select>
                
                <label for="family_id">Family ID</label>
                <input type="text" id="family_id" name="family_id" placeholder="e.g., fam1, fam2" required>
                
                <button type="submit">Create Account</button>
            </form>
            <div class="back-link">
                <a href="/welcome">← Back to Welcome</a> | 
                <a href="/login">Already have an account? Login</a>
            </div>
        </div>
    </body>
    </html>
    ''')

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
        
        return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Login</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }
                .container {
                    background: white;
                    padding: 40px;
                    border-radius: 10px;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                    width: 100%;
                    max-width: 400px;
                }
                h2 { text-align: center; color: #333; margin-bottom: 20px; }
                .error {
                    background: #fee;
                    color: #c33;
                    padding: 10px;
                    border-radius: 5px;
                    margin-bottom: 15px;
                    text-align: center;
                }
                input {
                    width: 100%;
                    padding: 12px;
                    margin: 10px 0;
                    border: 2px solid #ddd;
                    border-radius: 5px;
                    font-size: 16px;
                }
                button {
                    width: 100%;
                    padding: 12px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-size: 16px;
                    cursor: pointer;
                }
                .back-link {
                    text-align: center;
                    margin-top: 15px;
                }
                .back-link a {
                    color: #667eea;
                    text-decoration: none;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>💰 Login</h2>
                <div class="error">❌ Invalid credentials. Please try again.</div>
                <form method="POST">
                    <input type="text" name="username" placeholder="Username" required>
                    <input type="password" name="password" placeholder="Password" required>
                    <button type="submit">Login</button>
                </form>
                <div class="back-link">
                    <a href="/welcome">← Back to Welcome</a> | 
                    <a href="/register">New User? Register</a>
                </div>
            </div>
        </body>
        </html>
        ''')
    
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                width: 100%;
                max-width: 400px;
            }
            h2 { text-align: center; color: #333; margin-bottom: 20px; }
            input {
                width: 100%;
                padding: 12px;
                margin: 10px 0;
                border: 2px solid #ddd;
                border-radius: 5px;
                font-size: 16px;
            }
            input:focus {
                outline: none;
                border-color: #667eea;
            }
            button {
                width: 100%;
                padding: 12px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
                margin-top: 10px;
            }
            button:hover {
                opacity: 0.9;
            }
            .back-link {
                text-align: center;
                margin-top: 15px;
            }
            .back-link a {
                color: #667eea;
                text-decoration: none;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>💰 Login</h2>
            <form method="POST">
                <input type="text" name="username" placeholder="Username" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">Login</button>
            </form>
            <div class="back-link">
                <a href="/welcome">← Back to Welcome</a> | 
                <a href="/register">New User? Register</a>
            </div>
        </div>
    </body>
    </html>
    ''')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/welcome')

if __name__ == '__main__':
    auth_app.init_db()
    app.run(debug=True)
