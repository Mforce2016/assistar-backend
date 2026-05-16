import firebase_admin

from firebase_admin import messaging

from services.firebase_service import db


# =========================================
# ENVIAR PUSH
# =========================================

def enviar_push(
    token,
    titulo,
    cuerpo
):

    try:

        message = messaging.Message(

            notification=messaging.Notification(
                title=titulo,
                body=cuerpo
            ),

            token=token
        )

        response = messaging.send(
            message
        )

        print(
            "PUSH OK:",
            response
        )

    except Exception as e:

        print(
            "ERROR PUSH:",
            e
        )


# =========================================
# ENVIAR A TODOS
# =========================================

def enviar_push_global(
    titulo,
    cuerpo
):

    docs = db().collection(
        "users"
    ).stream()

    for doc in docs:

        data = doc.to_dict()

        token = data.get(
            "fcm_token"
        )

        if token:

            enviar_push(
                token,
                titulo,
                cuerpo
            )