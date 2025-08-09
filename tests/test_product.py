import unittest
from app.user import User
from app.category import Category
from app.product import Product
from app.databasemanager import DatabaseManager
from unittest.mock import patch

TEST_DB = "test_marketplace.db"

class TestProduct(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_manager = DatabaseManager("test_marketplace.db")
        cls.db_manager.execute_query("DELETE FROM users") # Curățăm tabela la început
        cls.db_manager.execute_query("DELETE FROM categories")
        cls.db_manager.execute_query("DELETE FROM products")
        # Creează un user admin necesar pentru adaugarea unui produs
        cls.admin = User(username="adminuser", email="adminuser@example.com", password="pass1234",
                         first_name="admin_first_name",
                         last_name="admin_last_name", address="adminaddress", city="admincity",
                         postal_code="admin_postal_code", country="admincountry", db_manager=cls.db_manager)
        cls.admin.save_to_db()
        # Adăugăm o categorie necesară produsului
        cls.category = Category("Electrocasnice", "Test Electrocasnice", db_manager=cls.db_manager)
        cls.category.save_to_db()
        cls.category_id = cls.db_manager.fetch_data("SELECT id FROM categories WHERE name = ?", ("Electrocasnice",))[0][0]
        # Adăugăm un produs asociat categoriei
        cls.product = Product("Televizor", 1500, "Smart TV", 10, cls.category_id, db_manager=cls.db_manager)
        cls.product.save_to_db()
        Product.db_manager = cls.db_manager


    def test_1_save_to_db(self):
        """Verifică dacă un produs este salvat corect în baza de date."""
        self.db_manager.execute_query("DELETE FROM products WHERE name = ?", (self.product.name,))
        self.product.save_to_db()
        result = self.db_manager.fetch_data("SELECT * FROM products WHERE name = ?", (self.product.name,))
        self.assertEqual(len(result), 1)  # Trebuie să fie exact 1 produs cu acest nume
        self.assertEqual(result[0][1], self.product.name)  # Verificăm dacă numele corespunde


    def test_2_get_product_by_id(self):
        # Curățăm produsul (dacă există deja)
        self.db_manager.execute_query("DELETE FROM products WHERE name = ?", (self.product.name,))
        # Salvăm produsul
        self.product.save_to_db()
        # Obținem ID-ul nou salvat
        product_data = self.db_manager.fetch_data("SELECT * FROM products WHERE name = ?", ("Televizor",))[0]
        product_id = product_data[0]
        # Simulăm inputul utilizatorului în metoda get_product_by_id()
        with patch("builtins.input", return_value=str(product_id)):
            product = Product.get_product_by_id(db_manager=self.db_manager)
        # Verificăm rezultatul
        self.assertIsInstance(product, Product)
        self.assertEqual(product.name, "Televizor")


    def test_3_update_product(self):
        # Curățăm produsul (dacă există deja)
        self.db_manager.execute_query("DELETE FROM products WHERE name = ?", (self.product.name,))
        # Salvăm produsul
        self.product.save_to_db()
        product = self.db_manager.fetch_data("SELECT * FROM products WHERE name = ?", ("Televizor",))[0]
        product_obj = Product(product[1], product[2], product[3], product[4], product[5], product[0], db_manager=self.db_manager)

        product_obj.update(new_price=1800)
        updated = self.db_manager.fetch_data("SELECT price FROM products WHERE id = ?", (product_obj.id,))
        self.assertEqual(updated[0][0], 1800)
        

    def test_4_delete_product(self):
        product = self.db_manager.fetch_data("SELECT * FROM products WHERE name = ?", ("Televizor",))[0]
        product_obj = Product(product[1], product[2], product[3], product[4], product[5], product[0],  db_manager=self.db_manager)

        product_obj.delete()
        deleted = self.db_manager.fetch_data("SELECT * FROM products WHERE id = ?", (product_obj.id,))
        self.assertFalse(deleted)


    @classmethod
    def tearDownClass(cls):
        cls.db_manager.execute_query("DELETE FROM products")
        cls.db_manager.execute_query("DELETE FROM categories")
        cls.db_manager.close()

if __name__ == "__main__":
    unittest.main()
