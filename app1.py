import random

def evaluar(estado):
    """ Función de evaluación, debe ser definida según el problema """
    return sum(estado)

def generar_vecinos(estado):
    """ Genera estados vecinos, depende del problema específico """
    vecinos = []
    for i in range(len(estado)):
        nuevo_estado = estado[:]
        nuevo_estado[i] = random.randint(0, 100)  # Ejemplo de modificación aleatoria
        vecinos.append(nuevo_estado)
    return vecinos

def busqueda_tabu(estado_actual, iteraciones=100, memoria_tabu_tamano=10):
    mejor_estado = estado_actual[:]
    memoria_tabu = []
    persistencia = {}
    numero_iteraciones = iteraciones

    while numero_iteraciones > 0:
        numero_iteraciones -= 1
        val_actual = evaluar(estado_actual)
        vecinos = generar_vecinos(estado_actual)

        for estado_nuevo in vecinos:
            if estado_nuevo not in memoria_tabu:
                if evaluar(estado_nuevo) > val_actual:
                    estado_actual = estado_nuevo[:]
                    memoria_tabu.append(estado_actual)
                    if evaluar(estado_actual) > evaluar(mejor_estado):
                        mejor_estado = estado_actual[:]
                    break
                else:
                    if evaluar(estado_nuevo) > evaluar(mejor_estado):
                        estado_actual = estado_nuevo[:]
                        memoria_tabu.append(estado_actual)
                        mejor_estado = estado_actual[:]
                        break
        
        # Mantener tamaño de la memoria tabú
        if len(memoria_tabu) > memoria_tabu_tamano:
            memoria_tabu.pop(0)

    return mejor_estado

# Ejemplo de uso
estado_inicial = [random.randint(0, 100) for _ in range(5)]
mejor_solucion = busqueda_tabu(estado_inicial)
print("Mejor solución encontrada:", mejor_solucion)
