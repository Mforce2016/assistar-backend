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

    try:

        data = request.json

        if not data:

            return jsonify({
                "ok": False,
                "error": "Sin datos"
            }), 400

        uid = data.get("uid")
        pack_id = data.get("pack_id")

        if not uid or not pack_id:

            return jsonify({
                "ok": False,
                "error": "Datos incompletos"
            }), 400

        init_point = crear_preferencia(
            uid,
            pack_id
        )

        if not init_point:

            return jsonify({
                "ok": False,
                "error": "No se pudo crear preferencia"
            }), 400

        return jsonify({
            "ok": True,
            "url": init_point
        })

    except Exception as e:

        print("ERROR CREAR PAGO:", e)

        return jsonify({
            "ok": False,
            "error": "Error interno"
        }), 500


# ====================================
# WEBHOOK MERCADO PAGO
# ====================================

@mp_bp.route(
    "/webhook",
    methods=["POST"]
)
def webhook():

    try:

        print("========== WEBHOOK ==========")
        print("ARGS:", request.args)
        print("JSON:", request.json)
        print("HEADERS:", request.headers)

        # ====================================
        # IGNORAR MERCHANT ORDER
        # ====================================

        topic = request.args.get("topic")

        if topic == "merchant_order":
            print("Merchant order ignorado")

            return "ok", 200

        # ====================================
        # OBTENER PAYMENT ID
        # ====================================

        payment_id = None

        # 1. query params modernos
        payment_id = request.args.get(
            "data.id"
        )

        # 2. query params antiguos
        if not payment_id:
            payment_id = request.args.get(
                "id"
            )

        # 3. body json
        if not payment_id:

            data = request.json

            if not data:
                print("No llegaron datos")

                return "ok", 200

            # formato moderno
            if "data" in data:

                payment_id = data["data"].get(
                    "id"
                )

            # formato antiguo
            elif "resource" in data:

                resource = data["resource"]

                # puede venir URL o ID directo
                if isinstance(resource, str):
                    payment_id = resource.split("/")[-1]

        # ====================================
        # VALIDAR ID
        # ====================================

        if not payment_id:
            print("No se pudo obtener payment_id")

            return "ok", 200

        print("PAYMENT ID:", payment_id)

        # ====================================
        # OBTENER INFO DEL PAGO
        # ====================================

        payment = sdk.payment().get(
            payment_id
        )

        print("PAYMENT INFO:", payment)

        # ====================================
        # VALIDAR RESPUESTA
        # ====================================

        if payment["status"] != 200:

            print("Pago inexistente")

            return "payment not found", 404

        payment_data = payment["response"]

        print("PAYMENT DATA:", payment_data)

        # ====================================
        # SOLO PAGOS APROBADOS
        # ====================================

        if payment_data.get("status") != "approved":

            print("Pago no aprobado")

            return "ok", 200

        # ====================================
        # METADATA
        # ====================================

        metadata = payment_data.get(
            "metadata",
            {}
        )

        uid = metadata.get("uid")
        fichas = metadata.get("fichas")

        print("UID:", uid)
        print("FICHAS:", fichas)

        if not uid or not fichas:

            print("Metadata incompleta")

            return "metadata error", 400

        # ====================================
        # EVITAR DUPLICADOS
        # ====================================

        pago_ref = db().collection(
            "pagos_mp"
        ).document(str(payment_id))

        if pago_ref.get().exists:

            print("Pago ya procesado")

            return "ok", 200

        # ====================================
        # SUMAR FICHAS
        # ====================================

        ref = db().collection(
            "users"
        ).document(uid)

        ref.update({
            "fichas":
            firestore.Increment(
                int(fichas)
            )
        })

        print("Fichas sumadas correctamente")

        # ====================================
        # GUARDAR PAGO PROCESADO
        # ====================================

        pago_ref.set({

            "uid": uid,

            "fichas": int(fichas),

            "payment_id": str(payment_id),

            "status": payment_data.get(
                "status"
            ),

            "monto": payment_data.get(
                "transaction_amount"
            ),

            "fecha":
            firestore.SERVER_TIMESTAMP
        })

        print("Pago guardado en Firestore")
        print("FICHAS ACREDITADAS")

        return "ok", 200

    except Exception as e:

        print("WEBHOOK ERROR:", e)

        return "error", 500