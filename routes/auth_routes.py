from flask import Blueprint, request, jsonify
from backend.services.firebase_service import db

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.json

    usuario = data.get("usuario")
    clave = data.get("clave")

    ref = db().collection("users").document(usuario)
    doc = ref.get()

    if not doc.exists:
        return jsonify({
            "success": False,
            "error": "Usuario no existe"
        })

    datos = doc.to_dict()

    if datos["password"] != clave:
        return jsonify({
            "success": False,
            "error": "Contraseña incorrecta"
        })

    return jsonify({
        "success": True,
        "usuario": usuario
    })