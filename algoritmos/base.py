from dataclasses import dataclass
from collections import Counter
from typing import Optional
from .costos import ConfiguracionCostos

Posicion = tuple[int, int]
CASILLAS_TRANSITABLES = {0, 3, 4}

@dataclass
class ResultadoBusqueda:
    camino: list[tuple[int, int]]
    costo: float
    nodos_explorados: int
    encontrado: bool

@dataclass
class ContextoBusqueda:
    mapa: list[list[int]]
    inicio: Posicion
    objetivo: Posicion
    ocupacion: Counter[Posicion]
    configuracion_costos: ConfiguracionCostos

class AlgoritmoBusqueda:
    nombre = "Sin nombre"

    def buscar(self, contexto: ContextoBusqueda) -> ResultadoBusqueda:
        raise NotImplementedError("El método 'buscar' debe ser implementado por la subclase.")

    def encontrar_inicio(self, mapa) -> Optional[tuple[int, int]]:
        for fila, valores_fila in enumerate(mapa):
            for columna, valor in enumerate(valores_fila):
                if valor == 4:  # Suponiendo que el valor 4 representa el inicio
                    return fila, columna
        return None

    def encontrar_salida(self, mapa) -> Optional[tuple[int, int]]:
        for fila, valores_fila in enumerate(mapa):
            for columna, valor in enumerate(valores_fila):
                if valor == 3:  # Suponiendo que el valor 3 representa la salida
                    return fila, columna
        return None

    #Devuelve los vecinos ortogonales (arriba, abajo, izquierda y derecha)
    def vecinos_ortogonales(self, mapa, posicion):
        fila, columna = posicion # Posición actual en el mapa
        for cambio_fila, cambio_columna in ((-1, 0), (1, 0), (0, -1), (0, 1)): # Cambios posibles (arriba, abajo, izquierda, derecha)
            vecino = (fila + cambio_fila, columna + cambio_columna) # Nueva posición del vecino
            if 0 <= vecino[0] < len(mapa) and 0 <= vecino[1] < len(mapa[0]): # Verificar que esté en los límites del mapa
                yield vecino # Devuelve el vecino
    
    