from aiogram.dispatcher.filters.state import State, StatesGroup


# Класс состояний (Админ и Юзер)
class BotMode(StatesGroup):
    AdminStatus = State()
    UserStatus = State()
