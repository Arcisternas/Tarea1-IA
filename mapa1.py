import tkinter as tk

def abrir_mapa1(algoritmo_seleccionado, ventana_menu):
    ventana_mapa1 = tk.Toplevel(ventana_menu)
    ventana_mapa1.protocol("WM_DELETE_WINDOW", lambda: volver_al_menu(ventana_mapa1, ventana_menu))
    ventana_mapa1.title("Mapa 1 - Algoritmo seleccionado: " + algoritmo_seleccionado)
    ventana_mapa1.geometry("900x600")
    ventana_mapa1.resizable(False, False)
    ventana_mapa1.configure(bg="lightslategrey")
    ventana_mapa1.iconbitmap("fire_icon.ico")

    boton_volver = tk.Button(ventana_mapa1, text="Volver al menú", font=("Agency FB", 16), bg="lightsteelblue", width=20, command=lambda: volver_al_menu(ventana_mapa1, ventana_menu))
    boton_volver.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

def volver_al_menu(ventana_actual, ventana_menu):
    ventana_actual.destroy()
    ventana_menu.deiconify()