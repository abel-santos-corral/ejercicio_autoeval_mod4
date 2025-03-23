# Importar librerías necesarias
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
import os

# Crear carpetas de salida si no existen
output_dirs = [
    'data/output/variables_linguisticas',
    'data/output/funcion_pertenencia',
    'data/output/puntos_corte',
    'data/output/salida'
]

for directory in output_dirs:
    os.makedirs(directory, exist_ok=True)


def piecewise_linear(x, puntos):
    x_points = np.array(puntos[::2])
    y_points = np.array(puntos[1::2])
    return np.interp(x, x_points, y_points)


def graficar_y_guardar(x, mfs, nombre_variable):
    plt.figure()
    for nombre, mf in mfs.items():
        plt.plot(x, mf, label=nombre)
    plt.title(f'Variable lingüística: {nombre_variable}')
    plt.xlabel(nombre_variable)
    plt.ylabel('Pertenencia')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'data/output/variables_linguisticas/{nombre_variable}.png')
    plt.close()


def guardar_funcion_pertenencia(nombre_variable, mfs):
    with open(f'data/output/funcion_pertenencia/{nombre_variable}.md', 'w') as file:
        file.write(f'# {nombre_variable}\n\n')
        for nombre, puntos in mfs.items():
            file.write(f'## {nombre}\n\n')
            file.write(f'{puntos}\n\n')


def calcular_puntos_corte(valor, x, mfs, nombre_variable):
    cortes = {}
    plt.figure()
    for nombre, mf in mfs.items():
        pertenencia = np.interp(valor, x, mf)
        if pertenencia > 0:
            cortes[nombre] = pertenencia
            plt.plot(x, mf, label=f'{nombre} (corte: {pertenencia:.2f})')
    plt.title(f'Cortes para {nombre_variable} = {valor}')
    plt.xlabel(nombre_variable)
    plt.ylabel('Pertenencia')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'data/output/puntos_corte/{nombre_variable}_corte.png')
    plt.close()
    return cortes


def guardar_puntos_corte(nombre_variable, cortes):
    with open(f'data/output/puntos_corte/puntos_corte.md', 'a') as file:
        file.write(f'# {nombre_variable}\n\n')
        for nombre, pertenencia in cortes.items():
            file.write(f'- {nombre}: {pertenencia}\n')
        file.write('\n')


def aplicar_reglas(cortes_VarA, cortes_VarB, cortes_VarC):
    reglas = {
        'R1': max(cortes_VarA.get('L', 0), cortes_VarB.get('L', 0), cortes_VarC.get('L', 0)),
        'R2': max(cortes_VarA.get('M', 0), cortes_VarB.get('L', 0), cortes_VarC.get('M', 0)),
        'R3': max(cortes_VarA.get('M', 0), cortes_VarB.get('L', 0), cortes_VarC.get('L', 0)),
        'R4': max(cortes_VarA.get('VL', 0), cortes_VarB.get('L', 0), cortes_VarC.get('VL', 0)),
        'R5': max(cortes_VarA.get('M', 0), cortes_VarB.get('M', 0), cortes_VarC.get('L', 0)),
        'R6': max(cortes_VarA.get('M', 0), cortes_VarB.get('M', 0), cortes_VarC.get('H', 0)),
        'R7': max(cortes_VarA.get('H', 0), cortes_VarB.get('H', 0), cortes_VarC.get('H', 0))
    }
    return reglas


def defuzzificar(reglas, x_Out, Out_mfs):
    salida_L = np.fmin(reglas['R1'], Out_mfs['L'])
    salida_M = np.fmin(reglas['R5'], Out_mfs['M'])
    salida_H = np.fmin(max(reglas['R6'], reglas['R7']), Out_mfs['H'])
    salida_aggregada = np.fmax(salida_L, np.fmax(salida_M, salida_H))

    plt.figure()
    plt.plot(x_Out, salida_L, label='L')
    plt.plot(x_Out, salida_M, label='M')
    plt.plot(x_Out, salida_H, label='H')
    plt.plot(x_Out, salida_aggregada, label='Salida Agregada', linestyle='--')
    plt.title('Función de pertenencia de salida')
    plt.legend()
    plt.grid(True)
    plt.savefig('data/output/salida/funcion_pertenencia.png')
    plt.close()

    salida_defuzzificada = fuzz.defuzz(x_Out, salida_aggregada, 'centroid')
    with open('data/output/salida/salida_sistema.md', 'w') as file:
        file.write(f'# Resultado del Sistema\n\n')
        file.write(f'Salida Nítida: {salida_defuzzificada}\n')

    return salida_defuzzificada


if __name__ == "__main__":
    # Definición de variables lingüísticas
    x_VarA = np.linspace(0, 15, 100)
    x_VarB = np.linspace(0, 10, 100)
    x_VarC = np.linspace(-5, 10, 100)
    x_Out = np.linspace(0, 10, 100)

    VarA_mfs = {
        'VL': piecewise_linear(x_VarA, [0, 1, 2, 1, 3, 0, 15, 0]),
        'L': piecewise_linear(x_VarA, [0, 0, 3, 1, 4, 1, 7, 0, 15, 0]),
        'M': piecewise_linear(x_VarA, [0, 0, 5, 0, 7, 1, 9, 1, 10, 0, 15, 0]),
        'H': piecewise_linear(x_VarA, [0, 0, 9, 0, 10, 1, 12, 1, 15, 0]),
        'VH': piecewise_linear(x_VarA, [0, 0, 12, 0, 13, 1, 15, 1])
    }
    graficar_y_guardar(x_VarA, VarA_mfs, "VarA")
    guardar_funcion_pertenencia("VarA", VarA_mfs)

    VarB_mfs = {
        'L': piecewise_linear(x_VarB, [0, 1, 1, 1, 4, 0, 10, 0]),
        'M': piecewise_linear(x_VarB, [0, 0, 1, 0, 5, 1, 7, 0, 10, 0]),
        'H': piecewise_linear(x_VarB, [0, 0, 6, 0, 9, 1, 10, 1])
    }
    graficar_y_guardar(x_VarB, VarB_mfs, "VarB")
    guardar_funcion_pertenencia("VarB", VarB_mfs)

    VarC_mfs = {
        'VL': piecewise_linear(x_VarC, [-5, 1, -4, 1, -2, 0, 10, 0]),
        'L': piecewise_linear(x_VarC, [-5, 0, -4, 0, -2, 1, 0, 1, 4, 0, 10, 0]),
        'M': piecewise_linear(x_VarC, [-5, 0, 0, 0, 2, 1, 4, 0, 10, 0]),
        'H': piecewise_linear(x_VarC, [-5, 0, 2, 0, 5, 1, 10, 1])
    }
    graficar_y_guardar(x_VarC, VarC_mfs, "VarC")
    guardar_funcion_pertenencia("VarC", VarC_mfs)

    Out_mfs = {
        'L': piecewise_linear(x_Out, [0, 1, 3, 1, 6, 0, 10, 0]),
        'M': piecewise_linear(x_Out, [0, 0, 4, 0, 5, 1, 6, 0, 10, 0]),
        'H': piecewise_linear(x_Out, [0, 0, 3, 0, 7, 1, 10, 1])
    }
    graficar_y_guardar(x_Out, Out_mfs, "Out")
    guardar_funcion_pertenencia("Out", Out_mfs)

    # Calcular puntos de corte
    cortes_VarA = calcular_puntos_corte(6, x_VarA, VarA_mfs, "VarA")
    cortes_VarB = calcular_puntos_corte(2, x_VarB, VarB_mfs, "VarB")
    cortes_VarC = calcular_puntos_corte(3, x_VarC, VarC_mfs, "VarC")
    guardar_puntos_corte("VarA", cortes_VarA)
    guardar_puntos_corte("VarB", cortes_VarB)
    guardar_puntos_corte("VarC", cortes_VarC)

    # Aplicar reglas
    reglas = aplicar_reglas(cortes_VarA, cortes_VarB, cortes_VarC)

    # Calcular la salida del sistema
    salida = defuzzificar(reglas, x_Out, Out_mfs)
    print(f"Salida Nítida del Sistema: {salida}")
