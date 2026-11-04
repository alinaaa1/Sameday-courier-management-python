# Sameday-courier-management-python
# SameDay Courier Management Platform (Python & Streamlit)

Aplicație web interactivă de gestiune a fluxului de comenzi și expedieri într-o companie de curierat, dezvoltată în Python cu framework-ul Streamlit și bază de date SQLite[cite: 33, 34].

---

## 🛠️ Tehnologii Utilizate
* **Limbaj:** Python[cite: 33]
* **Framework Web:** Streamlit
* **Bază de date:** SQLite (persistență locală și interogări relaționale)[cite: 33, 35]
* **Model Date:** Tabela `orders` (ID, client, destinație, cod unic AWB, timestamp, status, greutate, curier alocat)[cite: 35]

---

## 📌 Funcționalități Cheie
* **Înregistrare comenzi & Alocare automată:** Preluare date expediție, generare automată de cod unic AWB și alocare algoritmică a curierului pe baza greutății coletului[cite: 33, 35, 36].
* **Dashboard interactiv:** Vizualizarea centralizată a comenzilor într-un tabel dinamic cu opțiuni de filtrare[cite: 36, 39].
* **Căutare după AWB:** Identificare instantă a stării coletului și a detaliilor comenzii[cite: 36, 40].
* **Actualizare dinamică a statusului:** Modificarea ciclului de viață al livrării (*Înregistrată*, *În tranzit*, *Livrată*, *Anulată*)[cite: 35, 36, 41].

---

## 📁 Structură
* `app.py` – Scriptul principal Python care conține logica de rutare, interogările SQLite și interfața Streamlit.
* `PROIECT5.pdf` – Documentația tehnică detaliată a arhitecturii aplicației[cite: 29, 32].
