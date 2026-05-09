from flask import Blueprint, request, jsonify

from services.firebase_service import db
from services.firebase_service import asegurar_usuario

auth_bp = Blueprint("auth", __name__)


# =========================================
# LOGIN
# =========================================

@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.json

    usuario = data.get("usuario")
    clave = data.get("clave")

    ref = db().collection("users").document(usuario)

    doc = ref.get()

    if not doc.exists:

        return jsonify({
            "ok": False
        })

    datos = doc.to_dict()

    if datos["password"] != clave:

        return jsonify({
            "ok": False
        })

    return jsonify({
        "ok": True
    })


# =========================================
# REGISTER
# =========================================

@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.json

    usuario = data.get("usuario")
    clave = data.get("clave")

    ref = db().collection("users").document(usuario)

    if ref.get().exists:

        return jsonify({
            "ok": False
        })

    ref.set({
        "usuario": usuario,
        "password": clave
    })

    asegurar_usuario(usuario)

    return jsonify({
        "ok": True
    })