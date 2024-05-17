from sqlite3 import connect  # Для подключения к базе данных MySQL

# file = 'user_informations.db' Название файла бд


class DataBase:

    file = 'handlers/DataBase/user_informations.db'
    story_maxsize = 5

    def __init__(self, file: str = 'handlers/DataBase/user_informations.db'):
        self.file = file

    # Функция создания пустой базы данных
    def create_db(self):

        connection = connect(self.file)
        cursor = connection.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS requests (
        id INTEGER,
        time TIMESTAMP,
        req TEXT,
        ans TEXT
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
        id INTEGER,
        time TIMESTAMP,
        comment TEXT,
        req TEXT,
        ans TEXT
        )
        ''')

        connection.commit()
        connection.close()
        return None

    # Функция добавления запроса пользователя в историю сообщений
    def insert_request(self, user_id: int, request: str, answer: str):

        connection = connect(self.file)
        cursor = connection.cursor()

        cursor.execute(f'''SELECT * FROM requests
        WHERE id={user_id}
        ''')
        story = cursor.fetchall()

        if len(story) < self.story_maxsize:
            cursor.execute(f'''
            INSERT INTO requests (id, time, req, ans)
            VALUES ('{user_id}', CURRENT_TIMESTAMP, '{request}', '{answer}')
            ''')

        elif len(story) == self.story_maxsize:
            cursor.execute(f'''
            UPDATE requests
            SET id={user_id}, time=CURRENT_TIMESTAMP, req='{request}', ans='{answer}'
            WHERE time = (SELECT MIN(time) from requests)
            ''')

        connection.commit()
        connection.close()
        return None

    # Функция добавления комментария
    def insert_comment(self, user_id: int, comment: str):

        connection = connect(self.file)
        cursor = connection.cursor()

        cursor.execute(f'''
        INSERT INTO comments (id, time, comment)
        VALUES ('{user_id}', CURRENT_TIMESTAMP, '{comment}')
        ''')

        connection.commit()
        connection.close()
        return None

    # Функция добавления ошибки
    def insert_error(self, user_id: int, comment: str):

        connection = connect(self.file)
        cursor = connection.cursor()

        cursor.execute(f'''
                INSERT INTO comments (id, time, comment)
                VALUES ('{user_id}', CURRENT_TIMESTAMP, '{comment}')
                ''')

        connection.commit()
        connection.close()
        return None

    # Функция извлечения всех данных(история, отзывы, жалобы)
    def select_all(self):
        return self.select_requests(), self.select_comments(), self.select_errors()

    # Функция извлечения комментариев(id, time comment)
    def select_comments(self):
        connection = connect(self.file)
        cursor = connection.cursor()

        cursor.execute('''
        SELECT id, time, comment FROM comments
        WHERE req IS NULL
        ORDER BY time DESC
        ''')
        comments = cursor.fetchall()

        connection.close()

        return comments

    # Функция извлечения жалоб на ошибки(id, time, comment, request, answer)
    def select_errors(self):
        connection = connect(self.file)
        cursor = connection.cursor()

        cursor.execute('''
        SELECT * FROM comments
        WHERE req > ''
        ORDER BY time DESC
        ''')
        errors = cursor.fetchall()

        connection.close()

        return errors

    # Функция извлечения всех запросов пользователей(id, time, request, answer)
    def select_requests(self):
        connection = connect(self.file)
        cursor = connection.cursor()

        cursor.execute('''
        SELECT * FROM requests
        ORDER BY time DESC
        ''')
        requests = cursor.fetchall()

        connection.close()
        return requests

    # Функция извлечения последних запросов пользователя
    def select_last_requests(self, user_id: int):
        connection = connect(self.file)
        cursor = connection.cursor()

        cursor.execute(f'''
        SELECT req, ans FROM requests
        WHERE id={user_id}
        ORDER BY time
        ''')
        requests = cursor.fetchall()

        connection.close()
        return requests

    # Функция извлечения всей сохраненной информации от пользователя(запросы, комментарии, ошибки)
    def select_userinfo(self, user_id: int):
        connection = connect(self.file)
        cursor = connection.cursor()

        cursor.execute(f'''
        SELECT * FROM requests
        WHERE id={user_id}
        ORDER BY time
        ''')
        requests = cursor.fetchall()

        cursor.execute(f'''
                SELECT * FROM comments
                WHERE id={user_id} AND req = ''
                ORDER BY time
                ''')
        comments = cursor.fetchall()

        cursor.execute(f'''
                SELECT * FROM errors
                WHERE id={user_id} AND req > ''
                ORDER BY time
                ''')
        errors = cursor.fetchall()

        connection.close()
        return requests, comments, errors

    # Функция удаления запросов пользователя
    def delete_requests(self, user_id: int):

        connection = connect(self.file)
        cursor = connection.cursor()

        cursor.execute(f'''
        DELETE FROM requests
        WHERE id={user_id}
        ''')

        connection.commit()
        connection.close()

        return None

    # Функция удаления всех запросов пользователей
    def delete_all_requests(self):

        connection = connect(self.file)
        cursor = connection.cursor()

        cursor.execute(f'''
        DELETE FROM requests
        ''')

        connection.commit()
        connection.close()

        return None

