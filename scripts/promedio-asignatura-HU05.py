"""
HU05 - Promedio por asignatura
Como profesor, quiero ver los promedios por asignatura,
para saber en qué materia los estudiantes están teniendo más dificultad.
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

def calcular_promedio_notas(df):
    """Calcula el promedio de nota1, nota2 y nota3 para cada registro"""
    df['promedio_notas'] = (df['nota1'] + df['nota2'] + df['nota3']) / 3
    return df

def calcular_promedios_por_asignatura(df):
    """Calcula los promedios agrupados por asignatura"""
    # Calcular promedio de las 3 notas
    df = calcular_promedio_notas(df)

    # Agrupar por asignatura y calcular estadísticas
    promedios = df.groupby('asignatura').agg({
        'promedio_notas': ['mean', 'std', 'count'],
        'nota1': 'mean',
        'nota2': 'mean',
        'nota3': 'mean'
    }).round(2)

    # Renombrar columnas para mejor legibilidad
    promedios.columns = ['Promedio_General', 'Desviacion_Std', 'Total_Registros',
                         'Promedio_Nota1', 'Promedio_Nota2', 'Promedio_Nota3']

    # Ordenar por promedio general (de menor a mayor para identificar dificultades)
    promedios = promedios.sort_values('Promedio_General')

    return promedios

def calcular_promedio_general(df):
    """Calcula el promedio general cuando no hay columna de asignatura"""
    df = calcular_promedio_notas(df)

    promedio_general = df['promedio_notas'].mean()
    desviacion = df['promedio_notas'].std()
    total_registros = len(df)

    return {
        'Promedio_General': round(promedio_general, 2),
        'Desviacion_Std': round(desviacion, 2),
        'Total_Registros': total_registros
    }

def mostrar_tabla_asignaturas(promedios_df):
    """Muestra la tabla de promedios por asignatura en consola"""
    print("\n" + "="*100)
    print("PROMEDIOS POR ASIGNATURA".center(100))
    print("="*100)

    print(f"\n{'Asignatura':<25} {'Promedio':>12} {'Desv. Std':>12} {'Registros':>12} "
          f"{'Nota 1':>10} {'Nota 2':>10} {'Nota 3':>10}")
    print("-"*100)

    for asignatura, row in promedios_df.iterrows():
        print(f"{asignatura:<25} {row['Promedio_General']:>12.2f} {row['Desviacion_Std']:>12.2f} "
              f"{int(row['Total_Registros']):>12} {row['Promedio_Nota1']:>10.2f} "
              f"{row['Promedio_Nota2']:>10.2f} {row['Promedio_Nota3']:>10.2f}")

    print("-"*100)
    promedio_total = promedios_df['Promedio_General'].mean()
    print(f"{'PROMEDIO GENERAL DEL CURSO':<25} {promedio_total:>12.2f}")
    print("="*100)

    # Identificar asignaturas con dificultad
    print("\n" + "="*100)
    print("ANÁLISIS DE DIFICULTAD".center(100))
    print("="*100)

    asignaturas_dificiles = promedios_df[promedios_df['Promedio_General'] < 3.0]
    if not asignaturas_dificiles.empty:
        print("\n⚠️  ASIGNATURAS CON PROMEDIO BAJO (< 3.0):")
        for asignatura, row in asignaturas_dificiles.iterrows():
            print(f"  • {asignatura}: {row['Promedio_General']:.2f}")
    else:
        print("\n✅ Todas las asignaturas tienen promedio >= 3.0")

    asignaturas_criticas = promedios_df[promedios_df['Promedio_General'] < promedio_total - 0.5]
    if not asignaturas_criticas.empty:
        print(f"\n⚠️  ASIGNATURAS POR DEBAJO DEL PROMEDIO GENERAL ({promedio_total:.2f}):")
        for asignatura, row in asignaturas_criticas.iterrows():
            diferencia = promedio_total - row['Promedio_General']
            print(f"  • {asignatura}: {row['Promedio_General']:.2f} (−{diferencia:.2f})")

    print("="*100)

def mostrar_tabla_general(stats):
    """Muestra la tabla de promedio general en consola"""
    print("\n" + "="*80)
    print("PROMEDIO GENERAL DEL CURSO".center(80))
    print("="*80)

    print(f"\nPromedio General:     {stats['Promedio_General']:.2f}")
    print(f"Desviación Estándar:  {stats['Desviacion_Std']:.2f}")
    print(f"Total de Registros:   {stats['Total_Registros']}")

    print("\n" + "="*80)

def graficar_promedios_asignaturas(promedios_df):
    """Crea el gráfico de barras con los promedios por asignatura"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

    # Gráfico 1: Barras horizontales ordenadas
    asignaturas = promedios_df.index
    promedios = promedios_df['Promedio_General'].values

    # Colores según el promedio (rojo < 3.0, amarillo 3.0-3.5, verde > 3.5)
    colores = []
    for promedio in promedios:
        if promedio < 3.0:
            colores.append('#e74c3c')  # Rojo
        elif promedio < 3.5:
            colores.append('#f39c12')  # Amarillo
        else:
            colores.append('#27ae60')  # Verde

    bars = ax1.barh(asignaturas, promedios, color=colores, alpha=0.8, edgecolor='black')

    # Añadir valores en las barras
    for i, (bar, promedio) in enumerate(zip(bars, promedios)):
        ax1.text(promedio + 0.05, i, f'{promedio:.2f}',
                va='center', fontweight='bold', fontsize=10)

    # Línea de referencia
    promedio_general = promedios.mean()
    ax1.axvline(x=3.0, color='red', linestyle='--', linewidth=2, alpha=0.5, label='Nota mínima (3.0)')
    ax1.axvline(x=promedio_general, color='blue', linestyle='--', linewidth=2, alpha=0.5,
                label=f'Promedio general ({promedio_general:.2f})')

    ax1.set_xlabel('Promedio de Notas', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Asignatura', fontsize=12, fontweight='bold')
    ax1.set_title('Promedios por Asignatura (Ordenado de menor a mayor)',
                  fontsize=14, fontweight='bold', pad=15)
    ax1.set_xlim(0, 5.5)
    ax1.grid(axis='x', alpha=0.3, linestyle='--')
    ax1.legend(loc='lower right')

    # Gráfico 2: Comparación de las 3 notas por asignatura
    x = np.arange(len(asignaturas))
    width = 0.25

    # Reordenar para el segundo gráfico (alfabético para mejor lectura)
    promedios_df_sorted = promedios_df.sort_index()
    asignaturas_sorted = promedios_df_sorted.index

    bars1 = ax2.bar(x - width, promedios_df_sorted['Promedio_Nota1'], width,
                    label='Nota 1', color='#3498db', alpha=0.8)
    bars2 = ax2.bar(x, promedios_df_sorted['Promedio_Nota2'], width,
                    label='Nota 2', color='#9b59b6', alpha=0.8)
    bars3 = ax2.bar(x + width, promedios_df_sorted['Promedio_Nota3'], width,
                    label='Nota 3', color='#e67e22', alpha=0.8)

    ax2.axhline(y=3.0, color='red', linestyle='--', linewidth=1.5, alpha=0.5)
    ax2.set_xlabel('Asignatura', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Promedio', fontsize=12, fontweight='bold')
    ax2.set_title('Comparación de Promedios por Nota (Nota 1, 2 y 3)',
                  fontsize=14, fontweight='bold', pad=15)
    ax2.set_xticks(x)
    ax2.set_xticklabels(asignaturas_sorted, rotation=45, ha='right')
    ax2.set_ylim(0, 5.5)
    ax2.legend()
    ax2.grid(axis='y', alpha=0.3, linestyle='--')

    plt.tight_layout()

    # Guardar el gráfico
    ruta_salida = os.path.join('..', 'outputs', 'promedios_asignaturas.png')
    plt.savefig(ruta_salida, dpi=300, bbox_inches='tight')
    print(f"\n✅ Gráfico guardado exitosamente en: {ruta_salida}")

    plt.show()

def graficar_promedio_general(stats):
    """Crea un gráfico simple para el promedio general"""
    fig, ax = plt.subplots(figsize=(10, 6))

    # Gráfico de barra simple
    ax.bar(['Promedio General'], [stats['Promedio_General']],
           color='#3498db', alpha=0.8, edgecolor='black', width=0.5)

    # Línea de referencia
    ax.axhline(y=3.0, color='red', linestyle='--', linewidth=2, alpha=0.5,
               label='Nota mínima (3.0)')

    # Valor en la barra
    ax.text(0, stats['Promedio_General'] + 0.1,
            f"{stats['Promedio_General']:.2f}",
            ha='center', fontweight='bold', fontsize=14)

    ax.set_ylabel('Promedio', fontsize=12, fontweight='bold')
    ax.set_title('Promedio General del Curso', fontsize=14, fontweight='bold', pad=15)
    ax.set_ylim(0, 5.5)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.legend()

    # Añadir información adicional
    info_text = f"Desviación Estándar: {stats['Desviacion_Std']:.2f}\n"
    info_text += f"Total de Registros: {stats['Total_Registros']}"
    ax.text(0.02, 0.98, info_text, transform=ax.transAxes,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
            fontsize=10)

    plt.tight_layout()

    # Guardar el gráfico
    ruta_salida = os.path.join('..', 'outputs', 'promedios_asignaturas.png')
    plt.savefig(ruta_salida, dpi=300, bbox_inches='tight')
    print(f"\n✅ Gráfico guardado exitosamente en: {ruta_salida}")

    plt.show()

def main():
    """Función principal del programa"""
    print("\n" + "="*100)
    print("HU05 - PROMEDIO POR ASIGNATURA".center(100))
    print("="*100)

    # Cargar datos
    df = cargar_datos()
    if df is None:
        return

    print(f"\n✅ Datos cargados exitosamente: {len(df)} registros")

    # Verificar si existe la columna 'asignatura'
    if 'asignatura' in df.columns:
        print("✅ Columna 'asignatura' encontrada. Generando análisis por asignatura...")

        # Calcular promedios por asignatura
        promedios_df = calcular_promedios_por_asignatura(df)

        # Mostrar tabla
        mostrar_tabla_asignaturas(promedios_df)

        # Graficar
        graficar_promedios_asignaturas(promedios_df)

    else:
        print("⚠️  Columna 'asignatura' no encontrada. Calculando promedio general...")

        # Calcular promedio general
        stats = calcular_promedio_general(df)

        # Mostrar tabla
        mostrar_tabla_general(stats)

        # Graficar
        graficar_promedio_general(stats)

    print("\n✅ Proceso completado exitosamente")

if __name__ == "__main__":
    main()

