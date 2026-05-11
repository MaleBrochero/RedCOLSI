# Validación Estadística de la Confiabilidad del Monitoreo Energético en un Sistema Fotovoltaico Urbano mediante Modelos Matemáticos y Datos Meteorológicos IoT: Caso de Estudio en una Institución Educativa de Malambo, Atlántico

## 📌 Resumen del Proyecto
Este repositorio documenta el desarrollo técnico y estadístico de la Capa C (Gateway) de un sistema de monitoreo energético integral. La investigación utiliza la analítica de datos para validar una arquitectura IoT donde se sincronizan variables ambientales y operativas para garantizar la precisión del monitoreo en entornos urbanos.

## 🔬 El Experimento de Validación
Para ratificar la necesidad de una infraestructura de monitoreo propia en la Institución Educativa, se realizó un contraste estadístico utilizando datos de una estación de referencia externa (Aeropuerto, a 5 km de distancia).

*   **Hallazgos Críticos:**
    *   **Prueba de Hipótesis:** Se aplicaron los tests de Shapiro-Wilk y Anderson-Darling (A^2 = 22.17) sobre los residuos del modelo de regresión multivariada.
    *   **Justificación de la Estación In Situ:** El rechazo de la normalidad en los errores del modelo basado en datos externos demuestra que los microcambios climáticos locales afectan drásticamente la confiabilidad del sistema.
    *   **Conclusión:** Se valida la necesidad de capturar datos en el punto exacto de generación, integrando la información climática con los parámetros operativos del sistema fotovoltaico.

## 📡 Arquitectura IoT y Flujo de Datos
El sistema emplea tecnología IoT para centralizar información proveniente de dos fuentes críticas en el terreno que se unifican mediante el procesamiento de datos:

1.  **Variables Climatológicas (`data/Estacion metereologica.xlsx`)**: Captura de irradiancia, temperatura ambiente y humedad mediante sensores locales.
2.  **Variables del Inversor (`data/Inversor.xlsx`)**: Monitoreo directo de la potencia generada ($pv\_power$) y estados del equipo para cuantificar la eficiencia real.

### El Proceso de Unificación (Paso a Paso)
Para garantizar que el Gateway (Raspberry Pi 4B) procese información sincronizada, se utilizan los scripts de este repositorio para alinear ambas fuentes por sus marcas de tiempo (*timestamps*), eliminando el sesgo de estaciones remotas y generando el archivo maestro: **`data/ANALISIS_SOLAR_UNIFICADO.xlsx`**.

## 🛠️ Componentes del Repositorio
*   **`notebooks/`**: Análisis exploratorio y pruebas de bondad de ajuste que sustentan el rechazo de modelos lineales simples debido a la variabilidad local.
*   **`scripts/`**: Algoritmos en Python para la descarga, limpieza y unificación de las tramas de datos del inversor y la estación.
*   **`data/`**: Base de datos unificada que vincula el recurso solar con la respuesta eléctrica del sistema, junto con sus fuentes originales.

## 🚀 Futuras Fases
Tras validar la necesidad de la infraestructura local, la siguiente etapa consiste en:
1.  Implementar comunicación LoRa para la transmisión inalámbrica de largo alcance de los datos del inversor y la estación meteorológica.
2.  Desplegar modelos de detección de anomalías para la supervisión inteligente de la planta.

---

## 🎓 Autoría y Créditos
**Investigadora:** Maria Jose Leal Brochero  
*Especialización en Ciencia de Datos - Institución Universitaria de Barranquilla*  
Presentado ante la **Red Colombiana de Semilleros de Investigación (RedCOLSI)**.