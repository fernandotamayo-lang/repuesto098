import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from groq import Groq

load_dotenv(dotenv_path=".env", override=True)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

print("TOKEN LEIDO:")
print(repr(TELEGRAM_TOKEN))

print("GROQ LEIDO:")
print(repr(GROQ_API_KEY))
client = Groq(api_key=GROQ_API_KEY)
PROMPT = """
Eres un asesor experto de una tienda de repuestos para motos.
Ayudas a vender repuestos, responder preguntas y atender clientes.
"""
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return

    await update.message.reply_text(
        "🏍️ Bienvenido a Repuestos Moto\n¿Qué repuesto necesitas?"
    )


async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return

    try:
        mensaje = update.message.text

        respuesta_ia = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": PROMPT
                },
                {
                    "role": "user",
                    "content": mensaje
                }
            ]
        )

        respuesta = (
            respuesta_ia.choices[0].message.content
            or "No pude generar una respuesta."
        )

        await update.message.reply_text(respuesta)

    except Exception as e:
        print("ERROR:", e)

        await update.message.reply_text(
            "Ocurrió un error al procesar tu mensaje."
        )


if not TELEGRAM_TOKEN:
    raise ValueError("No se encontró TELEGRAM_TOKEN")

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, responder)
)

print("Bot activo...")
app.run_polling()