"""
HU02 - Evolución individual del estudiante
Muestra cómo han cambiado las notas de un estudiante a lo largo de los tres periodos
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def cargar_datos():
    """Carga el archivo CSV con los datos"""
    ruta_csv = os.path.join('..', 'data', 'data-generada.csv')
    try:
        df = pd.read_csv(ruta_csv)
        return df
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {ruta_csv}")
        return None

def buscar_estudiante(df, busqueda):
    """Busca un estudiante por ID o nombre"""
    try:
        # Intentar buscar por ID
        id_estudiante = int(busqueda)
        estudiante_df = df[df['id_estudiante'] == id_estudiante]
    except ValueError:
        # Buscar por nombre (insensible a mayúsculas)
        estudiante_df = df[df['nombre'].str.lower() == busqueda.lower()]

    return estudiante_df

def calcular_promedios_por_periodo(df_estudiante):
    """Calcula el promedio de cada periodo para todas las asignaturas"""
    resultados = []

    for periodo in [1, 2, 3]:
        df_periodo = df_estudiante[df_estudiante['periodo'] == periodo]

        for _, row in df_periodo.iterrows():
            promedio = (row['nota1'] + row['nota2'] + row['nota3']) / 3
            resultados.append({
                'Asignatura': row['asignatura'],
                'Periodo': periodo,
                'Nota1': row['nota1'],
                'Nota2': row['nota2'],
                'Nota3': row['nota3'],
                'Promedio': round(promedio, 2)
            })

    return pd.DataFrame(resultados)

def mostrar_tabla(df_resultados, nombre_estudiante):
    """Muestra la tabla de notas por periodo en consola"""
    print("\n" + "="*80)
    print(f"EVOLUCIÓN DE NOTAS - {nombre_estudiante}")
    print("="*80)

    for periodo in [1, 2, 3]:
        df_periodo = df_resultados[df_resultados['Periodo'] == periodo]
        print(f"\n{'PERIODO ' + str(periodo):^80}")
        print("-"*80)
        print(f"{'Asignatura':<25} {'Nota 1':>10} {'Nota 2':>10} {'Nota 3':>10} {'Promedio':>10}")
        print("-"*80)

        for _, row in df_periodo.iterrows():
            print(f"{row['Asignatura']:<25} {row['Nota1']:>10.2f} {row['Nota2']:>10.2f} {row['Nota3']:>10.2f} {row['Promedio']:>10.2f}")

        promedio_periodo = df_periodo['Promedio'].mean()
        print("-"*80)
        print(f"{'PROMEDIO GENERAL DEL PERIODO':<25} {'':<30} {promedio_periodo:>10.2f}")

    print("="*80)

def graficar_evolucion(df_resultados, nombre_estudiante):
    """Crea el gráfico de evolución del estudiante"""
    # Calcular promedio general por periodo
    promedios_periodo = df_resultados.groupby('Periodo')['Promedio'].mean()

    # Crear figura con tamaño adecuado
    plt.figure(figsize=(12, 8))

    # Obtener asignaturas únicas
    asignaturas = df_resultados['Asignatura'].unique()

    # Colores para cada asignatura
    colores = plt.cm.tab10(np.linspace(0, 1, len(asignaturas)))

    # Graficar evolución de cada asignatura
    for i, asignatura in enumerate(asignaturas):
        df_asignatura = df_resultados[df_resultados['Asignatura'] == asignatura]
        periodos = df_asignatura['Periodo'].values
        promedios = df_asignatura['Promedio'].values

        plt.plot(periodos, promedios, marker='o', linewidth=2,
                label=asignatura, color=colores[i], markersize=8)

    # Graficar promedio general
    plt.plot([1, 2, 3], promedios_periodo.values, marker='s', linewidth=3,
            label='PROMEDIO GENERAL', color='red', markersize=10, linestyle='--')

    # Configurar el gráfico
    plt.title(f'Evolución de Notas - {nombre_estudiante}', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Periodo', fontsize=12, fontweight='bold')
    plt.ylabel('Promedio de Notas', fontsize=12, fontweight='bold')
    plt.xticks([1, 2, 3], ['Periodo 1', 'Periodo 2', 'Periodo 3'])
    plt.ylim(0, 5.5)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.legend(loc='best', fontsize=9, framealpha=0.9)

    # Añadir línea de referencia de aprobado (3.0)
    plt.axhline(y=3.0, color='orange', linestyle=':', linewidth=2, alpha=0.5, label='Nota mínima (3.0)')

    plt.tight_layout()

    # Guardar el gráfico
    ruta_salida = os.path.join('..', 'outputs', 'evolucion_estudiante.png')
    plt.savefig(ruta_salida, dpi=300, bbox_inches='tight')
    print(f"\n✅ Gráfico guardado exitosamente en: {ruta_salida}")

    plt.show()

def main():
    """Función principal del programa"""
    print("\n" + "="*80)
    print("HU02 - EVOLUCIÓN INDIVIDUAL DEL ESTUDIANTE".center(80))
    print("="*80)

    # Cargar datos
    df = cargar_datos()
    if df is None:
        return

    # Solicitar nombre o ID del estudiante
    busqueda = input("\nIngrese el nombre o ID del estudiante: ").strip()

    # Buscar estudiante
    df_estudiante = buscar_estudiante(df, busqueda)

    if df_estudiante.empty:
        print(f"\n❌ No se encontró ningún estudiante con: '{busqueda}'")
        print("\nEstudiantes disponibles:")
        estudiantes_unicos = df[['id_estudiante', 'nombre']].drop_duplicates().sort_values('id_estudiante')
        for _, row in estudiantes_unicos.iterrows():
            print(f"  - ID: {row['id_estudiante']} - {row['nombre']}")
        return

    # Obtener nombre del estudiante
    nombre_estudiante = df_estudiante['nombre'].iloc[0]
    id_estudiante = df_estudiante['id_estudiante'].iloc[0]

    print(f"\n✅ Estudiante encontrado: {nombre_estudiante} (ID: {id_estudiante})")

    # Calcular promedios por periodo
    df_resultados = calcular_promedios_por_periodo(df_estudiante)

    # Mostrar tabla
    mostrar_tabla(df_resultados, nombre_estudiante)

    # Graficar evolución
    graficar_evolucion(df_resultados, nombre_estudiante)

    print("\n✅ Proceso completado exitosamente")

if __name__ == "__main__":
    main()

