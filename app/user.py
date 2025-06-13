#Aplicatie-Marketplace-User
from base_entity import BaseEntity


class User(BaseEntity):
    logged_in_user = None  # Variabilă de clasă pentru a reține userul care este logat

    def __init__(self, username, email, password, first_name, last_name, address, city, postal_code, country, id=None):
        super().__init__()
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.city = city
        self.postal_code = postal_code
        self.country = country


    def save_to_db(self):
        query = '''INSERT INTO users (username, email, password, first_name, last_name, address, city, postal_code, country) 
                                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        params = (self.username, self.email, self.password, self.first_name, self.last_name, self.address, self.city,
                  self.postal_code, self.country)
        self.db_manager.execute_query(query, params)
        print(f"Userul {self.username}  a fost adaugat cu succes!")


    @staticmethod
    def create_from_input():
        temp = BaseEntity() #Folosirea unei instante temporare
        while True:
            username = input("Introduceți username-ul userului pe care doriti sa-l adaugati: ").strip()
            if not username:
                print("Username-ul nu poate fi gol!")
                continue
            # Verificați dacă username-ul nu există deja în baza de date
            query1 = "SELECT username FROM users"
            users_list = temp.db_manager.execute_query(query1)
            if users_list:
                existing_users = [user[0] for user in users_list]  # Extragem doar username
                if username in existing_users:
                    print("Username existent! Încercați alt username!")
                    continue  # Se cere sa se introduca un nou username
            break
        while True:
            email = input("Introduceti email-ul userului: ")
            if not email:
                print("Email-ul userului nu poate fi gol!")
                continue
            # Verificați dacă email-ul nu există deja în baza de date
            query2 = "SELECT email FROM users"
            email_list = temp.db_manager.execute_query(query2)
            if email_list:
                existing_emails = [user[0] for user in email_list]  # Extragem doar email
                if email in existing_emails:
                    print("Email existent! Încercați alt email!")
                    continue  # Se cere sa se introduca un nou email
            break
        first_name = input("Introduceti prenumele dumneavoastra: ")
        last_name = input("Introduceti numele dumneavoastra: ")
        address = input("Introduceti adresa dumneavoastra: ")
        city = input("Introduceti orasul de resedinta: ")
        postal_code = input("Introduceti codul postal: ")
        country = input("Introduceti tara: ")
        """Verificați parola si confirmare"""
        while True:
            password = input("Introduceți parola de autentificare: ")
            confirm_password = input("Confirmați parola: ")

            if password != confirm_password:
                print("Parolele nu coincid! Încercați din nou.")
                continue  # Se cere sa se introduca parola din nou
            break
        return User(username, email, password, first_name, last_name, address, city, postal_code, country)


    @staticmethod
    def add_user():
        """Salvează utilizatorul în baza de date utilizând DatabaseManager."""
        user = User.create_from_input()
        user.save_to_db()



    @staticmethod
    def get_all_users():
        temp = BaseEntity() #Folosirea unei instante temporare
        if not User.admin_login():
            print("Acces permis doar administratorului!")
            return

        """Returnează o listă cu toți utilizatorii din baza de date."""
        query = "SELECT id, username, email, first_name, last_name FROM users"
        users_list = temp.db_manager.fetch_data(query)

        if not users_list:
            print("Nu există utilizatori în baza de date.")
            return []

        print("\nLista utilizatorilor:")
        for user in users_list:
            print(f"ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Nume: {user[3]}, Prenume: {user[4]}")

        return users_list  # Returnează lista pentru utilizare ulterioară, dacă e nevoie.


    def update(self, new_email=None, new_address=None, new_city=None, new_postal_code=None, new_country=None):
        if new_email:
            self.email = new_email
        if new_address:
            self.address = new_address
        if new_city:
            self.city = new_city
        if new_postal_code:
            self.postal_code = new_postal_code
        if new_country:
            self.country = new_country

        query = """UPDATE users SET email = ?, address = ?, city = ?, postal_code = ?, country = ? WHERE id = ?"""
        self.db_manager.execute_query(query, (self.email, self.address, self.city, self.postal_code, self.country, self.id))


    @staticmethod
    def update_user():
        temp = BaseEntity() #Folosirea unei instante temporare
        if User.logged_in_user is None:
            print("Vă rugăm să vă autentificați mai întâi.")
            if not User.user_login():
                return

        username = User.logged_in_user

        # Obținem userul logat din baza de date
        query = "SELECT * FROM users WHERE username = ?"
        result = temp.db_manager.fetch_data(query, (username,))

        if not result:
            print("Eroare: utilizatorul logat nu a fost găsit în baza de date.")
            return

        id_, username, email, password, first_name, last_name, address, city, postal_code, country = result[0]
        user = User(username, email, password, first_name, last_name, address, city, postal_code, country, id_)

        print(f"Modificați datele pentru userul logat: {username}")

        # Datele noi
        new_email = input("Introduceți noul email (lăsați gol pentru a păstra același): ").strip()
        if new_email and new_email != email:
            # Verificăm dacă emailul este deja folosit
            query = "SELECT id FROM users WHERE email = ? AND id != ?"
            result = temp.db_manager.fetch_data(query, (new_email, user.id))
            if result:
                print("Această adresă de email este deja folosită de alt user.")
                return
        else:
            new_email = email

        new_address = input("Introduceți noua adresă (gol = neschimbată): ").strip() or address
        new_city = input("Introduceți noul oraș (gol = neschimbat): ").strip() or city
        new_postal_code = input("Introduceți noul cod poștal (gol = neschimbat): ").strip() or postal_code
        new_country = input("Introduceți noua țară (gol = neschimbată): ").strip() or country

        # Actualizăm userul
        user.update(new_email, new_address, new_city, new_postal_code, new_country)
        print("Datele au fost actualizate cu succes.")


    @staticmethod
    def update_password():
        temp = BaseEntity() #Folosirea unei instante temporare
        """Actualizează parola userului logat după verificarea celei vechi."""
        if User.logged_in_user is None:
            print("Vă rugăm să vă autentificați mai întâi.")
            if not User.user_login():  # Dacă login-ul eșuează, ieșim din funcție
                return

        username = User.logged_in_user  # Folosim utilizatorul logat

        # Obține parola din baza de date
        query = "SELECT password FROM users WHERE username = ?"
        result = temp.db_manager.fetch_data(query, (username,))

        if not result or not result[0][0]:  # Verifică dacă user-ul există și are parolă validă
            print("Eroare: User inexistent sau parola nu este setată corect în baza de date!")
            return

        stored_password = result[0][0]  # Extragerea parolei din tupla

        """Userul are maxim 3 incercari de introducere a parolei!"""
        max_attempts = 3
        attempt = 0

        while attempt < max_attempts:
            old_password = input("Introduceți vechea parolă: ")

            if old_password == stored_password:
                new_password = input("Introduceți noua parolă: ").strip()
                if not new_password:
                    print("Parola nouă nu poate fi goală!")
                    return
                confirm_password = input("Confirmați noua parolă: ").strip()

                if new_password != confirm_password:
                    print("Parolele nu coincid. Parola nu a fost schimbată.")
                    return

                # Actualizăm parola în baza de date
                query = "UPDATE users SET password = ? WHERE username = ?"
                params = (new_password, username)
                temp.db_manager.execute_query(query, params)

                print(f"Parola pentru userul '{username}' a fost schimbată cu succes!")
                return
            else:
                attempt += 1
                print(f"Parola veche este incorectă! Încercare {attempt}/{max_attempts}.")

        print("Ați depășit numărul maxim de încercări! Parola nu a fost schimbată.")
        

    @staticmethod
    def get_user_by_id():
        temp = BaseEntity() #Folosirea unei instante temporare
        # Cerem admin să introducă Id-ul userului
        user_id = int(input("Introduceți Id-ul userului: ").strip())

        # Căutăm userul în baza de date
        query = "SELECT * FROM users WHERE id = ?"
        result = temp.db_manager.fetch_data(query, (user_id,))

        if result:
            id_, username, email, password, first_name, last_name, address, city, postal_code, country = result[0]
            return User(username, email, password, first_name, last_name, address, city, postal_code, country, id_)
        else:
            print(f"Userul cu ID-ul'{user_id}' nu a fost găsit!.")
            return None


    def delete(self):
        """Șterge userul din baza de date."""
        query = "DELETE FROM users WHERE id = ?"
        self.db_manager.execute_query(query, (self.id,))
        print(f"Userul a fost ștears!")


    @staticmethod
    def delete_user():
        if not User.admin_login():
            print("Acces permis doar administratorului!")
            return

        User.get_all_users()

        print("Doriti sa stergeti un user?")
        user = User.get_user_by_id()

        if user:
            user.delete()  # Apelăm metoda delete() pe obiectul găsit
        else:
            print("Userul nu a fost găsit!")

        User.get_all_users()  # Afișăm lista actualizată de useri


    @staticmethod
    def admin_login():
        temp = BaseEntity() #Folosirea unei instante temporare
        if User.logged_in_user:  # Dacă deja e logat cineva (nu e None)
            return User.logged_in_user

        admin1 = input("Introduceți username-ul administratorului: ")
        password1 = input("Introduceți parola de administrator: ")

        query1 = "SELECT username, password FROM users WHERE Id = 1"
        admin_data = temp.db_manager.fetch_data(query1)

        if not admin_data:
            print("Eroare: Nu există un administrator în baza de date!")
            return None

        admin_username, admin_password = admin_data[0]

        if admin1 == admin_username and password1 == admin_password:
            User.logged_in_user = admin_username
            print(f"Administratorul '{admin_username}' este logat!")
            return admin_username
        else:
            print("Username sau parolă incorecte!")
            return None


    @staticmethod
    def user_login():
        temp = BaseEntity() #Folosirea unei instante temporare
        """Verifică username-ul și parola și returnează user_id-ul sau None dacă autentificarea eșuează."""
        user1 = input("Introduceți username-ul: ")
        password1 = input("Introduceți parola: ")

        # Obținem doar id-ul și parola din baza de date
        query = "SELECT id, password FROM users WHERE username = ?"
        result = temp.db_manager.fetch_data(query, (user1,))

        if not result:
            print("Autentificare eșuată! Verifică datele introduse.")
            return None

        user_id, stored_password = result[0]  # Extragem datele din baza de date

        # Compară parola introdusă cu cea stocata în baza de date
        if password1 == stored_password:  # Comparăm parolele direct
            print(f"Autentificare reușită! Bine ai venit, {user1}.")
            User.logged_in_user = user_id
            # Setăm utilizatorul logat
            return user_id
        else:
            print("Autentificare eșuată! Verifică parola.")
            return None


    @staticmethod
    def user_logout():
        """Deconectează userul curent."""
        if User.logged_in_user is not None:
            print(f"Userul {User.logged_in_user} a fost deconectat.")
            User.logged_in_user = None  # Setează logged_in_user la None pentru a marca deconectarea
        else:
            print("Nici un user nu este logat.")


                    
# Exemplu de utilizare
#if __name__ == "__main__":
    # Adăugăm un utilizator nou
    #User.add_user()

    # Listăm utilizatorii
    #User.get_all_users()
    # #User.update_password()
    # #User.delete_user()
    #User.user_logout()

    #db_manager.close()  # Închidem conexiunea la final
