import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import ttk, messagebox
from Logica.ventas_servicio import VentaServicio


class ConsultaVentas:

    def __init__(self, parent=None):
        if parent is None:
            self.ventana = tk.Tk()
            self.ventana.title("Consulta de Ventas")
            self.ventana.geometry("1200x650")
            self.ventana.resizable(True, True)
            self.es_ventana_principal = True
        else:
            self.ventana = tk.Toplevel(parent)
            self.ventana.title("Consulta de Ventas")
            self.ventana.geometry("1200x650")
            self.es_ventana_principal = False
        
        # Colores
        self.color_principal = "#2C3E50"
        self.color_secundario = "#34495E"
        self.color_acento = "#E74C3C"
        self.color_exito = "#27AE60"
        self.color_fondo = "#ECF0F1"
        self.color_texto = "#2C3E50"
        
        # Configurar estilos
        self.configurar_estilos()
        
        # Fondo
        self.ventana.configure(bg=self.color_fondo)
        
        # Crear interfaz
        self.crear_encabezado()
        self.crear_contenido()
        self.cargar_ventas()
        
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
            text="📊 CONSULTA DE VENTAS REALIZADAS",
            font=("Segoe UI", 18, "bold"),
            bg=self.color_principal,
            fg="white"
        )
        title.pack(pady=15)
        
        divider = tk.Frame(self.ventana, bg=self.color_acento, height=2)
        divider.pack(fill="x", padx=0, pady=0)

    def crear_contenido(self):
        frame_contenido = ttk.Frame(self.ventana)
        frame_contenido.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Frame para tabla de ventas
        frame_tabla = ttk.Frame(frame_contenido)
        frame_tabla.pack(fill="both", expand=True, side="top")
        
        titulo = tk.Label(
            frame_tabla,
            text="Ventas Registradas",
            font=("Segoe UI", 12, "bold"),
            bg=self.color_secundario,
            fg="white",
            pady=8
        )
        titulo.pack(fill="x")
        
        frame_scroll = ttk.Frame(frame_tabla)
        frame_scroll.pack(fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(frame_scroll)
        scrollbar.pack(side="right", fill="y")
        
        self.tabla_ventas = ttk.Treeview(
            frame_scroll,
            columns=("id_venta", "fecha", "total"),
            show="headings",
            yscrollcommand=scrollbar.set,
            height=15
        )
        scrollbar.config(command=self.tabla_ventas.yview)
        
        self.tabla_ventas.column("id_venta", width=100, anchor="center")
        self.tabla_ventas.column("fecha", width=200, anchor="center")
        self.tabla_ventas.column("total", width=150, anchor="center")
        
        self.tabla_ventas.heading("id_venta", text="ID Venta")
        self.tabla_ventas.heading("fecha", text="Fecha")
        self.tabla_ventas.heading("total", text="Total")
        
        self.tabla_ventas.pack(fill="both", expand=True)
        self.tabla_ventas.bind("<<TreeviewSelect>>", self.mostrar_detalle)
        
        # Frame para detalles
        frame_detalle = tk.Frame(self.ventana, bg=self.color_secundario, height=150)
        frame_detalle.pack(fill="x", padx=0, pady=0)
        frame_detalle.pack_propagate(False)
        
        titulo_detalle = tk.Label(
            frame_detalle,
            text="Detalle de la Venta",
            font=("Segoe UI", 11, "bold"),
            bg=self.color_secundario,
            fg="white",
            pady=5
        )
        titulo_detalle.pack(fill="x", padx=10)
        
        self.label_detalle = tk.Label(
            frame_detalle,
            text="Selecciona una venta para ver los detalles",
            font=("Segoe UI", 10),
            bg=self.color_secundario,
            fg="white",
            justify="left",
            wraplength=1180
        )
        self.label_detalle.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Frame de botones
        frame_botones = tk.Frame(self.ventana, bg=self.color_fondo)
        frame_botones.pack(fill="x", padx=10, pady=10)
        
        btn_recargar = tk.Button(
            frame_botones,
            text="🔄 Recargar",
            command=self.cargar_ventas,
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
        
        btn_cerrar = tk.Button(
            frame_botones,
            text="✕ Cerrar",
            command=self.ventana.destroy,
            bg=self.color_acento,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=6,
            cursor="hand2",
            relief="raised",
            bd=2
        )
        btn_cerrar.pack(side="right", padx=5)
        
        # Botón Volver al Menú (solo si es ventana secundaria)
        if not self.es_ventana_principal:
            btn_volver = tk.Button(
                frame_botones,
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
            btn_volver.pack(side="right", padx=(5, 15))

    def cargar_ventas(self):
        """Carga todas las ventas en la tabla"""
        try:
            self.tabla_ventas.delete(*self.tabla_ventas.get_children())
            
            ventas = VentaServicio.obtener_ventas()
            
            if not ventas:
                messagebox.showinfo("Información", "No hay ventas registradas")
                return
            
            for i, venta in enumerate(ventas):
                tag = "oddrow" if i % 2 == 0 else "evenrow"
                id_venta, fecha, total = venta
                self.tabla_ventas.insert(
                    "",
                    "end",
                    tags=(tag,),
                    values=(id_venta, fecha, f"${total:.2f}")
                )
            
            self.tabla_ventas.tag_configure("oddrow", background="#F8F9F9")
            self.tabla_ventas.tag_configure("evenrow", background="#FFFFFF")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar ventas:\n{str(e)}")

    def mostrar_detalle(self, event):
        """Muestra el detalle de la venta seleccionada"""
        try:
            selection = self.tabla_ventas.selection()
            if not selection:
                return
            
            item = selection[0]
            valores = self.tabla_ventas.item(item, "values")
            id_venta = int(valores[0])
            
            detalle = VentaServicio.obtener_detalle_venta(id_venta)
            
            if not detalle:
                self.label_detalle.config(text="No hay detalle para esta venta")
                return
            
            texto_detalle = f"Venta #{id_venta}:\n\n"
            total = 0
            for item_detalle in detalle:
                id_detalle, id_prod, nombre, categoria, cantidad, precio_unit = item_detalle
                subtotal = cantidad * precio_unit
                total += subtotal
                texto_detalle += f"• {nombre} [{categoria}]: {cantidad} x ${precio_unit:.0f} = ${subtotal:.2f}\n"
            
            texto_detalle += f"\n{'='*50}\nTOTAL: ${total:.2f}"
            
            self.label_detalle.config(text=texto_detalle)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar detalle:\n{str(e)}")


if __name__ == "__main__":
    ConsultaVentas()
