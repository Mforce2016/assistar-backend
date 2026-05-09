import mercadopago
import os
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN")

sdk = mercadopago.SDK(ACCESS_TOKEN)


# =========================================
# CREAR PREFERENCIA MP
# =========================================
def crear_preferencia(usuario, plan):

    precio = 12000

    if plan == "anual":
        precio = 120000

    preference_data = {
        "items": [
            {
                "title": f"AssistAR Plan {plan}",
                "quantity": 1,
                "currency_id": "ARS",
                "unit_price": precio
            }
        ],

        "payer": {
            "name": usuario
        },

        "back_urls": {
            "success": "https://www.jforceapps.com.ar/pago-exitoso",
            "failure": "https://www.jforceapps.com.ar/pago-fallido",
            "pending": "https://www.jforceapps.com.ar/pago-pendiente"
        },

        "auto_return": "approved"
    }

    preference_response = sdk.preference().create(preference_data)

    preference = preference_response["response"]

    return {
        "url": preference["init_point"]
    }