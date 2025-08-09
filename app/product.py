#Aplicatie-Marketplace
from user import User
from category import Category
from .base_entity import BaseEntity

class Product(BaseEntity):
    logged_in_user = None  # Variabilă de clasă pentru a reține userul care este logat

    def __init__(self, name, price, description, stock_count=0, category_id=None, id_=None,db_manager=None):
        super().__init__()
        self.id = id_  # ← Salvăm și ID-ul produsului
        self.name = name
        self.price = price
        self.description = description
        self.stock_count = stock_count
        self.category_id = category_id
        self.db_manager = db_manager


    def save_to_db(self):
        query = '''INSERT INTO products(name, price, description, stock_count, category_id) VALUES(?, ?, ?, ?, ?)'''
        params = (self.name, self.price, self.description, self.stock_count, self.category_id)
        self.db_manager.execute_query(query,params)

        # Obține id-ul inserat
        result = self.db_manager.fetch_data("SELECT id FROM products WHERE name = ?", (self.name,))
        if result:
            self.id = result[0][0]
            print(f"Produsul '{self.name}' a fost adăugat în categoria cu ID-ul {self.category_id}!")


    @staticmethod
    def create_from_input(category_id = None):
        temp = BaseEntity()  # Folosirea unei instante temporare
        while True:
            name = input("Introduceți numele produsului pe care doriti sa-l adaugati: ").strip()
            if not name:
                print("Numele produsului nu poate fi gol!")
                continue
            break
        while True:
            price = int(input("Introduceti pretul produsului: "))
            if not price:
                print("Pretul produsului nu poate fi gol!")
                continue
            break
        description = input("Introduceți descrierea produsului: ")
        print("Selecteaza categoria pentru produsul pe care urmeaza sa-l adaugi in baza de date!")
        categories = []
        if category_id is None:
            categories = Category.get_all_categories()
            if not categories:
                print("Nu există categorii disponibile! Adaugă mai întâi o categorie.")
                return
        while True:
            try:
                category_id = int(input("Introdu ID-ul categoriei: "))
                if any(cat[0] == category_id for cat in categories):
                    break
                else:
                    print("ID invalid! Alege un ID din lista de mai sus.")
            except ValueError:
                print("Te rog să introduci un număr valid.")

        # Calculăm noul stock_count pentru această categorie
        query = "SELECT COUNT(*) FROM products WHERE category_id = ?"
        result = temp.db_manager.fetch_data(query, (category_id,))
        stock_count = result[0][0] + 1  # Auto-incrementăm

        return Product(name, price, description, stock_count, category_id)


    @staticmethod
    def add_product():
        """Permite adăugarea unei produs doar dacă utilizatorul este logat ca administrator."""
        if not User.admin_login():
            print("Acces permis doar administratorului!")
            return

        Product.list_products()

        product = Product.create_from_input()
        product.save_to_db()
        Product.list_products()


    @staticmethod
    def list_products():
        temp = BaseEntity()  # Folosirea unei instante temporare
        """Returnează o listă cu toate produsele din baza de date."""
        query = "SELECT * FROM products"
        products = temp.db_manager.fetch_data(query)
        if not products:
            print("Nu există produse disponibile!")
            return None
        print("\nProduse disponibile:")
        for product in products:
            print(f"ID: {product[0]} | Name: {product[1]} | Price: {product[2]} | "
                  f"Description: {product[4]} | Stock: {product[3]} | CategoryId: {product[5]}")

        return products


    @staticmethod
    def read_product(product_id=None):
        temp = BaseEntity()  # Folosirea unei instante temporare
        """Afișează un anumit produs din baza de date."""
        query = "SELECT * FROM products" #Afiseaza toate produsele
        products = temp.db_manager.fetch_data(query)
        if not products:
            print("Nu există produse în baza de date.")
            return
        print("\nProduse disponibile:")
        for product in products:
            print(f"ID: {product[0]} | Name: {product[1]}")
        if product_id is None:  # Dacă ID-ul nu este furnizat, îl cerem de la utilizator
            try:
                product_id = int(input("Introdu ID-ul produsului: "))
            except ValueError:
                print("Te rog să introduci un număr valid.")
                return
        query2 = "SELECT * FROM products WHERE id = ?"
        params = (product_id,)
        result = temp.db_manager.fetch_data(query2, params)
        if result:
            product = result[0]
            print(f"\nDetalii produs:\n"
                  f"ID: {product[0]} | Name: {product[1]} | Price: {product[2]} | "
                  f"Description: {product[3]} | Stock: {product[4]} | CategoryId: {product[5]}")
        else:
            print("Produsul nu a fost găsit!")


    def update(self, new_name=None, new_price=None, new_description=None, new_stock_count=None):
        """Actualizează parametrii produsului dacă sunt furnizate valori noi."""
        if new_name:
            self.name = new_name
        if new_price:
            self.price = new_price
        if new_description:
            self.description = new_description
        if new_stock_count:
            self.stock_count = new_stock_count

        query = "UPDATE products SET name = ?, price = ?, description = ?, stock_count = ? WHERE id = ?"
        self.db_manager.execute_query(query, (self.name, self.price, self.description, self.stock_count, self.id))
        print(f"Produsul '{self.name}' a fost actualizat!")
        Product.list_products()


    @staticmethod
    def update_product():
        if not User.admin_login():
            print("Acces permis doar administratorului!")
            return
        Product.list_products()
        print("Doriți să faceți update la un produs?")
        product = Product.get_product_by_id()
        if product:
            new_name = input("Introduceți noul nume al produsului (lăsați gol pentru a păstra același): ").strip()
            # Verificăm prețul
            while True:
                try:
                    new_price = input("Introduceți noul preț al produsului (lăsați gol pentru a păstra același): ").strip()
                    if new_price:
                        new_price = int(new_price)
                        if new_price <= 0:
                            print("Prețul trebuie să fie un număr pozitiv!")
                            continue
                    break
                except ValueError:
                    print("Te rog să introduci un preț valid!")
            new_description = input("Introduceți noua descriere a produsului (lăsați gol pentru a păstra aceeași): ").strip()
            # Verificăm stocul
            while True:
                try:
                    new_stock_count = input("Introduceți noul stoc al produsului (lăsați gol pentru a păstra același): ").strip()
                    if new_stock_count:
                        new_stock_count = int(new_stock_count)
                        if new_stock_count < 0:
                            print("Stocul nu poate fi negativ!")
                            continue
                    break
                except ValueError:
                    print("Te rog să introduci un număr valid pentru stoc!")

            # Actualizăm produsul folosind metoda de instanță
            product.update(new_name, new_price, new_description, new_stock_count)
        else:
            print("Produsul nu a fost găsit!")


    @staticmethod
    def get_product_by_id(db_manager=None):
        temp = BaseEntity(db_manager=db_manager)  # Folosim baza de date de test, dacă e transmisă
        # Cerem utilizatorului să introducă Id-ul produsului
        product_id = int(input("Introduceți Id-ul produsului: ").strip())

        # Căutăm produsul în baza de date
        query = "SELECT * FROM products WHERE id = ?"
        result = temp.db_manager.fetch_data(query, (product_id,))

        if result:
            id_, name, price, description, stock_count, category_id = result[0]
            return Product(name, price, description, stock_count, category_id, id_)
        else:
            print(f"Produsul cu ID-ul'{product_id}' nu a fost găsit!.")
            return None


    def delete(self):
        """Șterge produsul din baza de date."""
        query = "DELETE FROM products WHERE id = ?"
        self.db_manager.execute_query(query, (self.id,))
        print(f"Produsul '{self.name}' a fost ștears!")


    @staticmethod
    def delete_product():
        if not User.admin_login():
            print("Acces permis doar administratorului!")
            return

        Product.list_products()

        print("Doriti sa stergeti un produs?")
        prod = Product.get_product_by_id()

        if prod:
            prod.delete()  # Apelăm metoda delete() pe obiectul găsit
        else:
            print("Produsul nu a fost găsit!")

        Product.list_products()  # Afișăm lista actualizată de produse

# Exemplu de utilizare
#if __name__ == "__main__":

    # prod1 = Product("Audi A4",12000,"Se adauga un Audi A4")
    #Product.add_product()
    #Product.list_products()
    #Product.delete_product()
    #Product.update_product()

    #db_manager.close()  # Închidem conexiunea la final




