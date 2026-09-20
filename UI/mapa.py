import tkinter as tk
import json
import random
from functools import partial
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent / "Mapas"

ARCHIVOS_MAPA = {
    1: BASE_DIR / "mapa1.json",
    2: BASE_DIR / "mapa2.json",
    3: BASE_DIR / "mapa3.json",
}

TAMAÑO = 20
PROPAGACION_FUEGO = 3
TIEMPO_TURNO_MS = 3000

CASILLA = {0: "white", 1: "black", 2: "red", 3: "green", 4: "blue"}

def abrir_mapa(numero_mapa, algoritmo_seleccionado, ventana_menu):
    mapa = cargar_mapa(numero_mapa)
    iniciar_fuego(mapa)
    estado = {
        "turno": 0,
        "bajas": 0,
        "temporizador": None,
        "segundos_restantes": TIEMPO_TURNO_MS // 1000,
    }
    filas = len(mapa)
    columnas = len(mapa[0])
    ventana_mapa = tk.Toplevel(ventana_menu)
    cerrar_mapa_callback = partial(cerrar_mapa, ventana_mapa, ventana_menu, estado)
    ventana_mapa.protocol("WM_DELETE_WINDOW", cerrar_mapa_callback)
    ventana_mapa.title("Mapa " + str(numero_mapa) + " - Algoritmo seleccionado: " + algoritmo_seleccionado)
    ventana_mapa.geometry("900x600")
    ventana_mapa.resizable(False, False)
    ventana_mapa.configure(bg="lightslategrey")
    ventana_mapa.iconbitmap("resources/fire_icon.ico")

    boton_volver = tk.Button(
        ventana_mapa,
        text="Volver al menú",
        font=("Agency FB", 16),
        bg="lightsteelblue",
        width=20, 
        command=cerrar_mapa_callback
    )

    boton_volver.pack(pady=10)

    canvas = tk.Canvas(
        ventana_mapa,
        width=columnas*TAMAÑO,
        height=filas*TAMAÑO,
        bg="white"
    )
    canvas.pack()

    dibujar_mapa(canvas, mapa)
    canvas.bind("<Button-1>", lambda evento: cambiar_casilla(evento, canvas, mapa, numero_mapa))

    informacion = tk.Label(
        ventana_mapa,
        text="Turno: 0 | Bajas: 0 | El fuego se propaga cada 3 turnos | Siguiente turno en 3 segundos",
        font=("Agency FB", 14),
        bg="lightslategrey",
    )
    informacion.pack(pady=5)

    avanzar_turno_automaticamente_callback = partial(avanzar_turno_automaticamente, mapa, canvas, informacion, estado, ventana_mapa)

    boton_turno = tk.Button(
        ventana_mapa,
        text="Siguiente turno",
        font=("Agency FB", 16),
        bg="lightsteelblue",
        width=20,
        command=lambda: avanzar_turno_interfaz(
            mapa, canvas, informacion, estado, PROPAGACION_FUEGO
        ),
    )
    boton_turno.pack(pady=5)
    estado["temporizador"] = ventana_mapa.after(1000, avanzar_turno_automaticamente_callback)

def cerrar_mapa(ventana_mapa, ventana_menu, estado):
    if estado["temporizador"] is not None:
        ventana_mapa.after_cancel(estado["temporizador"])
    volver_al_menu(ventana_mapa, ventana_menu)

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
    
    if mapa[fila][columna] in (2, 3, 4):
        return

    mapa[fila][columna] = 0 if mapa[fila][columna] == 1 else 1

    guardar_mapa(limpiar_fuego(mapa), numero_mapa)
    dibujar_mapa(canvas, mapa)

def volver_al_menu(ventana_actual, ventana_menu):
    ventana_actual.destroy()
    ventana_menu.deiconify()

def iniciar_fuego(mapa):
    casillas_transitables = [(fila, columna) for fila, valores_fila in enumerate(mapa) for columna, valor in enumerate(valores_fila) if valor == 0]

    if not casillas_transitables:
        return None

    fila, columna = random.choice(casillas_transitables)
    mapa[fila][columna] = 2

    return fila, columna

def vecinos_ortogonales(mapa, fila, columna):
    for desplazamiento_fila, desplazamiento_columna in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        vecino_fila = fila + desplazamiento_fila
        vecino_columna = columna + desplazamiento_columna
        if 0 <= vecino_fila < len(mapa) and 0 <= vecino_columna < len(mapa[0]):
            yield vecino_fila, vecino_columna


def propagar_fuego(mapa):
    fuego_actual = [(fila, columna) for fila, valores_fila in enumerate(mapa) for columna, valor in enumerate(valores_fila) if valor == 2]
    nuevas_casillas = set()
    bajas = 0

    for fila, columna in fuego_actual:
        for vecino_fila, vecino_columna in vecinos_ortogonales(mapa, fila, columna):
            valor = mapa[vecino_fila][vecino_columna]
            if valor == 1 or valor == 2:
                continue
            if valor == 4 and (vecino_fila, vecino_columna) not in nuevas_casillas:
                bajas += 1
            nuevas_casillas.add((vecino_fila, vecino_columna))

    for fila, columna in nuevas_casillas:
        mapa[fila][columna] = 2

    return {"nuevas_casillas": nuevas_casillas, "bajas": bajas}

def limpiar_fuego(mapa):
     return [[0 if valor == 2 else valor for valor in fila] for fila in mapa]

def avanzar_turno(mapa, turno, k = PROPAGACION_FUEGO):
    nuevo_turno = turno + 1
    resultado = {"nuevas_casillas": set(), "bajas": 0}
    if nuevo_turno % k == 0:
        resultado = propagar_fuego(mapa)

    return nuevo_turno, resultado

def avanzar_turno_automaticamente(mapa, canvas, informacion, estado, ventana_mapa):
    estado["segundos_restantes"] -= 1
    if estado["segundos_restantes"] == 0:
        avanzar_turno_interfaz(mapa, canvas, informacion, estado, PROPAGACION_FUEGO)
        estado["segundos_restantes"] = TIEMPO_TURNO_MS // 1000
    else:
        informacion.config(
            text=(
                f"Turno: {estado['turno']} | Bajas: {estado['bajas']} | "
                f"Próxima propagación en {PROPAGACION_FUEGO - estado['turno'] % PROPAGACION_FUEGO} turnos | "
                f"Siguiente turno en {estado['segundos_restantes']} segundos"
            )
        )
    estado["temporizador"] = ventana_mapa.after(1000, partial(avanzar_turno_automaticamente, mapa, canvas, informacion, estado, ventana_mapa))

def avanzar_turno_interfaz(mapa, canvas, informacion, estado, k):
    estado["turno"], resultado = avanzar_turno(mapa, estado["turno"], k)
    estado["bajas"] += resultado["bajas"]
    dibujar_mapa(canvas, mapa)
    informacion.config(
        text=(
            f"Turno: {estado['turno']} | Bajas: {estado['bajas']} | "
            f"Próxima propagación en {k - estado['turno'] % k} turnos | "
            f"Siguiente turno en {estado['segundos_restantes']} segundos"
        )
    )