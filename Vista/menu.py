import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from tkinter import messagebox
from cajero import AppFerreteria
from consulta_ventas import ConsultaVentas
from gestionar_productos import GestionarProductos


class MenuPrincipal:

    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Ferretería - Pegatriplex SAS")
        self.ventana.geometry("600x500")
        self.ventana.resizable(False, False)
        self.ventana.config(bg="#2C3E50")
        
        # Centrar ventana
        self.centrar_ventana()
        
        # Crear interfaz
        self.crear_menu()
        
        self.ventana.mainloop()

    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.ventana.update_idletasks()
        ancho = self.ventana.winfo_width()
        alto = self.ventana.winfo_height()
        x = (self.ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (alto // 2)
        self.ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    def crear_menu(self):
        """Crea la interfaz del menú principal"""
        
        # Encabezado
        frame_header = tk.Frame(self.ventana, bg="#E74C3C", height=100)
        frame_header.pack(fill="x", padx=0, pady=0)
        frame_header.pack_propagate(False)
        
        # Logo/Título principal
        titulo = tk.Label(
            frame_header,
            text="🏪 FERRETERÍA PEGATRIPLEX SAS",
            font=("Segoe UI", 22, "bold"),
            bg="#E74C3C",
            fg="white"
        )
        titulo.pack(pady=20)
        
        subtitulo = tk.Label(
            frame_header,
            text="Sistema de Ventas",
            font=("Segoe UI", 12),
            bg="#E74C3C",
            fg="white"
        )
        subtitulo.pack()
        
        # Frame de contenido
        frame_contenido = tk.Frame(self.ventana, bg="#2C3E50")
        frame_contenido.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Botones del menú
        botones_info = [
            {
                "texto": "💰 REALIZAR VENTA",
                "descripcion": "Accede al módulo de ventas para\nregistrar compras de clientes",
                "comando": self.abrir_cajero,
                "color": "#27AE60"
            },
            {
                "texto": "📊 CONSULTAR VENTAS",
                "descripcion": "Visualiza el historial de ventas\nrealizadas y sus detalles",
                "comando": self.abrir_consulta,
                "color": "#3498DB"
            },
            {
                "texto": "📦 GESTIONAR PRODUCTOS",
                "descripcion": "Registra, actualiza o elimina\nproductos del inventario",
                "comando": self.abrir_gestionar,
                "color": "#E67E22"
            }
        ]
        
        for i, btn_info in enumerate(botones_info):
            self.crear_boton_menu(
                frame_contenido,
                btn_info["texto"],
                btn_info["descripcion"],
                btn_info["comando"],
                btn_info["color"],
                i
            )
        
        # Frame de pie de página
        frame_footer = tk.Frame(self.ventana, bg="#34495E", height=40)
        frame_footer.pack(fill="x", padx=0, pady=0, side="bottom")
        frame_footer.pack_propagate(False)
        
        footer = tk.Label(
            frame_footer,
            text="Versión 1.0 © 2026 Pegatriplex SAS",
            font=("Segoe UI", 9),
            bg="#34495E",
            fg="white"
        )
        footer.pack(pady=10)

    def crear_boton_menu(self, parent, texto, descripcion, comando, color, posicion):
        """Crea un botón del menú con descripción"""
        
        frame_boton = tk.Frame(parent, bg=color, height=90)
        frame_boton.pack(fill="x", pady=15)
        frame_boton.pack_propagate(False)
        
        # Crear un botón con estilo personalizado
        btn = tk.Button(
            frame_boton,
            text=f"{texto}\n\n{descripcion}",
            command=comando,
            bg=color,
            fg="white",
            font=("Segoe UI", 13, "bold"),
            padx=20,
            pady=15,
            cursor="hand2",
            relief="raised",
            bd=3,
            wraplength=400,
            justify="left",
            activebackground="#1E8449" if color == "#27AE60" else "#2980B9" if color == "#3498DB" else "#D35400" if color == "#E67E22" else color,
            activeforeground="white"
        )
        btn.pack(fill="both", expand=True, padx=2, pady=2)

    def abrir_cajero(self):
        """Abre el módulo de ventas (cajero)"""
        try:
            self.ventana.withdraw()
            app = AppFerreteria(self.ventana)
            self.ventana.deiconify()
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir el módulo de ventas:\n{str(e)}")
            self.ventana.deiconify()

    def abrir_consulta(self):
        """Abre la consulta de ventas"""
        try:
            ConsultaVentas(self.ventana)
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir consulta de ventas:\n{str(e)}")

    def abrir_gestionar(self):
        """Abre la gestión de productos"""
        try:
            GestionarProductos(self.ventana)
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir gestión de productos:\n{str(e)}")


if __name__ == "__main__":
    MenuPrincipal()
