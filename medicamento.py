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

class Medicamento(tk.Toplevel):
    def __init__(self, parent, container):
        super().__init__(parent)
        self.container = container
        self.title("Datos Medicamentos")

        self.resizable(False, False)

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

        titulo = tk.Label(self, text="Datos Medicamento", bg="#fffce3", font="sans 35 bold", anchor="center")
        titulo.pack()
        titulo.place(x=0, y=0, width=1000, height=80)

        framecontenido = tk.LabelFrame(self, bg="#fffce3", text="Información", font="sans 13 bold")
        framecontenido.place(x=635, y=90, width=350, height=380)

        def validar(event):
            # Permitir solo números y la tecla de retroceso
            if event.char.isdigit() or event.keysym == "BackSpace":
                return
            else:
                return "break"
            
        self.lblnumeroCodigo = Label(framecontenido, text="Codigo:", font="sans 15 bold", bg="#fffce3")
        self.lblnumeroCodigo.place(x=10, y=20)
        self.entrynumeroCodigo = tk.Entry(framecontenido, font="sans 15")
        self.entrynumeroCodigo.place(x=100, y=20, width=130, height=30)

        self.lblNombre = Label(framecontenido, text="Nombre:", font="sans 15 bold", bg="#fffce3")
        self.lblNombre.place(x=10, y=60)
        self.entryNombre = tk.Entry(framecontenido, font="sans 15")
        self.entryNombre.place(x=100, y=60, width=235, height=30)

        self.lblDescripcion = Label(framecontenido, text="Descripción:", font="sans 15 bold", bg="#fffce3")
        self.lblDescripcion.place(x=10, y=100)
        self.entryDescripcion = tk.Text(framecontenido, font="sans 15")
        self.entryDescripcion.place(x=10, y=138, width=320, height=100)

        self.lblDosificacion = Label(framecontenido, text="Dosificacion:", font="sans 15 bold", bg="#fffce3")
        self.lblDosificacion.place(x=10, y=260)
        self.entryDosificacion = tk.Entry(framecontenido, font="sans 15")
        self.entryDosificacion.place(x=145, y=260, width=180, height=30)

        self.lblFechaVencimiento = Label(framecontenido, text="Vencimiento:", font="sans 15 bold", bg="#fffce3")
        self.lblFechaVencimiento.place(x=10, y=300)        

        # Label donde se mostrará la fecha seleccionada
        self.label_fecha_Vencimiento = Label(framecontenido, text="Selecciona una fecha", font="sans 12", bg="#fffce3")
        self.label_fecha_Vencimiento.place(x=140, y=303)
        self.datoFechaVencimiento = ""

        # Botón para abrir el calendario
        self.btn_calendario_Vencimiento = tk.Button(framecontenido, text="📅", command=self.abrir_calendario_fecha_vencimiento)
        self.btn_calendario_Vencimiento.place(x=300, y=300, width=30, height=30)

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

        self.tree_medicamento = ttk.Treeview(treFrame, columns=("Codigo", "Nombre", "Descripcion", "Dosificacion", "Fecha Vencimiento"), show="headings", height=50, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_y.config(command=self.tree_medicamento.yview)
        scroll_x.config(command=self.tree_medicamento.xview)

        self.tree_medicamento.bind('<<TreeviewSelect>>', self.seleccionarDatosMedicamentos)

        self.tree_medicamento.heading("#1", text="Codigo")             
        self.tree_medicamento.heading("#2", text="Nombre")        
        self.tree_medicamento.heading("#3", text="Descripcion")
        self.tree_medicamento.heading("#4", text="Dosificacion")
        self.tree_medicamento.heading("#5", text="Fecha Vencimiento")

        self.tree_medicamento.column("Codigo", width=120, anchor="center")
        self.tree_medicamento.column("Nombre", width=150, anchor="center")
        self.tree_medicamento.column("Descripcion", width=500, anchor="center")
        self.tree_medicamento.column("Dosificacion", width=200, anchor="center")
        self.tree_medicamento.column("Fecha Vencimiento", width=200, anchor="center")

        self.tree_medicamento.pack(expand=True, fill=BOTH)

        try:
            cursor.execute("SELECT * FROM Tabla_Medicamentos")
            datos = cursor.fetchall()
            for dato in datos:
                self.tree_medicamento.insert("", "end", values=dato)
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error al cargar los datos: {e}")

        self.imagen_Crear = Image.open("imagenes/crear.png")
        self.imagen_redimensionadaCrear = self.imagen_Crear.resize((50, 50))  # Cambia los valores según el tamaño que desees
        self.icono_btn_Crear = ImageTk.PhotoImage(self.imagen_redimensionadaCrear)
        self.btn_Crear = Button(framecontenidoTabla, text="Crear", image=self.icono_btn_Crear, padx=20, pady=10, bg="#fffce3", font="sans 18 bold", compound="top", command=self.crearDatoMedicamento, borderwidth=0, highlightthickness=0)
        self.btn_Crear.place(x=50, y=430, width=60, height=80)

        self.imagen_Actualizar = Image.open("imagenes/actualizar.png")
        self.imagen_redimensionadaActualizar = self.imagen_Actualizar.resize((50, 50))  # Cambia los valores según el tamaño que desees
        self.icono_btn_Actualizar = ImageTk.PhotoImage(self.imagen_redimensionadaActualizar)
        self.btn_Actualizar = Button(framecontenidoTabla, text="Actualizar", image=self.icono_btn_Actualizar, padx=20, pady=5, bg="#fffce3", font="sans 18 bold", compound="top", command=self.actualizar_tabla_medicamento, borderwidth=0, highlightthickness=0)
        self.btn_Actualizar.place(x=180, y=430, width=120, height=90)

        self.imagen_Borrar = Image.open("imagenes/borrar.png")
        self.imagen_redimensionadaBorrar = self.imagen_Borrar.resize((50, 50))  # Cambia los valores según el tamaño que desees
        self.icono_btn_Borrar = ImageTk.PhotoImage(self.imagen_redimensionadaBorrar)
        self.btn_Borrar = Button(framecontenidoTabla, text="Borrar", image=self.icono_btn_Borrar, padx=20, pady=5, bg="#fffce3", font="sans 18 bold", compound="top", command=self.eliminarDatoMedicamento, borderwidth=0, highlightthickness=0)
        self.btn_Borrar.place(x=340, y=430, width=120, height=90)

        self.imagen_Limpiar = Image.open("imagenes/limpiar.png")
        self.imagen_redimensionadaLimpiar = self.imagen_Limpiar.resize((50, 50))  # Cambia los valores según el tamaño que desees
        self.icono_btn_Limpiar = ImageTk.PhotoImage(self.imagen_redimensionadaLimpiar)
        self.btn_Limpiar = Button(framecontenidoTabla, text="Limpiar", image=self.icono_btn_Limpiar, padx=20, pady=5, bg="#fffce3", font="sans 18 bold", compound="top", command=self.limpiar, borderwidth=0, highlightthickness=0)
        self.btn_Limpiar.place(x=490, y=430, width=120, height=90)

    def buscarInfo (self):
        nombre_buscado = self.entryBuscarDato.get()

        # Limpiar el Treeview
        for item in self.tree_medicamento.get_children():
            self.tree_medicamento.delete(item)

        # Buscar en la base de datos
        try:
            cursor.execute("SELECT * FROM Tabla_Medicamentos WHERE Nombre LIKE %s", ('%' + nombre_buscado + '%',))
            registros = cursor.fetchall()

            # Mostrar los datos encontrados o mensaje de error
            if registros:
                for registro in registros:
                    self.tree_medicamento.insert("", "end", values=registro)
            else:
                messagebox.showinfo("Aviso", "No se encontró ningún registro con ese nombre.")

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo realizar la búsqueda: {e}")

    def crearDatoMedicamento (self):
        codigo = self.entrynumeroCodigo.get()
        nombre = self.entryNombre.get()
        descripcion = self.entryDescripcion.get("1.0", "end-1c")
        dosificacion = self.entryDosificacion.get()
        vencimiento = self.datoFechaVencimiento

        # Validar campos antes de insertar en la base de datos
        if not codigo or not nombre or not descripcion or not dosificacion or not vencimiento:
            messagebox.showerror("Error", "Por favor, completa todos los campos obligatorios.")
            return

        # Insertar en la base de datos
        try:
            cursor.execute("INSERT INTO Tabla_Medicamentos (Codigo, Nombre, Descripcion, Dosificacion, FechaVencimiento) VALUES (%s, %s, %s, %s, %s)",
                        (codigo, nombre, descripcion, dosificacion, vencimiento))
            conn.commit()
            messagebox.showinfo("Éxito", "Registro creado con éxito.")
            self.tree_medicamento.insert("", "end", values=(codigo, nombre, descripcion, dosificacion, vencimiento))
            self.limpiar()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error al crear registro: {e}")

    def eliminarDatoMedicamento (self):
        selected_item = self.tree_medicamento.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un registro para eliminar.")
            return

        # Confirmar eliminación
        if messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas eliminar el registro seleccionado?"):
            codigo = self.tree_medicamento.item(selected_item)["values"][0]
            try:
                cursor.execute("DELETE FROM Tabla_Medicamentos WHERE Codigo = %s", (codigo,))
                conn.commit()
                self.tree_medicamento.delete(selected_item)
                messagebox.showinfo("Éxito", "Registro eliminado con éxito.")
                self.limpiar()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al eliminar registro: {e}")

    def actualizar_tabla_medicamento (self):
        codigo = self.entrynumeroCodigo.get()
        nombre = self.entryNombre.get()
        descripcion = self.entryDescripcion.get("1.0", "end-1c")
        dosificacion = self.entryDosificacion.get()
        vencimiento = self.label_fecha_Vencimiento.cget("text")

        try:
            # Actualizar los datos de la tabla medicamentos
            cursor.execute("""
                UPDATE tabla_medicamentos
                SET Nombre = %s, Descripcion = %s, Dosificacion = %s, FechaVencimiento = %s
                WHERE Codigo = %s
            """, (nombre, descripcion, dosificacion, vencimiento, codigo))
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
        for item in self.tree_medicamento.get_children():
            self.tree_medicamento.delete(item)

        # Conectar a la base de datos y obtener los datos actualizados
        cursor.execute("SELECT * FROM tabla_medicamentos")
        registros = cursor.fetchall()

        # Insertar los datos en el Treeview
        for registro in registros:
            self.tree_medicamento.insert("", "end", values=registro)

    def limpiar (self):
        self.entrynumeroCodigo.config(state="normal")
        self.entrynumeroCodigo.delete(0, END)
        self.entryNombre.delete(0, END)
        self.entryDescripcion.delete("1.0", "end")
        self.entryDosificacion.delete(0, END)
        self.label_fecha_Vencimiento.config(text="Selecciona una fecha")

    def seleccionarDatosMedicamentos (self, event):
        selected_item = self.tree_medicamento.selection()
        if selected_item:
            item = self.tree_medicamento.item(selected_item)
            datos = item['values']

            self.entrynumeroCodigo.config(state="normal")  # Habilitar la edición temporalmente para mostrar el ID
            self.entrynumeroCodigo.delete(0, tk.END)
            self.entrynumeroCodigo.insert(0, datos[0])
            self.entrynumeroCodigo.config(state="disabled")  # Deshabilitar nuevamente después de mostrar el ID
            self.entryNombre.delete(0, tk.END)
            self.entryNombre.insert(0, datos[1])
            self.entryDescripcion.delete("1.0", "end")
            self.entryDescripcion.insert("1.0", datos[2])
            self.entryDosificacion.delete(0, tk.END)
            self.entryDosificacion.insert(0, datos[3])
            self.label_fecha_Vencimiento.config(text=(datos[4]))
                    
    def abrir_calendario_fecha_vencimiento(self):
        # Crear una ventana emergente para el calendario
        top = Toplevel(self)
        top.title("Fecha")
        top.resizable(False, False)
        
        # Crear el calendario
        calendario = Calendar(top, date_pattern="dd-mm-yyyy")
        calendario.pack(pady=20)
        
        # Botón para confirmar la selección de las fechas
        def seleccionar_fecha_vencimiento():
            # Obtener la fecha seleccionada en el formato "dd-mm-aa"
            fecha_seleccionada = calendario.get_date()
            fecha_formateada_mysql = datetime.strptime(fecha_seleccionada, "%d-%m-%Y").strftime("%Y-%m-%d")
            self.label_fecha_Vencimiento.config(text=fecha_formateada_mysql)  # Actualizar el label con la fecha seleccionada
            self.datoFechaVencimiento = fecha_formateada_mysql
            top.destroy()  # Cerrar la ventana del calendario

        btn_seleccionar_vencimiento = tk.Button(top, text="Seleccionar Fecha", command=seleccionar_fecha_vencimiento)
        btn_seleccionar_vencimiento.pack(pady=10)