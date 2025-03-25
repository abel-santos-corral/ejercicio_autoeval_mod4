def implicacion_logica(temperatura, ventilador_encendido):
    """
    Evalúa la certeza de la implicación 'Si la temperatura es alta, entonces encender ventilador'.
    Se considera:
    - Si temperatura es alta (True) y ventilador apagado (False) → FALSO
    - En cualquier otro caso → VERDADERO
    """
    if temperatura and not ventilador_encendido:
        return False  # Regla rota: temperatura alta y ventilador apagado
    return True  # En todos los demás casos, la implicación se cumple

# Casos de prueba
casos = [
    (True, True),   # Temperatura alta, ventilador encendido → ✅ VERDADERO
    (True, False),  # Temperatura alta, ventilador apagado → ❌ FALSO
    (False, True),  # Temperatura no alta, ventilador encendido → ✅ VERDADERO
    (False, False)  # Temperatura no alta, ventilador apagado → ✅ VERDADERO
]

# Evaluamos los casos
for temp, vent in casos:
    resultado = implicacion_logica(temp, vent)
    print(f"Temp Alta: {temp}, Ventilador Encendido: {vent} → Implicación: {resultado}")
