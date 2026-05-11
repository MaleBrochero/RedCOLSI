import requests
import pandas as pd
from datetime import datetime, timedelta
import os

# 1. CONFIGURACIÓN
url = "https://neapi.hoymiles.com/pvm-report/api/0/station/report/select_power_by_station"

headers = {
    "authorization": "3.9tb63eWojN4eNYKO4jsLdnJL5vlmBQ0S9OyumPbhNxYRmr6zKkGEU7SV44YhmCyiNLQK7PbsojTT7BKPXevICsVD2eGSjXOAyrxCvsV3uLFk2VJdk.0",
    "content-type": "application/json",
    "origin": "https://global.hoymiles.com",
    "referer": "https://global.hoymiles.com/"
}

# Rango de fechas del estudio
fecha_inicio = datetime(2026, 4, 17)
fecha_fin = datetime(2026, 5, 8)

# Ruta de salida ajustada a la carpeta 'data'
OUTPUT_FILE = "../data/Inversor.xlsx"

todos_los_datos = []
fecha_actual = fecha_inicio

# 2. PROCESO DE DESCARGA
print(f"🚀 Iniciando descarga de datos desde {fecha_inicio.date()} hasta {fecha_fin.date()}...")

while fecha_actual <= fecha_fin:
    fecha_str = fecha_actual.strftime("%Y-%m-%d")
    print("⌛ Consultando API para el día:", fecha_str)

    payload = {
        "sid_list": [13173880],
        "sid": 13173880,
        "start_date": fecha_str,
        "end_date": fecha_str,
        "page": 1,
        "page_size": 100
    }

    try:
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            data = response.json()
            # Se asume que la respuesta tiene la estructura data[0]['data_list']
            lista = data["data"][0]["data_list"]

            for item in lista:
                fila = {
                    "fecha": fecha_str,
                    "hora": item["date"],
                    "pv_power": item["pv_power"],
                    "consumption_power": item["consumption_power"],
                    "grid_power": item["grid_p_power"]
                }
                todos_los_datos.append(fila)
        else:
            print(f"⚠️ Error HTTP {response.status_code} en fecha: {fecha_str}")
    except Exception as e:
        print(f"❌ Error de conexión en fecha {fecha_str}: {e}")

    fecha_actual += timedelta(days=1)

# 3. GUARDADO DE DATOS
if todos_los_datos:
    df = pd.DataFrame(todos_los_datos)
    
    # Asegurar que la carpeta 'data' existe (un nivel arriba del script)
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    df.to_excel(OUTPUT_FILE, index=False)
    print("-" * 30)
    print(f"✅ Descarga completada con éxito.")
    print(f"📁 Archivo guardado en: {OUTPUT_FILE}")
    print(f"📊 Total de registros descargados: {len(df)}")
    print("-" * 30)
else:
    print("❌ No se pudieron descargar datos. Revisa el token de autorización en el script.")
