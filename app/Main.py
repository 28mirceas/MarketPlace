#Aplicatie-Marketplace-Main
import sys
from databasemanager import DatabaseManager
from user import User
from category import Category
from product import Product
from order import Order

db_manager = DatabaseManager("baza12.db")  # Variabilă globală


def show_main_menu():
    print("\nMeniu principal:")
    print("1. User Management")
    print("2. Category Management")
    print("3. Product Management")
    print("4. Order Management")
    print("5. Ieșire din program")


def user_menu():
    while True:
        print("\n[User Management]")
        print("1. Adaugă utilizator")
        print("2. Listează utilizatori")
        print("3. Logare utilizator")
        print("4. Delogare utilizator")
        print("5. Update utilizator")
        print("6. Update password")
        print("7. Stergere utilizator")
        print("8. Înapoi la meniul principal")

        option = input("Alege o opțiune: ")
        if option == '1':
            User.add_user()
        elif option == '2':
            User.get_all_users()
        elif option == '3':
            User.user_login()
        elif option == '4':
            User.user_logout()
        elif option == '5':
            User.update_user()
        elif option == '6':
            User.update_password()
        elif option == '7':
            User.delete_user()
        elif option == '8':
            break
        else:
            print("Opțiune invalidă, încearcă din nou.")


def category_menu():
    while True:
        print("\n[Category Management]")
        print("1. Adaugă categorie")
        print("2. Șterge categorie")
        print("3. Listează categorii")
        print("4. Update categorie")
        print("5. Înapoi la meniul principal")

        option = input("Alege o opțiune: ")
        if option == '1':
            Category.add_category()
        elif option == '2':
            Category.delete_category()
        elif option == '3':
            Category.get_all_categories()
        elif option == '4':
           Category.update_category()
        elif option == '5':
            break
        else:
            print("Opțiune invalidă, încearcă din nou.")


def product_menu():
    while True:
        print("\n[Product Management]")
        print("1. Adaugă produs")
        print("2. Șterge produs")
        print("3. Listează produse")
        print("4. Listează produs")
        print("5. Update produs")
        print("6. Înapoi la meniul principal")

        option = input("Alege o opțiune: ")
        if option == '1':
            Product.add_product()
        elif option == '2':
            Product.delete_product()
        elif option == '3':
            Product.list_products()
        elif option == '4':
            Product.read_product()
        elif option == '5':
            Product.update_product()
        elif option == '6':
            break
        else:
            print("Opțiune invalidă, încearcă din nou.")


def order_menu():

    while True:
        print("\n[Order Management]")
        print("1. Plasează comandă")
        print("2. Listează comenzi")
        print("3. Update comanda")
        print("4. Șterge comanda")
        print("5. Logout")
        print("6. Înapoi la meniul principal")

        option = input("Alege o opțiune: ")


        if option == '1':
            Order.add_order()

        elif option == '2':
            Order.list_orders()

        elif option == '3':
            Order.update_order()

        elif option == '4':
            Order.delete_order()

        elif option == '5':
            User.user_logout()
            print("Te-ai deconectat cu succes.")

        elif option == '6':
            break

        else:
            print("Opțiune invalidă, încearcă din nou.")


def main():
    while True:
        show_main_menu()
        option = input("Alege o opțiune (1-5): ")

        if option == '1':
            user_menu()
        elif option == '2':
            category_menu()
        elif option == '3':
            product_menu()
        elif option == '4':
            order_menu()
        elif option == '5':
            print("Ieșire din program...")
            sys.exit()
        else:
            print("Opțiune invalidă, încearcă din nou.")


# Exemplu de utilizare
if __name__ == "__main__":
    main()