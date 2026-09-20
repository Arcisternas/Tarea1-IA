import tkinter as tk
from mapa import abrir_mapa

def abrir_algoritmo(numero_mapa, ventana_menu):
    ventana_algoritmo = tk.Toplevel(ventana_menu)
    ventana_algoritmo.protocol("WM_DELETE_WINDOW", ventana_menu.destroy)
    ventana_algoritmo.title("Mapa " + str(numero_mapa) + " - Elección de algoritmo")
    ventana_algoritmo.geometry("900x600")
    ventana_algoritmo.resizable(False, False)
    ventana_algoritmo.configure(bg="lightslategrey")
    ventana_algoritmo.iconbitmap("resources/fire_icon.ico")

    label_titulo = tk.Label(ventana_algoritmo, text="Elija un algoritmo", font=("Agency FB", 24, "bold"), bg="lightslategrey")
    label_titulo.pack(pady=20)

    boton_algoritmo1 = tk.Button(ventana_algoritmo, text="BFS", font=("Agency FB", 20), bg="lightsteelblue", width=40, command=lambda: abrir_mapa_seleccionado(numero_mapa, "BFS", ventana_menu, ventana_algoritmo))
    boton_algoritmo2 = tk.Button(ventana_algoritmo, text="UCS   ", font=("Agency FB", 20), bg="lightsteelblue", width=40, command=lambda: abrir_mapa_seleccionado(numero_mapa, "UCS", ventana_menu, ventana_algoritmo))
    boton_algoritmo3 = tk.Button(ventana_algoritmo, text="Greedy Best-First Search", font=("Agency FB", 20), bg="lightsteelblue", width=40, command=lambda: abrir_mapa_seleccionado(numero_mapa, "Greedy", ventana_menu, ventana_algoritmo))
    boton_algoritmo4 = tk.Button(ventana_algoritmo, text="A*", font=("Agency FB", 20), bg="lightsteelblue", width=40, command=lambda: abrir_mapa_seleccionado(numero_mapa, "A*", ventana_menu, ventana_algoritmo))
    boton_algoritmo5 = tk.Button(ventana_algoritmo, text="Algoritmo genético", font=("Agency FB", 20), bg="lightsteelblue", width=40, command=lambda: abrir_mapa_seleccionado(numero_mapa, "Algoritmo genético", ventana_menu, ventana_algoritmo))

    boton_algoritmo1.pack(pady=10)
    boton_algoritmo2.pack(pady=10)
    boton_algoritmo3.pack(pady=10)
    boton_algoritmo4.pack(pady=10)
    boton_algoritmo5.pack(pady=10)

    boton_volver = tk.Button(ventana_algoritmo, text="Volver al menú", font=("Agency FB", 16), bg="lightsteelblue", width=20, command=lambda: volver_al_menu(ventana_algoritmo, ventana_menu))
    boton_volver.pack(pady=20)

def abrir_mapa_seleccionado(numero_mapa, algoritmo_seleccionado, ventana_menu, ventana_algoritmo):
    ventana_algoritmo.destroy() 
    abrir_mapa(numero_mapa, algoritmo_seleccionado, ventana_menu)
            
def volver_al_menu(ventana_actual, ventana_menu):
    ventana_actual.destroy()
    ventana_menu.deiconify()