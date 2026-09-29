from .base import AlgoritmoBusqueda, CASILLAS_TRANSITABLES, ContextoBusqueda, ResultadoBusqueda
from .costos import calcular_costo_casilla
from collections import deque

class BFS(AlgoritmoBusqueda):
    nombre = "BFS"

    def buscar(self, contexto: ContextoBusqueda) -> ResultadoBusqueda:
        #Comprobraciones iniciales
        mapa = contexto.mapa
        if not mapa or not mapa[0]:
            return ResultadoBusqueda(camino=[], costo=float("inf"), nodos_explorados=0,encontrado=False)

        inicio = contexto.inicio
        salida = contexto.objetivo

        if inicio is None or salida is None:
            return ResultadoBusqueda(camino=[], costo=float("inf"), nodos_explorados=0,encontrado=False)

        # Cola que representa la frontera de la búsqueda. Se exploran primero los nodos más antiguos.
        cola = deque([inicio])

        # Guarda el nodo anterior de cada posición visitada.
        # Esto permite reconstruir el camino al encontrar la salida.
        padres: dict[tuple[int, int], tuple[int, int] | None] = {inicio: None}
        costos: dict[tuple[int, int], float] = {inicio: 0.0}

        # Cuenta cuántas posiciones fueron retiradas de la cola.
        nodos_explorados = 0

        while cola:
            # BFS siempre procesa primero la posición más antigua.
            actual = cola.popleft()
            nodos_explorados += 1

            # La busqueda termina al alcanzar la salida.
            if actual == salida:
                break

            # Revisa las cuatro posiciones vecinas.
            for vecino in self.vecinos_ortogonales(mapa, actual):
                fila, columna = vecino

                # Ignora paredes y fuego.
                if mapa[fila][columna] not in CASILLAS_TRANSITABLES:
                    continue

                # No vuelve a visitar una posición ya explorada.
                if vecino in padres:
                    continue
                
                # Registra como se llego a esta posición.
                padres[vecino] = actual
                costo = calcular_costo_casilla(
                    vecino,
                    contexto.ocupacion,
                    contexto.configuracion_costos,
                )
                costos[vecino] = costos[actual] + costo
                cola.append(vecino)

        # Si la salida no fue visitada, no existe un camino válido.
        if salida not in padres:
            return ResultadoBusqueda(camino=[], costo=float("inf"), nodos_explorados=nodos_explorados, encontrado=False)

        # Reconstruye el camino desde la salida hasta el inicio.
        camino = []
        posicion_actual = salida

        while posicion_actual is not None:
            camino.append(posicion_actual)
            posicion_actual = padres[posicion_actual]

        # La reconstrucción se hizo al revés.
        camino.reverse()

        return ResultadoBusqueda(
            camino=camino,
            costo=costos[salida],
            nodos_explorados=nodos_explorados,
            encontrado=True,
        )