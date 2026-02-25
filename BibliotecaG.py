from DBbiblioteca import conn, cursor

# --- Funciones de Libros ---
def agregarLibro(titulo, autor, anio):
    cursor.execute("SELECT * FROM libros WHERE titulo=? AND autor=?", (titulo, autor))
    if cursor.fetchone():
        print("⚠️ Ese libro ya existe en la base.")
    else:
        cursor.execute("INSERT INTO libros (titulo, autor, anio) VALUES (?, ?, ?)", (titulo, autor, anio))
        conn.commit()
        print("✅ Libro agregado correctamente.")

def obtenerLibros():
    cursor.execute("SELECT * FROM libros")
    return cursor.fetchall()

def librosDosmilMas():
    cursor.execute("SELECT * FROM libros WHERE anio >= 2000")
    return cursor.fetchall()

def contarLibros():
    cursor.execute("SELECT COUNT(*) FROM libros")
    total = cursor.fetchone()[0]
    print(f"📚 Total de libros en la biblioteca: {total}")

# --- Funciones de Socios ---
def agregarSocio(nombre, dni, email):
    cursor.execute("SELECT * FROM socios WHERE dni=?", (dni,))
    if cursor.fetchone():
        print("⚠️ Ese socio ya está registrado.")
    else:
        cursor.execute("INSERT INTO socios (nombre, dni, email) VALUES (?, ?, ?)", (nombre, dni, email))
        conn.commit()
        print("✅ Socio agregado correctamente.")

def obtenerSocios():
    cursor.execute("SELECT * FROM socios")
    return cursor.fetchall()

# --- Funciones de Préstamos ---
def prestarLibro(libro_id, socio_id, fecha_prestamo):
    # Validar que el libro no esté prestado
    cursor.execute("SELECT * FROM prestamos WHERE libro_id=? AND fecha_devolucion IS NULL", (libro_id,))
    if cursor.fetchone():
        print("⚠️ Ese libro ya está prestado.")
    else:
        cursor.execute("INSERT INTO prestamos (libro_id, socio_id, fecha_prestamo) VALUES (?, ?, ?)",
                       (libro_id, socio_id, fecha_prestamo))
        conn.commit()
        print("✅ Préstamo registrado correctamente.")

def devolverLibro(libro_id, fecha_devolucion):
    cursor.execute("UPDATE prestamos SET fecha_devolucion=? WHERE libro_id=? AND fecha_devolucion IS NULL",
                   (fecha_devolucion, libro_id))
    conn.commit()
    print("📖 Libro devuelto correctamente.")

def librosPrestados():
    cursor.execute("""
        SELECT l.titulo, s.nombre, p.fecha_prestamo
        FROM prestamos p
        JOIN libros l ON p.libro_id = l.id
        JOIN socios s ON p.socio_id = s.id
        WHERE p.fecha_devolucion IS NULL
    """)
    return cursor.fetchall()

# --- Menú interactivo ---
def menu():
    while True:
        print("\n--- Biblioteca 2000 ---")
        print("1. Agregar libro")
        print("2. Ver todos los libros")
        print("3. Ver libros publicados desde el 2000")
        print("4. Contar libros")
        print("5. Agregar socio")
        print("6. Ver socios")
        print("7. Registrar préstamo")
        print("8. Registrar devolución")
        print("9. Ver libros prestados")
        print("10. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            titulo = input("Título: ")
            autor = input("Autor: ")
            anio = int(input("Año: "))
            agregarLibro(titulo, autor, anio)
        elif opcion == "2":
            for libro in obtenerLibros():
                print(libro)
        elif opcion == "3":
            for libro in librosDosmilMas():
                print(libro)
        elif opcion == "4":
            contarLibros()
        elif opcion == "5":
            nombre = input("Nombre: ")
            dni = input("DNI: ")
            email = input("Email: ")
            agregarSocio(nombre, dni, email)
        elif opcion == "6":
            for socio in obtenerSocios():
                print(socio)
        elif opcion == "7":
            libro_id = int(input("ID del libro: "))
            socio_id = int(input("ID del socio: "))
            fecha_prestamo = input("Fecha de préstamo (YYYY-MM-DD): ")
            prestarLibro(libro_id, socio_id, fecha_prestamo)
        elif opcion == "8":
            libro_id = int(input("ID del libro: "))
            fecha_devolucion = input("Fecha de devolución (YYYY-MM-DD): ")
            devolverLibro(libro_id, fecha_devolucion)
        elif opcion == "9":
            for prestado in librosPrestados():
                print(prestado)
        elif opcion == "10":
            print("👋 Saliendo del sistema...")
            break
        else:
            print("❌ Opción inválida.")

# --- Datos iniciales de prueba ---
agregarLibro("Cien Años de Soledad", "Gabriel García Márquez", 1967)
agregarLibro("El Código Da Vinci", "Dan Brown", 2003)
agregarLibro("La Sombra del Viento", "Carlos Ruiz Zafón", 2001)

agregarSocio("Juan Pérez", "12345678", "juan@example.com")
agregarSocio("María López", "87654321", "maria@example.com")

# --- Ejecutar menú ---
menu()