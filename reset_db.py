"""Модуль reset_db - сброс и пересоздание базы данных.

Содержит функцию для полного пересоздания базы данных игры
с таблицей для хранения результатов.
"""

import psycopg2
import sys


def reset_database():
    """Полностью пересоздает базу данных игры.

    Удаляет существующую базу данных moti_game и создает ее заново
    с таблицей scores для хранения результатов.

    Returns:
        bool: True если операция успешна, иначе False.
    """
    try:
        #Удаляем и создаем базу
        conn = psycopg2.connect("dbname=postgres user=postgres password=11111 host=localhost")
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute("DROP DATABASE IF EXISTS moti_game")
        cur.execute("CREATE DATABASE moti_game")

        cur.close()
        conn.close()

        #Создаем таблицу
        conn2 = psycopg2.connect("dbname=moti_game user=postgres password=11111 host=localhost")
        cur2 = conn2.cursor()

        cur2.execute("""
            CREATE TABLE scores (
                id SERIAL PRIMARY KEY,
                name TEXT,
                score INTEGER
            )
        """)
        conn2.commit()

        cur2.close()
        conn2.close()

        print("База данных moti_game пересоздана")
        return True

    except Exception as e:
        print(f"Ошибка: {e}")
        return False


if __name__ == "__main__":
    print("Сброс базы данных moti_game...")
    if reset_database():
        print("\nТеперь запусти игру:")
        sys.exit(0)
    else:
        sys.exit(1)