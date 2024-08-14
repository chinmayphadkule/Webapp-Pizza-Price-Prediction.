from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from model import Pizza_Sales_Model
import numpy as np

# database_setup
import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('pizza_login.db')
cursor = conn.cursor()

# Create a table for storing user data
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your secret key

# Function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('pizza_login.db')
    conn.row_factory = sqlite3.Row
    return conn

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
  def __init__(self, user_id, name, email):
    self.id = user_id
    self.name = name
    self.email = email

  @login_manager.user_loader
  def load_user(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if user:
      return User(user_id, user['name'], user['email'])
    else:
      return None

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Query the database for the user
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()

        # Check if user exists and password is correct
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['name'] = user['name']
            return redirect(url_for('dashboard'))
        else:
            flash('Incorrect email or password.', 'warning')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Insert the new user into the database
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (name, email, hashed_password))
            conn.commit()
            conn.close()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('register'))
        except sqlite3.IntegrityError:
            conn.close()
            flash('Email already exists!', 'warning')
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/dashboard',methods=['GET', 'POST'])
def dashboard():
    if 'user_id' in session:
        if request.method =='GET':
            return render_template('form.html', name=session.get('name'))
        else:
                
                data1 = request.form['quantity']
                data2 = request.form['category']
                data3 = request.form['ingredients']
                data4 = request.form['size']
                data5 = request.form['weekday']
                
                arr = np.array([data1,data2,data3,data4,data5])

                print(type(request.form['category']),request.form['category'])
                a = str(Pizza_Sales_Model.give_prediction(arr)[0])
                return render_template('form.html', name=session.get('name'),a=float(a))
                # return render_template(
                # 'form.html',
                # name=session.get('name'),
                # quantity=data1,
                # category=data2,
                # ingredients=data3,
                # size=data4,
                # weekday=data5,
                # prediction=float(a)
                # )
    else:
        return redirect(url_for('login'))
    

@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

