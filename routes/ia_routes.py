from flask import Blueprint, request, jsonify

from services.openai_service import (
    preguntar_ia,
    generar_correo,
    generar_informe,
    generar_titulo
)

ia_bp = Blueprint("ia", __name__)


# =========================================
# CHAT
# =========================================

@ia_bp.route("/chat", methods=["POST"])
def chat():

    data = request.json

    mensaje = data.get("mensaje")

    respuesta = preguntar_ia(mensaje)

    return jsonify({
        "respuesta": respuesta
    })


# =========================================
# CORREO
# =========================================

@ia_bp.route("/correo", methods=["POST"])
def correo():

    data = request.json

    texto = data.get("texto")

    respuesta = generar_correo(texto)

    return jsonify({
        "respuesta": respuesta
    })


# =========================================
# INFORME
# =========================================

@ia_bp.route("/informe", methods=["POST"])
def informe():

    data = request.json

    texto = data.get("texto")

    respuesta = generar_informe(texto)

    return jsonify({
        "respuesta": respuesta
    })


# =========================================
# TITULO CHAT
# =========================================

@ia_bp.route("/titulo", methods=["POST"])
def titulo():

    data = request.json

    texto = data.get("texto")

    respuesta = generar_titulo(texto)

    return jsonify({
        "respuesta": respuesta
    })