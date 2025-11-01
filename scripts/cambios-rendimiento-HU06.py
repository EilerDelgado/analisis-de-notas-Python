
import pandas as pd
import numpy as np
import os

# --- Constantes y Configuración ---
COLUMNAS_NOTAS = ['nota1', 'nota2', 'nota3']
CSV_FILE = '../data/data-generada.csv'
OUTPUT_CSV = 'cambios_bruscos.csv'
UMBRAL_DIFERENCIA = 1.0

def detectar_cambios_bruscos(csv_path, umbral=UMBRAL_DIFERENCIA):
    """
    Detecta estudiantes con cambios bruscos en su rendimiento entre periodos.
    """
    print(f"---  Detección de Cambios Bruscos en Rendimiento (HU06) ---")

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

    # Calcular el promedio de notas por estudiante y periodo
    df['promedio_parcial'] = df[COLUMNAS_NOTAS].mean(axis=1)

    # Pivotar para tener periodos como columnas
    df_pivot = df.pivot_table(
        index=['id_estudiante', 'nombre'],
        columns='periodo',
        values='promedio_parcial'
    ).reset_index()

    # Calcular diferencias entre periodos consecutivos
    for periodo in [2, 3]:
        df_pivot[f'diff_{periodo-1}_{periodo}'] = np.abs(
            df_pivot[periodo] - df_pivot[periodo - 1]
        )

    # Filtrar estudiantes con diferencias mayores al umbral
    condiciones = (
        (df_pivot['diff_1_2'] > umbral) |
        (df_pivot['diff_2_3'] > umbral)
    )
    df_cambios_bruscos = df_pivot[condiciones]

    if not df_cambios_bruscos.empty:
        print(f" Estudiantes con cambios bruscos (> {umbral}): {len(df_cambios_bruscos)}")
        print(df_cambios_bruscos[['id_estudiante', 'nombre', 'diff_1_2', 'diff_2_3']])

        # Guardar resultados en CSV
        df_cambios_bruscos.to_csv(OUTPUT_CSV, index=False)
        print(f" Resultados guardados en '{OUTPUT_CSV}'")
    else:
        print(" No se detectaron cambios bruscos en el rendimiento.")
def main():
    """Función principal"""
    detectar_cambios_bruscos(CSV_FILE)
if __name__ == "__main__":
    main()
