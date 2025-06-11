# MarketPlace

## Descriere

MarketPlace este o aplicație simplă de tip magazin online, scrisă în Python. Aplicația permite crearea și gestionarea unei baze de date, oferind operațiuni CRUD (Creare, Citire, Actualizare, Ștergere) pentru utilizatori, categorii, produse și comenzi.

## Tehnologii folosite

- Python 3.x  
- SQLite (baza de date)  
- Selenium (pentru testare automată)  
- unittest (framework pentru testare)

## Instalare

1. Clonează proiectul:
```bash
git clone https://github.com/28mirceas/MarketPlace.git
cd MarketPlace
```
3. Instalează dependențele:
```bash   
pip install -r requirements.txt
```
5. Creează baza de date rulând scriptul:
 ```bash  
python app/databasemanager.py
```

## Utilizare

1.	Porneste aplicatia:
```bash  
python Main.py
```
3.	Creează primul utilizator în secțiunea „User Management”.
Notă: Primul utilizator creat are drepturi de administrator și poate șterge utilizatori, categorii, produse și comenzi.
4.	Utilizează meniul pentru a administra utilizatorii, categoriile, produsele și comenzile.
5.	 Pentru a ieși din aplicație, selectează opțiunea „5. Ieșire din program”.


## Comenzi pentru administrarea magazinului  

1.	Pentru User se merge la sectiunea User Management si avem optiunile: adauga user, modifica user, schimba parola, stergere user, login si logout, listare useri;
2.	Pentru Categorie se merge la Category Management si avem optiunile: adauga categorie, modifica o categorie, sterge o categorie si listeaza categoriile existente; 
3.	Pentru Produs se merge pe sectiunea Product Management si avem optiunile: adauga produs, modifica un produs, sterge un produs si listeaza produsele existente;
4.	Pentru Comenzi se merge pe sectiunea Order Management si avem optiunile: adauga o comanda, modifica o comanda, sterge o comanda si listare comenzi care apartin userului logat.






