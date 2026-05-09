import firebase_admin
import json
import os

from firebase_admin import credentials
from firebase_admin import firestore

from datetime import datetime, timedelta


# =====================================
# INICIAR FIREBASE
# =====================================

def iniciar_firebase():

    try:
        firebase_admin.get_app()

    except:

        firebase_json = os.getenv(
            "FIREBASE_CREDENTIALS"
        )

        if not firebase_json:
            raise Exception(
                "Falta FIREBASE_CREDENTIALS"
            )

        cred_dict = json.loads(firebase_json)

        cred = credentials.Certificate(
            cred_dict
        )

        firebase_admin.initialize_app(cred)


# =====================================
# DB
# =====================================

def db():
    iniciar_firebase()
    return firestore.client()


# =====================================
# ASEGURAR USUARIO
# =====================================

def asegurar_usuario(usuario):

    ref = db().collection(
        "licenses"
    ).document(usuario)

    doc = ref.get()

    if not doc.exists:

        ref.set({
            "usuario": usuario,
            "consultas": 0,
            "plan": "trial",
            "vence": "",
            "creado": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        })


# =====================================
# OBTENER DATOS
# =====================================

def obtener_datos(usuario):

    ref = db().collection(
        "licenses"
    ).document(usuario)

    doc = ref.get()

    if doc.exists:
        return doc.to_dict()

    return None


# =====================================
# CONSULTAS RESTANTES
# =====================================

def consultas_restantes(usuario):

    datos = obtener_datos(usuario)

    if not datos:
        return 0

    if datos["plan"] == "trial":

        return 50 - datos["consultas"]

    return -1


# =====================================
# PUEDE CONSULTAR
# =====================================

def puede_consultar(usuario):

    datos = obtener_datos(usuario)

    if not datos:
        return False

    plan = datos["plan"]

    if plan == "trial":

        return datos["consultas"] < 50

    if plan in ["mensual", "anual"]:

        if datos["vence"] == "":
            return False

        vence = datetime.strptime(
            datos["vence"],
            "%Y-%m-%d"
        )

        return datetime.now() <= vence

    return False


# =====================================
# SUMAR CONSULTA
# =====================================

def sumar_consulta(usuario):

    ref = db().collection(
        "licenses"
    ).document(usuario)

    datos = obtener_datos(usuario)

    ref.update({
        "consultas": datos["consultas"] + 1
    })


# =====================================
# ACTIVAR PLAN
# =====================================

def activar_plan(usuario, plan):

    dias = 30

    if plan == "anual":
        dias = 365

    vence = datetime.now() + timedelta(
        days=dias
    )

    ref = db().collection(
        "licenses"
    ).document(usuario)

    ref.update({
        "plan": plan,
        "consultas": 0,
        "vence": vence.strftime("%Y-%m-%d")
    })


# =====================================
# BLOQUEAR USUARIO
# =====================================

def bloquear_usuario(usuario):

    ref = db().collection(
        "licenses"
    ).document(usuario)

    ref.update({
        "plan": "bloqueado"
    })