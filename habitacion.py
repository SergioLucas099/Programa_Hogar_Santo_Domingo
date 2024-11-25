from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from tkcalendar import Calendar
import sqlite3
import os
import sys
from datetime import datetime
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

class Habitacion(tk.Toplevel):
    def __init__(self, parent, container):
        super().__init__(parent)
        self.container = container
        self.title("Datos Habitacion")
        # Dimensiones de la ventana
        width = 1000
        height = 600

        # Obtener el tamaño de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calcular las coordenadas x e y para centrar la ventana
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2) - 25

        # Establecer la geometría de la ventana centrada
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.config(bg="#fffce3")        
        self.widgets()
        self.iconbitmap("icono.ico")

    def widgets(self):
        frametitulo = tk.Frame(self, bg="#fffce3")
        frametitulo.pack()
        frametitulo.place(x=0, y=0, width=1100, height=80)

        titulo = tk.Label(self, text="Datos Habitación", bg="#fffce3", font="sans 35 bold", anchor="center")
        titulo.pack()
        titulo.place(x=0, y=0, width=1000, height=80)

        framecontenido = tk.LabelFrame(self, bg="#fffce3", text="Información", font="sans 13 bold")
        framecontenido.place(x=635, y=90, width=350, height=400)

        def validar(event):
            # Permitir solo números y la tecla de retroceso
            if event.char.isdigit() or event.keysym == "BackSpace":
                return
            else:
                return "break"
            
        self.lblnumeroCodigo = Label(framecontenido, text="Codigo:", font="sans 15 bold", bg="#fffce3")
        self.lblnumeroCodigo.place(x=10, y=20)
        self.entrynumeroCodigo = tk.Entry(framecontenido, font="sans 15")
        self.entrynumeroCodigo.bind("<KeyPress>", validar)
        self.entrynumeroCodigo.place(x=100, y=20, width=130, height=30)

        self.lblNumero = Label(framecontenido, text="Número:", font="sans 15 bold", bg="#fffce3")
        self.lblNumero.place(x=10, y=60)
        self.entryNumero = tk.Entry(framecontenido, font="sans 15")
        self.entryNumero.place(x=100, y=60, width=235, height=30)

        self.lblTipo = Label(framecontenido, text="Tipo:", font="sans 15 bold", bg="#fffce3")
        self.lblTipo.place(x=10, y=100)
        self.rol_Tipo = StringVar(framecontenido)
        self.rol_Tipo.set("Sencilla")
        opciones_Tipo = ["Sencilla","Premium"]
        self.menu_Tipo = OptionMenu(framecontenido, self.rol_Tipo, *opciones_Tipo)
        self.menu_Tipo.config(font="sans 13")
        self.menu_Tipo.place(x=120, y=100, width=220, height=30)

        self.lblEstado = Label(framecontenido, text="Estado:", font="sans 15 bold", bg="#fffce3")
        self.lblEstado.place(x=10, y=140)
        self.rol_Estado = StringVar(framecontenido)
        self.rol_Estado.set("Disponible")
        opciones_Estado = ["Disponible","Ocupada"]
        self.menu_Estado = OptionMenu(framecontenido, self.rol_Estado, *opciones_Estado)
        self.menu_Estado.config(font="sans 13")
        self.menu_Estado.place(x=120, y=140, width=220, height=30)

        cursor.execute("SELECT Nombre FROM tabla_ancianos")
        nombres = [fila[0] for fila in cursor.fetchall()]

        self.lblAnciano = Label(framecontenido, text="Anciano:", font="sans 15 bold", bg="#fffce3")
        self.lblAnciano.place(x=10, y=180)
        self.rol_Anciano = StringVar(framecontenido)
        self.rol_Anciano.set("Seleccionar nombre")
        # Verificar si nombres es válido
        if not nombres or not isinstance(nombres, list):
            nombres = ["No hay nombres disponibles"]
        self.menu_Anciano = OptionMenu(framecontenido, self.rol_Anciano, *nombres)
        self.menu_Anciano.config(font="sans 13")
        self.menu_Anciano.place(x=120, y=180, width=220, height=30)

        self.lblDescripcion = Label(framecontenido, text="Descripción:", font="sans 15 bold", bg="#fffce3")
        self.lblDescripcion.place(x=10, y=220)
        self.entryDescripcion = tk.Text(framecontenido, font="sans 15")
        self.entryDescripcion.place(x=10, y=258, width=320, height=100)

        framecontenidoTabla = tk.Frame(self, bg="#fffce3")
        framecontenidoTabla.place(x=0, y=70, width=630, height=600)

        self.imagen_Buscar = Image.open("imagenes/buscar.png")
        self.imagen_redimensionadaBuscar = self.imagen_Buscar.resize((35, 35))  # Cambia los valores según el tamaño que desees
        self.icono_btn_Buscar = ImageTk.PhotoImage(self.imagen_redimensionadaBuscar)
        self.btn_Buscar = Button(framecontenidoTabla, image=self.icono_btn_Buscar, padx=20, pady=10, bg="#fffce3", font="sans 22 bold", compound="top", command=self.buscarInfo, borderwidth=0, highlightthickness=0)
        self.btn_Buscar.place(x=160, y=0, width=60, height=80)

        self.entryBuscarDato = tk.Entry(framecontenidoTabla, font="sans 15")
        self.entryBuscarDato.place(x=220, y=20, width=280, height=40)

        treFrame = tk.Frame(framecontenidoTabla, bg="#fffce3")
        treFrame.place(x=10, y=75, width=620, height=350)
        
        scroll_y = ttk.Scrollbar(treFrame, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)

        # Crear estilos para la cabecera y datos de la tabla
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("sans", 15, "bold"), foreground="#050026")  # Fuente y color para cabecera
        style.configure("Treeview", font=("sans", 11))  # Fuente para los datos

        self.tree_habitacion = ttk.Treeview(treFrame, columns=("Codigo", "Numero", "Tipo", "Estado", "Nombre Anciano", "Descripción Habitación"), show="headings", height=50, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_y.config(command=self.tree_habitacion.yview)
        scroll_x.config(command=self.tree_habitacion.xview)

        self.tree_habitacion.bind('<<TreeviewSelect>>', self.seleccionarDatosHabitacion)

        self.tree_habitacion.heading("#1", text="Codigo")             
        self.tree_habitacion.heading("#2", text="Numero")        
        self.tree_habitacion.heading("#3", text="Tipo")
        self.tree_habitacion.heading("#4", text="Estado")
        self.tree_habitacion.heading("#5", text="Nombre Anciano")
        self.tree_habitacion.heading("#6", text="Descripción Habitación")

        self.tree_habitacion.column("Codigo", width=120, anchor="center")
        self.tree_habitacion.column("Numero", width=100, anchor="center")
        self.tree_habitacion.column("Tipo", width=150, anchor="center")
        self.tree_habitacion.column("Estado", width=160, anchor="center")
        self.tree_habitacion.column("Nombre Anciano", width=250, anchor="center")
        self.tree_habitacion.column("Descripción Habitación", width=380, anchor="center")

        self.tree_habitacion.pack(expand=True, fill=BOTH)

        try:
            cursor.execute("SELECT * FROM tabla_habitacion")
            datos = cursor.fetchall()
            for dato in datos:
                self.tree_habitacion.insert("", "end", values=dato)
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error al cargar los datos: {e}")

        self.imagen_Crear = Image.open("imagenes/crear.png")
        self.imagen_redimensionadaCrear = self.imagen_Crear.resize((50, 50))  # Cambia los valores según el tamaño que desees
        self.icono_btn_Crear = ImageTk.PhotoImage(self.imagen_redimensionadaCrear)
        self.btn_Crear = Button(framecontenidoTabla, text="Crear", image=self.icono_btn_Crear, padx=20, pady=10, bg="#fffce3", font="sans 18 bold", compound="top", command=self.crearDatoHabitacion, borderwidth=0, highlightthickness=0)
        self.btn_Crear.place(x=50, y=430, width=60, height=80)

        self.imagen_Actualizar = Image.open("imagenes/actualizar.png")
        self.imagen_redimensionadaActualizar = self.imagen_Actualizar.resize((50, 50))  # Cambia los valores según el tamaño que desees
        self.icono_btn_Actualizar = ImageTk.PhotoImage(self.imagen_redimensionadaActualizar)
        self.btn_Actualizar = Button(framecontenidoTabla, text="Actualizar", image=self.icono_btn_Actualizar, padx=20, pady=5, bg="#fffce3", font="sans 18 bold", compound="top", command=self.actualizar_tabla_personal, borderwidth=0, highlightthickness=0)
        self.btn_Actualizar.place(x=180, y=430, width=120, height=90)

        self.imagen_Borrar = Image.open("imagenes/borrar.png")
        self.imagen_redimensionadaBorrar = self.imagen_Borrar.resize((50, 50))  # Cambia los valores según el tamaño que desees
        self.icono_btn_Borrar = ImageTk.PhotoImage(self.imagen_redimensionadaBorrar)
        self.btn_Borrar = Button(framecontenidoTabla, text="Borrar", image=self.icono_btn_Borrar, padx=20, pady=5, bg="#fffce3", font="sans 18 bold", compound="top", command=self.eliminarDatoHabitacion, borderwidth=0, highlightthickness=0)
        self.btn_Borrar.place(x=340, y=430, width=120, height=90)

        self.imagen_Limpiar = Image.open("imagenes/limpiar.png")
        self.imagen_redimensionadaLimpiar = self.imagen_Limpiar.resize((50, 50))  # Cambia los valores según el tamaño que desees
        self.icono_btn_Limpiar = ImageTk.PhotoImage(self.imagen_redimensionadaLimpiar)
        self.btn_Limpiar = Button(framecontenidoTabla, text="Limpiar", image=self.icono_btn_Limpiar, padx=20, pady=5, bg="#fffce3", font="sans 18 bold", compound="top", command=self.limpiar, borderwidth=0, highlightthickness=0)
        self.btn_Limpiar.place(x=490, y=430, width=120, height=90)

    def buscarInfo (self):
            nombre_buscado = self.entryBuscarDato.get()

            # Limpiar el Treeview
            for item in self.tree_habitacion.get_children():
                self.tree_habitacion.delete(item)

            # Buscar en la base de datos
            try:
                cursor.execute("SELECT * FROM tabla_ancianos WHERE NombreAnciano LIKE %s", ('%' + nombre_buscado + '%',))
                registros = cursor.fetchall()

                # Mostrar los datos encontrados o mensaje de error
                if registros:
                    for registro in registros:
                        self.tree_habitacion.insert("", "end", values=registro)
                else:
                    messagebox.showinfo("Aviso", "No se encontró ningún registro con ese nombre.")

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"No se pudo realizar la búsqueda: {e}")

    def crearDatoHabitacion (self):
        codigo = self.entrynumeroCodigo.get()
        numero = self.entryNumero.get()
        tipo = self.rol_Tipo.get()
        estado = self.rol_Estado.get()
        nombreAnciano = self.rol_Anciano.get()
        descripcion = self.entryDescripcion.get("1.0", "end-1c")

        # Validar campos antes de insertar en la base de datos
        if not codigo or not numero or not tipo or not estado or not nombreAnciano or not descripcion:
            messagebox.showerror("Error", "Por favor, completa todos los campos obligatorios.")
            return

        # Insertar en la base de datos
        try:
            cursor.execute("INSERT INTO tabla_habitacion (Codigo, Numero, Tipo, Estado, NombreAnciano, Descripcion) VALUES (%s, %s, %s, %s, %s, %s)",
                        (codigo, numero, tipo, estado, nombreAnciano, descripcion))
            conn.commit()
            messagebox.showinfo("Éxito", "Registro creado con éxito.")
            self.tree_habitacion.insert("", "end", values=(codigo, numero, tipo, estado, nombreAnciano, descripcion))
            self.limpiar()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error al crear registro: {e}")
    
    def eliminarDatoHabitacion (self):
        selected_item = self.tree_habitacion.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un registro para eliminar.")
            return
        
        # Confirmar eliminación
        if messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas eliminar el registro seleccionado?"):
            codigo = self.tree_habitacion.item(selected_item)["values"][0]
            try:
                cursor.execute("DELETE FROM tabla_habitacion WHERE Codigo = %s", (codigo,))
                conn.commit()
                self.tree_habitacion.delete(selected_item)
                messagebox.showinfo("Éxito", "Registro eliminado con éxito.")
                self.limpiar()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al eliminar registro: {e}")

    def actualizar_tabla_personal (self):
        codigo = self.entrynumeroCodigo.get()
        numero = self.entryNumero.get()
        tipo = self.rol_Tipo.get()
        estado = self.rol_Estado.get()
        nombreAnciano = self.rol_Anciano.get()
        descripcion = self.entryDescripcion.get("1.0", "end-1c")

        try:
            # Actualizar los datos de la tabla ancianos
            cursor.execute("""
                UPDATE tabla_habitacion
                SET Numero = %s, Tipo = %s, Estado = %s, NombreAnciano = %s, Descripcion = %s
                WHERE Codigo = %s
            """, (numero, tipo, estado, nombreAnciano, descripcion, codigo))
            conn.commit()

            # Verificar si se actualizó algún registro
            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", "Información actualizada exitosamente")
                self.actualizar_treeview()
                self.limpiar()
                
            else:
                messagebox.showwarning("Aviso", "No se encontró ningún dato con ese ID.")

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo actualizar el dato: {e}")
    
    def actualizar_treeview(self):
        # Limpiar el Treeview actual
        for item in self.tree_habitacion.get_children():
            self.tree_habitacion.delete(item)

        # Conectar a la base de datos y obtener los datos actualizados
        cursor.execute("SELECT * FROM tabla_habitacion")
        registros = cursor.fetchall()

        # Insertar los datos en el Treeview
        for registro in registros:
            self.tree_habitacion.insert("", "end", values=registro)

    def limpiar (self):
        self.entrynumeroCodigo.config(state="normal")
        self.entrynumeroCodigo.delete(0, END)
        self.entryNumero.delete(0, END)
        self.rol_Tipo.set("Sencilla")
        self.rol_Estado.set("Disponible")
        self.rol_Anciano.set("Seleccionar nombre")
        self.entryDescripcion.delete("1.0", "end")

    def seleccionarDatosHabitacion (self, event):
        selected_item = self.tree_habitacion.selection()
        if selected_item:
            item = self.tree_habitacion.item(selected_item)
            datos = item['values']

            self.entrynumeroCodigo.config(state="normal")  # Habilitar la edición temporalmente para mostrar el ID
            self.entrynumeroCodigo.delete(0, tk.END)
            self.entrynumeroCodigo.insert(0, datos[0])
            self.entrynumeroCodigo.config(state="disabled")  # Deshabilitar nuevamente después de mostrar el ID
            self.entryNumero.delete(0, tk.END)
            self.entryNumero.insert(0, datos[1])
            self.rol_Tipo.set(datos[2])
            self.rol_Estado.set(datos[3])
            self.rol_Anciano.set(datos[4])
            self.entryDescripcion.delete("1.0", "end")
            self.entryDescripcion.insert("1.0", datos[5])