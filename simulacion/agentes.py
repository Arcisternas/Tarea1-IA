from algoritmos.base import ContextoBusqueda
from algoritmos.costos import (
    capacidad_de_casilla,
    calcular_costo_casilla,
)
from collections import Counter

def inicializar_agentes(mapa, cantidad):
    agentes = []
    for fila, valores_fila in enumerate(mapa):
        for columna, valor in enumerate(valores_fila):
            if valor == 4:
                agentes.extend([(fila, columna)] * cantidad)
                return agentes
    return agentes

def mover_agentes(mapa, agentes, algoritmo, salida, configuracion):
    ocupacion = Counter(agentes)
    propuestas = []
    resultados_por_posicion = {}

    for posicion in agentes:
        if posicion not in resultados_por_posicion:
            contexto = ContextoBusqueda(mapa=mapa, inicio=posicion, objetivo=salida, ocupacion=ocupacion, configuracion_costos=configuracion)

            resultados_por_posicion[posicion] = algoritmo.buscar(contexto)

        resultado = resultados_por_posicion[posicion]

        if len(resultado.camino) > 1:
            destino = resultado.camino[1]
        else:
            destino = posicion

        propuestas.append((posicion, destino))

    nuevos_agentes = []
    destinos = Counter()
    evacuados = 0
    esperas = 0
    costo_total = 0.0

    for posicion, destino in propuestas:
        if destino == salida:
            if evacuados < configuracion.capacidad_salida:
                evacuados += 1
                continue

            # La salida también tiene un límite de flujo por turno.
            destino = posicion

        capacidad = capacidad_de_casilla(destino, salida, configuracion)

        # Las propuestas se aplican de forma secuencial para que la
        # ocupación resultante nunca supere la capacidad configurada.
        if destinos[destino] >= capacidad:
            destino = posicion

        destinos[destino] += 1

        # La posición actual puede estar sobreocupada al inicio, porque
        # representa el punto de reunión inicial de todos los agentes.
        # La restricción se aplica a nuevas entradas durante la simulación.
        costo_total += calcular_costo_casilla(
            destino,
            destinos,
            configuracion,
        )
        nuevos_agentes.append(destino)

        if destino == posicion:
            esperas += 1

    return {
        "agentes": nuevos_agentes,
        "evacuados": evacuados,
        "esperas": esperas,
        "costo": costo_total,
    }