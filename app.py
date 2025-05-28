from flask import Flask, render_template, request, jsonify
import math
import random

app = Flask(__name__)

# Diccionario de coordenadas de ciudades
CITIES = {
    'Jiloyork': (19.916012, -99.580580),
    'Toluca': (19.289165, -99.655697),
    'Atlacomulco': (19.799520, -99.873844),
    'Guadalajara': (20.677754, -103.346253),
    'Monterrey': (25.691611, -100.321838),
    'QuintanaRoo': (21.163111, -86.802315),
    'Michoacán': (19.701400, -101.208296),
    'Aguascalientes': (21.876410, -102.264386),
    'CDMX': (19.432713, -99.133183),
    'Querétaro': (20.597194, -100.386670)
}

# Función para calcular la distancia entre dos ciudades
def distancia(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

# Evaluar una ruta completa
def evalua_ruta(ruta, ciudades):
    total = sum(distancia(ciudades[ruta[i]], ciudades[ruta[i+1]]) for i in range(len(ruta)-1))
    total += distancia(ciudades[ruta[-1]], ciudades[ruta[0]])  # Completa el ciclo
    return total

# Generar vecinos intercambiando dos ciudades en la ruta
def obtener_vecinos(ruta):
    vecinos = []
    for i in range(len(ruta)):
        for j in range(i + 1, len(ruta)):
            vecino = ruta[:]
            vecino[i], vecino[j] = vecino[j], vecino[i]
            vecinos.append(vecino)
    return vecinos

# Algoritmo de búsqueda Tabú con enfriamiento simulado
def busqueda_tabu_enfriamiento(ruta_inicial, max_iteraciones, memoria_tabu_tamano, temperatura_normal, temperatura_minima, velocidad_enfriamiento):
    mejor_ruta = ruta_inicial[:]
    ruta_actual = ruta_inicial[:]
    memoria_tabu = []
    temperatura = temperatura_normal
    iteracion = 0

    while iteracion < max_iteraciones and temperatura > temperatura_minima:
        vecinos = obtener_vecinos(ruta_actual)
        mejor_vecino = None
        mejor_valor = float('inf')

        for vecino in vecinos:
            if vecino not in memoria_tabu:
                valor_vecino = evalua_ruta(vecino, CITIES)
                if valor_vecino < mejor_valor:
                    mejor_valor = valor_vecino
                    mejor_vecino = vecino

        if mejor_vecino:
            ruta_actual = mejor_vecino
            memoria_tabu.append(mejor_vecino)

            # Limitar la memoria Tabú
            if len(memoria_tabu) > memoria_tabu_tamano:
                memoria_tabu.pop(0)

            if mejor_valor < evalua_ruta(mejor_ruta, CITIES):
                mejor_ruta = mejor_vecino

        temperatura *= velocidad_enfriamiento  # Reducir temperatura en cada iteración
        iteracion += 1

    return mejor_ruta

@app.route('/')
def index():
    return render_template('index.html', cities=CITIES.keys())

@app.route('/solve', methods=['POST'])
def solve():
    data = request.form
    max_iteraciones = int(data['max_iteraciones'])
    memoria_tabu_tamano = int(data['memoria_tabu_tamano'])
    temperatura_normal = float(data['temperatura_normal'])
    temperatura_minima = float(data['temperatura_minima'])
    velocidad_enfriamiento = float(data['velocidad_enfriamiento'])
    origin_city = data['origin_city']
    destination_city = data['destination_city']

    # Crear ruta con origen y destino definidos
    ruta = list(CITIES.keys())
    ruta.remove(origin_city)
    ruta.remove(destination_city)
    random.shuffle(ruta)
    ruta = [origin_city] + ruta + [destination_city]

    ruta_optima = busqueda_tabu_enfriamiento(ruta, max_iteraciones, memoria_tabu_tamano, temperatura_normal, temperatura_minima, velocidad_enfriamiento)
    distancia_total = evalua_ruta(ruta_optima, CITIES)

    return jsonify({'ruta': ruta_optima, 'distancia_total': distancia_total})

if __name__ == '__main__':
    app.run(debug=True)
