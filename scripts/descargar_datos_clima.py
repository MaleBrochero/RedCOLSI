import requests
import pandas as pd
from datetime import datetime, timedelta
import os

# 🔑 CONFIGURACIÓN API
API_KEY = "e1f10a1e78da46f5b10a1e78da96f525"
LOCATION = "SKBQ:9:CO" # Barranquilla, Colombia

# Rango de fechas del estudio
fecha_inicio = datetime(2026, 4, 17)
fecha_fin = datetime(2026, 5, 8)

# Ruta de salida ajustada
OUTPUT_FILE = "../data/Estacion metereologica.xlsx"

datos = []
fecha_actual = fecha_inicio

# 🚀 INICIO DE DESCARGA
print(f"🌡️ Iniciando descarga de datos climáticos desde {fecha_inicio.date()} hasta {fecha_fin.date()}...")

while fecha_actual <= fecha_fin:
    fecha_str = fecha_actual.strftime("%Y%m%d")
    print(f"⌛ Consultando Weather.com para: {fecha_str}...")
    
    url = f"https://api.weather.com/v1/location/{LOCATION}/observations/historical.json"
    params = {
        "apiKey": API_KEY,
        "units": "m",
        "startDate": fecha_str,
        "endDate": fecha_str
    }

    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            observations = data.get("observations")
            
            if isinstance(observations, list):
                for obs in observations:
                    # Modelo de estimación de irradiancia basada en nubosidad
                    clds = obs.get("clds", "")
                    factor_nubes = {
                        "CLR": 1.0, "FEW": 0.9, "SCT": 0.7, 
                        "BKN": 0.5, "OVC": 0.3
                    }.get(clds, 0.6)

                    uv = obs.get("uv_index")
                    uv = uv if uv is not None else 0
                    irradiancia = uv * 25 * factor_nubes

                    datos.append({
                        "fecha": fecha_actual.strftime("%Y-%m-%d"),
                        "hora_gmt": obs.get("valid_time_gmt"),
                        "temperatura_C": obs.get("temp"),
                        "humedad_%": obs.get("rh"),
                        "punto_rocio": obs.get("dewPt"),
                        "viento_m_s": obs.get("wspd"),
                        "uv_index": uv,
                        "nubosidad": clds,
                        "condicion": obs.get("wx_phrase"),
                        "irradiancia_estimada_Wm2": irradiancia
                    })
            else:
                print(f"⚠️ No hay observaciones para {fecha_str}")
        else:
            print(f"❌ Error {response.status_code} en {fecha_str}: {response.text}")

    except Exception as e:
        print(f"💥 Error inesperado en {fecha_str}: {e}")

    fecha_actual += timedelta(days=1)

# 📊 PROCESAMIENTO Y GUARDADO
if datos:
    df = pd.DataFrame(datos)
    df["hora"] = pd.to_datetime(df["hora_gmt"], unit="s")
    
    # Ajustar a hora local de Barranquilla (GMT-5)
    df["hora"] = df["hora"] - pd.Timedelta(hours=5)
    
    # Asegurar que la carpeta 'data' existe
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    df.to_excel(OUTPUT_FILE, index=False)
    print("-" * 30)
    print(f"✅ Descarga climática completada.")
    print(f"📁 Archivo guardado en: {OUTPUT_FILE}")
    print(f"📊 Total de registros: {len(df)}")
    print("-" * 30)
else:
    print("\n⚠️ No se recolectó ningún dato. Revisa tu API Key o la conexión.")
