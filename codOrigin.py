Función busqueda_tabu(Estado_actual):
	Mejor_estado = estado_actual
	Inicializar memoria_tabu
	Inicializar persistencia
	Inicializar el número de iteraciones

	Mientras numero_iteraciones >=:
		Numero_iteraciones = numero_iteraciones -1
		Val_actual = evaluar(estado_actual)
		Para cada vecino:
			Estado_nuevo = elegir un estado vecino.
			Si estado_nuevo no es tabu:
				Si estado_nuevo mejora a estado_actual:
					Estado_actual = estado_nuevo
					Almacenar caombio en memoria tabú
					Si estado_actual es mejor que mejor_estado:
						Mejor_estado = estado_actual
					Salir del bucle para
				Si no:
					Si estado_nuevo menor que mejor_estado:
						Estado_actual = estado_nuevo
						Almacenar cambio en memoria tabu
						Mejor_estado = estado_acrual
						Salir del bucle para:
				Decrementar presistencia de estados tabu
Salir con mejor ruta.
