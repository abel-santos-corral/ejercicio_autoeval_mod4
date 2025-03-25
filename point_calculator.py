def classify_function(points):
    # Ordenar los puntos por el valor de x
    points = sorted(points, key=lambda p: p[0])

    # Extraer las coordenadas x e y
    x_values, y_values = zip(*points)

    # Verificar si es una L-Function
    if y_values[0] == 1 and y_values[-1] == 0 and all(y == 1 for y in y_values[:y_values.index(0)]):
        return "L-Function"

    # Verificar si es una R-Function
    if y_values[0] == 0 and y_values[-1] == 1 and all(y == 0 for y in y_values[:y_values.index(1)]):
        return "R-Function"

    # Verificar si es una función triangular
    if len(y_values) >= 3:
        increasing = any(y2 > y1 for y1, y2 in zip(y_values, y_values[1:]))
        single_peak = y_values.count(max(y_values)) == 1
        decreasing = any(y2 < y1 for y1, y2 in zip(y_values, y_values[1:]))

        if increasing and single_peak and decreasing:
            return "Función Triangular"

    # Verificar si es una función trapezoidal
    if len(y_values) >= 4:
        increasing = any(y2 > y1 for y1, y2 in zip(y_values, y_values[1:]))
        constant_max = any(y_values[i] == y_values[i + 1] == max(y_values) for i in range(len(y_values) - 1))
        decreasing = any(y2 < y1 for y1, y2 in zip(y_values, y_values[1:]))
        constant_min = any(y_values[i] == y_values[i + 1] == min(y_values) for i in range(len(y_values) - 1))

        if increasing and constant_max and decreasing and constant_min:
            return "Función Trapezoidal"

    return "Función Desconocida"

# Ejemplo de uso
puntos_triangular = [(0, 0), (1, 0), (5, 1), (7, 0), (10, 0)]
tipo_funcion_triangular = classify_function(puntos_triangular)
print(f"La función es: {tipo_funcion_triangular}")

# Ejemplo de uso
puntos = [(0, 0), (5, 0), (7, 1), (9, 1), (10, 0), (15, 0)]
tipo_funcion = classify_function(puntos)
print(f"La función es: {tipo_funcion}")