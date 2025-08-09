import os
import sqlite3
import unittest
from app.databasemanager import DatabaseManager


TEST_DB = "test_marketplace.db"


class TestDatabaseManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Se execută o singură dată la începutul suitei de teste."""
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)  # Acum ștergem baza de date înainte să facem DatabaseManager
        cls.db_manager = DatabaseManager(TEST_DB)

    def setUp(self):
        """Se execută înainte de fiecare test."""
        # Ștergem toate datele din toate tabelele
        self.db_manager.execute_query("DELETE FROM order_items", ())
        self.db_manager.execute_query("DELETE FROM orders", ())
        self.db_manager.execute_query("DELETE FROM products", ())
        self.db_manager.execute_query("DELETE FROM categories", ())
        self.db_manager.execute_query("DELETE FROM users", ())

    # @classmethod
    # def tearDownClass(cls):
    #     """Se execută o singură dată după toate testele."""
    #     cls.db_manager.close()
    #     if os.path.exists(TEST_DB):
    #         os.remove(TEST_DB)

    def test_tables_are_created(self):
        """Verificăm dacă tabelele au fost create corect."""
        connection = sqlite3.connect(TEST_DB)
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = sorted([table[0] for table in cursor.fetchall()])
        connection.close()

        expected_tables = sorted(["users", "categories", "products", "orders", "order_items"])
        self.assertEqual(tables, expected_tables)

    # def test_execute_query_insert_and_select(self):
    #     """Testăm dacă putem insera și selecta date folosind execute_query."""
    #     insert_query = "INSERT INTO categories (name, description) VALUES (?, ?)"
    #     self.db_manager.execute_query(insert_query, ("Electronice", "Gadgeturi și echipamente"))
    #
    #     select_query = "SELECT * FROM categories WHERE name = ?"
    #     result = self.db_manager.fetch_data(select_query, ("Electronice",))
    #
    #     self.assertEqual(len(result), 1)
    #     self.assertEqual(result[0][1], "Electronice")
    #     self.assertEqual(result[0][2], "Gadgeturi și echipamente")
    #
    # def test_fetch_data_returns_correct_values(self):
    #     """Testăm dacă fetch_data returnează datele corecte."""
    #     self.db_manager.execute_query(
    #         "INSERT INTO categories (name, description) VALUES (?, ?)",
    #         ("Carti", "Literatura si fictiune")
    #     )
    #
    #     result = self.db_manager.fetch_data("SELECT * FROM categories WHERE name = ?", ("Carti",))
    #
    #     self.assertEqual(len(result), 1)
    #     self.assertEqual(result[0][1], "Carti")
    #     self.assertEqual(result[0][2], "Literatura si fictiune")


if __name__ == "__main__":
    unittest.main()

