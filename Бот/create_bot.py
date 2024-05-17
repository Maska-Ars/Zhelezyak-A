from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from settings import TOKEN

# Объявление бота и диспетчера с хранилищем состояний
bot = Bot(TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())
