import mercadopago
import os


sdk = mercadopago.SDK(
    os.getenv("MP_ACCESS_TOKEN")
)


def crear_pago(usuario, plan):

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

        "external_reference": f"{usuario}|{plan}",

        "notification_url":
        "https://assistar-backend.onrender.com/webhook_mp"
    }

    preference_response = sdk.preference().create(
        preference_data
    )

    preference = preference_response["response"]

    return preference["init_point"]