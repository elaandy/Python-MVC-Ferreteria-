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
        """Obtiene todos los productos de la BD"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_producto, nombre, categoria, precio, stock FROM Productos")
        productos = cursor.fetchall()
        conn.close()
        return [Producto(*p) for p in productos]

    @staticmethod
    def obtener_por_id(id_producto):
        """Obtiene un producto específico por ID"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_producto, nombre, categoria, precio, stock FROM Productos WHERE id_producto = ?", 
                      (id_producto,))
        resultado = cursor.fetchone()
        conn.close()
        if resultado:
            return Producto(*resultado)
        return None

    def registrar(self):
        """Registra un nuevo producto en la BD"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Productos (nombre, categoria, precio, stock) VALUES (?, ?, ?, ?)",
            (self.nombre, self.categoria, self.precio, self.stock)
        )
        conn.commit()
        conn.close()

    def actualizar(self):
        """Actualiza los datos del producto en la BD"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Productos SET nombre = ?, categoria = ?, precio = ?, stock = ? WHERE id_producto = ?",
            (self.nombre, self.categoria, self.precio, self.stock, self.id_producto)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def eliminar(id_producto):
        """Elimina un producto de la BD"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Productos WHERE id_producto = ?", (id_producto,))
        conn.commit()
        conn.close()

    @staticmethod
    def obtener_estadisticas():
        """Obtiene estadísticas de productos para el dashboard"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM Productos")
        total_productos = cursor.fetchone()[0]
        
        cursor.execute("SELECT SUM(stock) FROM Productos")
        total_stock = cursor.fetchone()[0] or 0
        
        conn.close()
        return {
            'total_productos': total_productos,
            'total_stock': total_stock
        }
