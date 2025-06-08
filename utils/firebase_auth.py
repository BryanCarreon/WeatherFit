import requests
import os 
from dotenv import load_dotenv
import jwt

load_dotenv()
API_KEY = os.getenv('FIREBASE_API_KEY')
PROJECT_ID = os.getenv('FIREBASE_PROJECT_ID')

FIREBASE_AUTH_URL = "https://identitytoolkit.googleapis.com/v1/accounts"
FIRESTORE_URL = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents"

def signup_user(email, password):
    url = f"{FIREBASE_AUTH_URL}:signUp?key={API_KEY}"
    payload = {
        "email":email, 
        "password":password, 
        "returnSecureToken": True
    }
    
    res = requests.post(url, json=payload)
    # ebug 
    print("STATUS CODE:", res.status_code)       # Shows 200 or error
    print("RESPONSE TEXT:", res.text)            # Firebase response body

    try:
        json_res = res.json()
    except Exception as e:
        print("Error parsing JSON:", e)
        return False, None, None
    #to here
    
    if "idToken" in json_res:
        return True, json_res["idToken"], json_res["localId"]
    return False, None, None    

def login_user(email, password):
    url = f"{FIREBASE_AUTH_URL}:signInWithPassword?key={API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    res = requests.post(url, json=payload).json()
    if "idToken" in res:
        return True, res["idToken"], res["localId"]
    return False, None, None

def save_city(user_id, city):
    url = f"{FIRESTORE_URL}/users/{user_id}"
    data = {
        "fields": {
            "city": {"stringValue": city}
        }
    }
    
    res = requests.patch(url, json=data)
    print("SAVE_CITY status:", res.status_code)
    print("SAVE_CITY response:", res.text)
    
def get_city(user_id):
    url = f"{FIRESTORE_URL}/users/{user_id}"
    res = requests.get(url).json()
    try:
        return res["fields"]["city"]["stringValue"]
    except:
        return "unknown or not set"
    
def get_email_from_token(id_token):
    try:
        decoded = jwt.decode(id_token, options={"verify_signature": False})
        return decoded.get("email", "Unknown")
    except Exception as e:
        print("Error decoding token:", e)
        return "Unknown"