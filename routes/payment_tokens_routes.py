from flask import Blueprint
from flask import request
from flask import jsonify
import mercadopago
import os
from services.token_payment_service import (
    crear_pago_fichas
)
from services.firebase_service import (
    sumar_fichas
)

tokens_bp = Blueprint(
    "tokens",
    __name__
)

sdk = mercadopago.SDK(
    os.getenv("MP_ACCESS_TOKEN")
)


# =========================================
# CREAR PAGO
# =========================================

@tokens_bp.route(
    "/crear_pago",
    methods=["POST"]
)
def crear_pago():

    data = request.json

    uid = data.get("uid")
    pack = data.get("pack")

    if not uid or not pack:

        return jsonify({
            "ok": False,
            "error": "DATOS_INVALIDOS"
        }), 400

    try:

        url = crear_pago_fichas(
            uid,
            pack
        )

        return jsonify({
            "ok": True,
            "url": url
        })

    except Exception as e:

        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500


# =========================================
# WEBHOOK MERCADOPAGO
# =========================================

@tokens_bp.route(
    "/webhook",
    methods=["POST"]
)
def webhook():

    try:

        data = request.json

        if data["type"] != "payment":

            return "ok", 200

        payment_id = data["data"]["id"]

        payment_info = sdk.payment().get(
            payment_id
        )

        payment = payment_info["response"]

        status = payment["status"]

        if status != "approved":

            return "ok", 200

        external_reference = payment[
            "external_reference"
        ]

        uid, fichas = external_reference.split(
            "|"
        )

        sumar_fichas(
            uid,
            int(fichas)
        )

        return "ok", 200

    except Exception as e:

        print(str(e))

        return "error", 500