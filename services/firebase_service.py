import firebase_admin
import json
import os

from firebase_admin import credentials
from firebase_admin import firestore


# =====================================
# INICIAR FIREBASE
# =====================================

def iniciar_firebase():

    try:
        firebase_admin.get_app()

    except:

        firebase_json = os.getenv(
            "FIREBASE_CREDENTIALS"
        )

        if not firebase_json:
            raise Exception(
                "Falta FIREBASE_CREDENTIALS"
            )

        cred_dict = json.loads(firebase_json)

        cred = credentials.Certificate(
            cred_dict
        )

        firebase_admin.initialize_app(cred)


# =====================================
# DB
# =====================================

def db():
    iniciar_firebase()
    return firestore.client()