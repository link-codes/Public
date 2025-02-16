import os
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.types import Update
from aiogram.utils.executor import start_webhook
from fastapi import FastAPI
import uvicorn

TOKEN = os.getenv("TOKEN")  # Получаем токен из переменных окружения
WEBHOOK_URL = f"https://ТВОЙ_RAILWAY_URL/webhook"  # URL вебхука
WEBHOOK_PATH = "/webhook"
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.getenv("PORT", 8000))  # Railway даёт PORT автоматически

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
app = FastAPI()

# Подключаем базу данных
conn = sqlite3.connect("dating.db")
cursor = conn.cursor()

# Создаём таблицу пользователей (если её нет)
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE,
    name TEXT,
    age INTEGER,
    city TEXT,
    interests TEXT
)
""")
conn.commit()


# Команда /start
@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.answer("Привет! Это быстрый бот на вебхуках 🚀")


# Telegram будет отправлять запросы сюда
@app.post(WEBHOOK_PATH)
async def telegram_webhook(update: dict):
    telegram_update = Update(**update)
    await dp.process_update(telegram_update)


# Запускаем вебхук
async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown():
    await bot.delete_webhook()


if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(on_startup())
    uvicorn.run(app, host=WEBAPP_HOST, port=WEBAPP_PORT)
