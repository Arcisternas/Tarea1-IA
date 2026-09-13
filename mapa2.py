import tkinter as tk

def abrir_mapa2(algoritmo_seleccionado, ventana_menu):
    ventana_mapa2 = tk.Toplevel(ventana_menu)
    ventana_mapa2.protocol("WM_DELETE_WINDOW", lambda: volver_al_menu(ventana_mapa2, ventana_menu))
    ventana_mapa2.title("Mapa 2 - Algoritmo seleccionado: " + algoritmo_seleccionado)
    ventana_mapa2.geometry("900x600")
    ventana_mapa2.resizable(False, False)
    ventana_mapa2.configure(bg="lightslategrey")
    ventana_mapa2.iconbitmap("fire_icon.ico")


    boton_volver = tk.Button(ventana_mapa2, text="Volver al menú", font=("Agency FB", 16), bg="lightsteelblue", width=20, command=lambda: volver_al_menu(ventana_mapa2, ventana_menu))
    boton_volver.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

def volver_al_menu(ventana_actual, ventana_menu):
    ventana_actual.destroy()
    ventana_menu.deiconify()

