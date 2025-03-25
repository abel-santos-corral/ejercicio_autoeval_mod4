import numpy as np

def implicacion_zadeh(mu_A, mu_B):
    """
    Implementa la implicación difusa de Zadeh:
    Implicación(A → B) = max(1 - mu_A, mu_B)
    """
    return np.maximum(1 - mu_A, mu_B)

# Valores difusos de temperatura (A) y ventilador (B)
mu_temperatura = np.array([0.0, 0.2, 0.5, 0.8, 1.0])  # Grado de "Temperatura Alta"
mu_ventilador  = np.array([0.1, 0.3, 0.6, 0.9, 1.0])  # Grado de "Ventilador Encendido"

# Aplicamos la implicación difusa
implicacion_resultado = implicacion_zadeh(mu_temperatura, mu_ventilador)

# Mostramos los resultados
print("Temperatura Alta  :", mu_temperatura)
print("Ventilador Encendido :", mu_ventilador)
print("Implicación Difusa :", implicacion_resultado)
