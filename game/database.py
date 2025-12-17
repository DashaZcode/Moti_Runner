"""Модуль database - работа с базой данных результатов.

Содержит функции для сохранения, получения и очистки результатов игры
в PostgreSQL базе данных.
"""

import psycopg2


def save_score(name, score):
    """Сохраняет результат игры в базу данных.

    Args:
        name (str): Имя игрока.
        score (int): Количество очков.

    Returns:
        bool: True если сохранение успешно, иначе False.
    """
    try:
        conn = psycopg2.connect("host=localhost dbname=moti_game user=postgres password=11111")
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id SERIAL PRIMARY KEY,
                name TEXT,
                score INTEGER
            )
        """)

        cur.execute("INSERT INTO scores (name, score) VALUES (%s, %s)",
                    (str(name), int(score)))

        conn.commit()
        cur.close()
        conn.close()

        print(f"Сохранено: {name} = {score}")
        return True

    except Exception as e:
        print(f"Ошибка БД: {e}")
        return False


def get_all_scores():
    """Получает все результаты из базы данных, отсортированные по убыванию.

    Returns:
        list: Список кортежей (name, score) с результатами.
    """
    try:
        conn = psycopg2.connect("host=localhost dbname=moti_game user=postgres password=11111")
        cur = conn.cursor()

        # Используем правильные имена колонок
        cur.execute("SELECT name, score FROM scores ORDER BY score DESC")
        results = cur.fetchall()

        cur.close()
        conn.close()

        return results

    except Exception as e:
        print(f"Ошибка чтения: {e}")
        return []


def clear_all_scores():
    """Очищает все записи из таблицы результатов.

    Returns:
        bool: True если очистка успешна, иначе False.
    """
    try:
        conn = psycopg2.connect("host=localhost dbname=moti_game user=postgres password=11111")
        cur = conn.cursor()

        cur.execute("DELETE FROM scores")
        conn.commit()

        cur.close()
        conn.close()

        print("Таблица очищена")
        return True

    except Exception as e:
        print(f"Ошибка очистки: {e}")
        return False