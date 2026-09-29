
from .bfs import BFS
from .ucs import UCS
from .greedy import Greedy
from .A_star import AStar
from .genetico import Genetico

ALGORITMOS = {
    "BFS": BFS,
    "UCS": UCS,
    "Greedy": Greedy,
    "A*": AStar,
    "genético": Genetico,
}
