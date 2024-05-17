import bot_status
from aiogram import types, Dispatcher
from settings import ADMIN_ID
from aiogram.dispatcher import FSMContext


# Функция запуска и присваивание статуса пользователю
async def cmd_start(message: types.Message):
    await message.reply(f"!Бот успешно запущен!")
    if message.from_user.id in ADMIN_ID:
        await bot_status.BotMode.AdminStatus.set()
        await message.answer("Добро пожаловать! Вы перешли в режим Администратора. ")
    else:
        await bot_status.BotMode.UserStatus.set()
        await message.answer("Добро пожаловать! Для просмотра команд - введите /help")


# Функция перехода в Режим Администратора / Режим Пользователя
async def cmd_login(message: types.Message, state: FSMContext):
    current_state = Dispatcher.get_current().current_state()
    state_name = await current_state.get_state()
    if message.from_user.id in ADMIN_ID and state_name == 'BotMode:UserStatus':
        await state.set_state(bot_status.BotMode.AdminStatus)
        await message.answer("Вы перешли в режим Администратора.")
    elif message.from_user.id in ADMIN_ID and state_name == 'BotMode:AdminStatus':
        await state.set_state(bot_status.BotMode.UserStatus)
        await message.answer("Вы вышли из режима Администратора.")
    else:
        await message.answer("Неизвестная команда!")


# Функция получения списка команд
async def cmd_help(message: types.Message):
    current_state = Dispatcher.get_current().current_state()
    state_name = await current_state.get_state()
    if state_name == 'BotMode:AdminStatus':
        await message.reply('''
        Доступные команды:
        /help - Функция получения списка команд
        /login - Функция перехода в Режим Администратора / Режим Пользователя
        /ontology_update - Функция обновления онтологии
        /clear - Функция очистки истории пользователя
        /emergency_brake - Функция аварийного отключения (НЕ ВВОДИТЬ ДАЖЕ РАДИ ИНТЕРЕСА!!!)
        ''')
    else:
        await message.reply('''
        Доступные команды:
        /help - Функция получения списка команд
        /rate <текст> - Функция оставления отзыва
        /error <текст> - Функция сообщение об ошибке
        /clear - Функция очистки истории диалога
        ''')


# Функция для обработки обычных сообщений
async def cmd_echo(message: types.Message):
    await message.reply('''
    Вы являетесь не определенным пользователем.
    Введите команду /start, чтобы мы могли вас определить.
    ''')


# Регистрация всех команд в хендлер
def register_hamdlers_other(dp: Dispatcher):
    dp.register_message_handler(cmd_start, state='*', commands='start')
    dp.register_message_handler(cmd_login, state='*', commands='login')
    dp.register_message_handler(cmd_help, state='*', commands='help')
    dp.register_message_handler(cmd_echo, state=None)
