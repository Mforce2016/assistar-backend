from flask import Blueprint, request, jsonify

from services.mp_service import crear_pago
from services.firebase_service import activar_plan

import mercadopago
import os

payment_bp = Blueprint(
    "payment",
    __name__
)

sdk = mercadopago.SDK(
    os.getenv("MP_ACCESS_TOKEN")
)


# =========================================
# CREAR LINK PAGO
# =========================================

@payment_bp.route(
    "/crear_pago",
    methods=["POST"]
)
def crear_pago_route():

    data = request.json

    usuario = data.get("usuario")
    plan = data.get("plan")

    url = crear_pago(usuario, plan)

    return jsonify({
        "url": url
    })


# =========================================
# WEBHOOK MERCADOPAGO
# =========================================

@payment_bp.route(
    "/webhook_mp",
    methods=["POST"]
)
def webhook_mp():

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

        usuario, plan = external_reference.split("|")

        activar_plan(usuario, plan)

        return "ok", 200

    except Exception as e:

        print(str(e))

        return "error", 500