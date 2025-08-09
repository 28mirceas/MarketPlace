#Aplicatie-Marketplace
from app.user import User
from app.product import Product
from app.base_entity import BaseEntity


class Order(BaseEntity):
    logged_in_user = None  # Variabilă de clasă pentru a reține userul care este logat

    def __init__(self, order_date, user_id, id=None, db_manager=None):
        super().__init__()
        self.id = id
        self.order_date = order_date
        self.user_id = user_id
        self.db_manager = db_manager

    def save_to_db(self):
        query = '''INSERT INTO orders (order_date, user_id) VALUES (?, ?)'''
        params = (self.order_date, self.user_id)
        self.db_manager.execute_query(query, params)
        self.id = self.db_manager.cursor.lastrowid  # Salvează ID-ul comenzii
        print(f"Comanda cu ID {self.id} a fost adăugată cu succes in tabelul orders!")
        return self.id


    @staticmethod
    def create_from_input(db_manager=None):
        if User.logged_in_user is None:
            print("Nu sunteți autentificat!")
            user_id = User.user_login()
            if user_id is None:
                print("Trebuie să fii logat pentru a face o comandă!")
                return None
        else:
            user_id = User.logged_in_user.id

        order_date = input("Introduceți data comenzii (AAAA-LL-ZZ): ").strip()

        # Folosește db_manager primit sau creează unul temporar
        if db_manager is None:
            temp = BaseEntity()
            db_manager = temp.db_manager

        return Order(order_date, user_id, db_manager=db_manager)


    @staticmethod
    def add_order(db_manager=None):
        # Folosirea unei instanțe temporare doar dacă nu e furnizat db_manager
        if db_manager is None:
            temp = BaseEntity()
            db_manager = temp.db_manager
        else:
            temp = BaseEntity(db_manager=db_manager)

        # Trimite db_manager la create_from_input()
        order = Order.create_from_input(db_manager=db_manager)
        if order is None:
            return

        order_id = order.save_to_db()
        if order_id is None:
            print("Eroare la salvarea comenzii.")
            return

        # Selectează produsul
        product_id = Order.select_product()
        if product_id is None:
            return

        try:
            quantity = int(input("Introduceți cantitatea pentru produsul selectat: "))
        except ValueError:
            print("Cantitate invalidă.")
            return

        # Obține prețul produsului selectat
        query = "SELECT price FROM products WHERE id = ?"
        result = db_manager.fetch_data(query, (product_id,))
        if not result:
            print("Produsul nu există.")
            return

        total_price = result[0][0] * quantity

        # Inserăm în order_items
        insert_query = '''
            INSERT INTO order_items (quantity, total_price, order_id, product_id)
            VALUES (?, ?, ?, ?)
        '''
        params = (quantity, total_price, order_id, product_id)
        db_manager.execute_query(insert_query, params)

        # Afișăm ce s-a inserat
        order_item = db_manager.fetch_data(
            "SELECT * FROM order_items WHERE order_id = ?", (order_id,)
        )
        print("\n>>> Conținutul din order_items pentru ultima comandă:")
        print(order_item)
        # print(f"OrderID: {order_item[0]} | Data: {order_item[1]} | "
        #       f"Produs: {order_item[2]} | Preț: {order_item[3]} | "
        #       f"Cantitate: {order_item[4]} | Total: {order_item[5]}")

        print(f"Produsul {product_id} a fost adăugat cu succes în comanda {order_id}!")
        Order.list_orders(db_manager=db_manager)


    @staticmethod
    def select_product():
        """Afișează produsele și permite utilizatorului să selecteze un ID valid."""
        products = Product.list_products()
        if not products:
            print("Nu există produse disponibile! Adaugă mai întâi un produs.")
            return None

        while True:
            try:
                product_id = int(input("Introdu ID-ul produsului in comanda: "))
                if any(product[0] == product_id for product in products):
                    return product_id
                else:
                    print("ID invalid! Alege un ID din lista de mai sus.")
            except ValueError:
                print("Te rog să introduci un număr valid.")


    @staticmethod
    def list_orders2(db_manager=None):
        # Folosirea unei instante temporare
        if db_manager is None:
            temp = BaseEntity()
            db_manager = temp.db_manager
        else:
            temp = BaseEntity(db_manager=db_manager)
        print("Pentru a vedea comenzile dumneavoastră trebuie să fiți autentificat!")

        if User.logged_in_user is None:
            print("Nu sunteți autentificat!")
            user_id = User.user_login()
            if user_id is None:
                print("Eroare: trebuie să fii autentificat pentru a vedea comenzile!")
                return
        else:
            user_id = User.logged_in_user

        # Selectăm comenzile asociate cu user_id
        query = '''SELECT o.id, o.order_date, p.name, p.price, oi.quantity, oi.total_price
                   FROM orders o 
                   JOIN users u ON o.user_id = u.id 
                   JOIN order_items oi ON o.id = oi.order_id
                   JOIN products p ON oi.product_id = p.id 
                   WHERE o.user_id = ?'''
        params = (user_id,)
        orders = temp.db_manager.fetch_data(query, params)

        if not orders:
            print("Nu ai făcut nicio comandă!")
        else:
            print(f"Comenzile userului cu ID={user_id} sunt:")
            for order in orders:
                print(f"OrderID: {order[0]} | Data: {order[1]} | "
                      f"Produs: {order[2]} | Preț: {order[3]} | "
                      f"Cantitate: {order[4]} | Total: {order[5]}")

    @staticmethod
    def list_orders(db_manager=None):
        if User.logged_in_user is None:
            print("Trebuie să fii logat pentru a vedea comenzile tale.")
            return

        if db_manager is None:
            temp = BaseEntity()
            db_manager = temp.db_manager

        query = '''
            SELECT oi.id, oi.quantity, oi.total_price, oi.order_id, oi.product_id
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.id
            WHERE o.user_id = ?
        '''
        #results = db_manager.fetch_data(query, (User.logged_in_user.id,))
        results = db_manager.fetch_data(query, (User.logged_in_user,))
        print("\nVizualizare comenzi:")
        if results:
            for row in results:
                print(row)
        else:
            print("Nu ai făcut nicio comandă!")


    def update(self, new_order_date=None):
        """Actualizează parametrii comenzii dacă sunt furnizate valori noi."""
        if new_order_date:
            self.order_date = new_order_date

        query = "UPDATE orders SET order_date = ? WHERE id = ?"
        self.db_manager.execute_query(query, (self.order_date, self.id))
        print(f"Comanda '{self.id}' a fost actualizata!")
        Order.list_orders()


    @staticmethod
    def update_order():
        if User.logged_in_user is None:
            print("Vă rugăm să vă autentificați mai întâi.")
            user_id = User.user_login()
            if user_id is None:
                return
        else:
            user_id = User.logged_in_user

        username = User.logged_in_user
        Order.list_orders()
        print("Doriți să modificati o comanda?")
        order = Order.get_order_by_id(user_id)
        if order:
            new_order_date = input("Introduceți noua data a comenzii (lăsați gol pentru a păstra aceeasi data): ").strip()
            # Actualizăm comanda folosind metoda de instanță
            order.update(new_order_date, )
        else:
            print("Comanda nu a fost găsita!")


    @staticmethod
    def get_order_by_id(user_id, db_manager):
        temp = BaseEntity(db_manager=db_manager)  # Folosirea unei instante temporare
        while True:
            user_input = input("Introduceți ID-ul comenzii (sau apăsați Enter pentru a anula): ").strip()

            if user_input == '':
                print("Anulat de utilizator!")
                return None

            if not user_input.isdigit():
                print("ID-ul trebuie să fie un număr! Încercați din nou.")
                continue

            order_id = int(user_input)

            # Căutăm comanda cu acel ID și user_id
            query = "SELECT * FROM orders WHERE id = ? AND user_id = ?"
            result = temp.db_manager.fetch_data(query, (order_id, user_id))

            if result:
                id_, order_date, user_id = result[0]
                return Order(order_date, user_id, id_, db_manager)  # <-- Aici db_manager în plus
            else:
                print(f"Comanda cu ID-ul '{order_id}' nu a fost găsită sau nu aparține userului curent.")

    def delete(self):
        """Șterge comanda din baza de date."""
        query = "DELETE FROM orders WHERE id = ?"
        self.db_manager.execute_query(query, (self.id,))
        print(f"Comanda cu ID-ul '{self.id}' a fost ștearsa!")


    @staticmethod
    def delete_order():
        if User.logged_in_user is None:
            print("Vă rugăm să vă autentificați mai întâi.")
            user_id = User.user_login()
            if user_id is None:
                return
        else:
            user_id = User.logged_in_user

        Order.list_orders()

        print("Doriți să ștergeți o comandă?")
        order = Order.get_order_by_id(user_id)  # transmitem user_id

        if order:
            confirm = input(f"Sigur doriți să ștergeți comanda cu ID-ul {order.id}? (y/n): ").strip().lower()
            if confirm == 'y':
                order.delete()
            else:
                print("Ștergerea a fost anulată.")
        else:
            print("Nu s-a selectat nicio comandă pentru ștergere.")

        Order.list_orders()


# Exemplu de utilizare
#if __name__ == "__main__":
    #Order.add_order()
    #Order.list_orders()
    #Order.update_order()
    #Order.delete_order()
    #db_manager.close()  # Închidem conexiunea la final
