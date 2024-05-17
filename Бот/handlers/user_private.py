import bot_status
from aiogram import types
from aiogram import Dispatcher
from copy import deepcopy
import threading

from handlers.DataBase.DataBase_functions import DataBase

from handlers.ai.llm_functions import LLMModel
from handlers.ai.classification_functions import AIClassifier

from handlers.ontology.onto_functions import Onto
from handlers.ontology.NLTK_fucntions import reduction_to_sentenses

from handlers.Thread_functions import acl
# Объявление и/или создание БД пользователей
db = DataBase()

# Объявление LLM-модели
classifier = AIClassifier()

# Объявление LLM-модели
llm = LLMModel()

# Объявление онтологии
onto = Onto()
onto.read_onto('handlers/ontology/PCIron.owl')


# Функция отправки отзыва
async def cmd_rate(message: types.Message):
    message.text = message.text.replace('/rate ', '')
    db.insert_comment(message.from_user.id, message.text)
    await message.reply('Мы рады каждому вашему отзыву! Нельзя стать лучше без критики!')


# Функция отправки сообщения об ошибке
async def cmd_error(message: types.Message):
    message.text = message.text.replace('/error ', '')
    db.insert_error(message.from_user.id, message.text)
    await message.reply('Получается, вы нашли ошибку? Благодарим за помощь в улучшении работы продукта!')


# Функция очистки истории пользователя
async def cmd_clear(message: types.Message):
    db.delete_requests(message.from_user.id)
    await message.reply('Предыдущие запросы удалены')


# Функция получения ответа на запрос
async def cmd_echo(message: types.Message):
    if message.text[0] == '/':
        await message.answer('Простите, но я впервые слышу о такой команде!')
    else:
        history = db.select_last_requests(message.from_user.id)
        history_for_llm = []
        for i in range(0, len(history)):
            history_for_llm += [
                {"role": "assistant",
                "content": history[i][1]},
                {"role": "user",
                "content": history[i][0]}
            ]
        ans = ''
        for sent in reduction_to_sentenses(message.text.lower()):
            typ = classifier.classify_message(sent)
            print(typ)
            # Обрабатвыет все сообщения
            if typ == 0:
                answer = llm.request_1(sent, 'Используй более ранние сообщения', history_for_llm)
                ans += answer
                await message.reply(answer)
            # Обрабатывает поиск по описанию
            elif typ == 1:
                info = onto.search_object_by_description(sent)
                answer = llm.request_1(sent, info, history_for_llm)
                ans += answer
                await message.reply(answer)
            # Обрабатывает вопросы про сборку пк
            elif typ == 2:
                await message.reply('''К сожалению я не могу собрать ПК.
                                    Но я могу оценить вашу собственную сборку''')
            # Обрабатывает поиск по имени
            elif typ == 3:
                info = onto.search_object_by_name(sent)
                answer = llm.request_3(sent, info, history_for_llm)
                ans += answer
                await message.reply(answer)

        db.insert_request(message.from_user.id, message.text, ans)

# Регистрация всех команд в хендлер
def register_handlers_user_private(dp: Dispatcher):
    dp.register_message_handler(cmd_rate, state=bot_status.BotMode.UserStatus, commands='rate')
    dp.register_message_handler(cmd_error, state=bot_status.BotMode.UserStatus, commands='error')
    dp.register_message_handler(cmd_clear, state=bot_status.BotMode.UserStatus, commands='clear')
    dp.register_message_handler(cmd_echo, state=bot_status.BotMode.UserStatus)
