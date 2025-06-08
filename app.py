from flask import Flask, render_template, request, redirect, url_for, session
from utils.firebase_auth import signup_user, login_user
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.urandom(24)  # for session security

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        success, id_token, local_id = signup_user(email, password)
        if success:
            session['idToken'] = id_token
            session['localId'] = local_id
            return redirect(url_for('dashboard'))  # We'll build this later
        return "Signup failed"
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        success, id_token, local_id = login_user(email, password)
        if success:
            session['idToken'] = id_token
            session['localId'] = local_id
            return redirect(url_for('dashboard'))  # We'll build this later
        return "Login failed"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
def home():
    return redirect(url_for('login'))
