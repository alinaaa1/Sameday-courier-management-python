# Importurile necesare pentru aplicație: Streamlit pentru UI, datetime pentru timestampuri,
# random pentru generarea AWB-urilor, și SQLAlchemy pentru interacțiunea cu baza de date.
import streamlit as st
from datetime import datetime
import random
from database import Order, SessionLocal, init_db
from sqlalchemy.exc import IntegrityError

# Inițializez baza de date la pornirea aplicației.
init_db()

# Lista curierilor disponibili, fiecare cu o limită de greutate proprie.
CURIERI = [
    {"nume": "Ion", "max_kg": 5},
    {"nume": "Maria", "max_kg": 10},
    {"nume": "Vasile", "max_kg": 20},
    {"nume": "Andreea", "max_kg": 100},
]

# Posibilele statusuri pentru comenzi.
STATUS_OPTIONS = ['Înregistrată', 'În tranzit', 'Livrată', 'Anulată']

# Funcție simplă pentru generarea unui AWB random.
def generate_awb():
    return f"AWB{random.randint(100000, 999999)}"

# Aleg automat curierul în funcție de greutatea coletului.
def selecteaza_curier(greutate):
    for curier in CURIERI:
        if greutate <= curier["max_kg"]:
            return curier["nume"]
    return "Necunoscut"

# Configurez aspectul paginii Streamlit și stilizez aplicația cu puțin CSS personalizat.
st.set_page_config(page_title="SameDay Curier", layout="centered")
st.markdown("""
    <style>
    body {
        background-color: #e6f0ff;
    }
    .stApp {
        background-color: #e6f0ff;
        color: #000000;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .css-1d391kg {
        background-color: #b3c6ff;
        border-radius: 8px;
    }
    h1 {
        color: #003366;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar cu meniul principal al aplicației.
st.sidebar.title("📦 SameDay Menu")

menu_options = ["🏠 Acasă", "➕ Adaugă Comandă", "📋 Vizualizează Comenzi", "🔎 Caută AWB", "🔁 Actualizează Status"]
menu = st.sidebar.selectbox("Navigare", menu_options)

# Folosesc sesiunea Streamlit ca să păstrez selecția din meniu activă între re-randări.
if "menu" not in st.session_state:
    st.session_state["menu"] = menu
else:
    if st.session_state["menu"] != menu:
        st.session_state["menu"] = menu
menu = st.session_state["menu"]

# Pagina principală cu descrierea aplicației și funcționalitățile disponibile.
if menu == "🏠 Acasă":
    st.markdown("<h1 style='text-align: center; font-weight: 900; font-size: 48px; color: #003366;'>📦 SameDay Curier</h1>", unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align: center; font-size: 18px; padding-top: 10px; max-width: 600px; margin: auto;'>
            Bine ai venit în platforma de gestiune comenzi SameDay.<br><br>
            Aici poți:
            <ul style='text-align: left; margin-left: 40%;'>
                <li>➕ Adăuga comenzi noi</li>
                <li>📋 Vizualiza comenzile existente</li>
                <li>🔎 Căuta comenzi după AWB</li>
                <li>🔁 Actualiza statusul livrărilor</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# Pagina pentru adăugarea unei comenzi noi în baza de date.
elif menu == "➕ Adaugă Comandă":
    st.header("➕ Adaugă Comandă Nouă")
    client = st.text_input("Nume Client")
    destinatie = st.text_input("Destinație")
    greutate = st.number_input("Greutate colet (kg)", min_value=0.1, step=0.1)
    status = st.selectbox("Status Inițial", STATUS_OPTIONS)

    if st.button("Salvează Comanda"):
        if client and destinatie and greutate > 0:
            session = SessionLocal()
            awb = generate_awb()
            # Verific dacă AWB-ul generat e unic.
            while session.query(Order).filter_by(awb=awb).first():
                awb = generate_awb()
            curier = selecteaza_curier(greutate)
            # Creez obiectul comenzii și îl salvez în DB.
            order = Order(
                client=client,
                destinatie=destinatie,
                awb=awb,
                status=status,
                greutate=greutate,
                curier=curier
            )
            session.add(order)
            try:
                session.commit()
                st.success(f"Comandă salvată! AWB: `{awb}` • Curier: **{curier}**")
            except IntegrityError:
                session.rollback()
                st.error("Eroare: AWB duplicat.")
            session.close()
        else:
            st.warning("Completează toate câmpurile.")

# Pagina de vizualizare a tuturor comenzilor salvate.
elif menu == "📋 Vizualizează Comenzi":
    st.header("📋 Toate Comenzile")
    session = SessionLocal()
    orders = session.query(Order).all()
    if not orders:
        st.info("Nu există comenzi.")
    else:
        data = [{
            "Client": o.client,
            "Destinație": o.destinatie,
            "AWB": o.awb,
            "Data": o.data.strftime('%Y-%m-%d %H:%M'),
            "Status": o.status,
            "Greutate (kg)": o.greutate,
            "Curier": o.curier
        } for o in orders]
        # Afișez comenzile într-un tabel responsive.
        st.dataframe(data, use_container_width=True)
    session.close()

# Pagina pentru căutarea unei comenzi după AWB.
elif menu == "🔎 Caută AWB":
    st.header("🔎 Caută Comandă după AWB")
    search_awb = st.text_input("Introdu AWB")
    if st.button("Caută"):
        session = SessionLocal()
        order = session.query(Order).filter_by(awb=search_awb).first()
        if order:
            st.success("Comandă găsită:")
            st.write({
                "Client": order.client,
                "Destinație": order.destinatie,
                "Data": order.data.strftime('%Y-%m-%d %H:%M'),
                "Status": order.status,
                "Greutate (kg)": order.greutate,
                "Curier": order.curier
            })
        else:
            st.error("AWB-ul nu a fost găsit.")
        session.close()

# Pagina pentru actualizarea statusului unei comenzi existente.
elif menu == "🔁 Actualizează Status":
    st.header("🔁 Actualizează Status Comandă")
    session = SessionLocal()
    orders = session.query(Order).all()
    awbs = [o.awb for o in orders]
    if not awbs:
        st.info("Nu există comenzi.")
    else:
        selected_awb = st.selectbox("Selectează AWB", awbs)
        order = session.query(Order).filter_by(awb=selected_awb).first()
        if order:
            current_status = order.status
            st.write(f"Status curent: **{current_status}**")
            new_status = st.selectbox("Status nou", STATUS_OPTIONS, index=STATUS_OPTIONS.index(current_status))
            if st.button("Actualizează Status"):
                order.status = new_status
                session.commit()
                st.success(f"Statusul comenzii {selected_awb} a fost actualizat la '{new_status}'")
        session.close()
