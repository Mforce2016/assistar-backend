from flask import Blueprint
from flask import request
from flask import jsonify
from services.emotional_ai_service import (
    preguntar_ia_emocional,
    obtener_versiculo_dia,
    obtener_fichas
)

emotional_bp = Blueprint(
    "emotional",
    __name__
)


# =========================================
# CHAT EMOCIONAL
# =========================================

@emotional_bp.route(
    "/chat",
    methods=["POST"]
)
def chat_emocional():

    data = request.json

    uid = data.get("uid")
    mensaje = data.get("mensaje")

    if not uid or not mensaje:

        return jsonify({
            "ok": False,
            "error": "DATOS_INVALIDOS"
        }), 400

    respuesta = preguntar_ia_emocional(
        uid,
        mensaje
    )

    return jsonify(respuesta)


# =========================================
# FICHAS
# =========================================

@emotional_bp.route(
    "/fichas",
    methods=["POST"]
)
def fichas():

    data = request.json

    uid = data.get("uid")

    cantidad = obtener_fichas(uid)

    return jsonify({
        "ok": True,
        "fichas": cantidad
    })


# =========================================
# VERSICULO DEL DIA
# =========================================

@emotional_bp.route(
    "/versiculo_dia",
    methods=["GET"]
)
def versiculo_dia():

    data = obtener_versiculo_dia()

    return jsonify({
        "ok": True,
        "versiculo": data
    })

# =========================================
# TEST
# =========================================

@emotional_bp.route(
    "/test",
    methods=["GET"]
)
def emotional_test():

    return jsonify({
        "status": "Emotional routes online"
    })