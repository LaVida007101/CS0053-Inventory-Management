import mysql.connector
from mysql.connector import IntegrityError
import datetime


connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="products"
)



def add_data(values):
    cursor = connection.cursor()
    prod_id, name, ini_stock, restock_level, cost_per_unit, price, inventory_date = values
    inventory_date = inventory_date.strftime('%Y-%m-%d')

    # try:
    query = "INSERT INTO product (id,name,stockCount,restockLevel,costPerUnit,price,inventoryDate) VALUES (%s,%s,%s,%s,%s,%s,%s)"

    cursor.execute(query, (prod_id, name, ini_stock, restock_level, cost_per_unit, price, inventory_date))
    connection.commit()
    # except IntegrityError as e:
    #     raise e

def get_product(id):
    cursor = connection.cursor(dictionary=True)
    query = f"SELECT * FROM product WHERE id = {id}"
    cursor.execute(query)
    
    result = cursor.fetchall()

    if result:
        return result
    else:
        return -1
    
def get_all_products():
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM product ORDER BY stockCount DESC"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()

    return rows


def update_data(values):
    cursor = connection.cursor()
    prod_id, name, ini_stock, restock_level, cost_per_unit, price = values

    query = "UPDATE product SET id = %s, name = %s, stockCount = %s, restockLevel = %s, costPerUnit = %s, price = %s WHERE ID = %s"
    cursor.execute(query, prod_id)


def get_low_product_stock():
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM product WHERE stockCount < restockLevel"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()

    return rows


def remove_data(id):
    cursor = connection.cursor()
    query = f"DELETE FROM product WHERE id = {id}"

    cursor.execute(query)
    connection.commit()


def add_sales(id, number_sold):
    cursor = connection.cursor()
    query = "INSERT INTO product_sales (id,number_sold,date) VALUES (%s,%s,%s)"

    product = get_product(id)
    product = product[0] if product != -1 else -1
    if product != -1:
        date_today = datetime.date.today()
        date_today = date_today.strftime('%Y-%m-%d')
        print(date_today)
        cursor.execute(query, (product["id"], number_sold, date_today))
        connection.commit()
        
        total_amount = product["amount_sold"] + number_sold
        query = "UPDATE product SET amount_sold = %s WHERE id = %s"
        cursor.execute(query, (total_amount, id))
        connection.commit()
        
        return 0
    else:
        return -1



def get_most_recent_sold():
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM product_sales ORDER BY id ASC"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()

    amount_sold_the_last_2_weeks = {}
    for item in rows:
        if item["id"] not in amount_sold_the_last_2_weeks:
            amount_sold_the_last_2_weeks[item["id"]] = item["number_sold"]
        else:
            date_difference = (datetime.datetime.now().date() - item["date"]).days
            if date_difference <= 30:
                amount_sold_the_last_2_weeks[item["id"]] += item["number_sold"]
    
    amount_sold_the_last_2_weeks = sorted(amount_sold_the_last_2_weeks.items(), key=lambda item: item[1], reverse=True )
    
    return amount_sold_the_last_2_weeks

