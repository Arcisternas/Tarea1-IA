import tkinter as tk
from eleccion_algoritmo import abrir_algoritmo

def cargar_mapa(numero_mapa):
    ventana_menu.withdraw() 
    abrir_algoritmo(numero_mapa, ventana_menu)

def abrir_menu():
    global ventana_menu
    ventana_menu = tk.Tk()
    ventana_menu.protocol("WM_DELETE_WINDOW", cerrar_programa)
    ventana_menu.title("Escape de la torre")
    ventana_menu.geometry("900x600")
    ventana_menu.resizable(False, False)
    ventana_menu.configure(bg="lightslategrey")
    ventana_menu.iconbitmap("resources/fire_icon.ico")

    titulo = tk.Label(ventana_menu)
    titulo.configure(text="Escape de la torre", font=("Agency FB", 32, "bold"), pady=50, bg="lightslategrey")
    titulo.pack()

    botonmapa1 = tk.Button(ventana_menu)
    botonmapa1.configure(text="Mapa 1", font=("Agency FB", 22), bg="lightsteelblue", width=40, command=lambda: cargar_mapa(1))
    botonmapa2 = tk.Button(ventana_menu)
    botonmapa2.configure(text="Mapa 2", font=("Agency FB", 22), bg="lightsteelblue", width=40, command=lambda: cargar_mapa(2))
    botonmapa3 = tk.Button(ventana_menu)
    botonmapa3.configure(text="Mapa 3", font=("Agency FB", 22), bg="lightsteelblue", width=40, command=lambda: cargar_mapa(3))
    botonmapa1.pack(pady=20)
    botonmapa2.pack(pady=20)
    botonmapa3.pack(pady=20)

    ventana_menu.mainloop()

def cerrar_programa():
    ventana_menu.destroy()

if __name__ == "__main__":
    abrir_menu()
