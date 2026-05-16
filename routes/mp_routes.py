from flask import Blueprint
from flask import request
from flask import jsonify

from services.mp_service import (
    crear_preferencia
)

from services.firebase_service import db
from firebase_admin import firestore

import mercadopago
import os

mp_bp = Blueprint(
    "mp",
    __name__
)

sdk = mercadopago.SDK(
    os.getenv("MP_ACCESS_TOKEN")
)


# ====================================
# CREAR PAGO
# ====================================

@mp_bp.route(
    "/crear_pago",
    methods=["POST"]
)
def crear_pago():

    data = request.json

    uid = data.get("uid")
    pack_id = data.get("pack_id")

    init_point = crear_preferencia(
        uid,
        pack_id
    )

    if not init_point:

        return jsonify({
            "ok": False
        }), 400

    return jsonify({
        "ok": True,
        "url": init_point
    })


# ====================================
# WEBHOOK
# ====================================

@mp_bp.route(
    "/webhook",
    methods=["POST"]
)
def webhook():

    data = request.json

    try:

        payment_id = data["data"]["id"]

        payment = sdk.payment().get(
            payment_id
        )

        payment_data = payment["response"]

        if payment_data["status"] != "approved":
            return "ok"

        metadata = payment_data["metadata"]

        uid = metadata["uid"]

        fichas = metadata["fichas"]

        ref = db().collection(
            "users"
        ).document(uid)

        ref.update({
            "fichas":
            firestore.Increment(fichas)
        })

        return "ok"

    except Exception as e:

        print(e)

        return "error", 500