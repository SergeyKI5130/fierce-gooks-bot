import json
from datetime import date
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import QUESTION, OPTIONS

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напиши /poll чтобы пройти опрос.")

async def poll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(opt, callback_data=f"opt_{i}")]
        for i, opt in enumerate(OPTIONS)
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(QUESTION, reply_markup=reply_markup)

async def summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today = date.today().isoformat()

    try:
        with open("responses.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        await update.message.reply_text("❌ Нет данных за сегодня.")
        return

    responses = data.get(today)
    if not responses:
        await update.message.reply_text("❌ Нет ответов за сегодня.")
        return

    lines = [f"📊 Ответы за {today}:\n"]
    for r in responses:
        name = r.get("full_name", "Без имени")
        group_name = r.get("group_name", "никнейм не задан")
        link = r.get("link", "")
        answer = r.get("answer", "?")
        time = r.get("timestamp", "время неизвестно")

        lines.append(
            f"👤 {name} ({group_name})\n🔗 {link}\n💬 {answer}\n🕓 {time}\n"
        )

    lines.append(f"\nВсего ответов: {len(responses)}")
    await update.message.reply_text("\n".join(lines))

