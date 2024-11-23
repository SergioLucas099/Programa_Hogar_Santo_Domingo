from tkinter import *
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import os
import sys
from ventana_principal import VentanaPrincipal
from usuarios import Usuarios
import mysql.connector

# Conexión con la base de datos sqlite3
conn = sqlite3.connect('Hogar_Santo_Domingo.db')
cursor = conn.cursor()

# Conexión con la base de datos Mysql
connMysql = mysql.connector.connect(
        host="localhost",  # Siempre será localhost en XAMPP
        user="root",       # O el nombre de usuario que creaste
        password="",       # Contraseña (vacía si usas root)
        database="base_datos_hogar_santo_domingo"  # Nombre de tu base de datos
    )

cursorMysql = connMysql.cursor()

class Container(tk.Frame):
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        self.pack()
        self.place(x=0, y=0, width=1000, height=600)
        self.config(bg="#fffce3")
        self.widgets()

    # ------Funcion que muestres las distintas ventanas del proyecto------
    def show_frames(self, container):
        top_level = tk.Toplevel(self)
        frame = container(top_level, self.controlador)
        frame.config(bg="#fffce3")
        frame.pack(fill="both", expand=True)
        width = 1000
        height = 600
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2) - 25
        top_level.geometry(f"{width}x{height}+{x}+{y}")
        top_level.resizable(False, False)

        ruta=self.rutas(r"icono.ico")
        top_level.iconbitmap(ruta)
    
    def rutas(self, ruta):
        try:
            rutabase = sys.__MEIPASS
        except Exception:
            rutabase = os.path.abspath(".")
        return os.path.join(rutabase,ruta)
    
    def iniciar_sesion(self):
        dato_usuario = self.usuario.get()
        dato_contraseña = self.contraseña.get()

        # Consulta para verificar las credenciales
        cursor.execute("SELECT Id, NombreCompleto FROM Usuarios WHERE Correo=? AND Contraseña=?", (dato_usuario, dato_contraseña))
        resultado = cursor.fetchone()

        if resultado:            
            self.controlador.withdraw() # Destruye Ventana
            self.show_frames(VentanaPrincipal)
        elif dato_usuario == "adminPrincipal" and dato_contraseña =="1234":
            self.controlador.withdraw()
            self.show_frames(Usuarios)
        else:
            messagebox.showerror("Error", "Nombre o contraseña incorrectos")

        self.usuario.delete(0, tk.END)  # Limpia el contenido de la casilla de texto
        self.contraseña.delete(0, tk.END)  # Limpia el contenido de la casilla de texto
    
    def widgets(self):
        frametitulo = tk.Frame(self, bg="#fffce3")
        frametitulo.pack()
        frametitulo.place(x=0, y=0, width=1100, height=80)

        titulo = tk.Label(self, text="Gestor de Datos - Hogar Santo Domingo", bg="#fffce3", font="sans 35 bold", anchor="center")
        titulo.pack()
        titulo.place(x=0, y=0, width=1000, height=80)

        framecontenido = tk.Frame(self, bg="#fffce3")
        framecontenido.place(x=0, y=100, width=1100, height=550)

        self.logo_image = Image.open("imagenes/logo.png")
        self.logo_image = self.logo_image.resize((450,450))
        self.logo_image = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = tk.Label(framecontenido, image=self.logo_image, bg="#fffce3")
        self.logo_label.place(x=50, y=10)

        labelframe = LabelFrame(framecontenido, text="Iniciar Sesión", font="sans 30 bold", bg="#fffce3")
        labelframe.place(x=530, y=35, width=450, height=380)

        lblusuario = Label(labelframe, text="Usuario: ", font="sans 23 bold", bg="#fffce3")
        lblusuario.place(x=5, y=40)
        self.usuario = tk.Entry(labelframe, font="sans 20 bold")
        self.usuario.place(x=140, y=40, width=295, height=40)

        lblcontraseña = Label(labelframe, text="Contraseña: ", font="sans 23 bold", bg="#fffce3")
        lblcontraseña.place(x=5, y=130)
        self.contraseña = tk.Entry(labelframe, font="sans 23 bold", show="*")
        self.contraseña.place(x=190, y=130, width=240, height=40)

        # Variable para el estado del checkbox
        mostrar_contraseña_var = BooleanVar()

        # Función para mostrar/ocultar la contraseña
        def toggle_contraseña():
            if mostrar_contraseña_var.get():
                self.contraseña.config(show="")
            else:
                self.contraseña.config(show="*")

        # Checkbox para mostrar/ocultar la contraseña
        checkbox = Checkbutton(
            labelframe,
            text="Mostrar contraseña",
            font="sans 12",
            bg="#fffce3",
            variable=mostrar_contraseña_var,
            command=toggle_contraseña
        )
        checkbox.place(x=260, y=170)

        self.boton_imagen = Image.open("imagenes/iniciosesion.png")
        self.boton_imagen = self.boton_imagen.resize((50,50))
        self.boton_imagen = ImageTk.PhotoImage(self.boton_imagen)
        boton_ingresar = tk.Button(labelframe, text="Ingresar", font="sans 20 bold", bg="#fffce3", command=self.iniciar_sesion ,borderwidth=0, highlightthickness=0)
        boton_ingresar.config(image=self.boton_imagen, compound=TOP, padx=20, pady=10)
        boton_ingresar.place(x=150, y=220, width=145, height=90)