from telegram import Update
from telegram.ext import ContextTypes
from config import OPTIONS
from utils.save import save_response

async def handle_option(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    index = int(query.data.split("_")[1])
    selected_option = OPTIONS[index]

    save_response(update.effective_user, selected_option)
    await query.edit_message_text("Спасибо! Ответ сохранён.")
