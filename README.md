# Sameday-courier-management-python
# SameDay Courier Management Platform (Python & Streamlit)

Aplicație web interactivă de gestiune a fluxului de comenzi și expedieri într-o companie de curierat, dezvoltată în Python cu framework-ul Streamlit și bază de date SQLite.

---

## 🛠️ Tehnologii Utilizate
* **Limbaj:** Python
* **Framework Web:** Streamlit
* **Bază de date:** SQLite (persistență locală și interogări relaționale)
* **Model Date:** Tabela `orders` (ID, client, destinație, cod unic AWB, timestamp, status, greutate, curier alocat)

---

## 📌 Funcționalități Cheie
* **Înregistrare comenzi & Alocare automată:** Preluare date expediție, generare automată de cod unic AWB și alocare algoritmică a curierului pe baza greutății coletului.
* **Dashboard interactiv:** Vizualizarea centralizată a comenzilor într-un tabel dinamic cu opțiuni de filtrare.
* **Căutare după AWB:** Identificare instantă a stării coletului și a detaliilor comenzii.
* **Actualizare dinamică a statusului:** Modificarea ciclului de viață al livrării (*Înregistrată*, *În tranzit*, *Livrată*, *Anulată*).

---

## 📁 Structură
* `app.py` – Scriptul principal Python care conține logica de rutare, interogările SQLite și interfața Streamlit.
* `PROIECT5.pdf` – Documentația tehnică detaliată a arhitecturii aplicației.
