from Conexion.database import get_connection

class Usuario:
    def __init__(self, id_usuario, username, password, rol):
        self.id_usuario = id_usuario
        self.username = username
        self.password = password
        self.rol = rol

    @staticmethod
    def obtener_usuarios():
        """Obtiene todos los usuarios de la BD"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario, username, password, rol FROM Usuarios")
        usuarios = cursor.fetchall()
        conn.close()
        return [Usuario(*u) for u in usuarios]

    @staticmethod
    def obtener_por_id(id_usuario):
        """Obtiene un usuario por ID"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id_usuario, username, password, rol FROM Usuarios WHERE id_usuario = ?",
            (id_usuario,)
        )
        resultado = cursor.fetchone()
        conn.close()
        if resultado:
            return Usuario(*resultado)
        return None

    @staticmethod
    def login(username, password):
        """Valida el login del usuario"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id_usuario, username, password, rol FROM Usuarios WHERE username = ? AND password = ?",
            (username, password)
        )
        resultado = cursor.fetchone()
        conn.close()
        if resultado:
            return Usuario(*resultado)
        return None

    def registrar(self):
        """Registra un nuevo usuario"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Usuarios (username, password, rol) VALUES (?, ?, ?)",
            (self.username, self.password, self.rol)
        )
        conn.commit()
        conn.close()

    def actualizar(self):
        """Actualiza datos del usuario"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Usuarios SET username = ?, password = ?, rol = ? WHERE id_usuario = ?",
            (self.username, self.password, self.rol, self.id_usuario)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def eliminar(id_usuario):
        """Elimina un usuario"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM Usuarios WHERE id_usuario = ?",
            (id_usuario,)
        )
        conn.commit()
        conn.close()
