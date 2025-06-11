# MarketPlace

## Descriere

Acest proiect reprezintă o aplicație simpla de tip magazin-online implementată în limbajul de programare Python. Aplicatia permite contruirea unui baze de date si efectuarea de operatiuni operatiuni de tip CRUD cu elementele  bazei de date.

## Utilizare

1.	Pentru inceput recomand descarcarea aplicatiei din Git si rularea la nivel local într-un mediu Python de preferat PyCharm 2024.3.2.
2.	Se va merge in fisierul app/databasemanager.py si se va rula acest fisier pentru a se crea baza de date cu tabelele aferente. Am ales “baza12.bd” ca nume pentru baza de data creata. Se poate alege orice nume pentru baza de date cu conditia ca el sa fie modificat in celelate fisiere din folderul app. 
3.	Urmatorul pas este creerea unui user. Acest lucru se va face direct din fisierul “Main.py” la sectiunea “User Management”.
    FOARTE IMPORTANT: Primul user creat are drepturi de Administrator - numai el poate sterge alti useri creati, categorii, produse si comenzi pentru produsele aferente. 
5.	Pentru a ieși din program, se merge in meniul principal la optiunea “5. Iesire din program”.

## Comenzi pentru administrarea magazinului  

1.	Pentru User se merge la sectiunea User Management si avem optiunile: adauga user, modifica user, schimba parola, stergere user, login si logout, listare useri;
2.	Pentru Categorie se merge la Category Management si avem optiunile: adauga categorie, modifica o categorie, sterge o categorie si listeaza categoriile existente; 
3.	Pentru Produs se merge pe sectiunea Product Management si avem optiunile: adauga produs, modifica un produs, sterge un produs si listeaza produsele existente;
4.	Pentru Comenzi se merge pe sectiunea Order Management si avem optiunile: adauga o comanda, modifica o comanda, sterge o comanda si listare comenzi care apartin userului logat.






