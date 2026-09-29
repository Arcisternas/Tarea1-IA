from heapq import heappop, heappush

from .base import (
	AlgoritmoBusqueda,
	CASILLAS_TRANSITABLES,
	ContextoBusqueda,
	ResultadoBusqueda,
)
from .costos import calcular_costo_casilla
from .heuristicas import distancia_manhattan


class AStar(AlgoritmoBusqueda):
	nombre = "A*"

	def buscar(self, contexto: ContextoBusqueda) -> ResultadoBusqueda:
		mapa = contexto.mapa
		inicio = contexto.inicio
		objetivo = contexto.objetivo

		if not mapa or not mapa[0] or inicio is None or objetivo is None:
			return self._sin_camino()

		costo_base = contexto.configuracion_costos.costo_base

		# f(n) = g(n) + h(n), donde h(n) es Manhattan escalada por
		# el costo mínimo de realizar un movimiento.
		costo_inicial = 0.0
		frontera = [
			(
				costo_inicial + self._heuristica(
					inicio,
					objetivo,
					costo_base,
				),
				costo_inicial,
				inicio,
			)
		]
		padres: dict[tuple[int, int], tuple[int, int] | None] = {
			inicio: None
		}
		costos: dict[tuple[int, int], float] = {inicio: costo_inicial}
		nodos_explorados = 0

		while frontera:
			_, costo_actual, actual = heappop(frontera)

			# Ignora entradas antiguas que fueron reemplazadas por una
			# ruta más barata hacia el mismo nodo.
			if costo_actual != costos[actual]:
				continue

			nodos_explorados += 1

			if actual == objetivo:
				break

			for vecino in self.vecinos_ortogonales(mapa, actual):
				fila, columna = vecino

				# El fuego y los obstáculos no forman parte del grafo.
				if mapa[fila][columna] not in CASILLAS_TRANSITABLES:
					continue

				costo_movimiento = calcular_costo_casilla(
					vecino,
					contexto.ocupacion,
					contexto.configuracion_costos,
				)
				nuevo_costo = costo_actual + costo_movimiento

				# Solo actualiza el nodo cuando esta ruta es mejor.
				if nuevo_costo >= costos.get(vecino, float("inf")):
					continue

				costos[vecino] = nuevo_costo
				padres[vecino] = actual
				heuristica = self._heuristica(
					vecino,
					objetivo,
					costo_base,
				)
				heappush(
					frontera,
					(nuevo_costo + heuristica, nuevo_costo, vecino),
				)

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
	def _heuristica(
		posicion: tuple[int, int],
		objetivo: tuple[int, int],
		costo_base: float,
	) -> float:
		return distancia_manhattan(posicion, objetivo) * costo_base

	@staticmethod
	def _sin_camino() -> ResultadoBusqueda:
		return ResultadoBusqueda(
			camino=[],
			costo=float("inf"),
			nodos_explorados=0,
			encontrado=False,
		)
