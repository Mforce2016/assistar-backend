from flask import Blueprint, request, jsonify

from services.firebase_auth_service import (
    register_user,
    login_user,
    send_reset_email,
    send_verify_email,
    get_account_info
)

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

        data = request.json or {}

        email = data.get("email")
        password = data.get("password")

        if not email or not password:

            return jsonify({
                "ok": False,
                "error": "EMAIL_AND_PASSWORD_REQUIRED"
            }), 400

        result = register_user(
            email,
            password
        )

        if "error" in result:

            return jsonify({
                "ok": False,
                "error": result["error"]["message"]
            }), 400

        asegurar_usuario(email)

        id_token = result.get("idToken")

        if id_token:
            send_verify_email(id_token)

        return jsonify({
            "ok": True
        })

    except Exception as e:

        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500


# =========================================
# LOGIN
# =========================================

@auth_bp.route(
    "/login",
    methods=["POST"]
)
def login():

    try:

        data = request.json or {}

        email = data.get("email")
        password = data.get("password")

        if not email or not password:

            return jsonify({
                "ok": False,
                "error": "EMAIL_AND_PASSWORD_REQUIRED"
            }), 400

        result = login_user(
            email,
            password
        )

        if "error" in result:

            return jsonify({
                "ok": False,
                "error": result["error"]["message"]
            }), 400

        id_token = result.get("idToken")

        info = get_account_info(id_token)

        usuarios = info.get(
            "users",
            []
        )

        if not usuarios:

            return jsonify({
                "ok": False,
                "error": "USER_NOT_FOUND"
            }), 404

        email_verified = usuarios[0].get(
            "emailVerified",
            False
        )

        if not email_verified:

            return jsonify({
                "ok": False,
                "error": "EMAIL_NOT_VERIFIED"
            }), 403

        return jsonify({
            "ok": True,
            "token": id_token,
            "email": email
        })

    except Exception as e:

        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500


# =========================================
# RESET PASSWORD
# =========================================

@auth_bp.route(
    "/reset_password",
    methods=["POST"]
)
def reset_password_route():

    try:

        data = request.json or {}

        email = data.get("email")

        if not email:

            return jsonify({
                "ok": False,
                "error": "EMAIL_REQUIRED"
            }), 400

        result = send_reset_email(
            email
        )

        if "error" in result:

            return jsonify({
                "ok": False,
                "error": result["error"]["message"]
            }), 400

        return jsonify({
            "ok": True
        })

    except Exception as e:

        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500