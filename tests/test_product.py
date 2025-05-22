import unittest
from app.product import Product
from app.databasemanager import DatabaseManager


class TestProduct(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = DatabaseManager("test_marketplace.db")
        cls.db.execute_query("DELETE FROM products")  # Curățăm tabela la început

        # Adăugăm o categorie necesară produsului
        cls.db.execute_query("INSERT INTO categories (name, description) VALUES (?, ?)", ("Electrocasnice", "Test"))
        cls.category_id = cls.db.fetch_data("SELECT id FROM categories WHERE name = ?", ("Electrocasnice",))[0][0]

    def test_1_save_to_db(self):
        product = Product("Televizor", 1500, "Smart TV", 10, self.category_id)
        product.save_to_db()

        result = self.db.fetch_data("SELECT * FROM products WHERE name = ?", ("Televizor",))
        self.assertTrue(result)
        self.assertEqual(result[0][1], "Televizor")

    def test_2_get_product_by_id(self):
        product_data = self.db.fetch_data("SELECT * FROM products WHERE name = ?", ("Televizor",))[0]
        product_id = product_data[0]

        product = Product.get_product_by_id(product_id)
        self.assertIsInstance(product, Product)
        self.assertEqual(product.name, "Televizor")

    def test_3_update_product(self):
        product = self.db.fetch_data("SELECT * FROM products WHERE name = ?", ("Televizor",))[0]
        product_obj = Product(product[1], product[2], product[3], product[4], product[5], product[0])

        product_obj.update(new_price=1800)
        updated = self.db.fetch_data("SELECT price FROM products WHERE id = ?", (product_obj.id,))
        self.assertEqual(updated[0][0], 1800)

    def test_4_delete_product(self):
        product = self.db.fetch_data("SELECT * FROM products WHERE name = ?", ("Televizor",))[0]
        product_obj = Product(product[1], product[2], product[3], product[4], product[5], product[0])

        product_obj.delete()
        deleted = self.db.fetch_data("SELECT * FROM products WHERE id = ?", (product_obj.id,))
        self.assertFalse(deleted)

    @classmethod
    def tearDownClass(cls):
        cls.db.execute_query("DELETE FROM products")
        cls.db.execute_query("DELETE FROM categories")
        cls.db.close()

if __name__ == "__main__":
    unittest.main()