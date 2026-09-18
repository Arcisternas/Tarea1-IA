import tkinter as tk
from mapa1 import abrir_mapa1
from mapa2 import abrir_mapa2
from mapa3 import abrir_mapa3

def abrir_algoritmo(numero_mapa, ventana_menu):
    ventana_algoritmo = tk.Toplevel(ventana_menu)
    ventana_algoritmo.protocol("WM_DELETE_WINDOW", ventana_menu.destroy)
    ventana_algoritmo.title("Mapa " + str(numero_mapa) + " - Elección de algoritmo")
    ventana_algoritmo.geometry("900x600")
    ventana_algoritmo.resizable(False, False)
    ventana_algoritmo.configure(bg="lightslategrey")
    ventana_algoritmo.iconbitmap("fire_icon.ico")

    label_titulo = tk.Label(ventana_algoritmo, text="Elija un algoritmo", font=("Agency FB", 24, "bold"), bg="lightslategrey")
    label_titulo.pack(pady=20)

    boton_algoritmo1 = tk.Button(ventana_algoritmo, text="Algoritmo no informado 1", font=("Agency FB", 20), bg="lightsteelblue", width=40, command=lambda: abrir_mapa_seleccionado(numero_mapa, "Algoritmo no informado 1", ventana_menu, ventana_algoritmo))
    boton_algoritmo2 = tk.Button(ventana_algoritmo, text="Algoritmo no informado 2", font=("Agency FB", 20), bg="lightsteelblue", width=40, command=lambda: abrir_mapa_seleccionado(numero_mapa, "Algoritmo no informado 2", ventana_menu, ventana_algoritmo))
    boton_algoritmo3 = tk.Button(ventana_algoritmo, text="Algoritmo informado 1", font=("Agency FB", 20), bg="lightsteelblue", width=40, command=lambda: abrir_mapa_seleccionado(numero_mapa, "Algoritmo informado 1", ventana_menu, ventana_algoritmo))
    boton_algoritmo4 = tk.Button(ventana_algoritmo, text="Algoritmo informado 2", font=("Agency FB", 20), bg="lightsteelblue", width=40, command=lambda: abrir_mapa_seleccionado(numero_mapa, "Algoritmo informado 2", ventana_menu, ventana_algoritmo))
    boton_algoritmo5 = tk.Button(ventana_algoritmo, text="Algoritmo metaheurístico", font=("Agency FB", 20), bg="lightsteelblue", width=40, command=lambda: abrir_mapa_seleccionado(numero_mapa, "Algoritmo metaheurístico", ventana_menu, ventana_algoritmo))

    boton_algoritmo1.pack(pady=10)
    boton_algoritmo2.pack(pady=10)
    boton_algoritmo3.pack(pady=10)
    boton_algoritmo4.pack(pady=10)
    boton_algoritmo5.pack(pady=10)

    boton_volver = tk.Button(ventana_algoritmo, text="Volver al menú", font=("Agency FB", 16), bg="lightsteelblue", width=20, command=lambda: volver_al_menu(ventana_algoritmo, ventana_menu))
    boton_volver.pack(pady=20)

def abrir_mapa_seleccionado(numero_mapa, algoritmo_seleccionado, ventana_menu, ventana_algoritmo):
    ventana_algoritmo.destroy() 
    match numero_mapa:
        case 1:
            abrir_mapa1(algoritmo_seleccionado, ventana_menu)
        case 2:
            abrir_mapa2(algoritmo_seleccionado, ventana_menu)
        case 3:
            abrir_mapa3(algoritmo_seleccionado, ventana_menu)
            
def volver_al_menu(ventana_actual, ventana_menu):
    ventana_actual.destroy()
    ventana_menu.deiconify()