-- Включение поддержки внешних ключей
PRAGMA foreign_keys = ON;

-- Удаление таблиц (в обратном порядке зависимостей)
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS suppliers;
DROP TABLE IF EXISTS categories;

-- Таблица категорий товаров
CREATE TABLE categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT
);

-- Таблица поставщиков
CREATE TABLE suppliers (
    supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    contact_person TEXT,
    phone TEXT,
    email TEXT
);

-- Таблица товаров
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL CHECK (price >= 0),
    stock_quantity INTEGER NOT NULL DEFAULT 0 CHECK (stock_quantity >= 0),
    category_id INTEGER,
    supplier_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE SET NULL,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id) ON DELETE SET NULL
);

-- Таблица заказов
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL DEFAULT 'новый' CHECK (status IN ('новый', 'в обработке', 'отправлен', 'доставлен', 'отменён'))
);

-- Таблица позиций заказа (связь многое-ко-многим)
CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price_at_order REAL NOT NULL CHECK (price_at_order >= 0),
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE RESTRICT
);

-- =====================================================
-- НАЧАЛЬНЫЕ ДАННЫЕ (минимум 5 записей на таблицу)
-- =====================================================

-- Категории
INSERT INTO categories (name, description) VALUES
('Электроника', 'Телефоны, ноутбуки, планшеты и аксессуары'),
('Бытовая техника', 'Холодильники, стиральные машины, микроволновки'),
('Мебель', 'Столы, стулья, шкафы'),
('Канцелярия', 'Бумага, ручки, папки'),
('Спорттовары', 'Мячи, гантели, коврики');

-- Поставщики
INSERT INTO suppliers (name, contact_person, phone, email) VALUES
('ООО "ТехноПост"', 'Иванов Иван', '+7(495)123-45-67', 'info@tehnopost.ru'),
('АО "БытЭлектро"', 'Петрова Мария', '+7(812)765-43-21', 'sales@bytelectro.ru'),
('ИП "Мебельщик"', 'Сидоров Алексей', '+7(343)987-65-43', 'zakaz@mebelschik.ru'),
('ООО "КанцТорг"', 'Кузнецова Ольга', '+7(383)555-12-34', 'office@kanctorg.ru'),
('СпортМастер ЛТД', 'Смирнов Денис', '+7(499)222-33-44', 'info@sportmaster.ru');

-- Товары
INSERT INTO products (name, price, stock_quantity, category_id, supplier_id) VALUES
('Смартфон Galaxy A54', 24990.00, 15, 1, 1),
('Ноутбук IdeaPad 3', 45990.00, 8, 1, 1),
('Микроволновая печь LG', 7990.00, 12, 2, 2),
('Холодильник Bosch', 42990.00, 5, 2, 2),
('Офисный стол "Стандарт"', 5890.00, 20, 3, 3),
('Кресло компьютерное', 9990.00, 10, 3, 3),
('Бумага А4 "Снегурочка"', 349.00, 100, 4, 4),
('Набор ручек (12шт)', 299.00, 50, 4, 4),
('Гантели 5 кг (пара)', 1990.00, 25, 5, 5),
('Коврик для йоги', 1490.00, 18, 5, 5);

-- Заказы
INSERT INTO orders (order_date, status) VALUES
('2025-03-01 10:30:00', 'доставлен'),
('2025-03-05 14:15:00', 'отправлен'),
('2025-03-10 09:45:00', 'в обработке'),
('2025-03-12 16:20:00', 'новый'),
('2025-03-15 11:00:00', 'новый');

-- Позиции заказов
INSERT INTO order_items (order_id, product_id, quantity, price_at_order) VALUES
(1, 1, 2, 24990.00),
(1, 3, 1, 7990.00),
(2, 2, 1, 45990.00),
(2, 7, 3, 349.00),
(3, 5, 2, 5890.00),
(3, 6, 1, 9990.00),
(4, 4, 1, 42990.00),
(4, 8, 2, 299.00),
(5, 9, 1, 1990.00),
(5, 10, 2, 1490.00);