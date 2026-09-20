import tkinter as tk
import json
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent / "Mapas"

ARCHIVOS_MAPA = {
    1: BASE_DIR / "mapa1.json",
    2: BASE_DIR / "mapa2.json",
    3: BASE_DIR / "mapa3.json",
}

TAMAÑO = 20

CASILLA = {0: "white", 1: "black", 2: "red", 3: "green", 4: "blue"}

def abrir_mapa(numero_mapa, algoritmo_seleccionado, ventana_menu):
    mapa = cargar_mapa(numero_mapa)
    iniciar_fuego(mapa)
    filas = len(mapa)
    columnas = len(mapa[0])
    ventana_mapa = tk.Toplevel(ventana_menu)
    ventana_mapa.protocol("WM_DELETE_WINDOW", lambda: volver_al_menu(ventana_mapa, ventana_menu))
    ventana_mapa.title("Mapa " + str(numero_mapa) + " - Algoritmo seleccionado: " + algoritmo_seleccionado)
    ventana_mapa.geometry("900x600")
    ventana_mapa.resizable(False, False)
    ventana_mapa.configure(bg="lightslategrey")
    ventana_mapa.iconbitmap("resources/fire_icon.ico")

    boton_volver = tk.Button(ventana_mapa, text="Volver al menú", font=("Agency FB", 16), bg="lightsteelblue", width=20, command=lambda: volver_al_menu(ventana_mapa, ventana_menu))
    boton_volver.pack(pady=10)

    canvas = tk.Canvas(ventana_mapa, width=columnas*TAMAÑO, height=filas*TAMAÑO, bg="white")
    canvas.pack()

    dibujar_mapa(canvas, mapa)
    canvas.bind("<Button-1>", lambda evento: cambiar_casilla(evento, canvas, mapa, numero_mapa))

def guardar_mapa(mapa, numero_mapa):
    archivo = ARCHIVOS_MAPA[numero_mapa]

    with archivo.open("w", encoding="utf-8") as archivo_mapa:
        json.dump(mapa, archivo_mapa)

def cargar_mapa(numero_mapa):
    archivo = ARCHIVOS_MAPA[numero_mapa]

    with archivo.open("r", encoding="utf-8") as archivo_mapa:
        return json.load(archivo_mapa)

def dibujar_mapa(canvas, mapa):
    canvas.delete("all")

    for fila, valores_fila in enumerate(mapa):
        for columna, valor in enumerate(valores_fila):
            x1 = columna * TAMAÑO
            y1 = fila * TAMAÑO
            x2 = x1 + TAMAÑO
            y2 = y1 + TAMAÑO

            canvas.create_rectangle(x1, y1, x2, y2, fill=CASILLA[valor], outline="grey")

def cambiar_casilla(evento, canvas, mapa, numero_mapa):
    columna = evento.x // TAMAÑO
    fila = evento.y // TAMAÑO

    if not (0 <= fila < len(mapa) and 0 <= columna < len(mapa[0])):
        return
    
    if mapa[fila][columna] in (3, 4):
        return

    mapa[fila][columna] = 0 if mapa[fila][columna] == 1 else 1

    guardar_mapa(mapa, numero_mapa)
    dibujar_mapa(canvas, mapa)

def volver_al_menu(ventana_actual, ventana_menu):
    ventana_actual.destroy()
    ventana_menu.deiconify()

def iniciar_fuego(mapa):
    fila = random.randint(0, len(mapa) - 1)
    columna = random.randint(0, len(mapa[0]) - 1)

    if mapa[fila][columna] == 0:
        mapa[fila][columna] = 2
    else:
        iniciar_fuego(mapa)