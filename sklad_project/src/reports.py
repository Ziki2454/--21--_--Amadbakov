from db import get_connection

def show_products_with_suppliers():
    """Отчёт 1: Товары с поставщиками и категориями"""
    query = """
        SELECT 
            p.product_id,
            p.name AS product_name,
            p.price,
            p.stock_quantity,
            c.name AS category_name,
            s.name AS supplier_name,
            s.phone AS supplier_phone
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.category_id
        LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
        ORDER BY p.product_id
    """
    try:
        with get_connection() as conn:
            rows = conn.execute(query).fetchall()

        if not rows:
            print("\n[!] Товары отсутствуют.")
            return

        print("\n" + "=" * 100)
        print(f"{'ID':<4} | {'ТОВАР':<25} | {'ЦЕНА':<10} | {'ОСТАТОК':<8} | {'КАТЕГОРИЯ':<15} | {'ПОСТАВЩИК':<20}")
        print("-" * 100)
        for row in rows:
            print(f"{row['product_id']:<4} | {row['product_name']:<25} | {row['price']:<10.2f} | {row['stock_quantity']:<8} | {row['category_name'] or 'НЕТ':<15} | {row['supplier_name'] or 'НЕТ':<20}")
        print("=" * 100)
    except Exception as e:
        print(f"Ошибка отчёта: {e}")

def show_orders_full_info():
    """Отчёт 2: Детальная информация по заказам (с суммами)"""
    query = """
        SELECT 
            o.order_id,
            o.order_date,
            o.status,
            p.name AS product_name,
            oi.quantity,
            oi.price_at_order,
            (oi.quantity * oi.price_at_order) AS item_total
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.product_id
        ORDER BY o.order_id, oi.order_item_id
    """
    try:
        with get_connection() as conn:
            rows = conn.execute(query).fetchall()

        if not rows:
            print("\n[!] Заказы отсутствуют.")
            return

        current_order = None
        order_total = 0

        for row in rows:
            if current_order != row['order_id']:
                if current_order is not None:
                    print(f"  ИТОГО ПО ЗАКАЗУ: {order_total:.2f} руб.")
                    print("-" * 70)
                current_order = row['order_id']
                order_total = 0
                print(f"\n📦 ЗАКАЗ №{row['order_id']} | {row['order_date']} | СТАТУС: {row['status']}")
                print(f"{'Товар':<30} | {'Кол-во':<8} | {'Цена':<10} | {'Сумма':<10}")
                print("-" * 70)

            item_sum = row['item_total']
            order_total += item_sum
            print(f"{row['product_name']:<30} | {row['quantity']:<8} | {row['price_at_order']:<10.2f} | {item_sum:<10.2f}")

        # Последний заказ
        print(f"  ИТОГО ПО ЗАКАЗУ: {order_total:.2f} руб.")
        print("=" * 70)
    except Exception as e:
        print(f"Ошибка отчёта: {e}")

def show_low_stock_report(threshold=5):
    """Отчёт 3: Товары с низким остатком (менее threshold)"""
    query = "SELECT name, stock_quantity FROM products WHERE stock_quantity < ? ORDER BY stock_quantity"
    try:
        with get_connection() as conn:
            rows = conn.execute(query, (threshold,)).fetchall()

        if not rows:
            print(f"\n✓ Все товары в наличии (остаток >= {threshold} шт.)")
            return

        print(f"\n⚠️ ТОВАРЫ С ОСТАТКОМ МЕНЕЕ {threshold} ШТ.:")
        print("-" * 50)
        for row in rows:
            print(f"  {row['name']:<35} -> {row['stock_quantity']} шт.")
        print("-" * 50)
    except Exception as e:
        print(f"Ошибка отчёта: {e}")