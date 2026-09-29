from .base import Posicion


def distancia_manhattan(origen: Posicion, objetivo: Posicion) -> int:
    return abs(origen[0] - objetivo[0]) + abs(origen[1] - objetivo[1])
