# Importurile necesare pentru a lucra cu SQLAlchemy și pentru a defini modelul bazei de date.
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# Declar bază comună pentru toate clasele de tip ORM.
Base = declarative_base()

# Creez conexiunea cu baza de date SQLite. Nu folosesc echo pentru a evita loguri inutile în consolă.
engine = create_engine('sqlite:///orders.db', echo=False)

# Creez o sesiune locală pentru fiecare interacțiune cu baza de date.
SessionLocal = sessionmaker(bind=engine)


# Definirea modelului Order, corespunzător unui tabel în baza de date.
class Order(Base):
    __tablename__ = 'orders'  # Numele tabelului în baza de date.

    id = Column(Integer, primary_key=True, index=True)  # ID unic pentru fiecare comandă.
    client = Column(String, nullable=False)  # Numele clientului.
    destinatie = Column(String, nullable=False)  # Destinația coletului.
    awb = Column(String, unique=True, nullable=False)  # Codul AWB (unic pentru fiecare comandă).
    data = Column(DateTime, default=datetime.utcnow)  # Data înregistrării comenzii.
    status = Column(String, default="Înregistrată")  # Statusul curent al comenzii.
    greutate = Column(Float, nullable=False)  # Greutatea coletului.
    curier = Column(String, nullable=False)  # Curierul asignat.


# Funcția care creează tabelele și adaugă un set de comenzi de test la prima rulare.
def init_db():
    # Creez toate tabelele definite (dacă nu există deja).
    Base.metadata.create_all(bind=engine)

    # Creez o sesiune pentru a interacționa cu baza de date.
    db = SessionLocal()

    # Dacă nu există comenzi, inserez un set de comenzi predefinite.
    if db.query(Order).count() == 0:
        comenzi_initiale = [
            Order(client="Ion Popescu", destinatie="București", awb="SMD100001", status="În tranzit", greutate=2.5,
                  curier="Curier 1"),
            Order(client="Maria Ionescu", destinatie="Cluj", awb="SMD100002", status="Livrat", greutate=1.0,
                  curier="Curier 2"),
            Order(client="Andrei Georgescu", destinatie="Iași", awb="SMD100003", status="În depozit", greutate=5.5,
                  curier="Curier 3"),
            Order(client="Elena Dobre", destinatie="Timișoara", awb="SMD100004", status="În tranzit", greutate=3.0,
                  curier="Curier 1"),
            Order(client="Cristian Marin", destinatie="Brașov", awb="SMD100005", status="Înregistrată", greutate=0.8,
                  curier="Curier 2"),
            Order(client="Roxana Badea", destinatie="Constanța", awb="SMD100006", status="Livrat", greutate=4.2,
                  curier="Curier 3"),
            Order(client="Mihai Enache", destinatie="Oradea", awb="SMD100007", status="În depozit", greutate=6.0,
                  curier="Curier 1"),
            Order(client="Laura Stoica", destinatie="Sibiu", awb="SMD100008", status="În tranzit", greutate=2.0,
                  curier="Curier 2"),
            Order(client="Dan Iliescu", destinatie="Pitești", awb="SMD100009", status="Livrat", greutate=3.5,
                  curier="Curier 3"),
            Order(client="Irina Pavel", destinatie="Craiova", awb="SMD100010", status="Înregistrată", greutate=1.3,
                  curier="Curier 1"),
            Order(client="Vlad Radu", destinatie="Satu Mare", awb="SMD100011", status="În tranzit", greutate=4.7,
                  curier="Curier 2"),
            Order(client="Adelina Voicu", destinatie="Bacău", awb="SMD100012", status="În depozit", greutate=2.9,
                  curier="Curier 3"),
            Order(client="George Țuțuianu", destinatie="Focșani", awb="SMD100013", status="Livrat", greutate=1.1,
                  curier="Curier 1"),
            Order(client="Simona Cernat", destinatie="Arad", awb="SMD100014", status="În tranzit", greutate=3.8,
                  curier="Curier 2"),
            Order(client="Florin Costache", destinatie="Alba Iulia", awb="SMD100015", status="Înregistrată",
                  greutate=5.0, curier="Curier 3"),
        ]

        # Adaug comenzile în DB și salvez.
        db.add_all(comenzi_initiale)
        db.commit()

    # Închid sesiunea.
    db.close()
