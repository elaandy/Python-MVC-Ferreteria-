import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import messagebox


class LoginWindow:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Ferretería Pegatriplex - Login")
        self.ventana.geometry("900x550")
        self.ventana.resizable(False, False)
        self.ventana.config(bg="#ffffff")
        
        # Colores modernos
        self.color_principal = "#6366f1"
        self.color_secundario = "#4f46e5"
        self.color_hover = "#4338ca"
        self.color_fondo = "#f8fafc"
        self.color_texto = "#1e293b"
        self.color_gris = "#94a3b8"
        
        # Variables
        self.remember_me_var = tk.BooleanVar()
        
        # Crear interfaz
        self.crear_interfaz()
        
        # Centrar ventana
        self.centrar_ventana()
        
        self.ventana.mainloop()

    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.ventana.update_idletasks()
        ancho = self.ventana.winfo_width()
        alto = self.ventana.winfo_height()
        x = (self.ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (alto // 2)
        self.ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    def crear_interfaz(self):
        """Crea la interfaz del login"""
        
        # Frame principal izquierdo - Ilustración
        frame_izquierdo = tk.Frame(self.ventana, bg=self.color_principal, width=450)
        frame_izquierdo.pack(side="left", fill="both", expand=True)
        frame_izquierdo.pack_propagate(False)
        
        # Contenido lado izquierdo
        frame_contenido_iz = tk.Frame(frame_izquierdo, bg=self.color_principal)
        frame_contenido_iz.pack(fill="both", expand=True, padx=40, pady=60)
        
        # Logo/Ícono
        logo = tk.Label(
            frame_contenido_iz,
            text="🏪",
            font=("Segoe UI", 80),
            bg=self.color_principal
        )
        logo.pack(pady=(20, 10))
        
        # Título
        titulo_iz = tk.Label(
            frame_contenido_iz,
            text="FERRETERÍA",
            font=("Segoe UI", 22, "bold"),
            bg=self.color_principal,
            fg="white"
        )
        titulo_iz.pack()
        
        titulo_iz2 = tk.Label(
            frame_contenido_iz,
            text="PEGATRIPLEX SAS",
            font=("Segoe UI", 18, "bold"),
            bg=self.color_principal,
            fg="white"
        )
        titulo_iz2.pack(pady=(5, 30))
        
        # Descripción
        descripcion = tk.Label(
            frame_contenido_iz,
            text="Sistema de Gestión",
            font=("Segoe UI", 12),
            bg=self.color_principal,
            fg="white"
        )
        descripcion.pack()
        
        # Frame principal derecho - Formulario
        frame_derecho = tk.Frame(self.ventana, bg=self.color_fondo, width=450)
        frame_derecho.pack(side="right", fill="both", expand=True)
        frame_derecho.pack_propagate(False)
        
        # Contenido lado derecho
        frame_form = tk.Frame(frame_derecho, bg=self.color_fondo)
        frame_form.pack(fill="both", expand=True, padx=50, pady=60)
        
        # Título formulario
        titulo_form = tk.Label(
            frame_form,
            text="Iniciar Sesión",
            font=("Segoe UI", 24, "bold"),
            bg=self.color_fondo,
            fg=self.color_texto
        )
        titulo_form.pack(pady=(0, 5))
        
        # Subtítulo
        subtitulo = tk.Label(
            frame_form,
            text="Ingresa tus credenciales",
            font=("Segoe UI", 10),
            bg=self.color_fondo,
            fg=self.color_gris
        )
        subtitulo.pack(pady=(0, 30))
        
        # CAMPO USERNAME
        label_user = tk.Label(
            frame_form,
            text="👤 Usuario",
            font=("Segoe UI", 10, "bold"),
            bg=self.color_fondo,
            fg=self.color_texto
        )
        label_user.pack(anchor="w", pady=(0, 8))
        
        self.entry_username = tk.Entry(
            frame_form,
            font=("Segoe UI", 11),
            bg="white",
            fg=self.color_texto,
            border=0,
            relief="flat"
        )
        self.entry_username.pack(fill="x", ipady=12)
        
        # Separador
        sep1 = tk.Frame(frame_form, bg="#e2e8f0", height=1)
        sep1.pack(fill="x", pady=8)
        
        # CAMPO PASSWORD
        label_pass = tk.Label(
            frame_form,
            text="🔒 Contraseña",
            font=("Segoe UI", 10, "bold"),
            bg=self.color_fondo,
            fg=self.color_texto
        )
        label_pass.pack(anchor="w", pady=(15, 8))
        
        self.entry_password = tk.Entry(
            frame_form,
            font=("Segoe UI", 11),
            bg="white",
            fg=self.color_texto,
            show="•",
            border=0,
            relief="flat"
        )
        self.entry_password.pack(fill="x", ipady=12)
        
        # Separador
        sep2 = tk.Frame(frame_form, bg="#e2e8f0", height=1)
        sep2.pack(fill="x", pady=8)
        
        # CHECKBOX REMEMBER ME
        frame_remember = tk.Frame(frame_form, bg=self.color_fondo)
        frame_remember.pack(anchor="w", pady=(20, 25))
        
        checkbox = tk.Checkbutton(
            frame_remember,
            text="Recordarme",
            variable=self.remember_me_var,
            font=("Segoe UI", 9),
            bg=self.color_fondo,
            fg=self.color_texto,
            selectcolor=self.color_fondo,
            activebackground=self.color_fondo,
            activeforeground=self.color_principal
        )
        checkbox.pack()
        
        # BOTÓN LOGIN
        boton_login = tk.Button(
            frame_form,
            text="Iniciar Sesión",
            font=("Segoe UI", 12, "bold"),
            bg=self.color_principal,
            fg="white",
            border=0,
            relief="flat",
            padx=20,
            pady=13,
            cursor="hand2",
            command=self.hacer_login,
            activebackground=self.color_hover,
            activeforeground="white"
        )
        boton_login.pack(fill="x", pady=(10, 0))
        
        # Bind Enter key
        self.entry_password.bind("<Return>", lambda e: self.hacer_login())
        self.entry_username.bind("<Return>", lambda e: self.entry_password.focus())

    def hacer_login(self):
        """Valida las credenciales del login"""
        usuario = self.entry_username.get().strip()
        contraseña = self.entry_password.get().strip()
        
        if not usuario or not contraseña:
            messagebox.showwarning("Validación", "Por favor ingresa usuario y contraseña")
            return
        
        # Aquí puedes agregar validación contra base de datos
        # Por ahora solo validamos credenciales de prueba
        if usuario == "admin" and contraseña == "admin":
            messagebox.showinfo("Éxito", f"¡Bienvenido {usuario}!")
            # Aquí iría el código para abrir el menú principal
            self.ventana.destroy()
            from menu import MenuPrincipal
            MenuPrincipal()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
            self.entry_password.delete(0, tk.END)


if __name__ == "__main__":
    login = LoginWindow()
