from flask import Blueprint, request, jsonify

from services.firebase_auth_service import verify_email
from services.firebase_service import (
    asegurar_usuario
)

auth_bp = Blueprint(
    "auth",
    __name__
)

# =========================================
# REGISTER
# =========================================

@auth_bp.route(
    "/register",
    methods=["POST"]
)
def register():

    try:

        data = request.json

        email = data.get("email")
        password = data.get("password")

        result = register_user(
            email,
            password
        )

        if "error" in result:

            return jsonify({
                "ok": False,
                "error": result["error"]["message"]
            })

        asegurar_usuario(email)

        id_token = result["idToken"]

        send_verify_email(id_token)

        return jsonify({
            "ok": True
        })

    except Exception as e:

        return jsonify({
            "ok": False,
            "error": str(e)
        })

# =========================================
# LOGIN
# =========================================

@auth_bp.route(
    "/login",
    methods=["POST"]
)
def login():

    try:

        data = request.json

        email = data.get("email")
        password = data.get("password")

        result = login_user(
            email,
            password
        )

        if "error" in result:

            return jsonify({
                "ok": False,
                "error": result["error"]["message"]
            })

        info = get_account_info(
            result["idToken"]
        )

        usuarios = info.get(
            "users",
            []
        )

        if not usuarios:

            return jsonify({
                "ok": False,
                "error": "USER_NOT_FOUND"
            })

        email_verified = usuarios[0].get(
            "emailVerified",
            False
        )

        if not email_verified:

            return jsonify({
                "ok": False,
                "error": "EMAIL_NOT_VERIFIED"
            })

        return jsonify({
            "ok": True,
            "token": result["idToken"],
            "email": email
        })

    except Exception as e:

        return jsonify({
            "ok": False,
            "error": str(e)
        })

# =========================================
# RECUPERAR PASSWORD
# =========================================

@auth_bp.route(
    "/reset_password",
    methods=["POST"]
)
def reset_password():

    try:

        data = request.json

        email = data.get("email")

        result = send_reset_email(
            email
        )

        if "error" in result:

            return jsonify({
                "ok": False,
                "error": result["error"]["message"]
            })

        return jsonify({
            "ok": True
        })

    except Exception as e:

        return jsonify({
            "ok": False,
            "error": str(e)
        })