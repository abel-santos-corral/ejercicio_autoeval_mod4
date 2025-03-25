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

def guardar_funcion_pertenencia(nombre_variable, arrays):
    def imprimir_trapezoidal(nombre_variable, a, b, c, d):
        return (f'μ({nombre_variable}) = ' + r'$\left\{\begin{array}{ll}') + \
               (f'0 & \\text{{si }} x \\leq {a}, \\\\') + \
               (f'\\frac{{x-{a}}}{{{b}-{a}}} & \\text{{si }} {a} < x \\leq {b}, \\\\') + \
               (f'1 & \\text{{si }} {b} < x \\leq {c}, \\\\') + \
               (f'\\frac{{{d}-x}}{{{d}-{c}}} & \\text{{si }} {c} < x \\leq {d}, \\\\') + \
               (f'0 & \\text{{si }} x > {d}.') + \
               r'\end{array}\right.$'

    def imprimir_triangular(nombre_variable, a, b, c, d):
        return (f'μ({nombre_variable}) = ' + r'$\left\{\begin{array}{ll}') + \
               (f'0 & \\text{{si }} x \\leq {a}, \\\\') + \
               (f'\\frac{{x-{a}}}{{{b}-{a}}} & \\text{{si }} {a} < x \\leq {b}, \\\\') + \
               (f'\\frac{{{d}-x}}{{{d}-{b}}} & \\text{{si }} {b} < x \\leq {d}, \\\\') + \
               (f'0 & \\text{{si }} x > {d}.') + \
               r'\end{array}\right.$'

    def imprimir_lfunction(nombre_variable, a, b, c, d):
        return (f'μ({nombre_variable}) = ' + r'$\left\{\begin{array}{ll}') + \
               (f'1 & \\text{{si }} x \\leq {a}, \\\\') + \
               (f'\\frac{{{c}-x}}{{{c}-{a}}} & \\text{{si }} {a} < x \\leq {c}, \\\\') + \
               (f'0 & \\text{{si }} x > {c}.') + \
               r'\end{array}\right.$'

    def imprimir_rfunction(nombre_variable, a, b, c, d):
        return (f'μ({nombre_variable}) = ' + r'$\left\{\begin{array}{ll}') + \
               (f'0 & \\text{{si }} x \\leq {a}, \\\\') + \
               (f'\\frac{{x-{a}}}{{{c}-{a}}} & \\text{{si }} {a} < x \\leq {c}, \\\\') + \
               (f'1 & \\text{{si }} x > {c}.') + \
               r'\end{array}\right.$'

    with open(f'data/output/funcion_pertenencia/{nombre_variable}.md', 'w') as file:
        file.write(f'# {nombre_variable}\n\n')
        for nombre, valores in arrays.items():
            file.write(f'## {nombre}\n\n')
            x_points = np.array(valores[::2])
            y_points = np.array(valores[1::2])

            # Formatear los puntos como (x, y) y convertirlos a enteros de Python
            puntos_formateados = [(int(x), int(y)) for x, y in zip(x_points, y_points)]
            file.write(f'Puntos: {puntos_formateados}\n\n')

            # Encontrar los puntos donde la función cambia de valor
            changes = np.where(np.diff(y_points) != 0)[0]

            if len(changes) == 1:  # Triangular
                a, b, c, d = int(x_points[0]), int(x_points[changes[0]]), int(x_points[changes[0]]), int(x_points[-1])
                tipo = "Triangular"
                funcion_str = imprimir_triangular(nombre_variable, a, b, c, d)
            elif len(changes) == 2:  # Trapezoidal
                a, b, c, d = int(x_points[changes[0]]), int(x_points[changes[1]]), int(x_points[changes[1]]), int(x_points[-1])
                tipo = "Trapezoidal"
                funcion_str = imprimir_trapezoidal(nombre_variable, a, b, c, d)
            elif y_points[0] == 1 and y_points[-1] == 0:  # LFunction
                # Detectamos los puntos de la LFunction correctamente:
                a = int(x_points[0])  # Primero donde es 1
                b = int(x_points[changes[0]])  # Donde empieza a decrecer
                c = int(x_points[-1])  # Donde llega a 0
                tipo = "LFunction"
                funcion_str = imprimir_lfunction(nombre_variable, a, b, c, c)
            elif y_points[0] == 0 and y_points[-1] == 1:  # RFunction
                a, b, c, d = int(x_points[0]), int(x_points[changes[0]]), int(x_points[changes[1]]), int(x_points[-1])
                tipo = "RFunction"
                funcion_str = imprimir_rfunction(nombre_variable, a, b, c, d)
            else:
                continue

            file.write('Función de pertenencia:\n\n')
            file.write(funcion_str + '\n')
            file.write(f'Tipo: {tipo}\n\n')


def definir_matrices():
    global VarA_arrays, VarB_arrays, VarC_arrays, Out_arrays
    VarA_arrays = {
        'VL': [0, 1, 2, 1, 3, 0, 15, 0],
        'L': [0, 0, 3, 1, 4, 1, 7, 0, 15, 0],
        'M': [0, 0, 5, 0, 7, 1, 9, 1, 10, 0, 15, 0],
        'H': [0, 0, 9, 0, 10, 1, 12, 1, 15, 0],
        'VH': [0, 0, 12, 0, 13, 1, 15, 1]
    }
    VarB_arrays = {
        'L': [0, 1, 1, 1, 4, 0, 10, 0],
        'M': [0, 0, 1, 0, 5, 1, 7, 0, 10, 0],
        'H': [0, 0, 6, 0, 9, 1, 10, 1]
    }
    VarC_arrays = {
        'VL': [-5, 1, -4, 1, -2, 0, 10, 0],
        'L': [-5, 0, -4, 0, -2, 1, 0, 1, 4, 0, 10, 0],
        'M': [-5, 0, 0, 0, 2, 1, 4, 0, 10, 0],
        'H': [-5, 0, 2, 0, 5, 1, 10, 1]
    }
    Out_arrays = {
        'L': [0, 1, 3, 1, 6, 0, 10, 0],
        'M': [0, 0, 4, 0, 5, 1, 6, 0, 10, 0],
        'H': [0, 0, 3, 0, 7, 1, 10, 1]
    }

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
    definir_matrices()

    x_VarA = np.linspace(0, 15, 100)
    x_VarB = np.linspace(0, 10, 100)
    x_VarC = np.linspace(-5, 10, 100)
    x_Out = np.linspace(0, 10, 100)

    VarA_mfs = {nombre: piecewise_linear(x_VarA, valores) for nombre, valores in VarA_arrays.items()}
    VarB_mfs = {nombre: piecewise_linear(x_VarB, valores) for nombre, valores in VarB_arrays.items()}
    VarC_mfs = {nombre: piecewise_linear(x_VarC, valores) for nombre, valores in VarC_arrays.items()}
    Out_mfs = {nombre: piecewise_linear(x_Out, valores) for nombre, valores in Out_arrays.items()}

    graficar_y_guardar(x_VarA, VarA_mfs, "VarA")
    guardar_funcion_pertenencia("VarA", VarA_arrays)

    graficar_y_guardar(x_VarB, VarB_mfs, "VarB")
    guardar_funcion_pertenencia("VarB", VarB_arrays)

    graficar_y_guardar(x_VarC, VarC_mfs, "VarC")
    guardar_funcion_pertenencia("VarC", VarC_arrays)

    graficar_y_guardar(x_Out, Out_mfs, "Out")
    guardar_funcion_pertenencia("Out", Out_arrays)


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
