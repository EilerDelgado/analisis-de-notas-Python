# Sistema de Seguimiento de Notas Académicas

Sistema automatizado de análisis de calificaciones estudiantiles desarrollado en Python. Procesa archivos CSV con notas, calcula estadísticas, identifica estudiantes en riesgo y genera gráficos y reportes.

## Características

- ✅ Cálculo de promedios por periodo y anual
- ✅ Evolución individual de estudiantes
- ✅ Identificación de estudiantes en riesgo
- ✅ Detección del mejor estudiante
- ✅ Análisis por asignatura
- ✅ Detección de cambios bruscos
- ✅ Distribución general de notas
- ✅ Reporte general completo

## Requisitos

- Python 3.8 o superior
- Pandas
- NumPy
- Matplotlib

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/EilerDelgado/analisis-de-notas-Python.git
cd analisis-de-notas-Python

# Instalar dependencias
pip install pandas numpy matplotlib
```

## Estructura del Proyecto

```
proyecto_notas/
├── data/
│   └── data-generada.csv          # Archivo con las notas
├── scripts/
│   ├── hu01_promedio_curso.py     # Promedio del curso
│   ├── hu02_evolucion_estudiante.py
│   ├── hu03_estudiantes_riesgo.py
│   ├── hu04_mejor_estudiante.py
│   ├── hu05_promedio_asignatura.py
│   ├── hu06_cambios_bruscos.py
│   ├── hu07_distribucion_notas.py
│   └── hu08_reporte_general.py
├── outputs/
│   ├── graficos/                   # Gráficos generados (PNG)
│   └── reportes/                   # Reportes generados (CSV)
└── README.md
```

## Formato del Archivo CSV

El archivo debe tener las siguientes columnas:

```csv
id_estudiante,nombre,asignatura,periodo,nota1,nota2,nota3,asistencia_%,participacion
1,Juan Pérez,Matemáticas,1,3.5,4.0,3.8,85.0,0.75
```

## Uso

### Generar Datos de Prueba

```bash
python generador_datos.py --estudiantes 40 --output data/data-generada.csv
```

### Ejecutar Análisis

```bash
# Ver promedio del curso
python scripts/hu01_promedio_curso.py

# Ver evolución de un estudiante
python scripts/hu02_evolucion_estudiante.py

# Identificar estudiantes en riesgo
python scripts/hu03_estudiantes_riesgo.py

# Ver mejor estudiante
python scripts/hu04_mejor_estudiante.py

# Análisis por asignatura
python scripts/hu05_promedio_asignatura.py

# Detectar cambios bruscos
python scripts/hu06_cambios_bruscos.py

# Ver distribución de notas
python scripts/hu07_distribucion_notas.py

# Generar reporte general
python scripts/hu08_reporte_general.py
```

## Salidas

### Gráficos (outputs/graficos/)
- `promedios_periodos.png` - Gráfico de barras con promedios por periodo
- `evolucion_estudiante.png` - Línea de evolución individual
- `promedios_asignaturas.png` - Barras con promedio por materia
- `histograma_notas.png` - Distribución general de notas

### Reportes (outputs/reportes/)
- `estudiantes_en_riesgo.csv` - Lista de estudiantes con promedio < 3.0
- `cambios_bruscos.csv` - Estudiantes con cambios mayores a 1.0
- `reporte_general.csv` - Reporte completo del curso

## Ejemplos de Uso

### Ejemplo 1: Análisis rápido del curso

```bash
python scripts/hu01_promedio_curso.py
```

**Salida esperada:**
```
Promedio Periodo 1: 3.25
Promedio Periodo 2: 3.18
Promedio Periodo 3: 3.30
Promedio Anual: 3.24
```

### Ejemplo 2: Identificar estudiantes en riesgo

```bash
python scripts/hu03_estudiantes_riesgo.py
```

**Salida esperada:**
```
Estudiantes en riesgo (< 3.0):
- Ana García (ID: 7) - Promedio: 2.15 - Necesita: 4.65 en periodo 4
- Nicolás Rodríguez (ID: 19) - Promedio: 2.50 - Necesita: 4.00 en periodo 4
```

## Tecnologías Utilizadas

- **Python 3.8+** - Lenguaje principal
- **Pandas** - Manipulación de datos
- **NumPy** - Cálculos numéricos
- **Matplotlib** - Visualización de datos

## Equipo de Desarrollo

- Delgado Eiler
- Forbes Johny
- Peña Dandy
- Valdes Sebastián

**Institución:** CESDE - Técnico en Desarrollo de Software

**Curso:** Nuevas Tecnologías (Python)

## Licencia

Este proyecto fue desarrollado con fines educativos.

## Contacto

Para preguntas o sugerencias, crear un issue en el repositorio de GitHub.