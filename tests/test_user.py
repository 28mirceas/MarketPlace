import os
import sys
import unittest
from app.user import User
from app.databasemanager import DatabaseManager
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

TEST_DB = "test_marketplace.db"


class TestUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db_manager = DatabaseManager(TEST_DB)
        cls.admin = User(username="adminuser", email="adminuser@example.com", password="pass1234", first_name="admin_first_name",
                        last_name="admin_last_name", address="adminaddress", city="admincity",postal_code="admin_postal_code",country="admincountry", db_manager=cls.db_manager)
        cls.user1 = User(username="testuser1", email="testuser1@example.com", password="pass1234",
                        first_name="test_first_name",
                        last_name="test_last_name", address="testaddress", city="testcity",
                        postal_code="test_postal_code", country="testcountry", db_manager=cls.db_manager)
        cls.user2 = User(username="testuser2", email="testuser2@example.com", password="pass1234",
                        first_name="test_first_name",
                        last_name="test_last_name", address="testaddress", city="testcity",
                        postal_code="test_postal_code", country="testcountry", db_manager=cls.db_manager)


    def test_save_to_db(self):
        """Verifică dacă un user a fost salvat corect în baza de date."""
        self.db_manager.execute_query("DELETE FROM users WHERE email = ?", (self.admin.email,))
        self.admin.save_to_db()
        result = self.db_manager.fetch_data("SELECT * FROM users WHERE username = ?", (self.admin.username,))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], self.admin.username)  # presupunem username pe poziția 1


    def test_update_user(self):
        """Verifică dacă un user poate fi actualizat corect."""
        self.db_manager.execute_query("DELETE FROM users WHERE email = ?", (self.user2.email,))
        self.user2.save_to_db()
        self.user2.update(new_email="updated@example.com")
        result = self.db_manager.fetch_data("SELECT * FROM users WHERE username = ?", ("testuser2",))
        self.assertEqual(result[0][2], "updated@example.com")  # email pe poziția 2


    def test_delete_user(self):
        """Verifică dacă un user poate fi șters corect."""
        self.db_manager.execute_query("DELETE FROM users WHERE username = ?", (self.user2.username,))
        self.user2.save_to_db()
        self.user2.delete()
        result = self.db_manager.fetch_data("SELECT * FROM users WHERE username = ?", (self.user2.username,))
        self.assertEqual(len(result), 0)


    @classmethod
    def tearDownClass(cls):
        cls.db_manager.execute_query("DELETE FROM users")


if __name__ == "__main__":   
    unittest.main()
