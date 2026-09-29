from heapq import heappop, heappush

from .base import (
    AlgoritmoBusqueda,
    CASILLAS_TRANSITABLES,
    ContextoBusqueda,
    ResultadoBusqueda,
)
from .costos import calcular_costo_casilla

class UCS(AlgoritmoBusqueda):
    nombre = "UCS"

    def buscar(self, contexto: ContextoBusqueda) -> ResultadoBusqueda:
        mapa = contexto.mapa
        if not mapa or not mapa[0]:
            return ResultadoBusqueda(camino=[], costo=float("inf"), nodos_explorados=0, encontrado=False)

        inicio = contexto.inicio
        salida = contexto.objetivo

        if inicio is None or salida is None:
            return ResultadoBusqueda(camino=[], costo=float("inf"), nodos_explorados=0, encontrado=False)

        # Cola de prioridad que representa la frontera de la búsqueda.
        # Siempre se extrae el nodo con menor costo acumulado.
        frontera = [(0.0, inicio)]
        padres: dict[tuple[int, int], tuple[int, int] | None] = {inicio: None}
        costos: dict[tuple[int, int], float] = {inicio: 0.0}

        nodos_explorados = 0

        while frontera:
            # Extrae el nodo con menor costo acumulado.
            costo_actual, actual = heappop(frontera)

            # Puede existir una entrada vieja si encontramos una ruta
            # más barata hacia el mismo nodo después de insertarlo.
            if costo_actual != costos[actual]:
                continue

            nodos_explorados += 1

            if actual == salida:
                break

            for vecino in self.vecinos_ortogonales(mapa, actual):
                fila, columna = vecino

                if mapa[fila][columna] not in CASILLAS_TRANSITABLES:
                    continue

                nuevo_costo = costos[actual] + calcular_costo_casilla(
                    vecino,
                    contexto.ocupacion,
                    contexto.configuracion_costos,
                )

                if vecino not in costos or nuevo_costo < costos[vecino]:
                    costos[vecino] = nuevo_costo
                    padres[vecino] = actual
                    heappush(frontera, (nuevo_costo, vecino))

        if salida not in padres:
            return ResultadoBusqueda(camino=[], costo=float("inf"), nodos_explorados=nodos_explorados, encontrado=False)

        camino = []
        nodo_actual = salida
        while nodo_actual is not None:
            camino.append(nodo_actual)
            nodo_actual = padres[nodo_actual]
        camino.reverse()

        return ResultadoBusqueda(camino=camino, costo=costos[salida], nodos_explorados=nodos_explorados, encontrado=True)