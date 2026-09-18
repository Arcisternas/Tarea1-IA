import tkinter as tk
import json

ARCHIVO_MAPA = "mapa3.json"

with open("mapa3.json", "r") as f:
    MAPA = json.load(f)

FILAS = len(MAPA)
COLUMNAS = len(MAPA[0])
TAMAÑO = 20

CASILLA = {0: "white", 1: "black", 2: "red", 3: "green", 4: "blue"}

def abrir_mapa3(algoritmo_seleccionado, ventana_menu):
    ventana_mapa3 = tk.Toplevel(ventana_menu)
    ventana_mapa3.protocol("WM_DELETE_WINDOW", lambda: volver_al_menu(ventana_mapa3, ventana_menu))
    ventana_mapa3.title("Mapa 3 - Algoritmo seleccionado: " + algoritmo_seleccionado)
    ventana_mapa3.geometry("900x600")
    ventana_mapa3.resizable(False, False)
    ventana_mapa3.configure(bg="lightslategrey")
    ventana_mapa3.iconbitmap("fire_icon.ico")


    boton_volver = tk.Button(ventana_mapa3, text="Volver al menú", font=("Agency FB", 16), bg="lightsteelblue", width=20, command=lambda: volver_al_menu(ventana_mapa3, ventana_menu))
    boton_volver.pack(pady=10)

    mapa = cargar_mapa()
    canvas = tk.Canvas(ventana_mapa3, width=COLUMNAS*TAMAÑO, height=FILAS*TAMAÑO, bg="white")
    canvas.pack()
    
    dibujar_mapa(canvas, mapa)
    canvas.bind("<Button-1>", lambda evento: cambiar_casilla(evento, canvas, mapa))

def guardar_mapa(mapa):
    with open(ARCHIVO_MAPA, "w", encoding="utf-8") as archivo:
        json.dump(mapa, archivo)

def cargar_mapa():
    try:
        with open(ARCHIVO_MAPA, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return [fila.copy() for fila in MAPA]

def dibujar_mapa(canvas, mapa):
    canvas.delete("all")

    for fila in range(FILAS):
        for columna in range(COLUMNAS):
            x1 = columna * TAMAÑO
            y1 = fila * TAMAÑO
            x2 = x1 + TAMAÑO
            y2 = y1 + TAMAÑO

            valor = mapa[fila][columna]

            canvas.create_rectangle(x1, y1, x2, y2, fill=CASILLA[valor], outline="grey")

def crear_mapa():
    return [fila.copy() for fila in MAPA]

def cambiar_casilla(evento, canvas, mapa):
    columna = evento.x // TAMAÑO
    fila = evento.y // TAMAÑO

    if not (0 <= fila < FILAS and 0 <= columna < COLUMNAS):
        return
    
    if mapa[fila][columna] in (3, 4):
        return

    mapa[fila][columna] = 0 if mapa[fila][columna] == 1 else 1

    guardar_mapa(mapa)
    dibujar_mapa(canvas, mapa)

def volver_al_menu(ventana_actual, ventana_menu):
    ventana_actual.destroy()
    ventana_menu.deiconify()