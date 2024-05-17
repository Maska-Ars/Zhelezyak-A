import bot_status
from aiogram import types
from aiogram import Dispatcher
from sys import exit

from handlers.DataBase.DataBase_functions import DataBase

# Объявление и/или создание БД пользователей
db = DataBase()


# Функция очистки истории запросов
async def cmd_clear(message: types.Message):
    db.delete_all_requests()
    await message.reply('История всех запросов была очищена!')


# Функция экстренного стоп-крана
async def cmd_emergency_brake(message: types.Message):
    await message.reply('Вы включили аварийный стоп-кран для бота!')
    await message.answer('!Бот остановлен!')
    exit()


# Регистрация всех команд в хендлер
def register_hamdlers_admin_private(dp: Dispatcher):
    dp.register_message_handler(cmd_clear, state=bot_status.BotMode.AdminStatus, commands='clear')
    dp.register_message_handler(cmd_emergency_brake, state=bot_status.BotMode.AdminStatus, commands='emergency_brake')
