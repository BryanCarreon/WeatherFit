import requests
import os 
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('FIREBASE_API_KEY')

FIREBASE_AUTH_URL = "https://identitytoolkit.googleapis.com/v1/accounts"
print("KEY:", API_KEY)  # Debug print (optional)

def signup_user(email, password):
    url = f"{FIREBASE_AUTH_URL}:signUp?key={API_KEY}"
    payload = {
        "email":email, 
        "password":password, 
        "returnSecureToken": True
    }
    
    res = requests.post(url, json=payload)
    #here
    print("STATUS CODE:", res.status_code)       # ✅ Shows 200 or error
    print("RESPONSE TEXT:", res.text)            # ✅ Firebase response body

    try:
        json_res = res.json()
    except Exception as e:
        print("Error parsing JSON:", e)
        return False, None, None
    #to here
    if "idToken" in res:
        return True, res["idToken"], res["localId"]
    return False, None, None

def login_user(email, password):
    url = f"{FIREBASE_AUTH_URL}:signInWithPassword?key={API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    res = requests.post(url, json=payload).json()
    if "idToken" in res:
        return True, res["idToken"], res["localId"]
    return False, None, None