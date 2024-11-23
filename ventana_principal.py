from tkinter import *
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from anciano import Anciano
from personal import Personal
from medicamento import Medicamento
from habitacion import Habitacion
import sqlite3
import os
import sys

# Conectar a la base de datos
conn = sqlite3.connect('Hogar_Santo_Domingo.db')
cursor = conn.cursor()

class VentanaPrincipal(tk.Frame):
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

        titulo = tk.Label(self, text="Menú", bg="#fffce3", font="sans 45 bold", anchor="center")
        titulo.pack()
        titulo.place(x=0, y=0, width=1000, height=80)

        framecontenido = tk.Frame(self, bg="#fffce3")
        framecontenido.place(x=0, y=100, width=1100, height=550)

        self.logo_image = Image.open("imagenes/logo.png")
        self.logo_image = self.logo_image.resize((450,450))
        self.logo_image = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = tk.Label(framecontenido, image=self.logo_image, bg="#fffce3")
        self.logo_label.place(x=500, y=0)

        self.boton_imagen_anciano = Image.open("imagenes/ancianos.png")
        self.boton_imagen_anciano = self.boton_imagen_anciano.resize((60,60))
        self.boton_imagen_anciano = ImageTk.PhotoImage(self.boton_imagen_anciano)
        boton_ingresar_anciano = tk.Button(self, text="Anciano", font="sans 30 bold", bg="#fffce3", command=self.BotonAnciano, borderwidth=0, highlightthickness=0)
        boton_ingresar_anciano.config(image=self.boton_imagen_anciano, compound="left", padx=20, pady=10)
        boton_ingresar_anciano.place(x=25, y=80, width=280, height=80)

        self.boton_imagen_personal = Image.open("imagenes/personal.png")
        self.boton_imagen_personal = self.boton_imagen_personal.resize((60,60))
        self.boton_imagen_personal = ImageTk.PhotoImage(self.boton_imagen_personal)
        boton_ingresar_personal = tk.Button(self, text="Personal", font="sans 30 bold", bg="#fffce3", command=self.BotonPersonal, borderwidth=0, highlightthickness=0)
        boton_ingresar_personal.config(image=self.boton_imagen_personal, compound="left", padx=20, pady=10)
        boton_ingresar_personal.place(x=25, y=180, width=290, height=80)

        self.boton_imagen_medicamento = Image.open("imagenes/medicamento.png")
        self.boton_imagen_medicamento = self.boton_imagen_medicamento.resize((60,60))
        self.boton_imagen_medicamento = ImageTk.PhotoImage(self.boton_imagen_medicamento)
        boton_ingresar_medicamento = tk.Button(self, text="Medicamentos", font="sans 30 bold", bg="#fffce3", command=self.BotonMedicamento, borderwidth=0, highlightthickness=0)
        boton_ingresar_medicamento.config(image=self.boton_imagen_medicamento, compound="left", padx=20, pady=10)
        boton_ingresar_medicamento.place(x=25, y=280, width=390, height=80)

        self.boton_imagen_habitacion = Image.open("imagenes/dormitorio.png")
        self.boton_imagen_habitacion = self.boton_imagen_habitacion.resize((60,60))
        self.boton_imagen_habitacion = ImageTk.PhotoImage(self.boton_imagen_habitacion)
        boton_ingresar_habitacion = tk.Button(self, text="Habitación", font="sans 30 bold", bg="#fffce3", command=self.BotonHabitación, borderwidth=0, highlightthickness=0)
        boton_ingresar_habitacion.config(image=self.boton_imagen_habitacion, compound="left", padx=20, pady=10)
        boton_ingresar_habitacion.place(x=25, y=380, width=320, height=80)

        self.boton_imagen_salir = Image.open("imagenes/salir.png")
        self.boton_imagen_salir = self.boton_imagen_salir.resize((60,60))
        self.boton_imagen_salir = ImageTk.PhotoImage(self.boton_imagen_salir)
        boton_ingresar_salir = tk.Button(self, text="Salir", font="sans 30 bold", bg="#fffce3", command=self.Salir, borderwidth=0, highlightthickness=0)
        boton_ingresar_salir.config(image=self.boton_imagen_salir, compound="left", padx=20, pady=10)
        boton_ingresar_salir.place(x=25, y=500, width=210, height=80)

    def BotonAnciano(self):        
        VentanaAnciano = Anciano(self.parent, self.container)
        VentanaAnciano.tkraise()

    def BotonPersonal(self):
        VentanaPersonal = Personal(self.parent, self.container)
        VentanaPersonal.tkraise()

    def BotonMedicamento(self):
        VentanaMedicamento = Medicamento(self.parent, self.container)
        VentanaMedicamento.tkraise()

    def BotonHabitación(self):
        VentanaHabitacion = Habitacion(self.parent, self.container)
        VentanaHabitacion.tkraise()
    
    def Salir(self):
        response = messagebox.askquestion("Confirmación", "¿Seguro que quiere salir?")
        if response == 'yes':
            self.parent.destroy()  # Cierra `VentanaPrincipal`
            self.container.deiconify()  # Muestra `Container` correctamente