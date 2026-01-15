from Conexion.database import get_connection


class Producto:
    def __init__(self, id_producto, nombre, categoria, precio, stock):
        self.id_producto = id_producto
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.stock = stock

    @staticmethod
    def obtener_productos():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_producto, nombre, categoria, precio, stock FROM Productos")
        productos = cursor.fetchall()
        conn.close()
        return [Producto(*p) for p in productos]

    def registrar(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Productos (nombre, categoria, precio, stock) VALUES (?, ?, ?, ?)",
            (self.nombre, self.categoria, self.precio, self.stock)
        )
        conn.commit()
        conn.close()

    def actualizar(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Productos SET nombre = ?, categoria = ?, precio = ?, stock = ? WHERE id_producto = ?"
            (self.nombre, self.categoria, self.precio, self.stock, self.id_producto)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def eliminar(id_producto):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Productos WHERE id_producto = ?", (id_producto,))
        conn.commit()
        conn.close()
