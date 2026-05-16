import os
import mercadopago

sdk = mercadopago.SDK(
    os.getenv("MP_ACCESS_TOKEN")
)

PACKS = {
    "10": {
        "fichas": 10,
        "precio": 2000
    },

    "30": {
        "fichas": 30,
        "precio": 4000
    },

    "50": {
        "fichas": 50,
        "precio": 7000
    },

    "100": {
        "fichas": 100,
        "precio": 15000
    }
}


def crear_preferencia(uid, pack_id):

    if pack_id not in PACKS:
        return None

    pack = PACKS[pack_id]

    preference_data = {
        "items": [
            {
                "title": f"{pack['fichas']} fichas InspirAR IA",
                "quantity": 1,
                "currency_id": "ARS",
                "unit_price": pack["precio"]
            }
        ],

        "metadata": {
            "uid": uid,
            "fichas": pack["fichas"]
        },

        "back_urls": {
            "success": "https://google.com",
            "failure": "https://google.com",
            "pending": "https://google.com"
        },

        "auto_return": "approved",

        "notification_url":
        "https://assistar-backend.onrender.com/mp/webhook"
    }

    preference_response = sdk.preference().create(
        preference_data
    )

    preference = preference_response["response"]

    return preference["init_point"]