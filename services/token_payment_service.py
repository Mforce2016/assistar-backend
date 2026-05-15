import os
import mercadopago

sdk = mercadopago.SDK(
    os.getenv("MP_ACCESS_TOKEN")
)


# =========================================
# CREAR PAGO FICHAS
# =========================================

def crear_pago_fichas(
    uid,
    pack
):

    fichas = 10
    precio = 1000

    if pack == "50":

        fichas = 50
        precio = 4500

    elif pack == "100":

        fichas = 100
        precio = 8000

    preference_data = {

        "items": [
            {
                "title": f"Pack {fichas} fichas",
                "quantity": 1,
                "currency_id": "ARS",
                "unit_price": precio
            }
        ],

        "external_reference":
            f"{uid}|{fichas}",

        "notification_url":
            "https://assistar-backend.onrender.com/tokens/webhook",

        "back_urls": {
            "success":
                "https://google.com",
            "failure":
                "https://google.com",
            "pending":
                "https://google.com"
        },

        "auto_return": "approved"
    }

    preference_response = sdk.preference().create(
        preference_data
    )

    preference = preference_response["response"]

    return preference["init_point"]