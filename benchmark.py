import argparse
import random
import time
from pathlib import Path

from algoritmos import ALGORITMOS
from algoritmos.costos import ConfiguracionCostos
from UI.mapa import (
    REPORTES_DIR,
    avanzar_turno_con_agentes,
    cargar_mapa,
    copiar_mapa,
    generar_reporte,
    iniciar_fuego,
    motivo_fin_simulacion,
)
from simulacion.agentes import inicializar_agentes

MIN_ITERACIONES = 80
ITERACIONES_POR_DEFECTO = 200
MAX_TURNOS = 10000
ALGORITMOS_CLI = {
    "BFS": "BFS",
    "UCS": "UCS",
    "Greedy": "Greedy",
    "A*": "A*",
    "genetico": "genético",
}


def ejecutar_simulacion(numero_mapa, algoritmo_nombre, cantidad_agentes, semilla):
    random.seed(semilla)
    mapa = copiar_mapa(cargar_mapa(numero_mapa))
    iniciar_fuego(mapa)
    agentes = inicializar_agentes(mapa, cantidad_agentes)
    algoritmo_clase = ALGORITMOS[algoritmo_nombre]
    algoritmo = (
        algoritmo_clase(semilla=semilla)
        if algoritmo_nombre == "genético"
        else algoritmo_clase()
    )
    configuracion = ConfiguracionCostos()
    estado = {
        "agentes": agentes,
        "evacuados": 0,
        "total_agentes": len(agentes),
        "turno": 0,
    }
    ultimo_turno_evacuado = None
    inicio = time.perf_counter()
    motivo = motivo_fin_simulacion(mapa, estado)

    while motivo is None and estado["turno"] < MAX_TURNOS:
        estado["turno"], resultado = avanzar_turno_con_agentes(
            mapa,
            estado["turno"],
            agentes,
            algoritmo=algoritmo,
            configuracion=configuracion,
        )
        estado["evacuados"] += resultado["evacuados"]
        if resultado["evacuados"] > 0:
            ultimo_turno_evacuado = estado["turno"]
        motivo = motivo_fin_simulacion(mapa, estado)

    if motivo is None:
        motivo = f"Se alcanzo el limite de {MAX_TURNOS} turnos"

    tiempo_real = time.perf_counter() - inicio
    return {
        "tasa_supervivencia": (
            estado["evacuados"] / estado["total_agentes"] * 100
            if estado["total_agentes"]
            else 0.0
        ),
        "turnos": estado["turno"],
        "turnos_ultimo_evacuado": ultimo_turno_evacuado,
        "tiempo_real_segundos": tiempo_real,
        "evacuados": estado["evacuados"],
        "bajas": estado["total_agentes"] - estado["evacuados"] - len(agentes),
        "motivo": motivo,
        "semilla": semilla,
    }


def ejecutar_benchmark(numero_mapa, algoritmo_nombre, iteraciones, cantidad_agentes, semilla_base):
    resultados = []
    for indice in range(iteraciones):
        semilla = semilla_base + indice
        numero_iteracion = indice + 1
        print(
            f"  Iteracion {numero_iteracion}/{iteraciones} en curso...",
            end="",
            flush=True,
        )
        resultado = ejecutar_simulacion(
            numero_mapa,
            algoritmo_nombre,
            cantidad_agentes,
            semilla,
        )
        resultados.append(resultado)
        print(
            f" completada ({resultado['tiempo_real_segundos']:.4f} s)",
            flush=True,
        )

    ruta_reporte = generar_reporte(numero_mapa, algoritmo_nombre, resultados)
    return ruta_reporte, resultados


def parsear_argumentos():
    parser = argparse.ArgumentParser(
        description="Ejecuta benchmarks sin interfaz grafica y genera reportes TXT."
    )
    parser.add_argument(
        "--mapa",
        type=int,
        choices=(1, 2, 3),
        default=None,
        help="Mapa a ejecutar. Por defecto ejecuta los tres mapas.",
    )
    parser.add_argument(
        "--algoritmo",
        choices=tuple(ALGORITMOS_CLI),
        default=None,
        help="Algoritmo a ejecutar. Por defecto ejecuta los cinco algoritmos.",
    )
    parser.add_argument(
        "--iteraciones",
        "--iterations",
        dest="iteraciones",
        type=int,
        default=ITERACIONES_POR_DEFECTO,
        help="Cantidad de iteraciones por configuracion. Minimo: 80.",
    )
    parser.add_argument(
        "--agentes",
        type=int,
        default=150,
        help="Cantidad de agentes por simulacion.",
    )
    parser.add_argument(
        "--semilla",
        type=int,
        default=2026,
        help="Semilla base; cada iteracion usa semilla + indice.",
    )
    return parser.parse_args()


def main():
    argumentos = parsear_argumentos()
    if argumentos.iteraciones < MIN_ITERACIONES:
        raise SystemExit(
            f"Error: --iteraciones debe ser al menos {MIN_ITERACIONES}."
        )
    if argumentos.agentes < 1:
        raise SystemExit("Error: --agentes debe ser positivo.")

    mapas = (argumentos.mapa,) if argumentos.mapa else (1, 2, 3)
    nombres = (
        (ALGORITMOS_CLI[argumentos.algoritmo],)
        if argumentos.algoritmo
        else tuple(ALGORITMOS_CLI.values())
    )
    total_configuraciones = len(mapas) * len(nombres)
    configuracion_actual = 0

    print(f"Ejecutando {total_configuraciones} configuraciones...")
    for numero_mapa in mapas:
        for algoritmo_nombre in nombres:
            configuracion_actual += 1
            print(
                f"[{configuracion_actual}/{total_configuraciones}] "
                f"Mapa {numero_mapa} - {algoritmo_nombre} - "
                f"{argumentos.iteraciones} iteraciones"
            )
            ruta_reporte, resultados = ejecutar_benchmark(
                numero_mapa,
                algoritmo_nombre,
                argumentos.iteraciones,
                argumentos.agentes,
                argumentos.semilla,
            )
            tiempo_total = sum(
                resultado["tiempo_real_segundos"] for resultado in resultados
            )
            print(f"Reporte: {ruta_reporte}")
            print(f"Tiempo de calculo: {tiempo_total:.4f} s")

    print(f"Reportes generados en: {REPORTES_DIR}")


if __name__ == "__main__":
    main()
