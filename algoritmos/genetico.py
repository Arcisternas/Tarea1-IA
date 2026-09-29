import random
from dataclasses import dataclass

from .base import (
	AlgoritmoBusqueda,
	CASILLAS_TRANSITABLES,
	ContextoBusqueda,
	ResultadoBusqueda,
)
from .costos import calcular_costo_casilla
from .heuristicas import distancia_manhattan


MOVIMIENTOS = {
	"U": (-1, 0),
	"D": (1, 0),
	"L": (0, -1),
	"R": (0, 1),
	"W": (0, 0),
}


@dataclass
class Evaluacion:
	costo: float
	camino: list[tuple[int, int]]
	encontrado: bool


class Genetico(AlgoritmoBusqueda):
	nombre = "Algoritmo genético"

	def __init__(
		self,
		tamano_poblacion=40,
		generaciones=35,
		tasa_mutacion=0.08,
		elitismo=4,
		semilla=None,
	):
		if tamano_poblacion < 2:
			raise ValueError("La población debe tener al menos dos individuos")
		if generaciones < 1:
			raise ValueError("Debe existir al menos una generación")
		if not 0 <= tasa_mutacion <= 1:
			raise ValueError("La tasa de mutación debe estar entre 0 y 1")
		if not 1 <= elitismo <= tamano_poblacion:
			raise ValueError("El elitismo debe estar dentro del tamaño de población")

		self.tamano_poblacion = tamano_poblacion
		self.generaciones = generaciones
		self.tasa_mutacion = tasa_mutacion
		self.elitismo = elitismo
		self.rng = random.Random(semilla)

	def buscar(self, contexto: ContextoBusqueda) -> ResultadoBusqueda:
		mapa = contexto.mapa
		inicio = contexto.inicio
		objetivo = contexto.objetivo

		if not mapa or not mapa[0] or inicio is None or objetivo is None:
			return self._sin_camino()

		if inicio == objetivo:
			return ResultadoBusqueda(
				camino=[inicio],
				costo=0.0,
				nodos_explorados=1,
				encontrado=True,
			)

		longitud = self._longitud_cromosoma(inicio, objetivo)
		poblacion = [
			self._crear_individuo(longitud)
			for _ in range(self.tamano_poblacion)
		]
		mejor = None
		nodos_explorados = 0

		for _ in range(self.generaciones):
			evaluaciones = []

			for individuo in poblacion:
				evaluacion = self._evaluar(individuo, contexto)
				evaluaciones.append((evaluacion, individuo))
				nodos_explorados += 1

			evaluaciones.sort(key=lambda elemento: elemento[0].costo)

			if mejor is None or evaluaciones[0][0].costo < mejor.costo:
				mejor = evaluaciones[0][0]

			if mejor.encontrado:
				break

			nueva_poblacion = [
				individuo[:]
				for _, individuo in evaluaciones[:self.elitismo]
			]

			while len(nueva_poblacion) < self.tamano_poblacion:
				padre_a = self._seleccion_torneo(evaluaciones)
				padre_b = self._seleccion_torneo(evaluaciones)
				hijo_a, hijo_b = self._cruzar(padre_a, padre_b)

				self._mutar(hijo_a)
				self._mutar(hijo_b)
				nueva_poblacion.append(hijo_a)

				if len(nueva_poblacion) < self.tamano_poblacion:
					nueva_poblacion.append(hijo_b)

			poblacion = nueva_poblacion

		if mejor is None:
			return self._sin_camino()

		return ResultadoBusqueda(
			camino=mejor.camino,
			costo=mejor.costo,
			nodos_explorados=nodos_explorados,
			encontrado=mejor.encontrado,
		)

	def _evaluar(self, individuo, contexto: ContextoBusqueda) -> Evaluacion:
		posicion = contexto.inicio
		objetivo = contexto.objetivo
		camino = [posicion]
		costo_total = 0.0
		penalizacion = 0.0

		for accion in individuo:
			cambio_fila, cambio_columna = MOVIMIENTOS[accion]
			siguiente = (
				posicion[0] + cambio_fila,
				posicion[1] + cambio_columna,
			)

			if accion == "W":
				costo_total += contexto.configuracion_costos.costo_base
				camino.append(posicion)
				continue

			if not self._es_transitable(contexto.mapa, siguiente):
				penalizacion += 1000.0
				camino.append(posicion)
				continue

			costo_total += calcular_costo_casilla(
				siguiente,
				contexto.ocupacion,
				contexto.configuracion_costos,
			)
			posicion = siguiente
			camino.append(posicion)

			if posicion == objetivo:
				break

		distancia_restante = distancia_manhattan(posicion, objetivo)
		costo_total += distancia_restante * contexto.configuracion_costos.costo_base
		costo_total += penalizacion

		if posicion == objetivo:
			costo_total -= 10000.0

		return Evaluacion(
			costo=costo_total,
			camino=camino,
			encontrado=posicion == objetivo,
		)

	def _seleccion_torneo(self, evaluaciones, tamano_torneo=3):
		candidatos = self.rng.sample(
			evaluaciones,
			min(tamano_torneo, len(evaluaciones)),
		)
		_, individuo = min(
			candidatos,
			key=lambda elemento: elemento[0].costo,
		)
		return individuo[:]

	def _cruzar(self, padre_a, padre_b):
		if len(padre_a) < 2:
			return padre_a[:], padre_b[:]

		punto = self.rng.randint(1, len(padre_a) - 1)
		return (
			padre_a[:punto] + padre_b[punto:],
			padre_b[:punto] + padre_a[punto:],
		)

	def _mutar(self, individuo):
		acciones = tuple(MOVIMIENTOS)

		for indice in range(len(individuo)):
			if self.rng.random() < self.tasa_mutacion:
				individuo[indice] = self.rng.choice(acciones)

	@staticmethod
	def _es_transitable(mapa, posicion):
		fila, columna = posicion

		if not (0 <= fila < len(mapa) and 0 <= columna < len(mapa[0])):
			return False

		return mapa[fila][columna] in CASILLAS_TRANSITABLES

	@staticmethod
	def _longitud_cromosoma(inicio, objetivo):
		# El margen permite rodear obstáculos sin hacer el cromosoma enorme.
		return max(8, distancia_manhattan(inicio, objetivo) + 12)

	def _crear_individuo(self, longitud):
		acciones = tuple(MOVIMIENTOS)
		return [self.rng.choice(acciones) for _ in range(longitud)]

	@staticmethod
	def _sin_camino():
		return ResultadoBusqueda(
			camino=[],
			costo=float("inf"),
			nodos_explorados=0,
			encontrado=False,
		)
