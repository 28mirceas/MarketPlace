# MarketPlace

## Descriere

MarketPlace este o aplicație simplă de tip magazin-online, scrisă în Python. Aplicația permite crearea și gestionarea unei baze de date, oferind operațiuni CRUD (Creare, Citire, Actualizare, Ștergere) pentru utilizatori, categorii, produse și comenzi.

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
2.	Creează primul utilizator în secțiunea „User Management”.
Notă: Primul utilizator creat are drepturi de administrator și poate șterge utilizatori, categorii, produse și comenzi.
3.	Utilizează meniul pentru a administra utilizatorii, categoriile, produsele și comenzile.
4.	Pentru a ieși din aplicație, selectează opțiunea „5. Ieșire din program”.


## Funcționalități principale

1. User Management: adaugă, modifică, șterge utilizatori; schimbă parola; login/logout; listare utilizatori
2. Category Management: adaugă, modifică, șterge categorii; listare categorii
3. Product Management: adaugă, modifică, șterge produse; listare produse
4. Order Management: adaugă, modifică, șterge comenzi; listare comenzi pentru utilizatorul logat

##  Testare automată

Aplicația folosește Selenium și unittest pentru testarea automată a funcționalităților.

Rulează testele cu:
```bash 
python tests/suita_teste.py
```
Pentru generarea rapoartelor HTML, se folosește HtmlTestRunner.

##  Structura proiectului
```bash 
MarketPlace/
│
├── app/
│   ├── databasemanager.py
│   ├── user.py
│   ├── category.py
│   ├── product.py
│   ├── order.py
│   └── Main.py
├── tests/
│   ├── suita_teste.py
│   ├── test_user.py
│   ├── test_product.py
│   ├── test_category.py
│   ├── test_order.py
│
|
├── requirements.txt
└── README.md

## Licenta

[MIT](https://choosealicense.com/licenses/mit/)

```




