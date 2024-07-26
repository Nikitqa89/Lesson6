import pandas as pd
import sqlite3 as sq
import seaborn as sns
import matplotlib.pyplot as plt

# Создаем базу данных
with sq.connect('Warehouse_and_Retail_Sales.db') as wrs:
    c = wrs.cursor()

    # Создание таблицы warehouse
    c.execute('''CREATE TABLE IF NOT EXISTS warehouse (
        year INTEGER,
        month INTEGER,
        supplier TEXT,
        item_code INTEGER,
        item_description TEXT,
        item_type TEXT,
        retail_sales REAL,
        retail_transfers REAL,
        warehouse_sales REAL
        )''')

    # Открываем базу данных
    df = pd.read_csv(r'C:\\Users\User\PycharmProjects\lesson6\Warehouse_and_Retail_Sales.csv', delimiter=',')

    # Преобразуем базу в кортежи для внесения в базу данных
    data_sql = []
    for idx, row in df.iterrows():
        data_sql.append(tuple(row))

    # Вносим дааные в БД
    c.executemany("INSERT INTO warehouse VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", data_sql)

    # Выводим кол-во позиций вина при показателе розничной торговли больше 40
    c.execute("SELECT COUNT(*) FROM warehouse WHERE item_type = 'WINE' and retail_sales > 40")
    print(c.fetchall())

    # Выведем среднее кол-во складских продаж от поставщика REPUBLIC NATIONAL DISTRIBUTING CO
    c.execute("SELECT AVG(warehouse_sales) FROM warehouse WHERE supplier = 'REPUBLIC NATIONAL DISTRIBUTING CO'")
    print(c.fetchall())

# Гистограмма по продукции
plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='ITEM TYPE')
plt.title('Кол-во позиций по типам продукции')
plt.xlabel('Типы продукции')
plt.ylabel('Кол-во')
plt.grid(True)
plt.show()

