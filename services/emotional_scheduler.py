import json

from apscheduler.schedulers.background import (
    BackgroundScheduler
)

from openai import OpenAI

from services.notification_service import (
    enviar_push_global
)

client = OpenAI()


# =========================================
# VERSICULO DEL DIA
# =========================================

def generar_versiculo():

    try:

        response = client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[
                {
                    "role": "system",

                    "content": """
Generar un versículo corto inspirador.

Responder JSON válido:

{
  "titulo": "...",
  "mensaje": "..."
}
"""
                }
            ]
        )

        texto = response.choices[
            0
        ].message.content

        data = json.loads(texto)

        enviar_push_global(

            data["titulo"],
            data["mensaje"]
        )

        print(
            "VERSICULO ENVIADO"
        )

    except Exception as e:

        print(
            "ERROR VERSICULO:",
            e
        )


# =========================================
# MENSAJE MOTIVACIONAL
# =========================================

def generar_mensaje_motivacional():

    try:

        response = client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[
                {
                    "role": "system",

                    "content": """
Generá un mensaje emocional corto.

JSON válido:

{
  "titulo": "...",
  "mensaje": "..."
}
"""
                }
            ]
        )

        texto = response.choices[
            0
        ].message.content

        data = json.loads(texto)

        enviar_push_global(

            data["titulo"],
            data["mensaje"]
        )

        print(
            "MENSAJE ENVIADO"
        )

    except Exception as e:

        print(
            "ERROR MOTIVACIONAL:",
            e
        )


# =========================================
# SCHEDULER
# =========================================

scheduler = BackgroundScheduler()


# 9 AM
scheduler.add_job(

    generar_versiculo,

    "cron",

    hour=9,
    minute=0
)


# 20 PM
scheduler.add_job(

    generar_mensaje_motivacional,

    "cron",

    hour=20,
    minute=0
)


scheduler.start()