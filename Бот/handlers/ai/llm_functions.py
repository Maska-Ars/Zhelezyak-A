from openai import OpenAI


# Класс для работы с LLM-моделью
class LLMModel:
    def __init__(self):
        self.client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

    # Функция для обработки сообщений с вопросом по характеристикам
    def request_3(self, question: str, info: str, history: list) -> str:
        pre = '''You are a expert ai in computer components.
        Please answer in Russian and only in Russian and \
        do not answer in any other language. This is very important, \
        make sure to only answer in Russian. Ответь только на русском!!!
        '''
        pre += 'У тебя есть следующая информация про объект:\n'
        pre += info
        pre += 'Ответь на следующий вопрос, используя только данную информацию:\n'
        pre += question

        completion = self.client.chat.completions.create(
            model="QuantFactory/Meta-Llama-3-8B-Instruct-GGUF",
            messages=history+[
                {"role": "system", "content": "Справочная информация про комплектующие пк."},
                {"role": "user", "content": pre}
            ],
            temperature=0.7,
        )
        return completion.choices[0].message.content

    # Функция для обработки сообщений с вопросом по характеристикам
    def request_1(self, question: str, info: str, history: list) -> str:
        pre = '''You are a expert ai in computer components. Please answer in Russian and only in Russian and \
        do not answer in any other language. This is very important, \
        make sure to only answer in Russian. Ответь только на русском!!!
        '''
        pre += 'У тебя есть следующий список объектов:\n'
        pre += info
        pre += 'Ответь на следующий вопрос, используя только данную информацию:\n'
        pre += question

        completion = self.client.chat.completions.create(
            model="QuantFactory/Meta-Llama-3-8B-Instruct-GGUF",
            messages=history+[
                {"role": "system", "content": "Справочная информация про комплектующие пк."},
                {"role": "user", "content": pre}
            ],
            temperature=0.7,
        )
        return completion.choices[0].message.content
