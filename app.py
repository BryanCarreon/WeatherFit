from flask import Flask, render_template, request, redirect, url_for, session
from utils.firebase_auth import signup_user, login_user, save_city, get_city, get_email_from_token
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
        city = request.form['city']
        success, id_token, local_id = signup_user(email, password)
        if success:
            session['idToken'] = id_token
            session['localId'] = local_id
            #return redirect(url_for('dashboard'))  # We'll build this later
            try:
                save_city(local_id, city)
            except Exception as e:
                print("Error saving to Firestore:", e)
                return "Signup succeeded but Firestore save failed."

            return "Signup successful and user data saved!"  # temp confirmation
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

@app.route('/dashboard')
def dashboard():
    if 'idToken' not in session:
        return redirect(url_for('login'))
    
    local_id = session['localId']
    email = get_email_from_token(session['idToken'])
    city = get_city(local_id)  # From Firestore

    return render_template('dashboard.html', email=email, city=city)

@app.route('/')
def home():
    return redirect(url_for('login'))
