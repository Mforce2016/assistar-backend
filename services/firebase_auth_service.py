import requests
import os


API_KEY = os.getenv(
    "FIREBASE_WEB_API_KEY"
)

BASE_URL = (
    "https://identitytoolkit.googleapis.com/v1"
)


# =========================================
# REGISTER
# =========================================

def register_user(email, password):

    url = (
        f"{BASE_URL}/accounts:signUp"
        f"?key={API_KEY}"
    )

    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    r = requests.post(
        url,
        json=payload,
        timeout=60
    )

    return r.json()


# =========================================
# LOGIN
# =========================================

def login_user(email, password):

    url = (
        f"{BASE_URL}/accounts:signInWithPassword"
        f"?key={API_KEY}"
    )

    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    r = requests.post(
        url,
        json=payload,
        timeout=60
    )

    return r.json()


# =========================================
# RESET PASSWORD
# =========================================

def send_reset_email(email):

    url = (
        f"{BASE_URL}/accounts:sendOobCode"
        f"?key={API_KEY}"
    )

    payload = {
        "requestType": "PASSWORD_RESET",
        "email": email
    }

    r = requests.post(
        url,
        json=payload,
        timeout=60
    )

    return r.json()


# =========================================
# VERIFY EMAIL
# =========================================

def send_verify_email(id_token):

    url = (
        f"{BASE_URL}/accounts:sendOobCode"
        f"?key={API_KEY}"
    )

    payload = {
        "requestType": "VERIFY_EMAIL",
        "idToken": id_token
    }

    r = requests.post(
        url,
        json=payload,
        timeout=60
    )

    return r.json()


# =========================================
# ACCOUNT INFO
# =========================================

def get_account_info(id_token):

    url = (
        f"{BASE_URL}/accounts:lookup"
        f"?key={API_KEY}"
    )

    payload = {
        "idToken": id_token
    }

    r = requests.post(
        url,
        json=payload,
        timeout=60
    )

    return r.json()