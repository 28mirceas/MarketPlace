import unittest
from unittest.mock import patch
from app.order import Order
from app.databasemanager import DatabaseManager



class TestOrder(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = DatabaseManager("test_marketplace.db")
        cls.db.execute_query("DELETE FROM orders")
        cls.db.execute_query("DELETE FROM order_items")
        cls.db.execute_query("DELETE FROM categories")
        cls.db.execute_query("DELETE FROM products")
        cls.db.execute_query("DELETE FROM users")

        # Creăm un user,o categorie si un produs pentru teste
        cls.db.execute_query("INSERT INTO users (username, password) VALUES (?, ?)", ("test_user", "password"))
        cls.user_id = cls.db.fetch_data("SELECT id FROM users WHERE username = ?", ("test_user",))[0][0]
        cls.db.execute_query("INSERT INTO categories (name, description) VALUES (?, ?)", ("Electrocasnice", "Test"))
        cls.category_id = cls.db.fetch_data("SELECT id FROM categories WHERE name = ?", ("Electrocasnice",))[0][0]
        cls.db.execute_query("INSERT INTO products (name, price, description, stock, category_id) VALUES (?, ?, ?, ?, ?)",
                             ("Televizor", 1500, "Smart TV", 10, cls.category_id))
        cls.product_id = cls.db.fetch_data("SELECT id FROM products WHERE name = ?", ("Televizor",))[0][0]

    def test_1_save_order(self):
        order = Order("2025-05-13", self.user_id)
        order_id = order.save_to_db()

        result = self.db.fetch_data("SELECT * FROM orders WHERE id = ?", (order_id,))
        self.assertTrue(result)
        self.assertEqual(result[0][1], "2025-05-13")  # Verificăm data comenzii

    @patch('builtins.input', return_value='2025-05-13')
    def test_2_create_from_input(self, mock_input):
        # Testăm metoda create_from_input
        order = Order.create_from_input()
        self.assertIsInstance(order, Order)
        self.assertEqual(order.order_date, "2025-05-13")
        self.assertEqual(order.user_id, self.user_id)

    @patch('builtins.input', side_effect=['2025-05-13', '1', '2'])
    def test_3_add_order(self, mock_input):
        # Testăm metoda add_order
        Order.add_order()

        result = self.db.fetch_data("SELECT * FROM order_items WHERE order_id = (SELECT max(id) FROM orders)")
        self.assertTrue(result)
        self.assertEqual(result[0][1], 2)  # Cantitatea introdusă în input

    def test_4_list_orders(self):
        # Testăm metoda list_orders
        orders = Order.list_orders()
        self.assertIsInstance(orders, list)

    @patch('builtins.input', side_effect=['1', '2025-05-14'])
    def test_5_update_order(self, mock_input):
        # Testăm actualizarea unei comenzi
        order = Order.get_order_by_id(self.user_id)
        order.update(new_order_date="2025-05-14")

        updated_order = self.db.fetch_data("SELECT order_date FROM orders WHERE id = ?", (order.id,))
        self.assertEqual(updated_order[0][0], "2025-05-14")

    @patch('builtins.input', return_value='1')
    def test_6_delete_order(self, mock_input):
        # Testăm ștergerea unei comenzi
        order = Order.get_order_by_id(self.user_id)
        order.delete()

        deleted_order = self.db.fetch_data("SELECT * FROM orders WHERE id = ?", (order.id,))
        self.assertFalse(deleted_order)

    @classmethod
    def tearDownClass(cls):
        cls.db.execute_query("DELETE FROM orders")
        cls.db.execute_query("DELETE FROM order_items")
        cls.db.execute_query("DELETE FROM categories")
        cls.db.execute_query("DELETE FROM products")
        cls.db.execute_query("DELETE FROM users")
        cls.db.close()


if __name__ == "__main__":
    unittest.main()