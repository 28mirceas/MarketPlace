import os
import sqlite3
import unittest
from app.category import Category
from app.databasemanager import DatabaseManager
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

TEST_DB = "test_marketplace.db"


class TestCategory(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Configurarea inițială a testelor - de obicei pentru conexiuni la DB sau alte configurări globale."""
        cls.db_manager = DatabaseManager(TEST_DB)
        cls.category = Category("Test Category", "Test Description")

    def test_save_to_db(self):
        """Verifică dacă o categorie este salvată corect în baza de date."""
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
        cls.db_manager.execute_query("DELETE FROM categories WHERE name = ?", ("Test Category",))
        cls.db_manager.execute_query("DELETE FROM categories WHERE name = ?", ("Updated Category",))

if __name__ == "__main__":
    unittest.main()