from flask import Blueprint, request, jsonify

from services.firebase_service import (
    asegurar_usuario,
    puede_consultar,
    sumar_consulta,
    consultas_restantes,
    obtener_datos
)

license_bp = Blueprint(
    "license",
    __name__
)


# =========================================
# VERIFICAR ACCESO
# =========================================

@license_bp.route(
    "/verificar_acceso",
    methods=["POST"]
)
def verificar_acceso_route():

    data = request.json

    usuario = data.get("usuario")

    asegurar_usuario(usuario)

    permitido = puede_consultar(usuario)

    return jsonify({
        "permitido": permitido
    })


# =========================================
# REGISTRAR CONSULTA
# =========================================

@license_bp.route(
    "/registrar_consulta",
    methods=["POST"]
)
def registrar_consulta_route():

    data = request.json

    usuario = data.get("usuario")

    sumar_consulta(usuario)

    return jsonify({
        "ok": True
    })


# =========================================
# ESTADO USUARIO
# =========================================

@license_bp.route(
    "/estado_usuario",
    methods=["POST"]
)
def estado_usuario_route():

    data = request.json

    usuario = data.get("usuario")

    datos = obtener_datos(usuario)

    restantes = consultas_restantes(usuario)

    return jsonify({
        "plan": datos["plan"],
        "restantes": restantes
    })