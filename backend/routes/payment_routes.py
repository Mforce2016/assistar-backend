from flask import Blueprint, request, jsonify
from backend.services.mercado_pago_service import crear_preferencia

payment_bp = Blueprint("payment", __name__)


# =========================================
# CREAR LINK DE PAGO
# =========================================
@payment_bp.route("/crear_pago", methods=["POST"])
def crear_pago():

    datos = request.json

    usuario = datos.get("usuario")
    plan = datos.get("plan")

    if not usuario or not plan:
        return jsonify({
            "error": "Faltan datos"
        }), 400

    resultado = crear_preferencia(usuario, plan)

    return jsonify(resultado)