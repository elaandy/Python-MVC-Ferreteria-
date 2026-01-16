from flask import Flask, render_template, request, redirect, url_for
from Logica.product import Producto
from Logica.ventas_servicio import VentaServicio
import os
import json

# Obtener rutas absolutas de Vista
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VISTA_DIR = os.path.join(BASE_DIR, 'Vista')
TEMPLATES_DIR = os.path.join(VISTA_DIR, 'templates')
STATIC_DIR = os.path.join(VISTA_DIR, 'static')

app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)

# ==================== DASHBOARD ====================
@app.route('/')
def dashboard():
    """Página principal del dashboard"""
    # Obtener estadísticas de Logica
    stats_productos = Producto.obtener_estadisticas()
    stats_ventas = VentaServicio.obtener_estadisticas()
    
    return render_template('dashboard.html', 
                         total_productos=stats_productos['total_productos'],
                         total_ventas=stats_ventas['total_ventas'],
                         num_ventas=stats_ventas['num_ventas'],
                         total_stock=stats_productos['total_stock'])


# ==================== PRODUCTOS ====================
@app.route('/productos')
def productos():
    """Lista de productos"""
    productos_lista = Producto.obtener_productos()
    productos_json = [
        {
            'id': p.id_producto,
            'nombre': p.nombre,
            'categoria': p.categoria,
            'precio': p.precio,
            'stock': p.stock
        }
        for p in productos_lista
    ]
    return render_template('productos.html', productos=productos_json)


@app.route('/productos/agregar', methods=['GET', 'POST'])
def agregar_producto():
    """Agregar nuevo producto"""
    if request.method == 'POST':
        try:
            producto = Producto(
                id_producto=None,
                nombre=request.form['nombre'],
                categoria=request.form['categoria'],
                precio=float(request.form['precio']),
                stock=int(request.form['stock'])
            )
            producto.registrar()
            return redirect(url_for('productos'))
        except Exception as e:
            return render_template('agregar_producto.html', error=str(e))
    
    return render_template('agregar_producto.html')


@app.route('/productos/editar/<int:id_producto>', methods=['GET', 'POST'])
def editar_producto(id_producto):
    """Editar producto"""
    producto = Producto.obtener_por_id(id_producto)
    
    if not producto:
        return "Producto no encontrado", 404
    
    if request.method == 'POST':
        try:
            producto_actualizado = Producto(
                id_producto=id_producto,
                nombre=request.form['nombre'],
                categoria=request.form['categoria'],
                precio=float(request.form['precio']),
                stock=int(request.form['stock'])
            )
            producto_actualizado.actualizar()
            return redirect(url_for('productos'))
        except Exception as e:
            return render_template('editar_producto.html', producto=producto, error=str(e))
    
    return render_template('editar_producto.html', producto=producto)


@app.route('/productos/eliminar/<int:id_producto>', methods=['POST'])
def eliminar_producto(id_producto):
    """Eliminar producto"""
    try:
        Producto.eliminar(id_producto)
        return redirect(url_for('productos'))
    except Exception as e:
        return render_template('productos.html', error=str(e)), 400


# ==================== VENTAS ====================
@app.route('/venta')
def realizar_venta():
    """Página para realizar una nueva venta"""
    productos_lista = Producto.obtener_productos()
    productos_json = [
        {
            'id': p.id_producto,
            'nombre': p.nombre,
            'categoria': p.categoria,
            'precio': p.precio,
            'stock': p.stock
        }
        for p in productos_lista
    ]
    return render_template('realizar_venta.html', productos=productos_json)


@app.route('/venta/procesar', methods=['POST'])
def procesar_venta():
    """Procesa la venta"""
    try:
        # Obtener datos del formulario
        productos_json = request.form.get('productos')
        productos_cantidad = json.loads(productos_json)
        
        # Convertir a enteros
        productos_cantidad = [[int(id_prod), int(cant)] for id_prod, cant in productos_cantidad]
        
        # Registrar venta usando VentaServicio
        servicio = VentaServicio()
        id_venta, total = servicio.registrar_venta(productos_cantidad)
        
        # Redirigir a detalle de venta
        return redirect(url_for('detalle_venta', id_venta=id_venta))
    except ValueError as e:
        return render_template('realizar_venta.html', error=str(e))
    except Exception as e:
        return render_template('realizar_venta.html', error=f"Error al procesar la venta: {str(e)}")


@app.route('/ventas')
def ventas():
    """Lista de ventas"""
    ventas_lista = VentaServicio.obtener_ventas()
    
    ventas_json = [
        {
            'id': v[0],
            'total': v[1],
            'fecha': str(v[2])
        }
        for v in ventas_lista
    ]
    return render_template('ventas.html', ventas=ventas_json)


@app.route('/ventas/detalle/<int:id_venta>')
def detalle_venta(id_venta):
    """Detalle de una venta"""
    venta = VentaServicio.obtener_venta(id_venta)
    detalles = VentaServicio.obtener_detalle_venta(id_venta)
    
    return render_template('detalle_venta.html', venta=venta, detalles=detalles)


# ==================== ERROR HANDLERS ====================
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)

