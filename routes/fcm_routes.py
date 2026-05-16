from flask import Blueprint
from flask import request
from flask import jsonify

from services.firebase_service import db

fcm_bp = Blueprint(
    "fcm",
    __name__
)

@fcm_bp.route(
    "/guardar_token",
    methods=["POST"]
)
def guardar_token():

    data = request.json

    uid = data.get("uid")
    token = data.get("token")

    if not uid or not token:

        return jsonify({
            "ok": False
        }), 400

    db().collection(
        "users"
    ).document(uid).update({

        "fcm_token": token
    })

    return jsonify({
        "ok": True
    })