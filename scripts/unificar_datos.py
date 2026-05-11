import pandas as pd
import os

# 1. CONFIGURACIÓN DE RUTAS
# Ajustado para que funcione desde la carpeta 'scripts' apuntando a 'data'
DATA_DIR = "../data/"
FILE_CLIMA = os.path.join(DATA_DIR, "Estacion metereologica.xlsx")
FILE_INV = os.path.join(DATA_DIR, "Inversor.xlsx")
FILE_OUTPUT = os.path.join(DATA_DIR, "ANALISIS_SOLAR_UNIFICADO.xlsx")

# 2. CARGA DE DATOS
try:
    print(f"⌛ Cargando archivos desde {DATA_DIR}...")
    df_clima = pd.read_excel(FILE_CLIMA)
    df_inv = pd.read_excel(FILE_INV)
    print("✅ Archivos cargados correctamente.")
except Exception as e:
    print(f"❌ Error al cargar los archivos: {e}")
    print("Asegúrate de que los archivos 'Estacion metereologica.xlsx' e 'Inversor.xlsx' estén en la carpeta 'data/'.")
    exit()

# 3. LIMPIEZA DE COLUMNAS
df_clima.columns = df_clima.columns.str.strip()
df_inv.columns = df_inv.columns.str.strip()

# 4. NORMALIZACIÓN DE TIEMPO
print("⌛ Procesando timestamps...")
df_clima['timestamp'] = pd.to_datetime(df_clima['hora'], errors='coerce')
df_inv['timestamp'] = pd.to_datetime(df_inv['fecha'].astype(str) + ' ' + df_inv['hora'].astype(str), errors='coerce')

df_clima = df_clima.dropna(subset=['timestamp']).set_index('timestamp').sort_index()
df_inv = df_inv.dropna(subset=['timestamp']).set_index('timestamp').sort_index()

# Redondear para asegurar el match
df_clima.index = df_clima.index.floor('min')
df_inv.index = df_inv.index.floor('min')

# 5. FORZAR CONVERSIÓN NUMÉRICA
cols_numericas = ['temperatura_C', 'humedad_%', 'punto_rocio', 'viento_m_s', 'uv_index', 'irradiancia_estimada_Wm2']
for col in cols_numericas:
    if col in df_clima.columns:
        df_clima[col] = pd.to_numeric(df_clima[col], errors='coerce')

# 6. ALINEACIÓN (RESAMPLING)
print("⌛ Interpolando datos meteorológicos a 15 min...")
df_num = df_clima[df_clima.columns.intersection(cols_numericas)]
clima_num_15m = df_num.resample('15min').interpolate(method='linear')

cols_texto = ['nubosidad', 'condicion']
df_txt = df_clima[df_clima.columns.intersection(cols_texto)]
clima_txt_15m = df_txt.resample('15min').ffill()

clima_final = pd.concat([clima_num_15m, clima_txt_15m], axis=1)

# 7. UNIÓN FINAL (how='left' para no perder filas del inversor)
print("⌛ Unificando dataframes...")
df_final = pd.merge(df_inv, clima_final, left_index=True, right_index=True, how='left')

# 8. GUARDAR
df_final.to_excel(FILE_OUTPUT)

print("-" * 30)
print(f"✅ ¡ÉXITO! Base de datos unificada guardada en: {FILE_OUTPUT}")
print(f"📊 Registros totales: {len(df_final)}")
print("-" * 30)
