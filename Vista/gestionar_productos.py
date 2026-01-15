import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import ttk, messagebox
from Logica.product import Producto


class GestionarProductos:

    def __init__(self, parent=None):
        if parent is None:
            self.ventana = tk.Tk()
            self.ventana.title("Gestión de Productos")
            self.ventana.geometry("1200x700")
            self.ventana.resizable(True, True)
            self.es_ventana_principal = True
        else:
            self.ventana = tk.Toplevel(parent)
            self.ventana.title("Gestión de Productos")
            self.ventana.geometry("1200x700")
            self.es_ventana_principal = False
        
        # Colores
        self.color_principal = "#2C3E50"
        self.color_secundario = "#34495E"
        self.color_acento = "#E74C3C"
        self.color_exito = "#27AE60"
        self.color_fondo = "#ECF0F1"
        self.color_texto = "#2C3E50"
        self.color_advertencia = "#F39C12"
        
        # Variables para edición
        self.producto_seleccionado = None
        
        # Configurar estilos
        self.configurar_estilos()
        
        # Fondo
        self.ventana.configure(bg=self.color_fondo)
        
        # Crear interfaz
        self.crear_encabezado()
        self.crear_contenido()
        self.cargar_productos()
        
        if self.es_ventana_principal:
            self.ventana.mainloop()

    def configurar_estilos(self):
        style = ttk.Style()
        style.theme_use('clam')
        
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

    def crear_encabezado(self):
        frame_header = tk.Frame(self.ventana, bg=self.color_principal, height=70)
        frame_header.pack(fill="x", padx=0, pady=0)
        frame_header.pack_propagate(False)
        
        title = tk.Label(
            frame_header,
            text="📦 GESTIÓN DE PRODUCTOS",
            font=("Segoe UI", 18, "bold"),
            bg=self.color_principal,
            fg="white"
        )
        title.pack(pady=15)
        
        divider = tk.Frame(self.ventana, bg=self.color_acento, height=2)
        divider.pack(fill="x", padx=0, pady=0)

    def crear_contenido(self):
        # Frame principal para tabla y formulario
        frame_principal = tk.Frame(self.ventana, bg=self.color_fondo)
        frame_principal.pack(fill="both", expand=True, padx=10, pady=10)
        
        # LADO IZQUIERDO - Tabla
        frame_tabla = tk.Frame(frame_principal, bg=self.color_fondo)
        frame_tabla.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        titulo_tabla = tk.Label(
            frame_tabla,
            text="Productos Registrados",
            font=("Segoe UI", 12, "bold"),
            bg=self.color_secundario,
            fg="white",
            pady=8
        )
        titulo_tabla.pack(fill="x")
        
        frame_scroll = ttk.Frame(frame_tabla)
        frame_scroll.pack(fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(frame_scroll)
        scrollbar.pack(side="right", fill="y")
        
        self.tabla_productos = ttk.Treeview(
            frame_scroll,
            columns=("id", "nombre", "categoria", "precio", "stock"),
            show="headings",
            yscrollcommand=scrollbar.set,
            height=20
        )
        scrollbar.config(command=self.tabla_productos.yview)
        
        self.tabla_productos.column("id", width=50, anchor="center")
        self.tabla_productos.column("nombre", width=150, anchor="w")
        self.tabla_productos.column("categoria", width=100, anchor="w")
        self.tabla_productos.column("precio", width=80, anchor="center")
        self.tabla_productos.column("stock", width=80, anchor="center")
        
        for col in ("id", "nombre", "categoria", "precio", "stock"):
            self.tabla_productos.heading(col, text=col.capitalize())
        
        self.tabla_productos.pack(fill="both", expand=True)
        self.tabla_productos.bind("<<TreeviewSelect>>", self.seleccionar_producto)
        
        # LADO DERECHO - Formulario
        frame_form = tk.Frame(frame_principal, bg=self.color_secundario)
        frame_form.pack(side="right", fill="both", padx=(5, 0))
        frame_form.configure(width=300)
        
        titulo_form = tk.Label(
            frame_form,
            text="Formulario",
            font=("Segoe UI", 12, "bold"),
            bg=self.color_secundario,
            fg="white",
            pady=10
        )
        titulo_form.pack(fill="x")
        
        # Canvas con scrollbar para los campos
        canvas = tk.Canvas(frame_form, bg=self.color_secundario, highlightthickness=0)
        scrollbar_y = ttk.Scrollbar(frame_form, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.color_secundario)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar_y.set)
        
        # ID Producto
        tk.Label(scrollable_frame, text="ID Producto:", bg=self.color_secundario, fg="white", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=15, pady=(10, 0))
        self.entry_id = ttk.Entry(scrollable_frame, width=25)
        self.entry_id.pack(fill="x", padx=15, pady=(0, 10))
        
        # Nombre
        tk.Label(scrollable_frame, text="Nombre:", bg=self.color_secundario, fg="white", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=15, pady=(5, 0))
        self.entry_nombre = ttk.Entry(scrollable_frame, width=25)
        self.entry_nombre.pack(fill="x", padx=15, pady=(0, 10))
        
        # Categoría
        tk.Label(scrollable_frame, text="Categoría:", bg=self.color_secundario, fg="white", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=15, pady=(5, 0))
        self.entry_categoria = ttk.Entry(scrollable_frame, width=25)
        self.entry_categoria.pack(fill="x", padx=15, pady=(0, 10))
        
        # Precio
        tk.Label(scrollable_frame, text="Precio:", bg=self.color_secundario, fg="white", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=15, pady=(5, 0))
        self.entry_precio = ttk.Entry(scrollable_frame, width=25)
        self.entry_precio.pack(fill="x", padx=15, pady=(0, 10))
        
        # Stock
        tk.Label(scrollable_frame, text="Stock:", bg=self.color_secundario, fg="white", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=15, pady=(5, 0))
        self.entry_stock = ttk.Entry(scrollable_frame, width=25)
        self.entry_stock.pack(fill="x", padx=15, pady=(0, 20))
        
        # Botones
        frame_botones = tk.Frame(scrollable_frame, bg=self.color_secundario)
        frame_botones.pack(fill="x", padx=15, pady=(0, 15))
        
        btn_registrar = tk.Button(
            frame_botones,
            text="➕ Registrar",
            command=self.registrar_producto,
            bg=self.color_exito,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=8,
            cursor="hand2",
            relief="raised",
            bd=2
        )
        btn_registrar.pack(fill="x", pady=3)
        
        btn_actualizar = tk.Button(
            frame_botones,
            text="✏️ Actualizar",
            command=self.actualizar_producto,
            bg=self.color_advertencia,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=8,
            cursor="hand2",
            relief="raised",
            bd=2
        )
        btn_actualizar.pack(fill="x", pady=3)
        
        btn_eliminar = tk.Button(
            frame_botones,
            text="❌ Eliminar",
            command=self.eliminar_producto,
            bg=self.color_acento,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=8,
            cursor="hand2",
            relief="raised",
            bd=2
        )
        btn_eliminar.pack(fill="x", pady=3)
        
        btn_limpiar = tk.Button(
            frame_botones,
            text="🗑️ Limpiar",
            command=self.limpiar_formulario,
            bg="#95A5A6",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=8,
            cursor="hand2",
            relief="raised",
            bd=2
        )
        btn_limpiar.pack(fill="x", pady=3)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")
        
        # Frame de botones inferiores
        frame_botones_inf = tk.Frame(self.ventana, bg=self.color_fondo)
        frame_botones_inf.pack(fill="x", padx=10, pady=10)
        
        btn_recargar = tk.Button(
            frame_botones_inf,
            text="🔄 Recargar",
            command=self.cargar_productos,
            bg=self.color_exito,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=6,
            cursor="hand2",
            relief="raised",
            bd=2
        )
        btn_recargar.pack(side="left", padx=5)
        
        if not self.es_ventana_principal:
            btn_volver = tk.Button(
                frame_botones_inf,
                text="← Volver al Menú",
                command=self.ventana.destroy,
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
        try:
            self.tabla_productos.delete(*self.tabla_productos.get_children())
            
            productos = Producto.obtener_productos()
            
            for i, producto in enumerate(productos):
                tag = "oddrow" if i % 2 == 0 else "evenrow"
                self.tabla_productos.insert(
                    "",
                    "end",
                    tags=(tag,),
                    values=(producto.id_producto, producto.nombre, producto.categoria, f"${producto.precio:.0f}", producto.stock)
                )
            
            self.tabla_productos.tag_configure("oddrow", background="#F8F9F9")
            self.tabla_productos.tag_configure("evenrow", background="#FFFFFF")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar productos:\n{str(e)}")

    def seleccionar_producto(self, event):
        """Selecciona un producto y carga sus datos en el formulario"""
        try:
            selection = self.tabla_productos.selection()
            if not selection:
                return
            
            item = selection[0]
            valores = self.tabla_productos.item(item, "values")
            
            self.producto_seleccionado = int(valores[0])
            
            self.entry_id.config(state="normal")
            self.entry_id.delete(0, "end")
            self.entry_id.insert(0, valores[0])
            self.entry_id.config(state="readonly")
            
            self.entry_nombre.delete(0, "end")
            self.entry_nombre.insert(0, valores[1])
            
            self.entry_categoria.delete(0, "end")
            self.entry_categoria.insert(0, valores[2])
            
            self.entry_precio.delete(0, "end")
            self.entry_precio.insert(0, valores[3].replace("$", ""))
            
            self.entry_stock.delete(0, "end")
            self.entry_stock.insert(0, valores[4])
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al seleccionar producto:\n{str(e)}")

    def registrar_producto(self):
        """Registra un nuevo producto"""
        try:
            nombre = self.entry_nombre.get().strip()
            categoria = self.entry_categoria.get().strip()
            precio_str = self.entry_precio.get().strip()
            stock_str = self.entry_stock.get().strip()
            
            if not nombre or not categoria or not precio_str or not stock_str:
                messagebox.showwarning("Advertencia", "Completa todos los campos (excepto ID)")
                return
            
            precio = float(precio_str)
            stock = int(stock_str)
            
            if precio < 0 or stock < 0:
                messagebox.showwarning("Advertencia", "Precio y stock no pueden ser negativos")
                return
            
            # El ID se genera automáticamente, así que pasamos 0 como placeholder
            producto = Producto(0, nombre, categoria, precio, stock)
            producto.registrar()
            
            messagebox.showinfo("✓ Éxito", "Producto registrado correctamente")
            self.limpiar_formulario()
            self.cargar_productos()
            
        except ValueError:
            messagebox.showerror("Error", "Precio y Stock deben ser números válidos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar:\n{str(e)}")

    def actualizar_producto(self):
        """Actualiza el producto seleccionado"""
        try:
            if not self.producto_seleccionado:
                messagebox.showwarning("Advertencia", "Selecciona un producto para actualizar")
                return
            
            nombre = self.entry_nombre.get().strip()
            categoria = self.entry_categoria.get().strip()
            precio_str = self.entry_precio.get().strip()
            stock_str = self.entry_stock.get().strip()
            
            if not nombre or not categoria or not precio_str or not stock_str:
                messagebox.showwarning("Advertencia", "Completa todos los campos")
                return
            
            precio = float(precio_str)
            stock = int(stock_str)
            
            if precio < 0 or stock < 0:
                messagebox.showwarning("Advertencia", "Precio y stock no pueden ser negativos")
                return
            
            producto = Producto(self.producto_seleccionado, nombre, categoria, precio, stock)
            producto.actualizar()
            
            messagebox.showinfo("✓ Éxito", "Producto actualizado correctamente")
            self.limpiar_formulario()
            self.cargar_productos()
            
        except ValueError:
            messagebox.showerror("Error", "Precio y Stock deben ser números válidos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar:\n{str(e)}")

    def eliminar_producto(self):
        """Elimina el producto seleccionado"""
        try:
            if not self.producto_seleccionado:
                messagebox.showwarning("Advertencia", "Selecciona un producto para eliminar")
                return
            
            nombre = self.entry_nombre.get()
            
            if messagebox.askyesno("Confirmar", f"¿Deseas eliminar el producto '{nombre}'?"):
                Producto.eliminar(self.producto_seleccionado)
                messagebox.showinfo("✓ Éxito", "Producto eliminado correctamente")
                self.limpiar_formulario()
                self.cargar_productos()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar:\n{str(e)}")

    def limpiar_formulario(self):
        """Limpia el formulario"""
        self.entry_id.config(state="normal")
        self.entry_id.delete(0, "end")
        
        self.entry_nombre.delete(0, "end")
        self.entry_categoria.delete(0, "end")
        self.entry_precio.delete(0, "end")
        self.entry_stock.delete(0, "end")
        
        self.producto_seleccionado = None


if __name__ == "__main__":
    GestionarProductos()
