from Conexion.database import get_connection
from datetime import datetime

class VentaServicio:
    def __init__(self):
        self.conn = get_connection()

    def registrar_venta(self, productos_cantidad):
        """Registra una venta con múltiples productos"""
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO Ventas (total) VALUES (0)")
        cursor.execute("SELECT @@IDENTITY as id_venta")
        id_venta = cursor.fetchone()[0]
        total_venta = 0

        for id_producto, cantidad in productos_cantidad:
            # Obtener precio y stock actual del producto
            cursor.execute(
                "SELECT precio, stock FROM Productos WHERE id_producto = ?",
                (id_producto,)
            )
            resultado = cursor.fetchone()
            if not resultado:
                raise ValueError(f"Producto {id_producto} no existe")
            precio_unitario, stock_actual = resultado

            if cantidad > stock_actual:
                raise ValueError(f"No hay stock suficiente para el producto {id_producto}")

            # Insertar en Detalle_Venta
            cursor.execute(
                "INSERT INTO Detalle_Venta (id_venta, id_producto, cantidad, precio_unitario) VALUES (?, ?, ?, ?)",
                (id_venta, id_producto, cantidad, precio_unitario)
            )

            # Actualizar stock
            cursor.execute(
                "UPDATE Productos SET stock = stock - ? WHERE id_producto = ?",
                (cantidad, id_producto)
            )

            # Acumular total
            total_venta += precio_unitario * cantidad

        # Actualizar total de la venta
        cursor.execute(
            "UPDATE Ventas SET total = ? WHERE id_venta = ?",
            (total_venta, id_venta)
        )

        self.conn.commit()
        cursor.close()
        return id_venta, total_venta

    @staticmethod
    def obtener_ventas():
        """Obtiene todas las ventas registradas"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_venta, fecha, total FROM Ventas")
        ventas = cursor.fetchall()
        cursor.close()
        conn.close()
        return ventas

    @staticmethod
    def obtener_detalle_venta(id_venta):
        """Obtiene los detalles de una venta específica"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT dv.id_detalle, dv.id_producto, p.nombre, p.categoria, dv.cantidad, dv.precio_unitario
            FROM Detalle_Venta dv
            JOIN Productos p ON dv.id_producto = p.id_producto
            WHERE dv.id_venta = ?
        """, (id_venta,))
        detalle = cursor.fetchall()
        cursor.close()
        conn.close()
        return detalle
