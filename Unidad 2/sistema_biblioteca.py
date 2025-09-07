# Clase Libro
class Libro:
    def __init__(self, titulo, autor, categoria, isbn):
        # Usamos tupla para atributos inmutables
        self.__info = (titulo, autor, categoria)
        self.isbn = isbn
    
    @property
    def titulo(self):
        return self.__info[0]
    
    @property
    def autor(self):
        return self.__info[1]
    
    @property
    def categoria(self):
        return self.__info[2]
    
    def __str__(self):
        return f"{self.titulo} - {self.autor} [{self.categoria}] (ISBN: {self.isbn})"


# Clase Usuario
class Usuario:
    def __init__(self, nombre, id_usuario):
        self.nombre = nombre
        self.id_usuario = id_usuario
        self.libros_prestados = []  # Lista de libros actualmente prestados
    
    def __str__(self):
        return f"Usuario: {self.nombre} (ID: {self.id_usuario})"


# Clase Biblioteca
class Biblioteca:
    def __init__(self):
        self.libros = {}           # Diccionario {ISBN: Libro}
        self.usuarios = {}         # Diccionario {ID: Usuario}
        self.ids_usuarios = set()  # Conjunto para asegurar unicidad
    
    # --- Gestión de libros ---
    def añadir_libro(self, libro):
        if libro.isbn in self.libros:
            print("El libro ya existe en la biblioteca.")
        else:
            self.libros[libro.isbn] = libro
            print(f"Libro añadido: {libro}")

    def quitar_libro(self, isbn):
        if isbn in self.libros:
            eliminado = self.libros.pop(isbn)
            print(f"Libro eliminado: {eliminado}")
        else:
            print("No se encontró el libro con ese ISBN.")
    
    # --- Gestión de usuarios ---
    def registrar_usuario(self, usuario):
        if usuario.id_usuario in self.ids_usuarios:
            print("Ya existe un usuario con ese ID.")
        else:
            self.usuarios[usuario.id_usuario] = usuario
            self.ids_usuarios.add(usuario.id_usuario)
            print(f"Usuario registrado: {usuario}")

    def dar_baja_usuario(self, id_usuario):
        if id_usuario in self.usuarios:
            eliminado = self.usuarios.pop(id_usuario)
            self.ids_usuarios.remove(id_usuario)
            print(f"Usuario eliminado: {eliminado}")
        else:
            print("No se encontró el usuario con ese ID.")
    
    # --- Préstamos ---
    def prestar_libro(self, id_usuario, isbn):
        if id_usuario not in self.usuarios:
            print("Usuario no encontrado.")
            return
        if isbn not in self.libros:
            print("Libro no disponible en la biblioteca.")
            return
        
        usuario = self.usuarios[id_usuario]
        libro = self.libros.pop(isbn)  # Se retira de la colección disponible
        usuario.libros_prestados.append(libro)
        print(f"Libro prestado: {libro} a {usuario.nombre}")
    
    def devolver_libro(self, id_usuario, isbn):
        if id_usuario not in self.usuarios:
            print("Usuario no encontrado.")
            return
        
        usuario = self.usuarios[id_usuario]
        for libro in usuario.libros_prestados:
            if libro.isbn == isbn:
                usuario.libros_prestados.remove(libro)
                self.libros[isbn] = libro
                print(f"Libro devuelto: {libro}")
                return
        print("El usuario no tiene prestado ese libro.")
    
    # --- Búsquedas ---
    def buscar_libro(self, criterio, valor):
        resultados = [libro for libro in self.libros.values()
                      if getattr(libro, criterio, "").lower() == valor.lower()]
        if resultados:
            print("Resultados de búsqueda:")
            for l in resultados:
                print(l)
        else:
            print("No se encontraron libros con ese criterio.")
    
    # --- Listar préstamos ---
    def listar_libros_prestados(self, id_usuario):
        if id_usuario not in self.usuarios:
            print("Usuario no encontrado.")
            return
        usuario = self.usuarios[id_usuario]
        if usuario.libros_prestados:
            print(f"Libros prestados a {usuario.nombre}:")
            for libro in usuario.libros_prestados:
                print(libro)
        else:
            print(f"{usuario.nombre} no tiene libros prestados.")


# -------------------- PRUEBA DEL SISTEMA --------------------
if __name__ == "__main__":
    # Crear biblioteca
    biblio = Biblioteca()

    # Crear libros
    libro1 = Libro("Cien Años de Soledad", "Gabriel García Márquez", "Novela", "111")
    libro2 = Libro("1984", "George Orwell", "Distopía", "222")
    libro3 = Libro("El Principito", "Antoine de Saint-Exupéry", "Infantil", "333")

    # Añadir libros
    biblio.añadir_libro(libro1)
    biblio.añadir_libro(libro2)
    biblio.añadir_libro(libro3)

    # Crear usuarios
    usuario1 = Usuario("Ana", "U1")
    usuario2 = Usuario("Luis", "U2")

    # Registrar usuarios
    biblio.registrar_usuario(usuario1)
    biblio.registrar_usuario(usuario2)

    # Prestar libro
    biblio.prestar_libro("U1", "111")
    biblio.listar_libros_prestados("U1")

    # Buscar libro
    biblio.buscar_libro("autor", "George Orwell")

    # Devolver libro
    biblio.devolver_libro("U1", "111")
    biblio.listar_libros_prestados("U1")
