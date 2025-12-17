from game.database import get_all_scores, clear_all_scores


def main():
    """Инструмент для работы с базой данных"""
    print("1. Показать все результаты")
    print("2. Очистить все результаты")
    print("3. Выход")

    choice = input("\nВыберите действие: ")

    if choice == "1":
        scores = get_all_scores()
        if scores:
            print("\n РЕЗУЛЬТАТЫ")
            for name, score in scores:
                print(f"{name}: {score} очков")
        else:
            print("Таблица пуста")

    elif choice == "2":
        confirm = input("Удалить все записи? (y/n): ")
        if confirm.lower() == 'y':
            if clear_all_scores():
                print("Таблица очищена")
            else:
                print("Ошибка очистки")

    elif choice == "3":
        print("Выход")


if __name__ == "__main__":
    main()