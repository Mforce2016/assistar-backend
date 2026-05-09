import firebase_admin

from firebase_admin import credentials
from firebase_admin import firestore


def iniciar_firebase():
    try:
        firebase_admin.get_app()

    except:
        cred = credentials.Certificate(
            "firebase_key.json"
        )

        firebase_admin.initialize_app(cred)


def db():
    iniciar_firebase()
    return firestore.client()