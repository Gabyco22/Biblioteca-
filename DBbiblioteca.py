import sqlite3

conn = sqlite3.connect("biblioteca.db")
cursor = conn.cursor()

# Tabla de libros
cursor.execute("""CREATE TABLE IF NOT EXISTS libros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    autor TEXT NOT NULL,
    anio INTEGER NOT NULL
)""")

# Tabla de socios
cursor.execute("""CREATE TABLE IF NOT EXISTS socios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    dni TEXT UNIQUE NOT NULL,
    email TEXT
)""")

# Tabla de préstamos
cursor.execute("""CREATE TABLE IF NOT EXISTS prestamos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    libro_id INTEGER NOT NULL,
    socio_id INTEGER NOT NULL,
    fecha_prestamo TEXT NOT NULL,
    fecha_devolucion TEXT,
    FOREIGN KEY (libro_id) REFERENCES libros(id),
    FOREIGN KEY (socio_id) REFERENCES socios(id)
)""")

conn.commit()