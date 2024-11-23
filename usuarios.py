from tkinter import *
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import mysql.connector

# # Conectar a la base de datos sqlite3
# conn = sqlite3.connect('Hogar_Santo_Domingo.db')
# cursor = conn.cursor()

# Conexión con la base de datos Mysql
conn = mysql.connector.connect(
        host="localhost",  # Siempre será localhost en XAMPP
        user="root",       # O el nombre de usuario que creaste
        password="",       # Contraseña (vacía si usas root)
        database="base_datos_hogar_santo_domingo"  # Nombre de tu base de datos
    )

cursor = conn.cursor()

class Usuarios(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(parent)
        self.parent = parent
        self.container = container  # Debe ser una instancia de `Tk`
        self.widgets()

        # Deshabilita el botón de cerrar
        self.parent.protocol("WM_DELETE_WINDOW", self.disable_event)

    def disable_event(self):
            pass  # No hace nada, por lo tanto, el botón de cerrar no funciona
    
    # ------Funcion que muestres las distintas ventanas del proyecto------
    def show_frames(self, container):
        top_level = tk.Toplevel(self)
        ruta=self.rutas(r"icono.ico")
        top_level.iconbitmap(ruta)
    
    def widgets(self):
        frametitulo = tk.Frame(self, bg="#fffce3")
        frametitulo.pack()
        frametitulo.place(x=0, y=0, width=1100, height=80)

        titulo = tk.Label(self, text="Crear Usuarios", bg="#fffce3", font="sans 35 bold", anchor="center")
        titulo.pack()
        titulo.place(x=0, y=0, width=1000, height=80)

        framecontenido = tk.Frame(self, bg="#fffce3")
        framecontenido.place(x=0, y=100, width=1100, height=550)

        def validar(event):
            # Permitir solo números y la tecla de retroceso
            if event.char.isdigit() or event.keysym == "BackSpace":
                return
            else:
                return "break"

        self.logo_image = Image.open("imagenes/logo.png")
        self.logo_image = self.logo_image.resize((450,450))
        self.logo_image = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = tk.Label(framecontenido, image=self.logo_image, bg="#fffce3")
        self.logo_label.place(x=500, y=0)

        self.lblnumeroDocumento = Label(framecontenido, text="Cédula:", font="sans 23 bold", bg="#fffce3")
        self.lblnumeroDocumento.place(x=30, y=20)
        self.entrynumeroDocumento = tk.Entry(framecontenido, font="sans 23")
        self.entrynumeroDocumento.bind("<KeyPress>", validar)
        self.entrynumeroDocumento.place(x=160, y=20, width=180, height=40)

        self.lblNombre = Label(framecontenido, text="Nombre:", font="sans 23 bold", bg="#fffce3")
        self.lblNombre.place(x=30, y=100)
        self.entryNombre = tk.Entry(framecontenido, font="sans 23")
        self.entryNombre.place(x=160, y=100, width=290, height=40)

        self.lblCorreo = Label(framecontenido, text="Correo:", font="sans 23 bold", bg="#fffce3")
        self.lblCorreo.place(x=30, y=180)
        self.entryCorreo = tk.Entry(framecontenido, font="sans 23")
        self.entryCorreo.place(x=160, y=180, width=290, height=40)

        self.lblContraseña = Label(framecontenido, text="Contraseña:", font="sans 23 bold", bg="#fffce3")
        self.lblContraseña.place(x=30, y=260)
        self.entryContraseña = tk.Entry(framecontenido, font="sans 23")
        self.entryContraseña.place(x=220, y=260, width=250, height=40)

        self.boton_imagen_crearUsuario = Image.open("imagenes/agregar_usuario.png")
        self.boton_imagen_crearUsuario = self.boton_imagen_crearUsuario.resize((50,50))
        self.boton_imagen_crearUsuario = ImageTk.PhotoImage(self.boton_imagen_crearUsuario)
        boton_ingresar_crearUsuario = tk.Button(self, font="sans 23 bold", bg="#fffce3", command=self.CrearUsuario, borderwidth=0, highlightthickness=0)
        boton_ingresar_crearUsuario.config(image=self.boton_imagen_crearUsuario, compound="left", padx=20, pady=10)
        boton_ingresar_crearUsuario.place(x=150, y=420, width=210, height=80)

        self.boton_imagen_salir = Image.open("imagenes/salir.png")
        self.boton_imagen_salir = self.boton_imagen_salir.resize((60,60))
        self.boton_imagen_salir = ImageTk.PhotoImage(self.boton_imagen_salir)
        boton_ingresar_salir = tk.Button(self, text="Salir", font="sans 30 bold", bg="#fffce3", command=self.Salir, borderwidth=0, highlightthickness=0)
        boton_ingresar_salir.config(image=self.boton_imagen_salir, compound="left", padx=20, pady=10)
        boton_ingresar_salir.place(x=25, y=500, width=210, height=80)

    def CrearUsuario (self):
        cedula = self.entrynumeroDocumento.get()
        nombre = self.entryNombre.get()
        correo = self.entryCorreo.get()
        contraseña = self.entryContraseña.get()

        if not all ([cedula, nombre, correo, contraseña]):
            messagebox.showerror("Error", "Por favor, completa todos los campos obligatorios.")
            return
        
        # Insertar en la base de datos
        try:
            cursor.execute(
                "INSERT INTO usuarios (Id, NombreCompleto, Correo, Contraseña) VALUES (%s, %s, %s, %s)",
                (cedula, nombre, correo, contraseña)
            )
            conn.commit()  # Confirma los cambios en la base de datos
            messagebox.showinfo("Éxito", "Usuario creado con éxito.")
            self.limpiar()  # Función para limpiar los campos del formulario
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error al crear registro: {e}")

    def limpiar (self):

        self.entrynumeroDocumento.delete(0, END)
        self.entryNombre.delete(0, END)
        self.entryCorreo.delete(0, END)
        self.entryContraseña.delete(0, END)

    def Salir(self):
        response = messagebox.askquestion("Confirmación", "¿Seguro que quiere salir?")
        if response == 'yes':
            self.parent.destroy()  # Cierra `VentanaPrincipal`
            self.container.deiconify()  # Muestra `Container` correctamente