# keyword_bot.py
# Telegram-бот на aiogram 3.7+, отвечает только на фразу "на подработку"
# Выдаёт список людей в столбик

import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message

# ================== НАСТРОЙКИ ==================

BOT_TOKEN = "8205891122:AAFe38E_Q2fp-bHSDQfE--FsYOMPC-802X0"  # ← ТВОЙ ТОКЕН!

# Список людей, которых показываем при фразе "на подработку"
PEOPLE_ON_SUBWORK = [
    "Шеуджен Артур",
    "Зотов Максим",
    "Шеуджен Аскер",
    "Ткачев Максим",
    "Чуц Руслан",
    # Добавляй сюда новых людей — каждый в новой строке
    # "Петрова Анна",
    # "Сидоров Дмитрий",
    # "Кузнецова Ольга",
]

# Реагировать только в группах/супергруппах?
ONLY_IN_GROUPS = True

# Минимальная длина сообщения для обработки
MIN_MESSAGE_LENGTH = 3

# Игнорировать свои сообщения
IGNORE_OWN_MESSAGES = True

# ===============================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()


@dp.message(F.text)
async def keyword_handler(message: Message):
    if len(message.text) < MIN_MESSAGE_LENGTH:
        return

    if ONLY_IN_GROUPS and message.chat.type not in ("group", "supergroup"):
        return

    if IGNORE_OWN_MESSAGES and message.from_user.id == (await bot.get_me()).id:
        return

    text = message.text.lower()

    # Единственная реакция бота — на фразу "на подработку"
    if "на подработку" in text:
        if not PEOPLE_ON_SUBWORK:
            reply_text = "Список пока пустой"
        else:
            reply_text = "На подработку:\n" + "\n".join(f"• {person}" for person in PEOPLE_ON_SUBWORK)

        try:
            await message.reply(reply_text)
        except Exception as e:
            logging.error(f"Ошибка отправки списка: {e}")
        return  # Больше ничего не делаем


async def main():
    me = await bot.get_me()
    print(f"Бот запущен: @{me.username}")
    print(f"Людей в списке: {len(PEOPLE_ON_SUBWORK)}")
    print("Запуск polling...\n")

    await dp.start_polling(
        bot,
        allowed_updates=["message"],
        drop_pending_updates=True
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("\nБот остановлен")