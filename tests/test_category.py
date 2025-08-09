import unittest
from app.user import User
from app.category import Category
from app.databasemanager import DatabaseManager

TEST_DB = "test_marketplace.db"


class TestCategory(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Configurarea inițială a testelor - de obicei pentru conexiuni la DB sau alte configurări globale."""
        cls.db_manager = DatabaseManager(TEST_DB)
        cls.db_manager.execute_query("DELETE FROM users")
        cls.db_manager.execute_query("DELETE FROM categories")
        cls.db_manager.execute_query("DELETE FROM sqlite_sequence WHERE name='categories'")
        # Creează un user admin
        cls.admin = User(username="adminuser", email="adminuser@example.com", password="pass1234",
                         first_name="admin_first_name",
                         last_name="admin_last_name", address="adminaddress", city="admincity",
                         postal_code="admin_postal_code", country="admincountry", db_manager=cls.db_manager)
        cls.admin.save_to_db()
        cls.category = Category("Test Category", "Test Description", db_manager=cls.db_manager)



    def test_save_to_db(self):
        """Verifică dacă o categorie este salvată corect în baza de date."""
        self.db_manager.execute_query("DELETE FROM categories WHERE name = ?", (self.category.name,))
        self.category.save_to_db()
        result = self.db_manager.fetch_data("SELECT * FROM categories WHERE name = ?", (self.category.name,))
        self.assertEqual(len(result), 1)  # Trebuie să fie exact 1 categorie cu acest nume
        self.assertEqual(result[0][1], self.category.name)  # Verificăm dacă numele corespunde


    def test_category_exists(self):
        """Verifică dacă funcția category_exists funcționează corect."""
        self.assertTrue(Category.category_exists("Test Category"))
        self.assertFalse(Category.category_exists("Nonexistent Category"))


    def test_update_category(self):
        """Verifică dacă o categorie poate fi actualizată corect."""
        self.category.save_to_db()
        self.category.update(new_name="Updated Category", new_description="Updated Description")
        result = self.db_manager.fetch_data("SELECT * FROM categories WHERE name = ?", ("Updated Category",))
        self.assertEqual(result[0][1], "Updated Category")
        self.assertEqual(result[0][2], "Updated Description")


    def test_delete_category(self):
        """Verifică dacă o categorie poate fi ștearsă corect."""
        self.category.save_to_db()
        self.category.delete()
        result = self.db_manager.fetch_data("SELECT * FROM categories WHERE name = ?", (self.category.name,))
        self.assertEqual(len(result), 0)  # Categoria nu trebuie să mai existe


    @classmethod
    def tearDownClass(cls):
        """Curățenie după execuția testelor - elimină datele din baza de date dacă este necesar."""
        cls.db_manager.execute_query( "DELETE FROM categories WHERE name IN (?, ?)", ("Test Category", "Updated Category"))


if __name__ == "__main__":    
    unittest.main()
