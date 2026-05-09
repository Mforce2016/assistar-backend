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

IMPORTANTE:
- Responder claro y directo.
- NO usar markdown.
- NO usar símbolos como:
**, ---, ###, *, etc.
- NO actuar como ChatGPT.
- NO explicar lo que vas a hacer.
- NO usar frases como:
"Claro", "Acá tenés", etc.

Usuario:
{prompt_usuario}
"""
    )

    return respuesta.output_text.strip()


# =========================================
# CORREOS
# =========================================

def generar_correo(texto):

    prompt = f"""
Respondé el siguiente correo.

IMPORTANTE:
- Devolver ÚNICAMENTE el texto del correo.
- NO explicar nada.
- NO usar frases como:
"Claro", "Acá te dejo", etc.
- NO usar markdown.
- NO usar separadores.
- NO agregar comentarios finales.
- NO hacer preguntas.
- Mantener tono profesional y natural.

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
un informe ejecutivo corporativo profesional.

IMPORTANTE:

- NO usar markdown.
- NO usar símbolos como:
**, ---, ###, *, etc.
- NO usar emojis.
- NO usar formato estilo ChatGPT.
- Redactar como informe empresarial real.
- Mantener excelente estructura visual.
- Usar títulos limpios.
- Usar lenguaje corporativo.

FORMATO OBLIGATORIO:

TÍTULO DEL INFORME

RESUMEN EJECUTIVO

HALLAZGOS PRINCIPALES

RIESGOS DETECTADOS

RECOMENDACIONES

CONCLUSIÓN

Contenido:
{texto}
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

IMPORTANTE:
- Sin comillas
- Sin punto final
- Sin markdown

Texto:
{texto}
"""
    )

    return respuesta.output_text.strip()