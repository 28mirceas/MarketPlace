#Aplicatie-Marketplace-DatabaseManager
import sqlite3

class DatabaseManager:
   def __init__(self, db_path):
       self.connection =  sqlite3.connect(db_path)
       self.cursor = self.connection.cursor()
       self.create_tables()


   def create_tables(self):
       """Creează toate tabelele necesare în baza de date."""
       self.cursor.execute('''CREATE TABLE IF NOT EXISTS users(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT NOT NULL UNIQUE,
                   email TEXT NOT NULL UNIQUE,
                   password TEXT NOT NULL,
                   first_name TEXT NOT NULL,
                   last_name TEXT NOT NULL,
                   address TEXT,
                   city TEXT, 
                   postal_code TEXT,
                   country TEXT)''')

       self.cursor.execute('''CREATE TABLE IF NOT EXISTS categories(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL UNIQUE,
                   description TEXT)''')

       self.cursor.execute('''CREATE TABLE IF NOT EXISTS products(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL UNIQUE,       
                   price INTEGER NOT NULL,
                   stock_count INTEGER DEFAULT 0,
                   description TEXT,
                   category_id INTEGER NOT NULL,
                   FOREIGN KEY (category_id) REFERENCES categories(id))''')

       self.cursor.execute('''CREATE TABLE IF NOT EXISTS orders(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,        
                   order_date TEXT NOT NULL,
                   user_id INTEGER NOT NULL,
                   FOREIGN KEY (user_id) REFERENCES users(id))''')

       self.cursor.execute('''CREATE TABLE IF NOT EXISTS order_items(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,        
                   quantity INTEGER NOT NULL,
                   total_price FLOAT NOT NULL,
                   order_id INTEGER NOT NULL,
                   product_id INTEGER NOT NULL,
                   FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
                   FOREIGN KEY (product_id) REFERENCES products(id))''')

       self.connection.commit()


   def execute_query(self, query, params=()):
        """Execută o interogare SQL cu parametrii furnizați."""
        self.cursor.execute(query, params)
        self.connection.commit()

        # Returnează rezultatele doar pentru interogările SELECT
        if query.strip().upper().startswith("SELECT"):
            return self.cursor.fetchall()


   def fetch_data(self, query, params=()):
       """Execută o interogare SQL și returnează rezultatele."""
       self.cursor.execute(query, params)
       return self.cursor.fetchall()


   def close(self):
        """Închide conexiunea la baza de date."""
        self.cursor.close()
        self.connection.close()


# Exemplu de utilizare:
# if __name__ == "__main__":
#     db_manager = DatabaseManager("baza12.db")
#
#     #Verificare daca tabelele au fost adaugate
#     #Obține lista tabelor din baza de date
#     connection = sqlite3.connect("baza12.db")
#     cursor = connection.cursor()
#     cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
#     #
#     tables = cursor.fetchall()
#
#     # Afișează tabelele
#     print("Tabele în baza de date:")
#     for table in tables:
#         print(table[0])

    # db_manager.close()


