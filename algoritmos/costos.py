from collections import Counter
from dataclasses import dataclass
from typing import Iterable

Posicion = tuple[int, int]

@dataclass(frozen=True)
class ConfiguracionCostos:
    costo_base: float = 1.0
    peso_congestion: float = 1.0
    capacidad_casilla: int = 10
    capacidad_salida: int = 20

def calcular_ocupacion(agentes: Iterable[Posicion]) -> Counter[Posicion]:
    return Counter(agentes)

def calcular_costo_casilla(posicion: Posicion, ocupacion: Counter[Posicion], configuracion: ConfiguracionCostos) -> float:
    cantidad_agentes = ocupacion.get(posicion, 0)

    return configuracion.costo_base + cantidad_agentes * configuracion.peso_congestion


def capacidad_de_casilla(
    posicion: Posicion,
    salida: Posicion | None,
    configuracion: ConfiguracionCostos,
) -> int:
    if salida is not None and posicion == salida:
        return configuracion.capacidad_salida
    return configuracion.capacidad_casilla


def casilla_disponible(
    posicion: Posicion,
    ocupacion: Counter[Posicion],
    configuracion: ConfiguracionCostos,
    salida: Posicion | None = None,
) -> bool:
    return ocupacion.get(posicion, 0) < capacidad_de_casilla(
        posicion,
        salida,
        configuracion,
    )