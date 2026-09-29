from heapq import heappop, heappush

from .base import (
	AlgoritmoBusqueda,
	CASILLAS_TRANSITABLES,
	ContextoBusqueda,
	ResultadoBusqueda,
)
from .costos import calcular_costo_casilla
from .heuristicas import distancia_manhattan


class Greedy(AlgoritmoBusqueda):
	nombre = "Greedy"

	def buscar(self, contexto: ContextoBusqueda) -> ResultadoBusqueda:
		mapa = contexto.mapa
		inicio = contexto.inicio
		objetivo = contexto.objetivo

		if not mapa or not mapa[0] or inicio is None or objetivo is None:
			return self._sin_camino()

		# La prioridad principal es h(n), la distancia Manhattan al objetivo.
		# El costo acumulado se usa solo para desempatar rutas igual de cercanas.
		frontera = [
			(distancia_manhattan(inicio, objetivo), 0.0, inicio)
		]
		padres: dict[tuple[int, int], tuple[int, int] | None] = {
			inicio: None
		}
		costos: dict[tuple[int, int], float] = {inicio: 0.0}
		nodos_explorados = 0

		while frontera:
			_, _, actual = heappop(frontera)
			nodos_explorados += 1

			if actual == objetivo:
				break

			for vecino in self.vecinos_ortogonales(mapa, actual):
				fila, columna = vecino

				# Las paredes y las casillas consumidas por fuego no se pueden usar.
				if mapa[fila][columna] not in CASILLAS_TRANSITABLES:
					continue

				# Greedy marca la primera visita para evitar ciclos.
				if vecino in padres:
					continue

				costo = calcular_costo_casilla(
					vecino,
					contexto.ocupacion,
					contexto.configuracion_costos,
				)
				costo_acumulado = costos[actual] + costo
				padres[vecino] = actual
				costos[vecino] = costo_acumulado

				prioridad = distancia_manhattan(vecino, objetivo)
				heappush(frontera, (prioridad, costo_acumulado, vecino))

		if objetivo not in padres:
			return ResultadoBusqueda(
				camino=[],
				costo=float("inf"),
				nodos_explorados=nodos_explorados,
				encontrado=False,
			)

		camino = []
		posicion = objetivo

		while posicion is not None:
			camino.append(posicion)
			posicion = padres[posicion]

		camino.reverse()

		return ResultadoBusqueda(
			camino=camino,
			costo=costos[objetivo],
			nodos_explorados=nodos_explorados,
			encontrado=True,
		)

	@staticmethod
	def _sin_camino() -> ResultadoBusqueda:
		return ResultadoBusqueda(
			camino=[],
			costo=float("inf"),
			nodos_explorados=0,
			encontrado=False,
		)
