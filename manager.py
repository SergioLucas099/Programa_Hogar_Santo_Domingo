from tkinter import Tk, Frame
from container import Container
from ttkthemes import ThemedStyle
import os
import sys

class Manager(Tk):
    def __init__(self, *args, **kwargs):
        # -------Configurar Ventana-------
        super().__init__(*args, **kwargs)
        self.title("Gestor de Datos Hogar Santo Domingo")  # Titulo
        self.resizable(False, False)  # Evitar que la ventana se expanda
        self.configure(bg="#fffce3")  # Asignar un color de fondo        
        
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

        self.container = Frame(self, bg="#fffce3")  # Crear el contenedor tipo Frame, y le asignamos el color
        self.container.pack(fill="both", expand=True)  # Empaquetar el contenedor, el fill se usa para que el contenedor se expanda en toda la ventana        

        self.frames = {Container: None}  # Diccionarios para guardar los frames que se usaran

        self.load_frames() # Llamado del metodo cargar frames

        self.show_frame(Container) # Llamado metodo mostrar frames

        self.set_theme()

        # Asignar icono
        ruta=self.rutas(r"icono.ico")
        self.iconbitmap(ruta)
    
    def rutas(self, ruta):
        try:
            rutabase = sys.__MEIPASS
        except Exception:
            rutabase = os.path.abspath(".")
        return os.path.join(rutabase,ruta)

    # -------Metodo para cargar frames-------
    def load_frames(self):
        for FrameClass in self.frames.keys():
            frame = FrameClass(self.container, self)
            self.frames[FrameClass] = frame
    
    # -------Metodo para mostrar frames-------
    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()
    
    def set_theme(self):
        style = ThemedStyle(self)

# -------Metodo para iniciar el bucle para poner a correr el programa-------
def main():
    app = Manager()
    app.mainloop()

if __name__ == "__main__":
    main()