import sqlite3
from db import get_connection

# ========== CRUD для товаров ==========
def add_product(name, price, stock_quantity, category_id, supplier_id):
    """Добавление нового товара"""
    query = """
        INSERT INTO products (name, price, stock_quantity, category_id, supplier_id)
        VALUES (?, ?, ?, ?, ?)
    """
    try:
        with get_connection() as conn:
            conn.execute(query, (name, price, stock_quantity, category_id, supplier_id))
            conn.commit()
        print(f"✓ Товар '{name}' добавлен на склад.")
    except sqlite3.IntegrityError as e:
        print(f"Ошибка: неверный category_id или supplier_id. ({e})")
    except sqlite3.Error as e:
        print(f"Ошибка БД: {e}")

def update_product_stock(product_id, new_quantity):
    """Обновление остатков товара"""
    query = "UPDATE products SET stock_quantity = ? WHERE product_id = ?"
    try:
        with get_connection() as conn:
            conn.execute(query, (new_quantity, product_id))
            conn.commit()
        print(f"✓ Остаток товара ID={product_id} обновлён до {new_quantity} шт.")
    except sqlite3.Error as e:
        print(f"Ошибка БД: {e}")

def delete_product(product_id):
    """Удаление товара (если нет в заказах)"""
    query = "DELETE FROM products WHERE product_id = ?"
    try:
        with get_connection() as conn:
            conn.execute(query, (product_id,))
            conn.commit()
        print(f"✓ Товар ID={product_id} удалён.")
    except sqlite3.IntegrityError:
        print("Ошибка: нельзя удалить товар, который есть в заказах.")
    except sqlite3.Error as e:
        print(f"Ошибка БД: {e}")

# ========== Предметная логика ==========
def create_order(product_ids_with_quantities):
    """
    Создание нового заказа.
    product_ids_with_quantities: список кортежей [(product_id, quantity), ...]
    """
    try:
        with get_connection() as conn:
            # 1. Создаём заказ
            conn.execute("INSERT INTO orders (status) VALUES ('новый')")
            order_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

            total_cost = 0
            # 2. Добавляем позиции и проверяем остатки
            for product_id, quantity in product_ids_with_quantities:
                # Получаем текущую цену и остаток
                row = conn.execute(
                    "SELECT price, stock_quantity FROM products WHERE product_id = ?",
                    (product_id,)
                ).fetchone()

                if not row:
                    raise Exception(f"Товар ID={product_id} не найден")

                if row['stock_quantity'] < quantity:
                    raise Exception(f"Недостаточно товара ID={product_id} (есть {row['stock_quantity']}, нужно {quantity})")

                # Добавляем позицию
                conn.execute(
                    "INSERT INTO order_items (order_id, product_id, quantity, price_at_order) VALUES (?, ?, ?, ?)",
                    (order_id, product_id, quantity, row['price'])
                )

                # Уменьшаем остаток
                conn.execute(
                    "UPDATE products SET stock_quantity = stock_quantity - ? WHERE product_id = ?",
                    (quantity, product_id)
                )

                total_cost += row['price'] * quantity

            conn.commit()
            print(f"✓ Заказ №{order_id} создан на сумму {total_cost:.2f} руб.")
            return order_id

    except Exception as e:
        print(f"Ошибка при создании заказа: {e}")
        return None

def update_order_status(order_id, new_status):
    """Изменение статуса заказа (предметная логика)"""
    valid_statuses = ['новый', 'в обработке', 'отправлен', 'доставлен', 'отменён']
    if new_status not in valid_statuses:
        print(f"Ошибка: статус должен быть одним из {valid_statuses}")
        return

    query = "UPDATE orders SET status = ? WHERE order_id = ?"
    try:
        with get_connection() as conn:
            conn.execute(query, (new_status, order_id))
            conn.commit()
        print(f"✓ Статус заказа №{order_id} изменён на '{new_status}'")
    except sqlite3.Error as e:
        print(f"Ошибка БД: {e}")