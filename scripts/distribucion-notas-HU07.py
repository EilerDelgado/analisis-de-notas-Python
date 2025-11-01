
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
CSV_FILE = '../data/data-generada.csv'
OUTPUT_IMAGE = 'histograma_notas.png'

def generar_histograma_notas(csv_path):
    """
    Genera un histograma de las notas finales con líneas de media y mediana.
    """
    print(f"---  Generación de Histograma de Notas Finales (HU07) ---")


    try:
        df = pd.read_csv(csv_path)
        print(f" Archivo '{csv_path}' leído exitosamente.")
    except FileNotFoundError:
        print(f" ERROR: Archivo '{csv_path}' NO ENCONTRADO.")
        return
    except Exception as e:
        print(f" ERROR CRÍTICO: Falló la lectura del archivo CSV. Error: {e}")
        return

    print(f" {len(df)} filas encontradas y listas para analizar.")

    # 1. Crear columna promedio_periodo
    df['promedio_periodo'] = df[['nota1', 'nota2', 'nota3']].mean(axis=1)

    # 2. Calcular media y mediana
    media = np.mean(df['promedio_periodo'])
    mediana = np.median(df['promedio_periodo'])
    print(f" Media de notas finales: {media:.2f}")
    print(f" Mediana de notas finales: {mediana:.2f}")

    # 3. Graficar histograma
    plt.figure(figsize=(10, 6))
    plt.hist(df['promedio_periodo'], bins=20, color='skyblue', edgecolor='black', alpha=0.7)
    plt.axvline(media, color='red', linestyle='dashed', linewidth=1, label=f'Media: {media:.2f}')
    plt.axvline(mediana, color='green', linestyle='dashed', linewidth=1, label=f'Mediana: {mediana:.2f}')
    plt.title('Histograma de Notas Finales por Periodo')
    plt.xlabel('Nota Final')
    plt.ylabel('Número de Estudiantes')
    plt.legend()
    plt.grid(axis='y', alpha=0.75)

    # Guardar imagen
    plt.savefig(OUTPUT_IMAGE)
    print(f" Histograma guardado en '{OUTPUT_IMAGE}'")
    plt.close()
    plt.show()
def main():
    """Función principal del programa"""
    print("\n" + "="*80)
    print("HU07 - HISTOGRAMA DE NOTAS FINALES DEL PERIODO".center(80))
    print("="*80)

    generar_histograma_notas(CSV_FILE)
if __name__ == "__main__":
    main()
