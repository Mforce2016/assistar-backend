import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# =========================================
# CHAT GENERAL
# =========================================

def preguntar_ia(prompt_usuario):

    respuesta = client.responses.create(
        model="gpt-4.1-mini",

        input=f"""
Sos AssistAR, un asistente virtual argentino,
profesional, claro, inteligente y práctico.

Hablás natural como argentino cuando corresponde.
Ayudás con trabajo, informes, correos,
ideas y organización.

Usuario:
{prompt_usuario}
"""
    )

    return respuesta.output_text


# =========================================
# CORREOS
# =========================================

def generar_correo(texto):

    prompt = f"""
Respondé este correo de forma profesional,
amable y clara.

Correo:
{texto}
"""

    return preguntar_ia(prompt)


# =========================================
# INFORMES
# =========================================

def generar_informe(texto):

    prompt = f"""
Analizá el siguiente contenido y generá
un informe ejecutivo profesional.

Contenido:
{texto}

Formato:
- Resumen
- Hallazgos
- Riesgos
- Recomendaciones
"""

    return preguntar_ia(prompt)


# =========================================
# TITULO CHAT
# =========================================

def generar_titulo(texto):

    respuesta = client.responses.create(
        model="gpt-4.1-mini",

        input=f"""
Generá un título MUY corto (máx 5 palabras).

Texto:
{texto}

Sin comillas.
"""
    )

    return respuesta.output_text.strip()