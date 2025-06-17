from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 's3cr3tK3y_EmployeeSystem2025!'  # Strong session key

# Dummy user data with hashed password
users = {
    'admin': generate_password_hash('password')
}

# In-memory employee list
employees = []

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_pwd = users.get(username)

        if hashed_pwd and check_password_hash(hashed_pwd, password):
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials. Try again."
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', employees=employees)

@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name'].strip()
        role = request.form['role'].strip()
        if not name or not role:
            return "Error: All fields are required."
        employees.append({'name': name, 'role': role})
        return redirect(url_for('dashboard'))
    return render_template('add_employee.html')

@app.route('/delete/<int:id>')
def delete_employee(id):
    if 'user' not in session:
        return redirect(url_for('login'))
    if id < len(employees):
        employees.pop(id)
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
