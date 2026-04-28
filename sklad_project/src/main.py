import sys
from db import init_db
from services import add_product, update_product_stock, create_order, update_order_status
from reports import show_products_with_suppliers, show_orders_full_info, show_low_stock_report

def main():
    print("=" * 50)
    print("      СИСТЕМА УПРАВЛЕНИЯ СКЛАДОМ v1.0")
    print("=" * 50)

    # Инициализация БД при запуске
    init_db()

    while True:
        print("\n" + "-" * 40)
        print("ГЛАВНОЕ МЕНЮ:")
        print("1. 📋 Показать все товары (с поставщиками)")
        print("2. 📦 Показать все заказы (детально)")
        print("3. ⚠️  Товары с низким остатком")
        print("4. ➕ Добавить новый товар")
        print("5. 📝 Обновить остаток товара")
        print("6. 🛒 Создать новый заказ")
        print("7. 🔄 Изменить статус заказа")
        print("0. ❌ Выход")
        print("-" * 40)

        choice = input("Ваш выбор: ").strip()

        if choice == "1":
            show_products_with_suppliers()

        elif choice == "2":
            show_orders_full_info()

        elif choice == "3":
            threshold = input("Минимальный остаток (по умолчанию 5): ").strip()
            if threshold:
                try:
                    show_low_stock_report(int(threshold))
                except ValueError:
                    print("Ошибка: введите число")
            else:
                show_low_stock_report(5)

        elif choice == "4":
            print("\n--- Добавление товара ---")
            name = input("Название товара: ").strip()
            if not name:
                print("Ошибка: название не может быть пустым")
                continue

            try:
                price = float(input("Цена: "))
                stock = int(input("Количество на складе: "))
                cat_id = input("ID категории (1-5, Enter если нет): ").strip()
                sup_id = input("ID поставщика (1-5, Enter если нет): ").strip()

                cat_id = int(cat_id) if cat_id else None
                sup_id = int(sup_id) if sup_id else None

                add_product(name, price, stock, cat_id, sup_id)
            except ValueError:
                print("Ошибка: неверный формат числа")

        elif choice == "5":
            print("\n--- Обновление остатка ---")
            try:
                pid = int(input("ID товара: "))
                new_qty = int(input("Новое количество: "))
                update_product_stock(pid, new_qty)
            except ValueError:
                print("Ошибка: введите числа")

        elif choice == "6":
            print("\n--- Создание заказа ---")
            items = []
            while True:
                try:
                    pid = input("ID товара (0 - закончить): ").strip()
                    if pid == "0":
                        break
                    qty = int(input("Количество: "))
                    items.append((int(pid), qty))
                except ValueError:
                    print("Ошибка ввода")

            if items:
                create_order(items)
            else:
                print("Заказ не создан: нет товаров")

        elif choice == "7":
            print("\n--- Изменение статуса заказа ---")
            try:
                oid = int(input("ID заказа: "))
                print("Доступные статусы: новый, в обработке, отправлен, доставлен, отменён")
                status = input("Новый статус: ").strip().lower()
                update_order_status(oid, status)
            except ValueError:
                print("Ошибка: ID заказа должно быть числом")

        elif choice == "0":
            print("\nЗавершение работы. До свидания!")
            sys.exit()

        else:
            print("Ошибка: введите число из списка.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nПрограмма остановлена пользователем.")