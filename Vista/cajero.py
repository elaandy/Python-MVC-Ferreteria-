import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import ttk, messagebox
from Logica.ventas_servicio import VentaServicio
from Logica.product import Producto


class AppFerreteria:

    def __init__(self, parent_menu=None):
        self.servicio = VentaServicio()
        self.carrito = {}  # {id_producto: {"nombre": str, "precio": float, "cantidad": int, "stock": int}}
        self.parent_menu = parent_menu

        if parent_menu is None:
            self.ventana = tk.Tk()
            self.es_ventana_principal = True
        else:
            self.ventana = tk.Toplevel(parent_menu)
            self.es_ventana_principal = False
        
        self.ventana.title("Ferretería - Sistema de Ventas")
        self.ventana.geometry("1400x750")
        self.ventana.resizable(True, True)
        
        # Colores personalizados
        self.color_principal = "#2C3E50"
        self.color_secundario = "#34495E"
        self.color_acento = "#E74C3C"
        self.color_exito = "#27AE60"
        self.color_fondo = "#ECF0F1"
        self.color_texto = "#2C3E50"
        self.color_advertencia = "#F39C12"
        
        # Configurar estilos
        self.configurar_estilos()
        
        # Fondo
        self.ventana.configure(bg=self.color_fondo)
        
        # Crear interfaz
        self.crear_encabezado()
        self.crear_contenido_principal()
        self.cargar_productos()

        if self.es_ventana_principal:
            self.ventana.mainloop()

    def configurar_estilos(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Estilo para Treeview
        style.configure("Treeview",
                       background="#FFFFFF",
                       foreground=self.color_texto,
                       rowheight=28,
                       font=("Segoe UI", 10))
        style.configure("Treeview.Heading",
                       background=self.color_principal,
                       foreground="white",
                       font=("Segoe UI", 11, "bold"))
        style.map('Treeview', background=[('selected', self.color_acento)])
        
        # Estilo para botones
        style.configure("TButton",
                       font=("Segoe UI", 9, "bold"),
                       padding=8)
        style.map("TButton",
                 background=[('active', self.color_exito)])
        
        # Estilo para Entry
        style.configure("TEntry",
                       font=("Segoe UI", 10),
                       padding=5)
        
        # Estilo para Frame
        style.configure("TFrame",
                       background=self.color_fondo)
        
        # Estilo especial para botón principal
        style.configure("Accent.TButton",
                       background=self.color_acento,
                       foreground="white",
                       font=("Segoe UI", 11, "bold"),
                       padding=12)

    def crear_encabezado(self):
        frame_header = tk.Frame(self.ventana, bg=self.color_principal, height=70)
        frame_header.pack(fill="x", padx=0, pady=0)
        frame_header.pack_propagate(False)
        
        # Título
        title = tk.Label(
            frame_header,
            text="🏪 FERRETERÍA - SISTEMA DE VENTAS CON CARRITO",
            font=("Segoe UI", 18, "bold"),
            bg=self.color_principal,
            fg="white"
        )
        title.pack(pady=15)
        
        # Línea divisora
        divider = tk.Frame(self.ventana, bg=self.color_acento, height=2)
        divider.pack(fill="x", padx=0, pady=0)

    def crear_contenido_principal(self):
        """Crea la interfaz con dos columnas: productos a la izquierda y carrito a la derecha"""
        frame_contenido = ttk.Frame(self.ventana)
        frame_contenido.pack(fill="both", expand=True, padx=10, pady=10)
        
        # COLUMNA IZQUIERDA: Tabla de Productos
        self.crear_tabla_productos(frame_contenido)
        
        # COLUMNA DERECHA: Carrito
        self.crear_carrito(frame_contenido)

    def crear_tabla_productos(self, frame_padre):
        """Crea la tabla de productos disponibles"""
        frame_tabla = ttk.Frame(frame_padre)
        frame_tabla.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Título
        titulo = tk.Label(
            frame_tabla,
            text="Productos Disponibles",
            font=("Segoe UI", 12, "bold"),
            bg=self.color_secundario,
            fg="white",
            pady=8
        )
        titulo.pack(fill="x")
        
        # Frame para tabla y scrollbar
        frame_scroll = ttk.Frame(frame_tabla)
        frame_scroll.pack(fill="both", expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_scroll)
        scrollbar.pack(side="right", fill="y")
        
        # Tabla
        self.tabla_productos = ttk.Treeview(
            frame_scroll,
            columns=("id", "nombre", "precio", "stock"),
            show="headings",
            yscrollcommand=scrollbar.set,
            height=20
        )
        scrollbar.config(command=self.tabla_productos.yview)
        
        # Configurar columnas
        self.tabla_productos.column("id", width=40, anchor="center")
        self.tabla_productos.column("nombre", width=200, anchor="w")
        self.tabla_productos.column("precio", width=80, anchor="center")
        self.tabla_productos.column("stock", width=80, anchor="center")
        
        for col in ("id", "nombre", "precio", "stock"):
            self.tabla_productos.heading(col, text=col.capitalize())
        
        self.tabla_productos.pack(fill="both", expand=True)
        
        # Frame de controles
        frame_controles_prod = ttk.Frame(frame_tabla)
        frame_controles_prod.pack(fill="x", pady=10)
        
        # Label y Entry para cantidad
        ttk.Label(frame_controles_prod, text="Cantidad:").pack(side="left", padx=5)
        
        self.entry_cantidad_producto = ttk.Entry(frame_controles_prod, width=8)
        self.entry_cantidad_producto.pack(side="left", padx=5)
        self.entry_cantidad_producto.insert(0, "1")
        
        # Botón Agregar al carrito
        btn_agregar = tk.Button(
            frame_controles_prod,
            text="✓ Agregar al Carrito",
            command=self.agregar_al_carrito,
            bg=self.color_exito,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=6,
            cursor="hand2",
            relief="raised",
            bd=2
        )
        btn_agregar.pack(side="left", padx=5)

    def crear_carrito(self, frame_padre):
        """Crea el carrito de compras"""
        frame_carrito = ttk.Frame(frame_padre)
        frame_carrito.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # Título
        titulo = tk.Label(
            frame_carrito,
            text="🛒 Carrito de Compras",
            font=("Segoe UI", 12, "bold"),
            bg=self.color_acento,
            fg="white",
            pady=8
        )
        titulo.pack(fill="x")
        
        # Frame para tabla y scrollbar
        frame_scroll = ttk.Frame(frame_carrito)
        frame_scroll.pack(fill="both", expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_scroll)
        scrollbar.pack(side="right", fill="y")
        
        # Tabla del carrito
        self.tabla_carrito = ttk.Treeview(
            frame_scroll,
            columns=("nombre", "cantidad", "precio_unitario", "subtotal"),
            show="headings",
            yscrollcommand=scrollbar.set,
            height=20
        )
        scrollbar.config(command=self.tabla_carrito.yview)
        
        # Configurar columnas
        self.tabla_carrito.column("nombre", width=140, anchor="w")
        self.tabla_carrito.column("cantidad", width=70, anchor="center")
        self.tabla_carrito.column("precio_unitario", width=80, anchor="center")
        self.tabla_carrito.column("subtotal", width=100, anchor="center")
        
        for col in ("nombre", "cantidad", "precio_unitario", "subtotal"):
            self.tabla_carrito.heading(col, text=col.replace("_", " ").capitalize())
        
        self.tabla_carrito.pack(fill="both", expand=True)
        
        # Frame de totales y controles
        frame_totales = tk.Frame(frame_carrito, bg=self.color_secundario)
        frame_totales.pack(fill="x", padx=0, pady=0)
        
        # Total
        frame_total = tk.Frame(frame_totales, bg=self.color_secundario)
        frame_total.pack(fill="x", padx=15, pady=10)
        
        ttk.Label(frame_total, text="Total:", font=("Segoe UI", 11, "bold"), foreground="white", background=self.color_secundario).pack(side="left")
        
        self.label_total = tk.Label(
            frame_total,
            text="$0.00",
            font=("Segoe UI", 14, "bold"),
            bg=self.color_secundario,
            fg=self.color_exito
        )
        self.label_total.pack(side="left", padx=10)
        
        # Frame de botones de carrito
        frame_botones_carrito = tk.Frame(frame_totales, bg=self.color_secundario)
        frame_botones_carrito.pack(fill="x", padx=15, pady=(0, 10))
        
        # Botón Eliminar del carrito
        btn_eliminar = tk.Button(
            frame_botones_carrito,
            text="🗑️ Eliminar",
            command=self.eliminar_del_carrito,
            bg=self.color_advertencia,
            fg="white",
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=5,
            cursor="hand2",
            relief="raised",
            bd=1
        )
        btn_eliminar.pack(side="left", padx=5)
        
        # Botón Limpiar carrito
        btn_limpiar = tk.Button(
            frame_botones_carrito,
            text="🗑️ Limpiar",
            command=self.limpiar_carrito,
            bg=self.color_advertencia,
            fg="white",
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=5,
            cursor="hand2",
            relief="raised",
            bd=1
        )
        btn_limpiar.pack(side="left", padx=5)
        
        # Botón Completar Compra
        btn_comprar = tk.Button(
            frame_botones_carrito,
            text="💰 COMPLETAR COMPRA",
            command=self.completar_compra,
            bg=self.color_exito,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=6,
            cursor="hand2",
            relief="raised",
            bd=2
        )
        btn_comprar.pack(side="right", padx=5)
        
        # Botón Volver al Menú (solo si viene del menú)
        if self.parent_menu:
            btn_volver = tk.Button(
                frame_botones_carrito,
                text="← Volver al Menú",
                command=self.volver_menu,
                bg="#95A5A6",
                fg="white",
                font=("Segoe UI", 10, "bold"),
                padx=15,
                pady=6,
                cursor="hand2",
                relief="raised",
                bd=2
            )
            btn_volver.pack(side="right", padx=5)

    def cargar_productos(self):
        """Carga los productos en la tabla"""
        self.tabla_productos.delete(*self.tabla_productos.get_children())
        
        productos = Producto.obtener_productos()
        for i, p in enumerate(productos):
            # Alternar colores de filas
            tag = "oddrow" if i % 2 == 0 else "evenrow"
            self.tabla_productos.insert(
                "",
                "end",
                tags=(tag,),
                values=(p.id_producto, p.nombre, f"${p.precio:.0f}", p.stock)
            )
        
        # Configurar colores alternados
        self.tabla_productos.tag_configure("oddrow", background="#F8F9F9")
        self.tabla_productos.tag_configure("evenrow", background="#FFFFFF")

    def agregar_al_carrito(self):
        """Agrega un producto al carrito"""
        try:
            if not self.tabla_productos.selection():
                messagebox.showwarning("Advertencia", "Selecciona un producto de la tabla")
                return
            
            item = self.tabla_productos.selection()[0]
            valores = self.tabla_productos.item(item, "values")
            
            cantidad_str = self.entry_cantidad_producto.get().strip()
            if not cantidad_str:
                messagebox.showwarning("Advertencia", "Ingresa una cantidad")
                return
            
            cantidad = int(cantidad_str)
            if cantidad <= 0:
                messagebox.showwarning("Advertencia", "La cantidad debe ser mayor a 0")
                return
            
            id_producto = int(valores[0])
            nombre = valores[1]
            precio_str = valores[2].replace("$", "")
            precio = float(precio_str)
            stock = int(valores[3])
            
            if cantidad > stock:
                messagebox.showwarning("Advertencia", f"No hay suficiente stock. Disponible: {stock}")
                return
            
            # Si el producto ya existe en el carrito, sumar cantidad
            if id_producto in self.carrito:
                cantidad_actual = self.carrito[id_producto]["cantidad"]
                nueva_cantidad = cantidad_actual + cantidad
                
                if nueva_cantidad > stock:
                    messagebox.showwarning("Advertencia", f"No hay suficiente stock. Disponible: {stock}, en carrito: {cantidad_actual}")
                    return
                
                self.carrito[id_producto]["cantidad"] = nueva_cantidad
            else:
                self.carrito[id_producto] = {
                    "nombre": nombre,
                    "precio": precio,
                    "cantidad": cantidad,
                    "stock": stock
                }
            
            self.actualizar_tabla_carrito()
            self.entry_cantidad_producto.delete(0, "end")
            self.entry_cantidad_producto.insert(0, "1")
            messagebox.showinfo("✓ Éxito", f"Producto agregado al carrito")
            
        except ValueError:
            messagebox.showerror("Error", "Ingresa una cantidad válida (número)")
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error:\n{str(e)}")

    def actualizar_tabla_carrito(self):
        """Actualiza la tabla del carrito y el total"""
        self.tabla_carrito.delete(*self.tabla_carrito.get_children())
        
        total = 0
        for id_producto, item in self.carrito.items():
            nombre = item["nombre"]
            cantidad = item["cantidad"]
            precio_unitario = item["precio"]
            subtotal = cantidad * precio_unitario
            total += subtotal
            
            self.tabla_carrito.insert(
                "",
                "end",
                values=(nombre, cantidad, f"${precio_unitario:.0f}", f"${subtotal:.0f}")
            )
        
        # Actualizar etiqueta de total
        self.label_total.config(text=f"${total:.2f}")

    def eliminar_del_carrito(self):
        """Elimina un producto del carrito"""
        try:
            if not self.tabla_carrito.selection():
                messagebox.showwarning("Advertencia", "Selecciona un producto del carrito")
                return
            
            item = self.tabla_carrito.selection()[0]
            valores = self.tabla_carrito.item(item, "values")
            nombre_producto = valores[0]
            
            # Buscar el id_producto por el nombre
            id_producto_a_eliminar = None
            for id_producto, item_carrito in self.carrito.items():
                if item_carrito["nombre"] == nombre_producto:
                    id_producto_a_eliminar = id_producto
                    break
            
            if id_producto_a_eliminar:
                del self.carrito[id_producto_a_eliminar]
                self.actualizar_tabla_carrito()
                messagebox.showinfo("✓ Éxito", "Producto eliminado del carrito")
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error:\n{str(e)}")

    def limpiar_carrito(self):
        """Limpia todo el carrito"""
        if not self.carrito:
            messagebox.showinfo("Información", "El carrito está vacío")
            return
        
        if messagebox.askyesno("Confirmar", "¿Deseas limpiar todo el carrito?"):
            self.carrito = {}
            self.actualizar_tabla_carrito()
            messagebox.showinfo("✓ Éxito", "Carrito limpiado")

    def completar_compra(self):
        """Completa la compra con todos los productos en el carrito"""
        try:
            if not self.carrito:
                messagebox.showwarning("Advertencia", "El carrito está vacío")
                return
            
            # Confirmar compra
            total = sum(item["cantidad"] * item["precio"] for item in self.carrito.values())
            
            mensaje = "Resumen de compra:\n\n"
            for item in self.carrito.values():
                mensaje += f"{item['nombre']}: {item['cantidad']} x ${item['precio']:.0f} = ${item['cantidad'] * item['precio']:.2f}\n"
            mensaje += f"\n{'='*40}\nTOTAL: ${total:.2f}\n{'='*40}\n\n¿Confirmar compra?"
            
            if not messagebox.askyesno("Confirmar Compra", mensaje):
                return
            
            # Preparar lista de productos para el servicio
            productos_cantidad = [(id_prod, item["cantidad"]) for id_prod, item in self.carrito.items()]
            
            # Registrar venta
            id_venta, total_venta = self.servicio.registrar_venta(productos_cantidad)
            
            messagebox.showinfo("✓ Compra Realizada", f"Venta #{id_venta} registrada correctamente\n\nTotal: ${total_venta:.2f}")
            
            # Limpiar carrito
            self.carrito = {}
            self.actualizar_tabla_carrito()
            self.cargar_productos()
            
        except ValueError as e:
            messagebox.showerror("Error", f"Error en la compra:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error:\n{str(e)}")

    def volver_menu(self):
        """Cierra la ventana y regresa al menú"""
        self.ventana.destroy()


if __name__ == "__main__":
    AppFerreteria()