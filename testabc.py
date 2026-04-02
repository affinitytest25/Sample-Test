import sqlite3
import os
import datetime

class OrderProcessor:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            product TEXT,
            amount REAL,
            created_at TEXT
        )
        """)
        self.conn.commit()

    def add_order(self, user, product, amount):
        cursor = self.conn.cursor()
        query = f"INSERT INTO orders (user, product, amount, created_at) VALUES ('{user}', '{product}', {amount}, '{datetime.datetime.now()}')"  # ❌ SQL Injection
        cursor.execute(query)
        self.conn.commit()

    def get_orders_by_user(self, user):
        cursor = self.conn.cursor()
        query = f"SELECT * FROM orders WHERE user = '{user}'"  # ❌ SQL Injection
        cursor.execute(query)
        return cursor.fetchall()

    def delete_order(self, order_id):
        cursor = self.conn.cursor()
        cursor.execute(f"DELETE FROM orders WHERE id = {order_id}")  # ❌ Injection risk
        self.conn.commit()

    def export_orders(self):
        export_path = "exports/orders.txt"  # ❌ Directory may not exist
        with open(export_path, "w") as f:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM orders")
            for row in cursor.fetchall():
                f.write(str(row) + "\n")
        print("Orders exported")

    def import_orders(self, file_path):
        with open(file_path, "r") as f:
            for line in f:
                parts = line.strip().split(",")  # ❌ Weak parsing
                self.add_order(parts[0], parts[1], float(parts[2]))  # ❌ IndexError risk

    def calculate_total_sales(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT amount FROM orders")
        total = 0
        for row in cursor.fetchall():
            total += row[0]
        return total

    def process_refund(self, order_id):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT amount FROM orders WHERE id = {order_id}")
        result = cursor.fetchone()

        if result:
            refund_amount = result[0]
            print(f"Refunded {refund_amount}")
            self.delete_order(order_id)
        else:
            print("Order not found")

    def run(self):
        self.connect()
        self.create_table()

        while True:
            print("\n1. Add Order")
            print("2. View Orders by User")
            print("3. Delete Order")
            print("4. Export Orders")
            print("5. Import Orders")
            print("6. Total Sales")
            print("7. Refund Order")
            print("8. Exit")

            choice = input("Enter choice: ")

            if choice == "1":
                user = input("User: ")
                product = input("Product: ")
                amount = float(input("Amount: "))  # ❌ No validation
                self.add_order(user, product, amount)

            elif choice == "2":
                user = input("User: ")
                orders = self.get_orders_by_user(user)
                print(orders)

            elif choice == "3":
                order_id = input("Order ID: ")
                self.delete_order(order_id)

            elif choice == "4":
                self.export_orders()

            elif choice == "5":
                path = input("File path: ")
                self.import_orders(path)

            elif choice == "6":
                total = self.calculate_total_sales()
                print("Total Sales:", total)

            elif choice == "7":
                order_id = input("Order ID: ")
                self.process_refund(order_id)

            elif choice == "8":
                break

            else:
                print("Invalid option")


if __name__ == "__main__":
    processor = OrderProcessor("orders.db")
    processor.run()
