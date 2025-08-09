import unittest
from unittest.mock import patch
from app.user import User
from app.order import Order
from app.databasemanager import DatabaseManager
from app.category import Category
from app.product import Product

TEST_DB = "test_marketplace.db"

class TestOrder(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_manager = DatabaseManager("test_marketplace.db")
        cls.db_manager.execute_query("DELETE FROM orders")
        cls.db_manager.execute_query("DELETE FROM order_items")
        cls.db_manager.execute_query("DELETE FROM categories")
        cls.db_manager.execute_query("DELETE FROM products")
        cls.db_manager.execute_query("DELETE FROM users")


        # Creăm un user pentru teste
        cls.user = User(username="testuser", email="testuser@example.com", password="pass1234",
                         first_name="user_first_name",
                         last_name="user_last_name", address="useraddress", city="usercity",
                         postal_code="user_postal_code", country="usercountry", db_manager=cls.db_manager)
        cls.user.save_to_db()
        cls.user_id = cls.db_manager.fetch_data("SELECT id FROM users WHERE username = ?", ("testuser",))[0][0]
        # Linia urmatoare este necesara pentru ca userul creat mai sus sa fie logat
        User.logged_in_user = cls.user_id
        #cls.user.id = cls.user_id

        # Adăugăm o categorie pentru teste
        cls.category = Category("Electrocasnice", "Test Electrocasnice", db_manager=cls.db_manager)
        cls.category.save_to_db()
        cls.category_id = cls.db_manager.fetch_data("SELECT id FROM categories WHERE name = ?", ("Electrocasnice",))[0][0]

        # Adăugăm un produs asociat categoriei
        cls.product = Product(name="Televizor", description="Televizor 4K", price=1000.0, category_id=cls.category_id,
                              db_manager=cls.db_manager)
        cls.product.save_to_db()
        cls.product_id = cls.db_manager.fetch_data("SELECT id FROM products WHERE name = ?", ("Televizor",))[0][0]

        #Adaugam o comanda asociata produsului
        order = Order("2025-08-07", cls.user_id, db_manager=cls.db_manager)
        cls.order_id = order.save_to_db()

        cls.db_manager.execute_query(
            "INSERT INTO order_items (quantity, total_price, order_id, product_id) VALUES (?, ?, ?, ?)",
            (2, 2000, cls.order_id, cls.product_id)
        )

    def test_1_save_order(self):
        result = self.db_manager.fetch_data("SELECT * FROM orders WHERE id = ?", (self.order_id,))
        self.assertTrue(result)
        self.assertEqual(result[0][1], "2025-08-07")  # Verificăm data comenzii


    @patch('builtins.input', return_value='2025-05-13')
    def test_2_create_from_input(self, mock_input):
        User.logged_in_user = self.user_id  # asigurăm că userul este logat
        order = Order.create_from_input()  # nu trimiți db_manager aici
        self.assertIsInstance(order, Order)
        self.assertEqual(order.order_date, "2025-05-13")
        self.assertEqual(order.user_id, self.user_id)
        User.logged_in_user = None  # resetăm după test


    def test_3_add_order(self):
        User.logged_in_user = self.user
        with patch('app.order.Order.select_product', return_value=self.product_id), \
             patch('builtins.input', side_effect=['2025-05-13', '2']):  # dată + cantitate

             Order.add_order(db_manager=self.db_manager)

             result = self.db_manager.fetch_data(
                 "SELECT * FROM order_items ORDER BY id DESC LIMIT 1"
             )
             print("\n>>> Ultima comandă din tabelul orders:")
             print(result)

             self.assertTrue(result)
             self.assertEqual(result[0][1], 2)  # Cantitatea introdusă în input

             User.logged_in_user = None


    def test_4_list_orders(self):
        # Testăm metoda list_orders
         orders = Order.list_orders(db_manager=self.db_manager)
         self.assertIsInstance(orders, list)
         self.assertGreater(len(orders), 0)


    @patch('builtins.input')
    def test_5_update_order(self, mock_input):
        User.logged_in_user = self.user_id

        # Simulăm inputul: ID-ul comenzii existente + noua dată
        mock_input.side_effect = [str(self.order_id), '2025-05-14']

        # DEBUGGING block
        # print("DEBUG: self.user_id =", self.user_id)
        # print("DEBUG: self.order_id =", self.order_id)
        # print("DEBUG: User.logged_in_user =", User.logged_in_user)

        orders = self.db_manager.fetch_data("SELECT id, order_date, user_id FROM orders")
        print("DEBUG: orders in DB =", orders)

        order = Order.get_order_by_id(self.user_id, self.db_manager)
        order.update(new_order_date="2025-05-14")

        updated_order = self.db_manager.fetch_data("SELECT order_date FROM orders WHERE id = ?", (self.order_id,))
        self.assertEqual(updated_order[0][0], "2025-05-14")


    @patch('builtins.input')
    def test_6_delete_order(self, mock_input):
        mock_input.side_effect = [str(self.__class__.order_id), 'y']

        order = Order.get_order_by_id(self.user_id, self.db_manager)
        self.assertIsNotNone(order, f"Comanda cu ID {self.__class__.order_id} nu a fost găsită pentru ștergere")
        order.delete()

        deleted_order = self.db_manager.fetch_data("SELECT * FROM orders WHERE id = ?", (order.id,))
        self.assertFalse(deleted_order)
        

    @classmethod
    def tearDownClass(cls):
        cls.db_manager.execute_query("DELETE FROM orders")
        cls.db_manager.execute_query("DELETE FROM order_items")
        cls.db_manager.execute_query("DELETE FROM categories")
        cls.db_manager.execute_query("DELETE FROM products")
        cls.db_manager.execute_query("DELETE FROM users")
        cls.db_manager.close()


if __name__ == "__main__":
    unittest.main()
