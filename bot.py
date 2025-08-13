import asyncio
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
)
from aiohttp import web
import os

from config import BOT_TOKEN
from handlers.commands import start, poll, summary
from handlers.callbacks import handle_option


# 🔹 Telegram бот
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("poll", poll))
app.add_handler(CommandHandler("summary", summary))
app.add_handler(CallbackQueryHandler(handle_option))

# 🔹 HTTP-сервер для Render
async def handle(request):
    return web.Response(text="Bot is alive!")

async def main():
    # Запуск Telegram бота
    bot_task = asyncio.create_task(app.run_polling())

    # Запуск aiohttp-сервера
    server = web.Application()
    server.router.add_get("/", handle)   # Render будет пинговать этот endpoint
    runner = web.AppRunner(server)
    await runner.setup()
    site = web.TCPSite(runner, port=int(os.environ.get("PORT", 8080)))
    await site.start()

    print("Бот запущен и сервер работает на /")

    await bot_task  # Telegram бот будет работать постоянно

if __name__ == "__main__":
    asyncio.run(main())
