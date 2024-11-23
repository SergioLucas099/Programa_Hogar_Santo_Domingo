# Desde este archivo principal Index es que se estaran llamando las funciones de manager
# para mostrar las ventanas y poder correr nuestro programa

from manager import Manager # Llamar el archivo manager e importamos la clase Manager

# Indicar el mismo metodo para iniciar el bucle
if __name__ == "__main__":
    app = Manager()
    app.mainloop()