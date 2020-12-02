import os

import psycopg2
from psycopg2.errors import OperationalError

DATABASE = os.getenv('DATABASE')
USER = os.getenv('POSTGRES_USER')
PASSWORD = os.getenv('POSTGRES_PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')


def connect_to_database():
    """Подключение к postgresql. Возвращает объект подключения"""
    try:

        connection = psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT
        )
        return connection
    except OperationalError as e:
        pass


def execute_selection_query(query: str) -> list:
    """Выполняет запрос query, который получает данные из базы данных.
     Возвращает list с результатами.
     """
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return result


def execute_change_query(query: str) -> None:
    """Выполняет запрос query, который изменяет базу данных."""
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()
