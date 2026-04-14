import pandas as pd
from dbfread import DBF
from pathlib import Path

def decodificar_fila(fila):
    #Limpia y decodifica los bytes a string.
    fila_decodificada = {}
    for k, v in fila.items():
        if isinstance(v, bytes):
            fila_decodificada[k] = v.decode('latin-1', errors='replace').strip()
        else:
            fila_decodificada[k] = v
    return fila_decodificada

# --- CONFIGURACIÓN DE RUTAS ---
carpeta_salida = Path('salida_csvs') 
carpeta_salida.mkdir(parents=True, exist_ok=True)
# ------------------------------

archivos_dbf = list(Path('.').glob('*.[dD][bB][fF]'))

print(f"Iniciando rescate de emergencia de {len(archivos_dbf)} archivos DBF...\n")

csvs_generados = 0

for archivo in archivos_dbf:
    if archivo.name in ['convertir.py', 'limpiar_csvs.py']: continue
    
    print(f"Procesando: {archivo.name}...", end=" ", flush=True)
    
    try:
        tabla = DBF(archivo, encoding='latin-1', raw=True)
        
        registros_activos = [decodificar_fila(f) for f in tabla]
        registros_eliminados = [decodificar_fila(f) for f in tabla.deleted]

        # Guardar Activos
        if registros_activos:
            df_activos = pd.DataFrame(registros_activos)
            ruta_activos = carpeta_salida / archivo.with_suffix('.csv').name
            df_activos.to_csv(ruta_activos, index=False)
            csvs_generados += 1
            print(f"({len(registros_activos)} registros activos)", end=" | ")
        else:
            print("Sin registros activos", end=" | ")

        # Guardar Eliminados
        if registros_eliminados:
            df_eliminados = pd.DataFrame(registros_eliminados)
            nombre_csv_del = f"{archivo.stem}_eliminados.csv"
            ruta_eliminados = carpeta_salida / nombre_csv_del
            df_eliminados.to_csv(ruta_eliminados, index=False)
            csvs_generados += 1
            print(f"({len(registros_eliminados)} registros históricos rescatados)")
        else:
            print("Sin registros históricos.")

    except Exception as e:
        print(f"\nError fatal con {archivo.name}: {e}")

# <-- Print exacto de los CSV creados
print(f"\n¡Listo! Se generaron {csvs_generados} archivos CSV.") 
print(f"Revisa la carpeta: {carpeta_salida.absolute()}")
