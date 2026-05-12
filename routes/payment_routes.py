from flask import Blueprint, request, jsonify

from services.mercado_pago_service import crear_pago
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

        print("WEBHOOK RECIBIDO:")
        print(data)

        # validar tipo
        if data.get("type") != "payment":
            return "ok", 200

        payment_id = data["data"]["id"]

        payment_info = sdk.payment().get(
            payment_id
        )

        payment = payment_info["response"]

        print("PAYMENT INFO:")
        print(payment)

        status = payment.get("status")

        if status != "approved":
            print("Pago no aprobado")
            return "ok", 200

        external_reference = payment.get(
            "external_reference"
        )

        if not external_reference:
            print("Sin external_reference")
            return "ok", 200

        usuario, plan = external_reference.split("|")

        activar_plan(usuario, plan)

        print(
            f"PLAN ACTIVADO: {usuario} -> {plan}"
        )

        return "ok", 200

    except Exception as e:

        print("ERROR WEBHOOK:")
        print(str(e))

        return "error", 500