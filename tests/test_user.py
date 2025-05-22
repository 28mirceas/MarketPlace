import os
import sqlite3
import unittest
from app.user import User
from app.databasemanager import DatabaseManager
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

TEST_DB = "test_marketplace.db"


class TestUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db_manager = DatabaseManager(TEST_DB)
        cls.user = User(username="testuser", email="testuser@example.com", password="testpass", first_name="test_first_name",
                        last_name="test_last_name", address="testaddress", city="testcity",postal_code="test_postal_code",country="testcountry")

    def test_save_to_db(self):
        """Verifică dacă un user este salvat corect în baza de date."""
        self.user.save_to_db()
        result = self.db_manager.fetch_data("SELECT * FROM users WHERE username = ?", (self.user.username,))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], self.user.username)  # presupunem username pe poziția 1

    def test_user_exists(self):
        """Verifică dacă metoda user_exists funcționează corect."""
        self.assertTrue(User.user_exists("testuser"))
        self.assertFalse(User.user_exists("nonexistentuser"))

    def test_update_user(self):
        """Verifică dacă un user poate fi actualizat corect."""
        self.user.save_to_db()
        self.user.update(new_email="updated@example.com")
        result = self.db_manager.fetch_data("SELECT * FROM users WHERE username = ?", ("testuser",))
        self.assertEqual(result[0][2], "updated@example.com")  # email pe poziția 2

    def test_delete_user(self):
        """Verifică dacă un user poate fi șters corect."""
        self.user.save_to_db()
        self.user.delete()
        result = self.db_manager.fetch_data("SELECT * FROM users WHERE username = ?", (self.user.username,))
        self.assertEqual(len(result), 0)

    @classmethod
    def tearDownClass(cls):
        cls.db_manager.execute_query("DELETE FROM users WHERE username = ?", ("testuser",))


if __name__ == "__main__":
    unittest.main()