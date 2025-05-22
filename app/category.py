#Aplicatie-Marketplace
from databasemanager import DatabaseManager
from user import User

db_manager = DatabaseManager("baza12.db")  # Variabilă globală

class Category:
    logged_in_user = None  # Variabilă de clasă pentru a reține userul care este logat

    def __init__(self,name,description, id_=None):
        self.id = id_
        self.name = name
        self.description = description


    def save_to_db(self):
        query = '''INSERT INTO categories(name, description) VALUES(?,?)'''
        db_manager.execute_query(query,(self.name,self.description))
        print(f"Categoria '{self.name}' a fost adaugata cu succes!")


    @staticmethod
    def category_exists(name):
        query = '''SELECT * FROM categories WHERE name = ?'''
        result = db_manager.fetch_data(query, (name,))
        return len(result) > 0


    @staticmethod
    def create_from_input():
        while True:
            name = input("Introduceți numele categoriei pe care doriti sa o adaugati: ").strip()
            if not name:
                print("Numele categoriei nu poate fi gol!")
                continue
            if Category.category_exists(name):
                print("Această categorie există deja!")
                continue
            break
        description = input("Introduceți descrierea categoriei: ").strip()
        return Category(name, description)


    @staticmethod
    def add_category():
        """Permite adăugarea unei categorii doar dacă utilizatorul este logat ca administrator."""
        if not User.admin_login():
            print("Acces permis doar administratorului!")
            return
        Category.get_all_categories()
        category = Category.create_from_input()
        category.save_to_db()
        Category.get_all_categories()


    @staticmethod
    def get_all_categories():
        if not User.admin_login():
            print("Acces permis doar administratorului!")
            return
        """Returnează o listă cu toate categoriile din baza de date."""
        query = "SELECT id, name FROM categories"
        categories = db_manager.fetch_data(query)
        if not categories:
            print("Nu există categorii disponibile!")
            return None

        print("\nCategorii disponibile:")
        for cat in categories:
            print(f"ID: {cat[0]} | Nume: {cat[1]}")
        return categories


    @staticmethod
    def get_category_by_name():
        # Cerem utilizatorului să introducă numele categoriei
        category_name = input("Introduceți numele categoriei: ").strip()

        # Căutăm categoria în baza de date
        query = "SELECT id, name, description FROM categories WHERE name = ?"
        result = db_manager.fetch_data(query, (category_name,))

        if result:
            id_, name, desc = result[0]
            return Category(name, desc, id_)
        else:
            print(f"Categoria '{category_name}' nu a fost găsită.")
            return None


    def update(self, new_name=None, new_description=None):
        """Actualizează numele sau descrierea categoriei dacă sunt furnizate valori noi."""
        if new_name:
            self.name = new_name
        if new_description:
            self.description = new_description
        query = "UPDATE categories SET name = ?, description = ? WHERE id = ?"
        db_manager.execute_query(query, (self.name, self.description, self.id))
        print(f"Categoria '{self.name}' a fost actualizată.")


    @staticmethod
    def update_category():
        if not User.admin_login():
            print("Acces permis doar administratorului!")
            return
        Category.get_all_categories()
        # Căutăm categoria de actualizat
        print("Doriti sa faceti update la o categorie?")
        category = Category.get_category_by_name()
        if category:
            # Dacă categoria există, cerem noile informații
            new_name = input("Introduceți noul nume al categoriei (lăsați gol pentru a nu modifica): ").strip()
            new_description = input("Introduceți noua descriere a categoriei (lăsați gol pentru a nu modifica): ").strip()
            # Actualizăm categoria folosind metoda de instanță
            category.update(new_name, new_description)
        else:
             print(f"Categoria nu a fost gasita!")


    def delete(self):
        """Șterge categoria din baza de date."""
        query = "DELETE FROM categories WHERE id = ?"
        db_manager.execute_query(query, (self.id,))
        print(f"Categoria '{self.name}' a fost ștearsă.")


    @staticmethod
    def delete_category():
        if not User.admin_login():
            print("Acces permis doar administratorului!")
            return
        Category.get_all_categories()
        print("Doriti sa stergeti o categorie?")
        cat = Category.get_category_by_name()
        if cat:
            cat.delete()  # Apelăm metoda delete() pe obiectul găsit
        else:
            print("Categoria nu a fost găsită.")
        Category.get_all_categories()  # Afișăm lista actualizată de


# Exemplu de utilizare
#if __name__ == "__main__":
    #Adăugăm o categorie noua
    #Category.add_category()

    #Listăm categoriile
    #Category.get_all_categories()

    # Updatam o categorie
    #Category.update_category()

    #Stergem o categorie
    #Category.delete_category()

    #db_manager.close()  # Închidem conexiunea la final





