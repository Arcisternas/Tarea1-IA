import tkinter as tk
from tkinter import messagebox
import json
import random
import time
from collections import Counter, deque
from functools import partial
from pathlib import Path
from statistics import mean, stdev

from simulacion.agentes import inicializar_agentes, mover_agentes
from algoritmos import ALGORITMOS
from algoritmos.costos import ConfiguracionCostos

BASE_DIR = Path(__file__).resolve().parent.parent / "mapas"

ARCHIVOS_MAPA = {
    1: BASE_DIR / "mapa1.json",
    2: BASE_DIR / "mapa2.json",
    3: BASE_DIR / "mapa3.json",
}

TAMAÑO = 20
PROPAGACION_FUEGO = 3
TIEMPO_TURNO_MS = 10
REPORTES_DIR = Path(__file__).resolve().parent.parent / "reportes"

CASILLA = {0: "white", 1: "black", 2: "red", 3: "green", 4: "blue"}

def abrir_mapa(numero_mapa, algoritmo_seleccionado, ventana_menu):
    #Variables
    mapa_base = cargar_mapa(numero_mapa)
    mapa = copiar_mapa(mapa_base)
    algoritmo = ALGORITMOS[algoritmo_seleccionado]()
    agentes = []
    estado = {
        "turno": 0,
        "bajas": 0,
        "pausado": False,
        "evacuados": 0,
        "agentes": agentes,
        "algoritmo": algoritmo,
        "configuracion_costos": ConfiguracionCostos(),
        "tiempo_turno_ms": TIEMPO_TURNO_MS,
        "costo_congestion": 0,
        "temporizador": None,
        "mapa_base": mapa_base,
        "cantidad_agentes": 0,
        "total_agentes": 0,
        "simulaciones_totales": 1,
        "simulacion_actual": 0,
        "resultados_simulaciones": [],
        "finalizada": False,
        "motivo_fin": "",
        "numero_mapa": numero_mapa,
        "algoritmo_seleccionado": algoritmo_seleccionado,
    }
    filas = len(mapa)
    columnas = len(mapa[0])

    #Ventana principal del mapa
    ventana_mapa = tk.Toplevel(ventana_menu)
    cerrar_mapa_callback = partial(cerrar_mapa, ventana_mapa, ventana_menu, estado)
    ventana_mapa.protocol("WM_DELETE_WINDOW", cerrar_mapa_callback)
    ventana_mapa.title("Mapa " + str(numero_mapa) + " - Algoritmo seleccionado: " + algoritmo_seleccionado)
    ventana_mapa.geometry("1000x650")
    ventana_mapa.resizable(False, False)
    ventana_mapa.configure(bg="lightslategrey")
    ventana_mapa.iconbitmap("resources/fire_icon.ico")

    ventana_mapa.columnconfigure(0, weight=0)
    ventana_mapa.columnconfigure(1, weight=1)
    ventana_mapa.rowconfigure(0, weight=1)

    #Paneles y botones
    panel_izquierdo = tk.Frame(ventana_mapa, bg="lightslategrey", width=280)
    panel_izquierdo.grid(row=0, column=0, sticky="ns", padx=10, pady=10)
    panel_izquierdo.grid_propagate(False)

    panel_mapa = tk.Frame(ventana_mapa, bg="lightslategrey")
    panel_mapa.columnconfigure(0, weight=0)
    panel_mapa.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    panel_izquierdo.rowconfigure(2, weight=1)

    #Boton menú
    boton_volver = tk.Button(
        panel_izquierdo,
        text="Volver al menú",
        font=("Agency FB", 16),
        bg="lightsteelblue",
        width=20,
        command=cerrar_mapa_callback,
    )
    boton_volver.grid(row=0, column=0, padx=10, pady=10)

    #Zona de controles
    frame_controles = tk.LabelFrame(
    panel_izquierdo,
    text="Controles",
    font=("Agency FB", 16, "bold"),
    bg="lightslategrey",
    )

    frame_controles.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

    boton_iniciar = tk.Button(
        frame_controles,
        text="Iniciar simulación",
        font=("Agency FB", 16),
        bg="lightsteelblue",
        width=20,
    )

    boton_iniciar.grid(row=0, column=0, pady=5, padx=20)

    boton_pausar = tk.Button(
        frame_controles,
        text="Pausar simulación",
        font=("Agency FB", 16),
        bg="lightsteelblue",
        width=20,
        state=tk.DISABLED,
    )

    boton_pausar.grid(row=1, column=0, pady=5, padx=20)

    boton_turno = tk.Button(
        frame_controles,
        text="Siguiente turno",
        font=("Agency FB", 16),
        bg="lightsteelblue",
        width=20,
        state=tk.DISABLED,
        command=lambda: avanzar_turno_interfaz(mapa, canvas, informacion, estado, PROPAGACION_FUEGO)
    )

    boton_turno.grid(row=2, column=0, pady=5, padx=20)

    # Zona de opciones
    frame_opciones = tk.LabelFrame(
        panel_izquierdo,
        text="Configuración",
        font=("Agency FB", 16, "bold"),
        bg="lightslategrey",
    )
    frame_opciones.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

    tk.Label(frame_opciones, text="Agentes:", bg="lightslategrey").grid(
        row=0, column=0, sticky="w", pady=5
    )

    spin_agentes = tk.Spinbox(
        frame_opciones,
        from_=80,
        to=300,
        width=8,
    )
    spin_agentes.grid(row=0, column=1, padx=5)

    tk.Label(frame_opciones, text="Tiempo por turno (MS):", bg="lightslategrey").grid(
        row=1, column=0, sticky="w", pady=5
    )

    spin_tiempo = tk.Spinbox(
        frame_opciones,
        from_=1,
        to=3000,
        width=8,
    )
    spin_tiempo.grid(row=1, column=1, padx=5)

    tk.Label(frame_opciones, text="Simulaciones:", bg="lightslategrey").grid(
        row=2, column=0, sticky="w", pady=5
    )

    spin_simulaciones = tk.Spinbox(
        frame_opciones,
        from_=1,
        to=1000,
        width=8,
    )
    spin_simulaciones.grid(row=2, column=1, padx=5)

    #Mapa

    ancho_mapa = columnas * TAMAÑO
    alto_mapa = filas * TAMAÑO

    frame_canvas = tk.Frame(
        panel_mapa,
        width=ancho_mapa,
        height=alto_mapa,
        bg="white",
    )
    frame_canvas.grid(row=0, column=0)
    frame_canvas.grid_propagate(False)

    canvas = tk.Canvas(
        frame_canvas,
        width=ancho_mapa,
        height=alto_mapa,
        bg="white",
        highlightthickness=0,
    )
    canvas.pack()

    dibujar_mapa(canvas, mapa, agentes)
    canvas.bind(
        "<Button-1>",
        lambda evento: cambiar_casilla(evento, canvas, mapa, numero_mapa, agentes),
    )

    informacion = tk.Label(
        panel_mapa,
        text="Turno: 0 | Evacuados: 0/30 | Bajas: 0",
        font=("Agency FB", 14),
        bg="lightslategrey",
        wraplength=ancho_mapa,
        justify="center",
    )
    informacion.grid(row=1, column=0, sticky="ew", pady=5)

    boton_pausar.config(command=lambda: alternar_pausa(boton_pausar, boton_turno, mapa, canvas, informacion, estado, ventana_mapa))

    boton_iniciar.config(command=lambda: iniciar_simulacion(
        boton_iniciar,
        boton_turno,
        boton_pausar,
        spin_agentes,
        spin_tiempo,
        spin_simulaciones,
        mapa,
        canvas,
        informacion,
        estado,
        ventana_mapa,
    ))

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

def copiar_mapa(mapa):
    return [fila[:] for fila in mapa]

def reiniciar_simulacion(mapa, estado):
    mapa[:] = copiar_mapa(estado["mapa_base"])
    iniciar_fuego(mapa)
    estado["agentes"][:] = inicializar_agentes(mapa, estado["cantidad_agentes"])
    estado["total_agentes"] = len(estado["agentes"])
    estado["turno"] = 0
    estado["bajas"] = 0
    estado["evacuados"] = 0
    estado["costo_congestion"] = 0
    estado["pausado"] = False
    estado["finalizada"] = False
    estado["motivo_fin"] = ""
    estado["turnos_ultimo_evacuado"] = None
    estado["inicio_tiempo_real"] = time.perf_counter()
    estado["simulacion_actual"] += 1

def existe_ruta_a_salida(mapa, agentes):
    salida = next(
        (
            (fila, columna)
            for fila, valores_fila in enumerate(mapa)
            for columna, valor in enumerate(valores_fila)
            if valor == 3
        ),
        None,
    )
    if salida is None or not agentes:
        return False

    visitadas = set(agentes)
    pendientes = deque(agentes)
    while pendientes:
        posicion = pendientes.popleft()
        if posicion == salida:
            return True

        for vecino in vecinos_ortogonales(mapa, *posicion):
            if vecino in visitadas:
                continue
            fila, columna = vecino
            if mapa[fila][columna] not in (0, 3, 4):
                continue
            visitadas.add(vecino)
            pendientes.append(vecino)

    return False

def motivo_fin_simulacion(mapa, estado):
    if not estado["agentes"]:
        if estado["evacuados"] == estado["total_agentes"] and estado["total_agentes"]:
            return "Todos los agentes evacuaron"
        return "No quedan agentes en el mapa"

    if not any(valor == 3 for fila in mapa for valor in fila):
        return "El fuego consumió la salida"

    if not existe_ruta_a_salida(mapa, estado["agentes"]):
        return "El fuego bloqueó todas las rutas a la salida"

    return None

def generar_reporte(numero_mapa, algoritmo_seleccionado, resultados):
    REPORTES_DIR.mkdir(exist_ok=True)
    nombre_algoritmo = "".join(
        caracter if caracter.isalnum() else "_"
        for caracter in algoritmo_seleccionado
    ).strip("_")
    ruta_reporte = REPORTES_DIR / f"reporte_mapa{numero_mapa}_{nombre_algoritmo}.txt"

    tasas = [resultado["tasa_supervivencia"] for resultado in resultados]
    turnos = [
        resultado["turnos_ultimo_evacuado"]
        for resultado in resultados
        if resultado["turnos_ultimo_evacuado"] is not None
    ]
    tiempos_reales = [resultado["tiempo_real_segundos"] for resultado in resultados]
    desviacion = stdev(turnos) if len(turnos) > 1 else 0.0

    with ruta_reporte.open("w", encoding="utf-8") as archivo:
        archivo.write("Reporte de simulaciones - Escape de la Torre\n")
        archivo.write(f"Mapa: {numero_mapa}\n")
        archivo.write(f"Algoritmo: {algoritmo_seleccionado}\n")
        archivo.write(f"Simulaciones: {len(resultados)}\n\n")
        archivo.write("Tasa de supervivencia:\n")
        archivo.write(f"Media: {mean(tasas):.2f}%\n")
        archivo.write(f"Mínima: {min(tasas):.2f}%\n")
        archivo.write(f"Máxima: {max(tasas):.2f}%\n\n")
        archivo.write("Estadísticos descriptivos de tiempo (turnos):\n")
        if turnos:
            archivo.write(f"Iteraciones con al menos un evacuado: {len(turnos)}\n")
            archivo.write(f"Media: {mean(turnos):.2f}\n")
            archivo.write(f"Desviación estándar: {desviacion:.2f}\n")
            archivo.write(f"Mínimo: {min(turnos)}\n")
            archivo.write(f"Máximo: {max(turnos)}\n")
        else:
            archivo.write("No hubo corridas con agentes evacuados.\n")
        archivo.write("\nTiempo real de ejecución (segundos):\n")
        archivo.write(f"Promedio por simulación: {mean(tiempos_reales):.4f}\n")
        archivo.write(f"Total de todas las simulaciones: {sum(tiempos_reales):.4f}\n\n")
        archivo.write("Detalle por simulación:\n")
        for indice, resultado in enumerate(resultados, start=1):
            turnos_ultimo_evacuado = resultado["turnos_ultimo_evacuado"]
            turnos_texto = (
                str(turnos_ultimo_evacuado)
                if turnos_ultimo_evacuado is not None
                else "No aplica"
            )
            archivo.write(
                f"{indice}: supervivencia={resultado['tasa_supervivencia']:.2f}%, "
                f"turnos_ultimo_evacuado={turnos_texto}, "
                f"tiempo_real={resultado['tiempo_real_segundos']:.4f}s, "
                f"evacuados={resultado['evacuados']}, "
                f"bajas={resultado['bajas']}, "
                f"fin={resultado['motivo']}\n"
            )

    return ruta_reporte

def dibujar_mapa(canvas, mapa, agentes=None):
    canvas.delete("all")
    conteo_agentes = Counter(agentes or [])

    for fila, valores_fila in enumerate(mapa):
        for columna, valor in enumerate(valores_fila):
            x1 = columna * TAMAÑO
            y1 = fila * TAMAÑO
            x2 = x1 + TAMAÑO
            y2 = y1 + TAMAÑO

            canvas.create_rectangle(x1, y1, x2, y2, fill=CASILLA[valor], outline="grey")
            cantidad = conteo_agentes.get((fila, columna), 0)
            if cantidad > 0:
                canvas.create_text(
                    (x1 + x2) // 2,
                    (y1 + y2) // 2,
                    text=str(cantidad),
                    fill="white" if valor in (1, 2, 4) else "black",
                    font=("Arial", 9, "bold"),
                )

def iniciar_simulacion(
    boton_iniciar,
    boton_turno,
    boton_pausar,
    spin_agentes,
    spin_tiempo,
    spin_simulaciones,
    mapa,
    canvas,
    informacion,
    estado,
    ventana_mapa,
):
    cantidad_agentes = int(spin_agentes.get())
    tiempo_turno_ms = int(spin_tiempo.get())
    cantidad_simulaciones = int(spin_simulaciones.get())

    estado["tiempo_turno_ms"] = tiempo_turno_ms
    estado["cantidad_agentes"] = cantidad_agentes
    estado["total_agentes"] = cantidad_agentes
    estado["simulaciones_totales"] = cantidad_simulaciones
    estado["simulacion_actual"] = 0
    estado["resultados_simulaciones"][:] = []
    reiniciar_simulacion(mapa, estado)
    estado["boton_iniciar"] = boton_iniciar
    estado["boton_turno"] = boton_turno
    estado["boton_pausar"] = boton_pausar

    dibujar_mapa(canvas, mapa, estado["agentes"])
    actualizar_informacion(informacion, estado, PROPAGACION_FUEGO)
    boton_iniciar.config(state=tk.DISABLED)
    boton_turno.config(state=tk.NORMAL)
    boton_pausar.config(state=tk.NORMAL)

    estado["temporizador"] = ventana_mapa.after(
        estado["tiempo_turno_ms"],
        partial(
            avanzar_turno_automaticamente,
            mapa,
            canvas,
            informacion,
            estado,
            ventana_mapa,
        ),
    )

def alternar_pausa(
    boton_pausa,
    boton_turno,
    mapa,
    canvas,
    informacion,
    estado,
    ventana_mapa,
):
    if estado["finalizada"]:
        return

    if estado["pausado"]:
        estado["pausado"] = False
        boton_pausa.config(text="Pausar")
        boton_turno.config(state=tk.NORMAL)

        estado["temporizador"] = ventana_mapa.after(
            estado["tiempo_turno_ms"],
            partial(
                avanzar_turno_automaticamente,
                mapa,
                canvas,
                informacion,
                estado,
                ventana_mapa,
            ),
        )
    else:
        estado["pausado"] = True
        boton_pausa.config(text="Reanudar")
        boton_turno.config(state=tk.DISABLED)

        if estado["temporizador"] is not None:
            ventana_mapa.after_cancel(estado["temporizador"])
            estado["temporizador"] = None

def cambiar_casilla(evento, canvas, mapa, numero_mapa, agentes=None):
    columna = evento.x // TAMAÑO
    fila = evento.y // TAMAÑO

    if not (0 <= fila < len(mapa) and 0 <= columna < len(mapa[0])):
        return
    
    if mapa[fila][columna] in (2, 3, 4):
        return

    mapa[fila][columna] = 0 if mapa[fila][columna] == 1 else 1

    guardar_mapa(limpiar_fuego(mapa), numero_mapa)
    dibujar_mapa(canvas, mapa, agentes)

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


def propagar_fuego(mapa, agentes=None):
    fuego_actual = [(fila, columna) for fila, valores_fila in enumerate(mapa) for columna, valor in enumerate(valores_fila) if valor == 2]
    nuevas_casillas = set()
    bajas = 0

    for fila, columna in fuego_actual:
        for vecino_fila, vecino_columna in vecinos_ortogonales(mapa, fila, columna):
            valor = mapa[vecino_fila][vecino_columna]
            if valor == 1 or valor == 2:
                continue
            nuevas_casillas.add((vecino_fila, vecino_columna))

    for fila, columna in nuevas_casillas:
        mapa[fila][columna] = 2

    return {"nuevas_casillas": nuevas_casillas, "bajas": bajas}

def limpiar_fuego(mapa):
     return [[0 if valor == 2 else valor for valor in fila] for fila in mapa]

def avanzar_turno(mapa, turno, k=PROPAGACION_FUEGO, algoritmo=None, configuracion=None):
    return avanzar_turno_con_agentes(
        mapa,
        turno,
        [],
        k,
        algoritmo,
        configuracion or ConfiguracionCostos(),
    )


def avanzar_turno_con_agentes(
    mapa,
    turno,
    agentes,
    k=PROPAGACION_FUEGO,
    algoritmo=None,
    configuracion=None,
):
    nuevo_turno = turno + 1
    algoritmo = algoritmo or ALGORITMOS["BFS"]()
    configuracion = configuracion or ConfiguracionCostos()
    salida = algoritmo.encontrar_salida(mapa)
    movimiento = mover_agentes(
        mapa,
        agentes,
        algoritmo=algoritmo,
        salida=salida,
        configuracion=configuracion,
    )
    agentes[:] = movimiento["agentes"]
    resultado = {"nuevas_casillas": set(), "bajas": 0}
    if nuevo_turno % k == 0:
        resultado = propagar_fuego(mapa, agentes)

    posiciones_en_fuego = resultado["nuevas_casillas"]
    agentes_supervivientes = []
    for agente in agentes:
        if agente in posiciones_en_fuego:
            resultado["bajas"] += 1
        else:
            agentes_supervivientes.append(agente)
    agentes[:] = agentes_supervivientes
    resultado["evacuados"] = movimiento["evacuados"]
    resultado["costo"] = movimiento["costo"]
    resultado["esperas"] = movimiento["esperas"]

    return nuevo_turno, resultado

def avanzar_turno_automaticamente(mapa, canvas, informacion, estado, ventana_mapa):
    if estado["pausado"] or estado["finalizada"]:
        return

    termino = avanzar_turno_interfaz(
        mapa,
        canvas,
        informacion,
        estado,
        PROPAGACION_FUEGO,
        ventana_mapa,
    )
    if not termino:
        estado["temporizador"] = ventana_mapa.after(
            estado["tiempo_turno_ms"],
            partial(
                avanzar_turno_automaticamente,
                mapa,
                canvas,
                informacion,
                estado,
                ventana_mapa,
            ),
        )

def actualizar_informacion(informacion, estado, k):
    informacion.config(
        text=(
            f"Simulación: {estado['simulacion_actual']}/{estado['simulaciones_totales']} | "
            f"Turno: {estado['turno']} | "
            f"Evacuados: {estado['evacuados']}/{estado['total_agentes']} | "
            f"Bajas: {estado['bajas']} | "
            f"Próxima propagación en {k - estado['turno'] % k} turnos"
        )
    )

def finalizar_simulacion(mapa, canvas, informacion, estado, ventana_mapa, motivo):
    estado["motivo_fin"] = motivo
    tiempo_real_segundos = time.perf_counter() - estado["inicio_tiempo_real"]
    estado["resultados_simulaciones"].append(
        {
            "tasa_supervivencia": (
                estado["evacuados"] / estado["total_agentes"] * 100
                if estado["total_agentes"]
                else 0.0
            ),
            "turnos": estado["turno"],
            "turnos_ultimo_evacuado": estado["turnos_ultimo_evacuado"],
            "tiempo_real_segundos": tiempo_real_segundos,
            "evacuados": estado["evacuados"],
            "bajas": estado["bajas"],
            "motivo": motivo,
        }
    )

    if estado["simulacion_actual"] < estado["simulaciones_totales"]:
        reiniciar_simulacion(mapa, estado)
        dibujar_mapa(canvas, mapa, estado["agentes"])
        actualizar_informacion(informacion, estado, PROPAGACION_FUEGO)
        estado["temporizador"] = ventana_mapa.after(
            1,
            partial(
                avanzar_turno_automaticamente,
                mapa,
                canvas,
                informacion,
                estado,
                ventana_mapa,
            ),
        )
        return

    estado["finalizada"] = True
    estado["temporizador"] = None
    estado["boton_iniciar"].config(state=tk.NORMAL)
    estado["boton_turno"].config(state=tk.DISABLED)
    estado["boton_pausar"].config(state=tk.DISABLED, text="Pausar simulación")
    ruta_reporte = generar_reporte(
        estado["numero_mapa"],
        estado["algoritmo_seleccionado"],
        estado["resultados_simulaciones"],
    )
    informacion.config(
        text=(
            f"Simulaciones terminadas: {estado['simulaciones_totales']} | "
            f"Último fin: {motivo}"
        )
    )
    messagebox.showinfo(
        "Simulaciones terminadas",
        f"El reporte fue generado en:\n{ruta_reporte}",
        parent=ventana_mapa,
    )

def avanzar_turno_interfaz(mapa, canvas, informacion, estado, k, ventana_mapa=None):
    motivo = motivo_fin_simulacion(mapa, estado)
    if motivo is not None:
        if ventana_mapa is None:
            return True
        finalizar_simulacion(mapa, canvas, informacion, estado, ventana_mapa, motivo)
        return True

    estado["turno"], resultado = avanzar_turno_con_agentes(
        mapa,
        estado["turno"],
        estado["agentes"],
        k,
        estado["algoritmo"],
        estado["configuracion_costos"],
    )
    estado["bajas"] += resultado["bajas"]
    estado["evacuados"] += resultado["evacuados"]
    estado["costo_congestion"] += resultado["costo"]
    if resultado["evacuados"] > 0:
        estado["turnos_ultimo_evacuado"] = estado["turno"]
    dibujar_mapa(canvas, mapa, estado["agentes"])
    actualizar_informacion(informacion, estado, k)
    motivo = motivo_fin_simulacion(mapa, estado)
    if motivo is None:
        return False

    if ventana_mapa is None:
        return True

    finalizar_simulacion(mapa, canvas, informacion, estado, ventana_mapa, motivo)
    return True