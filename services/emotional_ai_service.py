import os
import json

from openai import OpenAI
from datetime import datetime
from firebase_admin import firestore
from services.firebase_service import db

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# =========================================
# OBTENER FICHAS
# =========================================

def obtener_fichas(uid):

    ref = db().collection(
        "users"
    ).document(uid)

    doc = ref.get()

    if not doc.exists:
        return 0

    datos = doc.to_dict()

    return datos.get("fichas", 0)


# =========================================
# DESCONTAR FICHA
# =========================================

def descontar_ficha(uid):

    ref = db().collection(
        "users"
    ).document(uid)

    ref.update({
        "fichas": firestore.Increment(-1)
    })


# =========================================
# GUARDAR MENSAJE
# =========================================

def guardar_historial(
    uid,
    mensaje,
    respuesta,
    emocion
):

    ref = db().collection(
        "users"
    ).document(uid).collection(
        "emotional_history"
    )

    ref.add({
        "mensaje": mensaje,
        "respuesta": respuesta,
        "emocion": emocion,
        "fecha": datetime.now()
    })


# =========================================
# OBTENER HISTORIAL
# =========================================

def obtener_historial(uid, limite=8):

    ref = db().collection(
        "users"
    ).document(uid).collection(
        "emotional_history"
    ).order_by(
        "fecha",
        direction=firestore.Query.DESCENDING
    ).limit(limite)

    docs = ref.stream()

    historial = []

    for doc in docs:

        data = doc.to_dict()

        historial.append({
            "mensaje": data.get("mensaje", ""),
            "respuesta": data.get("respuesta", "")
        })

    historial.reverse()

    return historial


# =========================================
# CHAT EMOCIONAL
# =========================================

def preguntar_ia_emocional(
    uid,
    mensaje
):

    try:

        fichas = obtener_fichas(uid)

        if fichas <= 0:

            return {
                "ok": False,
                "error": "SIN_FICHAS",
                "respuesta": "Te quedaste sin fichas."
            }

        historial = obtener_historial(uid)

        mensajes_contexto = []

        mensajes_contexto.append({
            "role": "system",
            "content": """
Sos un acompañante emocional y espiritual.

Tu objetivo es:
- escuchar con empatía
- acompañar emocionalmente
- transmitir paz y esperanza
- responder cálidamente
- recomendar versículos bíblicos relevantes
- hacer sentir acompañado al usuario

IMPORTANTE:
- responder natural y humano
- no sonar robótico
- no usar markdown
- no usar emojis
- máximo 2 párrafos
- no juzgar
- no imponer religión
- no discutir doctrinas
- no actuar como terapeuta
- hablar de manera cálida y cercana

Debés devolver SIEMPRE un JSON válido con esta estructura:

{
  "respuesta": "...",
  "emocion": "...",
  "versiculo_texto": "...",
  "versiculo_referencia": "..."
}

NO agregues texto fuera del JSON.
NO uses bloques markdown.
NO uses ```json.

Si detectás:
- suicidio
- autolesión
- desesperación severa

debés:
- responder con máxima empatía
- recomendar ayuda profesional
- recomendar contacto humano inmediato
"""
        })

        for item in historial:

            mensajes_contexto.append({
                "role": "user",
                "content": item["mensaje"]
            })

            mensajes_contexto.append({
                "role": "assistant",
                "content": item["respuesta"]
            })

        mensajes_contexto.append({
            "role": "user",
            "content": mensaje
        })

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=mensajes_contexto,
            temperature=0.8,
            max_tokens=300
        )

        texto = (
            response
            .choices[0]
            .message
            .content
        )

        if texto is None:
            texto = ""

        texto = texto.strip()

        print("========== OPENAI RESPONSE ==========")
        print(texto)
        print("=====================================")

        # LIMPIAR markdown
        texto = texto.replace(
            "```json",
            ""
        )

        texto = texto.replace(
            "```",
            ""
        )

        texto = texto.strip()

        try:

            data = json.loads(texto)

        except Exception as e:

            print("ERROR JSON:", str(e))

            data = {
                "respuesta":
                    texto if texto else
                    "Ahora mismo no pude responderte correctamente.",
                "emocion": "neutral",
                "versiculo_texto": "",
                "versiculo_referencia": ""
            }

        respuesta_final = data.get(
            "respuesta",
            ""
        )

        if not respuesta_final:

            respuesta_final = (
                "Estoy acá con vos. "
                "Contame un poco más cómo te sentís."
            )

        guardar_historial(
            uid,
            mensaje,
            respuesta_final,
            data.get(
                "emocion",
                "neutral"
            )
        )

        descontar_ficha(uid)

        return {

            "ok": True,

            "respuesta": respuesta_final,

            "emocion": data.get(
                "emocion",
                "neutral"
            ),

            "versiculo": {

                "texto": data.get(
                    "versiculo_texto",
                    ""
                ),

                "referencia": data.get(
                    "versiculo_referencia",
                    ""
                )
            },

            "fichas_restantes": fichas - 1
        }

    except Exception as e:

        print("ERROR GENERAL IA:")
        print(str(e))

        return {
            "ok": False,
            "respuesta": "Ocurrió un problema al conectar con la IA.",
            "error": str(e)
        }


# =========================================
# VERSICULO DEL DIA
# =========================================

def obtener_versiculo_dia():

    response = client.chat.completions.create(
        model="gpt-4.1-mini",

        messages=[
            {
                "role": "system",
                "content": """
Generá un versículo bíblico inspirador.

Devolver JSON válido:

{
  "texto": "...",
  "referencia": "..."
}
"""
            }
        ]
    )

    texto = response.choices[0].message.content

    try:
        return json.loads(texto)

    except:
        return {
            "texto": "",
            "referencia": ""
        }
