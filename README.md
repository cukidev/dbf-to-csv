# DBF to CSV Converter & Rescue Tool 🚑

Un script automatizado en Python diseñado para procesar archivos de bases de datos antiguas (`.dbf`) y convertirlos a formato `.csv`. 

Su principal característica es la capacidad de extraer no solo la información activa, sino también los registros marcados como eliminados lógicamente (*soft-deleted*) dentro de la estructura física del DBF, permitiendo recuperar información histórica u oculta.

## 🚀 Características Principales (Features)
- **Extracción Dual:** Genera archivos CSV independientes para registros activos y registros históricos/eliminados.
- **Bypass de Corrupción de Datos:** Utiliza lectura cruda (`raw=True`) para evitar excepciones fatales causadas por fechas inválidas o formatos corruptos, muy comunes en DBFs antiguos.
- **Manejo Seguro de Encoding:** Decodifica estructuras de bytes a `latin-1` con reemplazo inteligente de caracteres fallidos, asegurando la legibilidad de caracteres especiales.
- **Procesamiento por Lotes:** Escanea e itera automáticamente sobre todos los archivos `.dbf` (o `.DBF`) detectados en el directorio de ejecución.

## ⚙️ Prerrequisitos
Asegúrate de tener instaladas las siguientes librerías:
```bash
pip install pandas dbfread
```

## 🛠️ Uso
1. Coloca los archivos `.dbf` en la misma raíz que el script.
2. Ejecuta el script desde la terminal:
   ```bash
   python convertidor_dbf.py
   ```
3. Por cada base de datos procesada, se generarán automáticamente:
   - `nombre_archivo.csv` (Contiene los registros activos)
   - `nombre_archivo_eliminados.csv` (Contiene los registros rescatados)

