# Tarea1-IA
Integrantes: 
Ariel Cisternas (2023456152)

## Ejecucion

Desde la raiz del proyecto:

```bash
python main.py
```

La interfaz permite ejecutar una simulacion y configurar la cantidad de
agentes, el intervalo entre turnos y la cantidad de repeticiones.

## Benchmark

El modo Benchmark ejecuta las simulaciones sin Tkinter, sin esperas entre
turnos y sin redibujar el mapa. Por defecto ejecuta 200 iteraciones para cada
combinacion de los tres mapas y los cinco algoritmos:

```bash
python benchmark.py
```

El minimo permitido es de 80 iteraciones. Para ejecutar una sola configuracion:

```bash
python benchmark.py --mapa 1 --algoritmo BFS --iteraciones 80 --agentes 150
```

Los algoritmos disponibles son `BFS`, `UCS`, `Greedy`, `A*` y `genetico`.
La semilla base se puede cambiar con `--semilla`; cada iteracion usa una
semilla distinta y reproducible. Los reportes se guardan en `reportes/`.