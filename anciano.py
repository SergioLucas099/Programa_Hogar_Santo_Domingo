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

# Conectar a la base de datos
conn = sqlite3.connect('Hogar_Santo_Domingo.db')
cursor = conn.cursor()

class Anciano(tk.Toplevel):
    def __init__(self, parent, container):
        super().__init__(parent)
        self.container = container
        self.title("Datos Anciano")        

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
        frametitulo.place(x=0, y=0, width=1000, height=80)

        titulo = tk.Label(frametitulo, text="Datos Anciano", bg="#fffce3", font="sans 35 bold", anchor="center")
        titulo.pack()
        titulo.place(x=0, y=0, width=1000, height=80)

        framecontenido = tk.LabelFrame(self, bg="#fffce3", text="Información", font="sans 13 bold")
        framecontenido.place(x=635, y=70, width=350, height=525)

        def validar(event):
            # Permitir solo números y la tecla de retroceso
            if event.char.isdigit() or event.keysym == "BackSpace":
                return
            else:
                return "break"

        self.lblnumeroDocumento = Label(framecontenido, text="Número Documento:", font="sans 15 bold", bg="#fffce3")
        self.lblnumeroDocumento.place(x=10, y=20)
        self.entrynumeroDocumento = tk.Entry(framecontenido, font="sans 15")
        self.entrynumeroDocumento.bind("<KeyPress>", validar)
        self.entrynumeroDocumento.place(x=210, y=20, width=125, height=30)

        self.lblrolTipoDocumento = Label(framecontenido, text="Tipo Documento: ", font="sans 15 bold", bg="#fffce3")
        self.lblrolTipoDocumento.place(x=10, y=60)
        self.rol_varTipoDocumento = StringVar(framecontenido)
        self.rol_varTipoDocumento.set("Cedula")
        opciones_rol = ["Cedula", "Cedula Extranjera", "Permiso Especial"]
        self.menu_rolTipoDocumento = OptionMenu(framecontenido, self.rol_varTipoDocumento, *opciones_rol)
        self.menu_rolTipoDocumento.config(font="sans 13")
        self.menu_rolTipoDocumento.place(x=180, y=60, width=160, height=30)

        self.lblNombre = Label(framecontenido, text="Nombre:", font="sans 15 bold", bg="#fffce3")
        self.lblNombre.place(x=10, y=100)
        self.entryNombre = tk.Entry(framecontenido, font="sans 15")
        self.entryNombre.place(x=100, y=100, width=235, height=30)

        self.lblnumeroEdad = Label(framecontenido, text="Edad:", font="sans 15 bold", bg="#fffce3")
        self.lblnumeroEdad.place(x=10, y=140)
        self.entrynumeroEdad = tk.Entry(framecontenido, font="sans 15")
        self.entrynumeroEdad.bind("<KeyPress>", validar)
        self.entrynumeroEdad.place(x=100, y=140, width=50, height=30)

        # Campo de fecha de nacimiento y botón para abrir el calendario
        self.lblFechaNacimiento = Label(framecontenido, text="Nacimiento:", font="sans 15 bold", bg="#fffce3")
        self.lblFechaNacimiento.place(x=10, y=180)
        
        # Label donde se mostrará la fecha seleccionada
        self.label_fecha_nacimiento = Label(framecontenido, text="Selecciona una fecha", font="sans 12", bg="#fffce3")
        self.label_fecha_nacimiento.place(x=130, y=182)
        self.datoFechaNacimiento = ""

        # Botón para abrir el calendario
        self.btn_calendario_nacimiento = tk.Button(framecontenido, text="📅", command=self.abrir_calendario)
        self.btn_calendario_nacimiento.place(x=300, y=180, width=30, height=30)

        self.lblGenero = Label(framecontenido, text="Género:", font="sans 15 bold", bg="#fffce3")
        self.lblGenero.place(x=10, y=220)
        self.rol_Genero = StringVar(framecontenido)
        self.rol_Genero.set("Masculino")
        opciones_genero = ["Masculino", "Femenino"]
        self.menu_Genero = OptionMenu(framecontenido, self.rol_Genero, *opciones_genero)
        self.menu_Genero.config(font="sans 13")
        self.menu_Genero.place(x=120, y=220, width=160, height=30)

        self.lblAcudinete = Label(framecontenido, text="Acudiente:", font="sans 15 bold", bg="#fffce3")
        self.lblAcudinete.place(x=10, y=260)
        self.entryAcudinete = tk.Entry(framecontenido, font="sans 15")
        self.entryAcudinete.place(x=120, y=260, width=215, height=30)

        self.lblDireccion = Label(framecontenido, text="Dirección:", font="sans 15 bold", bg="#fffce3")
        self.lblDireccion.place(x=10, y=300)
        self.entryDireccion = tk.Entry(framecontenido, font="sans 15")
        self.entryDireccion.place(x=120, y=300, width=215, height=30)

        self.lblTelefono = Label(framecontenido, text="Teléfono:", font="sans 15 bold", bg="#fffce3")
        self.lblTelefono.place(x=10, y=340)
        self.entryTelefono = tk.Entry(framecontenido, font="sans 15")
        self.entryTelefono.bind("<KeyPress>", validar)
        self.entryTelefono.place(x=110, y=340, width=125, height=30)

        self.lblCondicion = Label(framecontenido, text="Condición:", font="sans 15 bold", bg="#fffce3")
        self.lblCondicion.place(x=10, y=380)
        self.entryCondicion = tk.Entry(framecontenido, font="sans 15")
        self.entryCondicion.place(x=120, y=380, width=215, height=30)

        self.lblFechaIngreso = Label(framecontenido, text="Ingreso:", font="sans 15 bold", bg="#fffce3")
        self.lblFechaIngreso.place(x=10, y=420)        

        # Label donde se mostrará la fecha seleccionada
        self.label_fecha_Ingreso = Label(framecontenido, text="Selecciona una fecha", font="sans 12", bg="#fffce3")
        self.label_fecha_Ingreso.place(x=100, y=423)
        self.datoFechaIngreso = ""

        # Botón para abrir el calendario
        self.btn_calendario_Ingreso = tk.Button(framecontenido, text="📅", command=self.abrir_calendario_fecha_ingreso)
        self.btn_calendario_Ingreso.place(x=300, y=420, width=30, height=30)

        self.lblFechaSalida = Label(framecontenido, text="Salida:", font="sans 15 bold", bg="#fffce3")
        self.lblFechaSalida.place(x=10, y=460)

        # Label donde se mostrará la fecha seleccionada
        self.label_fecha_salida = Label(framecontenido, text="Selecciona una fecha", font="sans 12", bg="#fffce3")
        self.label_fecha_salida.place(x=100, y=460)
        self.datoFechaSalida = ""

        # Botón para abrir el calendario
        self.btn_calendario_salida = tk.Button(framecontenido, text="📅", command=self.abrir_calendario_fecha_salida)
        self.btn_calendario_salida.place(x=300, y=460, width=30, height=30)

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

        self.tree_ancianos = ttk.Treeview(treFrame, columns=("Cedula", "Tipo de Documento", "Nombre", "Edad", "Nacimiento", "Género", "Acudiente", "Dirección", "Teléfono", "Condición", "Fecha Ingreso", "Fecha Salida"), show="headings", height=50, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_y.config(command=self.tree_ancianos.yview)
        scroll_x.config(command=self.tree_ancianos.xview)

        self.tree_ancianos.bind('<<TreeviewSelect>>', self.seleccionarDatosAnciano)

        self.tree_ancianos.heading("#1", text="Cedula")        
        self.tree_ancianos.heading("#2", text="Tipo de Documento")        
        self.tree_ancianos.heading("#3", text="Nombre")        
        self.tree_ancianos.heading("#4", text="Edad")
        self.tree_ancianos.heading("#5", text="Nacimiento")
        self.tree_ancianos.heading("#6", text="Género")
        self.tree_ancianos.heading("#7", text="Acudiente")
        self.tree_ancianos.heading("#8", text="Dirección")
        self.tree_ancianos.heading("#9", text="Teléfono")
        self.tree_ancianos.heading("#10", text="Condición")
        self.tree_ancianos.heading("#11", text="Fecha Ingreso")
        self.tree_ancianos.heading("#12", text="Fecha Salida")

        self.tree_ancianos.column("Cedula", width=120, anchor="center")
        self.tree_ancianos.column("Tipo de Documento", width=200, anchor="center")
        self.tree_ancianos.column("Nombre", width=200, anchor="center")
        self.tree_ancianos.column("Edad", width=60, anchor="center")
        self.tree_ancianos.column("Nacimiento", width=180, anchor="center")
        self.tree_ancianos.column("Género", width=130, anchor="center")
        self.tree_ancianos.column("Acudiente", width=130, anchor="center")
        self.tree_ancianos.column("Dirección", width=130, anchor="center")
        self.tree_ancianos.column("Teléfono", width=130, anchor="center")
        self.tree_ancianos.column("Condición", width=130, anchor="center")
        self.tree_ancianos.column("Fecha Ingreso", width=150, anchor="center")
        self.tree_ancianos.column("Fecha Salida", width=130, anchor="center")

        self.tree_ancianos.pack(expand=True, fill=BOTH)

        try:
            cursor.execute("SELECT * FROM Tabla_Ancianos")
            datos = cursor.fetchall()
            for dato in datos:
                self.tree_ancianos.insert("", "end", values=dato)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al cargar los datos: {e}")

        self.imagen_Crear = Image.open("imagenes/crear.png")
        self.imagen_redimensionadaCrear = self.imagen_Crear.resize((50, 50))  # Cambia los valores según el tamaño que desees
        self.icono_btn_Crear = ImageTk.PhotoImage(self.imagen_redimensionadaCrear)
        self.btn_Crear = Button(framecontenidoTabla, text="Crear", image=self.icono_btn_Crear, padx=20, pady=10, bg="#fffce3", font="sans 18 bold", compound="top", command=self.crearDatoAnciano, borderwidth=0, highlightthickness=0)
        self.btn_Crear.place(x=50, y=430, width=60, height=80)

        self.imagen_Actualizar = Image.open("imagenes/actualizar.png")
        self.imagen_redimensionadaActualizar = self.imagen_Actualizar.resize((50, 50))  # Cambia los valores según el tamaño que desees
        self.icono_btn_Actualizar = ImageTk.PhotoImage(self.imagen_redimensionadaActualizar)
        self.btn_Actualizar = Button(framecontenidoTabla, text="Actualizar", image=self.icono_btn_Actualizar, padx=20, pady=5, bg="#fffce3", font="sans 18 bold", compound="top", command=self.actualizar_tabla_ancianos, borderwidth=0, highlightthickness=0)
        self.btn_Actualizar.place(x=180, y=430, width=120, height=90)

        self.imagen_Borrar = Image.open("imagenes/borrar.png")
        self.imagen_redimensionadaBorrar = self.imagen_Borrar.resize((50, 50))  # Cambia los valores según el tamaño que desees
        self.icono_btn_Borrar = ImageTk.PhotoImage(self.imagen_redimensionadaBorrar)
        self.btn_Borrar = Button(framecontenidoTabla, text="Borrar", image=self.icono_btn_Borrar, padx=20, pady=5, bg="#fffce3", font="sans 18 bold", compound="top", command=self.eliminarDatoAnciano, borderwidth=0, highlightthickness=0)
        self.btn_Borrar.place(x=340, y=430, width=120, height=90)

        self.imagen_Limpiar = Image.open("imagenes/limpiar.png")
        self.imagen_redimensionadaLimpiar = self.imagen_Limpiar.resize((50, 50))  # Cambia los valores según el tamaño que desees
        self.icono_btn_Limpiar = ImageTk.PhotoImage(self.imagen_redimensionadaLimpiar)
        self.btn_Limpiar = Button(framecontenidoTabla, text="Limpiar", image=self.icono_btn_Limpiar, padx=20, pady=5, bg="#fffce3", font="sans 18 bold", compound="top", command=self.limpiar, borderwidth=0, highlightthickness=0)
        self.btn_Limpiar.place(x=490, y=430, width=120, height=90)

    def buscarInfo (self):
        nombre_buscado = self.entryBuscarDato.get()

        # Limpiar el Treeview
        for item in self.tree_ancianos.get_children():
            self.tree_ancianos.delete(item)

        # Buscar en la base de datos
        try:
            cursor.execute("SELECT * FROM Tabla_Ancianos WHERE Nombre LIKE ?", ('%' + nombre_buscado + '%',))
            registros = cursor.fetchall()

            # Mostrar los datos encontrados o mensaje de error
            if registros:
                for registro in registros:
                    self.tree_ancianos.insert("", "end", values=registro)
            else:
                messagebox.showinfo("Aviso", "No se encontró ningún registro con ese nombre.")

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo realizar la búsqueda: {e}")

    def crearDatoAnciano (self):
        cedula = self.entrynumeroDocumento.get()
        tipo_documento = self.rol_varTipoDocumento.get()
        nombre = self.entryNombre.get()
        edad = self.entrynumeroEdad.get()
        nacimiento = self.datoFechaNacimiento
        genero = self.rol_Genero.get()
        acudiente = self.entryAcudinete.get()
        direccion = self.entryDireccion.get()
        telefono = self.entryTelefono.get()
        condicion = self.entryCondicion.get()
        ingreso = self.datoFechaIngreso
        salida = self.datoFechaSalida

        # Validar campos antes de insertar en la base de datos
        if not all ([cedula, tipo_documento, nombre, edad, nacimiento, genero, acudiente, direccion, telefono, condicion, ingreso, salida]):
            messagebox.showerror("Error", "Por favor, completa todos los campos obligatorios.")
            return
        
        # Insertar en la base de datos
        try:
            cursor.execute("INSERT INTO Tabla_Ancianos (Cedula, TipoDocumento, Nombre, Edad, Nacimiento, Genero, Acudiente, Direccion, Telefono, Condicion, FechaIngreso, FechaSalida) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (cedula, tipo_documento, nombre, edad, nacimiento, genero, acudiente, direccion, telefono, condicion, ingreso, salida))
            conn.commit()
            messagebox.showinfo("Éxito", "Registro creado con éxito.")
            self.tree_ancianos.insert("", "end", values=(cedula, tipo_documento, nombre, edad, nacimiento, genero, acudiente, direccion, telefono, condicion, ingreso, salida))
            self.limpiar()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al crear registro: {e}")

    def eliminarDatoAnciano (self):
        selected_item = self.tree_ancianos.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un registro para eliminar.")
            return

        # Confirmar eliminación
        if messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas eliminar el registro seleccionado?"):
            cedula = self.tree_ancianos.item(selected_item)["values"][0]
            try:
                conn = sqlite3.connect('Hogar_Santo_Domingo.db')
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Tabla_Ancianos WHERE Cedula = ?", (cedula,))
                conn.commit()
                self.tree_ancianos.delete(selected_item)
                self.entrynumeroDocumento.config(state="normal")
                self.entrynumeroDocumento.delete(0, END)
                self.rol_varTipoDocumento.set("Cedula")
                self.entryNombre.delete(0, END)
                self.entrynumeroEdad.delete(0, END)
                self.label_fecha_nacimiento.config(text="Selecciona una fecha")
                self.rol_Genero.set("Masculino")
                self.entryAcudinete.delete(0, END)
                self.entryDireccion.delete(0, END)
                self.entryTelefono.delete(0, END)
                self.entryCondicion.delete(0, END)
                self.label_fecha_Ingreso.config(text="Selecciona una fecha")
                self.label_fecha_salida.config(text="Selecciona una fecha")
                messagebox.showinfo("Éxito", "Registro eliminado con éxito.")
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error al eliminar registro: {e}")
            finally:
                conn.close()            

    def actualizar_tabla_ancianos (self):
        cedula = self.entrynumeroDocumento.get()
        tipo_documento = self.rol_varTipoDocumento.get()
        nombre = self.entryNombre.get()
        edad = self.entrynumeroEdad.get()
        nacimiento = self.label_fecha_nacimiento.cget("text")
        genero = self.rol_Genero.get()
        acudiente = self.entryAcudinete.get()
        direccion = self.entryDireccion.get()
        telefono = self.entryTelefono.get()
        condicion = self.entryCondicion.get()
        ingreso = self.label_fecha_Ingreso.cget("text")
        salida = self.label_fecha_salida.cget("text")
        
        try:
            # Actualizar los datos de la tabla ancianos
            cursor.execute("""
                UPDATE Tabla_Ancianos
                SET TipoDocumento = ?, Nombre = ?, Edad = ?, Nacimiento = ?, Genero = ?, Acudiente = ?, Direccion = ?, Telefono = ?, Condicion = ?, FechaIngreso = ?, FechaSalida = ?
                WHERE Cedula = ?
            """, (tipo_documento, nombre, edad, nacimiento, genero, acudiente, direccion, telefono, condicion, ingreso, salida, cedula))
            conn.commit()

            # Verificar si se actualizó algún registro
            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", "Usuario actualizado exitosamente")
                self.actualizar_treeview()
                self.limpiar()
                
            else:
                messagebox.showwarning("Aviso", "No se encontró ningún usuario con ese ID.")

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo actualizar el usuario: {e}")

    def actualizar_treeview(self):
        # Limpiar el Treeview actual
        for item in self.tree_ancianos.get_children():
            self.tree_ancianos.delete(item)

        # Conectar a la base de datos y obtener los datos actualizados
        conn = sqlite3.connect('Hogar_Santo_Domingo.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Tabla_Ancianos")
        registros = cursor.fetchall()

        # Insertar los datos en el Treeview
        for registro in registros:
            self.tree_ancianos.insert("", "end", values=registro)

    def limpiar (self):
        self.entrynumeroDocumento.config(state="normal")
        self.entrynumeroDocumento.delete(0, END)
        self.rol_varTipoDocumento.set("Cedula")
        self.entryNombre.delete(0, END)
        self.entrynumeroEdad.delete(0, END)
        self.label_fecha_nacimiento.config(text="Selecciona una fecha")
        self.rol_Genero.set("Masculino")
        self.entryAcudinete.delete(0, END)
        self.entryDireccion.delete(0, END)
        self.entryTelefono.delete(0, END)
        self.entryCondicion.delete(0, END)
        self.label_fecha_Ingreso.config(text="Selecciona una fecha")
        self.label_fecha_salida.config(text="Selecciona una fecha")

    def seleccionarDatosAnciano (self, event):
        selected_item = self.tree_ancianos.selection()
        if selected_item:
            item = self.tree_ancianos.item(selected_item)
            datos = item['values']

            self.entrynumeroDocumento.config(state="normal")  # Habilitar la edición temporalmente para mostrar el ID
            self.entrynumeroDocumento.delete(0, tk.END)
            self.entrynumeroDocumento.insert(0, datos[0])
            self.entrynumeroDocumento.config(state="disabled")  # Deshabilitar nuevamente después de mostrar el ID
            self.rol_varTipoDocumento.set(datos[1])
            self.entryNombre.delete(0, tk.END)
            self.entryNombre.insert(0, datos[2])
            self.entrynumeroEdad.delete(0, tk.END)
            self.entrynumeroEdad.insert(0, datos[3])
            self.label_fecha_nacimiento.config(text=(datos[4]))
            self.rol_Genero.set(datos[5])
            self.entryAcudinete.delete(0, tk.END)
            self.entryAcudinete.insert(0, datos[6])
            self.entryDireccion.delete(0, tk.END)
            self.entryDireccion.insert(0, datos[7])
            self.entryTelefono.delete(0, tk.END)
            self.entryTelefono.insert(0, datos[8])
            self.entryCondicion.delete(0, tk.END)
            self.entryCondicion.insert(0, datos[9])
            self.label_fecha_Ingreso.config(text=(datos[10]))
            self.label_fecha_salida.config(text=(datos[11]))

    def abrir_calendario(self):
        # Crear una ventana emergente para el calendario
        top = Toplevel(self)
        top.title("Fecha")
        top.resizable(False, False)
        
        # Crear el calendario
        calendario = Calendar(top, date_pattern="dd-mm-yyyy")
        calendario.pack(pady=20)
        
        # Botón para confirmar la selección de las fechas
        def seleccionar_fecha_nacimiento():
            # Obtener la fecha seleccionada en el formato "dd-mm-aa"
            fecha_seleccionada = calendario.get_date()
            fecha_formateada = datetime.strptime(fecha_seleccionada, "%d-%m-%Y").strftime("%d-%B-%y")
            self.label_fecha_nacimiento.config(text=fecha_formateada)  # Actualizar el label con la fecha seleccionada
            self.datoFechaNacimiento = fecha_formateada
            top.destroy()  # Cerrar la ventana del calendario

        btn_seleccionar_nacimiento = tk.Button(top, text="Seleccionar Fecha", command=seleccionar_fecha_nacimiento)
        btn_seleccionar_nacimiento.pack(pady=10)

    def abrir_calendario_fecha_ingreso(self):
        # Crear una ventana emergente para el calendario
        top = Toplevel(self)
        top.title("Fecha")
        top.resizable(False, False)
        
        # Crear el calendario
        calendario = Calendar(top, date_pattern="dd-mm-yyyy")
        calendario.pack(pady=20)
        
        # Botón para confirmar la selección de las fechas
        def seleccionar_fecha_ingreso():
            # Obtener la fecha seleccionada en el formato "dd-mm-aa"
            fecha_seleccionada = calendario.get_date()
            fecha_formateada = datetime.strptime(fecha_seleccionada, "%d-%m-%Y").strftime("%d-%B-%y")
            self.label_fecha_Ingreso.config(text=fecha_formateada)  # Actualizar el label con la fecha seleccionada
            self.datoFechaIngreso = fecha_formateada
            top.destroy()  # Cerrar la ventana del calendario

        btn_seleccionar_ingreso = tk.Button(top, text="Seleccionar Fecha", command=seleccionar_fecha_ingreso)
        btn_seleccionar_ingreso.pack(pady=10)

    def abrir_calendario_fecha_salida(self):
        # Crear una ventana emergente para el calendario
        top = Toplevel(self)
        top.title("Fecha")
        top.resizable(False, False)
        
        # Crear el calendario
        calendario = Calendar(top, date_pattern="dd-mm-yyyy")
        calendario.pack(pady=20)
        
        # Botón para confirmar la selección de las fechas

        def seleccionar_fecha_salida():
            # Obtener la fecha seleccionada en el formato "dd-mm-aa"
            fecha_seleccionada = calendario.get_date()
            fecha_formateada = datetime.strptime(fecha_seleccionada, "%d-%m-%Y").strftime("%d-%B-%y")
            self.label_fecha_salida.config(text=fecha_formateada)  # Actualizar el label con la fecha seleccionada
            self.datoFechaSalida = fecha_formateada
            top.destroy()  # Cerrar la ventana del calendario

        btn_seleccionar_salida = tk.Button(top, text="Seleccionar Fecha", command=seleccionar_fecha_salida)
        btn_seleccionar_salida.pack(pady=10)