import pandas as pd
from dbfread import DBF
from pathlib import Path

def decodificar_fila(fila):
    """Limpia y decodifica los bytes a string."""
    fila_decodificada = {}
    for k, v in fila.items():
        if isinstance(v, bytes):
            fila_decodificada[k] = v.decode('latin-1', errors='replace').strip()
        else:
            fila_decodificada[k] = v
    return fila_decodificada

archivos_dbf = list(Path('.').glob('*.[dD][bB][fF]'))

print(f"Iniciando rescate de emergencia de {len(archivos_dbf)} archivos...\n")

for archivo in archivos_dbf:
    if archivo.name == 'convertir.py': continue
    
    print(f"Procesando: {archivo.name}...", end=" ", flush=True)
    
    try:
        tabla = DBF(archivo, encoding='latin-1', raw=True)
        
        # 1. Rescatar registros activos
        registros_activos = [decodificar_fila(f) for f in tabla]
        
        # 2. Rescatar registros eliminados
        registros_eliminados = [decodificar_fila(f) for f in tabla.deleted]

        # Guardar Activos
        if registros_activos:
            df_activos = pd.DataFrame(registros_activos)
            df_activos.to_csv(archivo.with_suffix('.csv'), index=False)
            print(f"({len(registros_activos)} activos)", end=" | ")
        else:
            print("Sin activos", end=" | ")

        # Guardar Eliminados / Históricos
        if registros_eliminados:
            df_eliminados = pd.DataFrame(registros_eliminados)
            nombre_eliminados = archivo.with_name(f"{archivo.stem}_eliminados.csv")
            df_eliminados.to_csv(nombre_eliminados, index=False)
            print(f"({len(registros_eliminados)} históricos rescatados)")
        else:
            print("Sin históricos.")

    except Exception as e:
        print(f"\nError fatal con {archivo.name}: {e}")

print("\nArchivos CSV generados con éxito.")