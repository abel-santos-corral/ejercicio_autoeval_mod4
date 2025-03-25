import numpy as np

def mu(x):
    """Ejemplo de función de pertenencia: Triangular"""
    if 0 <= x < 30:
        return x / 30
    elif 30 <= x < 60:
        return 1
    elif 60 <= x <= 90:
        return (90 - x) / 30
    return 0  # Fuera del rango

def defuzzification(start=0, end=90, step=0.02):
    v_numerador = 0
    v_denominador = 0
    
    x_values = np.arange(start, end + step, step)  # Generamos los valores de x
    for x in x_values:
        membership = mu(x)
        v_numerador += membership * x
        v_denominador += membership
    
    return v_numerador / v_denominador if v_denominador != 0 else None  # Evita división por cero

# Ejecutamos el cálculo de defuzzificación
resultado = defuzzification()
print("Valor defuzzificado:", resultado)
