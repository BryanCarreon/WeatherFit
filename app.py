from flask import Flask, render_template, request, redirect, url_for, session
from utils.firebase_auth import signup_user, login_user, save_city, get_city, get_email_from_token, get_all_users
from utils.weather import get_weather_now, get_forecast
from utils.openAI_recommender import outfit_recommendation 
from utils.emailing import send_weather_email
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import atexit
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
                save_city(local_id, city, email)
            except Exception as e:
                print("Error saving to Firestore:", e)
                return "Signup succeeded but Firestore save failed."

            return redirect(url_for('login'))
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
    
    current_weather = get_weather_now(city)
    #forecast = get_forecast(city)
    forecast = get_forecast(city, days=3)
    ai_suggestion = outfit_recommendation(forecast[0]) if forecast else "No forecast available"


    return render_template('dashboard.html', 
        email=email,
        city=city,
        current_weather=current_weather,
        forecast=forecast,
        ai_suggestion=ai_suggestion
    )

@app.route('/send_email')
def send_email():
    local_id = session['localId']
    city = get_city(local_id)  # From Firestore
    email = get_email_from_token(session['idToken'])  # <- Get logged-in user's email

    forecast = get_forecast(city, days=1)
    
    if not forecast:
        return "No forecast data available."
    
    weather_data = forecast[0]["values"] if "values" in forecast[0] else forecast[0]
    
    suggestion = outfit_recommendation(weather_data)
    
    subject = f"WeatherFit Outfit for {forecast[0].get('date', 'Today')}"
    body = suggestion  # Use OpenAI's output directly
    
    send_weather_email(subject, body, recipient_email=email)
    return "Email with outfit suggestion sent!"

@app.route('/')
def home():
    return redirect(url_for('login'))

#TESTING
@app.route('/send_all_emails')
def trigger_manual_email():
    send_daily_emails()
    return "Emails sent manually."


def send_daily_emails():
    users = get_all_users()
    for user in users:
        email = user.get("email")
        user_id = user.get("id")
        city = get_city(user_id)

        forecast = get_forecast(city, days=1)
        if not forecast:
            continue

        weather_data = forecast[0] if isinstance(forecast[0], dict) else {}
        suggestion = outfit_recommendation(weather_data)

        subject = f"WeatherFit Outfit for {forecast[0].get('date', 'Today')}"
        send_weather_email(subject, suggestion, recipient_email=email)
    
#schedule daily at 6AM 
scheduler = BackgroundScheduler()
scheduler.add_job(func=send_daily_emails, trigger='cron', hour=6, minute=0)  # e.g., 7:00 AM daily
scheduler.start()

# Shutdown gracefully when the app stops
atexit.register(lambda: scheduler.shutdown())