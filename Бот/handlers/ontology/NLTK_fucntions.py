from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import sent_tokenize


# Удаление лишних слов
def delete_prepositions(text: str) -> str:
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('russian'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(filtered_tokens)


# Приведение всех слов до их леммы
def reduction_to_roots(text: str) -> str:
    stemmer = SnowballStemmer('russian')
    tokens = word_tokenize(text)
    lemmatized_words = [stemmer.stem(word) for word in tokens]
    return ' '.join(lemmatized_words)


# функция генерации всех последовательных сочетаний слов
def generate_combinations(s: str) -> list:
    words = s.split()
    combinations = []

    for i in range(1, len(words) + 1):
        for j in range(len(words) - i + 1):
            combinations.append("*".join(words[j:j + i]))

    return combinations


# Разбиение на предложения
def reduction_to_sentenses(s: str) -> list:
    sentence_tokens = sent_tokenize(s)
    symbols = '.,!?'
    for i in range(0, len(sentence_tokens)):
        if sentence_tokens[i][-1] in symbols:
            sentence_tokens[i] = sentence_tokens[i][:-1:]

    return sentence_tokens