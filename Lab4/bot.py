import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# Конфігурація
API_TOKEN = '8787494433:AAEu9lJ805m94z1grzhGjKIT8Ue9dLoZT4g'

# Налаштування логування
logging.basicConfig(level=logging.INFO)

# Ініціалізація бота та диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Дані дисципліни для групи ПЗПІ-22-7
COURSE_INFO = {
    "subject": "Програмування в мережевих середовищах",
    "teacher": "Демчук В. Г.",
    "moodle_link": "https://pzm.nure.ua/",
    "group": "ПЗПІ-22-7",
    "student": "Тригуб І. О."
}

def get_main_keyboard():
    """Створює головне меню бота"""
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="📅 Розклад занять"))
    builder.row(types.KeyboardButton(text="📚 Навчальні матеріали"))
    builder.row(types.KeyboardButton(text="📧 Контакти викладача"), 
                types.KeyboardButton(text="🕒 Актуальні дедлайни"))
    return builder.as_markup(resize_keyboard=True)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обробка команди /start"""
    await message.answer(
        f"Вітаю, {message.from_user.first_name}!\n\n"
        f"Я бот-помічник групи **{COURSE_INFO['group']}**.\n"
        f"Супроводжую дисципліну: *{COURSE_INFO['subject']}*.\n"
        f"Автор: {COURSE_INFO['student']}",
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown"
    )

@dp.message(lambda message: message.text == "📅 Розклад занять")
async def show_schedule(message: types.Message):
    schedule = (
        "🗓 **Розклад ПЗПІ-22-7:**\n\n"
        "• Понеділок: 1 пара (Лекція, онлайн)\n"
        "• Середа: 3 пара (Лабораторна робота)\n"
        "• П'ятниця: 2 пара (Практичне заняття)"
    )
    await message.answer(schedule, parse_mode="Markdown")

@dp.message(lambda message: message.text == "📚 Навчальні матеріали")
async def show_materials(message: types.Message):
    await message.answer(
        f"🔗 **Посилання на Moodle:**\n{COURSE_INFO['moodle_link']}\n\n"
        "Тут ви знайдете методичні вказівки та лекції.",
        parse_mode="Markdown"
    )

@dp.message(lambda message: message.text == "📧 Контакти викладача")
async def show_contacts(message: types.Message):
    await message.answer(
        f"👤 **Викладач:** {COURSE_INFO['teacher']}\n"
        f"📩 Email: v.demchuk@nure.ua\n"
        f"💬 Telegram: @demchuk_v_g",
        parse_mode="Markdown"
    )

@dp.message(lambda message: message.text == "🕒 Актуальні дедлайни")
async def show_deadlines(message: types.Message):
    deadlines = (
        "⚠️ **Графік здачі робіт:**\n\n"
        "• ЛР №3 (Docker): до 29.03.2026\n"
        "• ЛР №4 (Чат-бот): до 15.04.2026\n"
        "• ПЗ №3 (Хмари): до 30.03.2026"
    )
    await message.answer(deadlines, parse_mode="Markdown")

async def main():
    """Запуск процесу опитування (Polling)"""
    print(f"Бот для групи {COURSE_INFO['group']} запущений...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот зупинений.")
