import logging
import handlers.user_private
import handlers.other
import handlers.admin_private
from aiogram import executor
from handlers.user_private import db
from create_bot import dp

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
handlers.other.register_hamdlers_other(dp)
handlers.admin_private.register_hamdlers_admin_private(dp)
handlers.user_private.register_handlers_user_private(dp)

# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=db.create_db())
