# Sistema de Informes Survey123

## Descripción del proyecto

Sistema web desarrollado en Python Flask para el procesamiento automatizado de datos Survey123 de obras de infraestructura física urbana. Implementa algoritmos de procesamiento de lenguaje natural (NLP) e inteligencia artificial para generar informes dinámicos e insights contextuales a partir de datos de campo.

## Arquitectura del sistema

### Stack tecnológico

**Backend:**

- Python 3.8+ con Flask 3.0.0
- Pandas 2.2.0 para análisis de datos
- ReportLab 4.0.9 para generación de PDF
- Scikit-learn 1.4.0, NLTK 3.8.1, spaCy 3.7.2 para NLP
- Folium 0.15.1 para visualización geográfica

**Frontend:**

- Bootstrap 5.x para diseño responsivo
- JavaScript vanilla para interacciones
- Folium para mapas interactivos
- Chart.js para visualizaciones estadísticas

**Procesamiento de datos:**

- OpenPyXL 3.1.2 para archivos Excel
- NumPy 1.26.3 para cálculos numéricos
- GeoPandas 0.14.3 para datos geoespaciales

## Funcionalidades principales

### 1. Ingesta y validación de datos

- Procesamiento automático de archivos Excel Survey123 (78 variables)
- Validación de estructura e integridad de datos
- Limpieza automática y normalización de valores
- Cálculo automático de totales y métricas derivadas

### 2. Motor de IA

- **AnalizadorInteligenteSurvey123**: Análisis semántico de las 78 variables
- Detección automática de patrones y correlaciones estadísticas
- Generación dinámica de insights contextuales
- Análisis de sentimientos y procesamiento de texto libre
- Recomendaciones inteligentes basadas en datos

### 3. Generación de informes

**Informes tradicionales:**

- Informe Estadístico: Análisis descriptivo básico
- Informe Detallado: Análisis completo con datos desagregados
- Resumen Ejecutivo: Síntesis para toma de decisiones

**Informes inteligentes (IA):**

- Análisis dinámico de patrones temporales
- Correlaciones automáticas entre variables
- Insights contextuales generados por NLP
- Recomendaciones estratégicas personalizadas
- Narrativa adaptativa según los datos

### 4. Visualización geoespacial

- Mapas interactivos de intervenciones por comuna
- Clustering automático de actividades por densidad
- Filtros dinámicos por estado, fecha y tipo de obra
- Exportación de mapas en formato imagen

### 5. Dashboard de análisis

- Métricas en tiempo real de recursos humanos
- Análisis de productividad por equipos de trabajo
- Distribución de maquinaria y equipos
- Cobertura territorial y concentración geográfica

## Estructura del proyecto

```tree
informes_med/
├── app.py                          # Aplicación principal Flask
├── config.py                       # Configuraciones del sistema
├── requirements.txt                # Dependencias Python
├── install.ps1                     # Script instalación Windows
├── install.sh                      # Script instalación Linux/Mac
│
├── modulos/                        # Módulos principales
│   ├── __init__.py                 # Inicialización del paquete
│   ├── ingesta.py                  # Procesamiento archivos Survey123
│   ├── modelos.py                  # Modelos de datos y estructuras
│   ├── analisis.py                 # Análisis estadístico básico
│   ├── reportes.py                 # Generadores de reportes tradicionales
│   ├── georreferenciacion.py       # Procesamiento geoespacial
│   ├── inteligencia_nlp.py         # Motor de IA y análisis NLP
│   ├── generador_inteligente.py    # Generador informes con IA
│   ├── generadores_pdf.py          # Generadores PDF tradicionales
│   └── generador_informes.py       # Utilidades generación informes
│
├── templates/                      # Plantillas HTML Jinja2
│   ├── base.html                   # Template base con Bootstrap
│   ├── index.html                  # Página principal
│   ├── cargar_datos.html           # Interfaz carga de archivos
│   ├── ver_analisis.html           # Dashboard de análisis
│   ├── generar_informe.html        # Interfaz generación informes
│   └── mapa_intervenciones.html    # Visualizador de mapas
│
├── static/                         # Recursos estáticos
│   ├── images/                     # Imágenes del sistema
│   │   ├── logo_alcaldia.jpg       # Logo institucional
│   │   └── .gitkeep                # Preservar directorio
│   └── maps/                       # Mapas generados
│       └── .gitkeep                # Preservar directorio
│
├── datos/                          # Almacenamiento de datos
│   ├── uploads/                    # Archivos cargados
│   ├── procesados/                 # Datos procesados
│   ├── reportes_generados/         # Informes generados
│   └── .gitkeep                    # Preservar estructura
│
└── docs/                           # Documentación técnica
    ├── instalacion.md              # Guía de instalación
    └── documentacion_tecnica.md    # Documentación detallada
```

## Instalación


**Windows (PowerShell):**

```powershell
.\install.ps1
```

**Linux/macOS (Bash):**

```bash
chmod +x install.sh
./install.sh
```

### Instalación Manual

1. **Verificar Python 3.8+**

```bash
python --version
```

2. **Clonar repositorio**

```bash
git clone https://github.com/afelipfo/informes_med.git
cd informes_med
```

3. **Crear entorno virtual**

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

4. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

5. **Ejecutar aplicación**

```bash
python app.py
```

## Configuración

### Configuración de datos

El sistema espera archivos Excel con 78 columnas específicas de Survey123:

**Columnas esenciales:**

- `Shape`, `X`, `Y`: Datos geoespaciales
- `start`, `id_punto`: Identificadores
- `estado_obr`: Estado de la obra
- `fecha_dilig`: Fecha de diligenciamiento
- `nombre_int`: Nombre de la intervención

**Columnas de recursos humanos:**

- `num_obreros`, `num_ayudan`, `num_operad`, `num_conduc`: Personal
- `nom_obrero*`, `nom_ayudan*`: Nombres del personal
- `total_hora`: Horas trabajadas

**Columnas de maquinaria:**

- `tipo_maq_*`: Tipos de maquinaria
- `placa_maq*`: Placas de equipos
- `horas_maq*`: Horas de uso

## Uso del sistema

### 1. Cargar datos

1. Acceder a `http://localhost:5000`
2. Ir a "Cargar Datos"
3. Seleccionar archivo Excel Survey123
4. El sistema valida y procesa automáticamente

### 2. Ver análisis

- Dashboard con métricas de recursos humanos
- Análisis de maquinaria y equipos
- Distribución de actividades por tipo
- Cobertura territorial por comunas

### 3. Generar informes

**Informes tradicionales:**

- Análisis estadístico básico
- Tablas y gráficos descriptivos
- Formato PDF profesional

**Informes inteligentes (IA):**

- Insights dinámicos generados por NLP
- Detección automática de patrones
- Correlaciones estadísticas significativas
- Recomendaciones estratégicas contextuales

### 4. Visualizar mapas

- Mapas interactivos por comuna
- Filtros por estado y fecha
- Clustering de intervenciones
- Exportación de mapas

## API REST

### Endpoints principales

```http
GET  /                              # Página principal
GET  /cargar_datos                  # Interfaz carga de datos
POST /procesar_archivo              # Procesar archivo Survey123
GET  /ver_analisis                  # Dashboard de análisis
GET  /generar_informe               # Interfaz generación informes
GET  /mapa_intervenciones           # Visualizador de mapas

# Generación de Informes Tradicionales
GET  /api/generar_informe_tradicional_estadistico
GET  /api/generar_informe_tradicional_detallado  
GET  /api/generar_informe_tradicional_ejecutivo

# Generación de Informes Inteligentes (IA)
GET  /api/generar_informe_estadistico
GET  /api/generar_informe_detallado/pdf
GET  /api/generar_informe_ejecutivo

# APIs de Datos
GET  /api/obtener_comunas           # Lista de comunas
GET  /api/obtener_estados           # Estados de obra
GET  /api/datos_mapa                # Datos para mapas
```

## Algoritmos de Inteligencia Artificial

### Motor de análisis NLP

1. **Análisis Semántico**: Mapeo de 78 variables en categorías semánticas
2. **Detección de Patrones**: Correlaciones estadísticas automáticas
3. **Generación de Insights**: Narrativa dinámica basada en datos
4. **Análisis Temporal**: Identificación de tendencias y concentraciones
5. **Recomendaciones**: Sugerencias basadas en correlaciones encontradas

### Categorías semánticas

```python
campos_semanticos = {
    'temporal': ['fecha_inic', 'fecha_fin_', 'hora_inici', 'hora_final'],
    'recursos_humanos': ['nom_obrero*', 'num_obreros', 'num_ayudan', ...],
    'maquinaria': ['tipo_maq_*', 'placa_maq*', 'horas_maq*', ...],
    'actividades': ['actividad_', 'tipo_activ', 'descripcio', ...],
    'ubicacion': ['barrio', 'comuna', 'direccion', 'X', 'Y', ...],
    'estado': ['estado_obr', 'porcentaje'],
    'observaciones': ['observacio', 'comentario', 'notas']
}
```

## Especificaciones técnicas

### Límites del sistema

- Tamaño máximo de archivo: 16 MB
- Formatos soportados: .xlsx, .xls
- Registros recomendados: Hasta 10,000 por archivo
- Variables procesadas: 78 columnas Survey123

### Rendimiento

- Procesamiento de 67 registros: < 2 segundos
- Generación de informes PDF: 3-8 segundos
- Análisis con IA: 5-15 segundos dependiendo del dataset

### Compatibilidad

- Python 3.8+
- Navegadores: Chrome 90+, Firefox 88+, Edge 90+
- Sistemas: Windows 10+, Linux, macOS 10.14+

## Desarrollo y contribución

### Estructura de módulos

**modulos/ingesta.py**: Procesador principal de archivos Survey123
**modulos/inteligencia_nlp.py**: Motor de IA y análisis NLP  
**modulos/generador_inteligente.py**: Generador de informes con IA
**modulos/georreferenciacion.py**: Procesamiento geoespacial

### Estándares de código

- PEP 8 para estilo Python
- Docstrings detallados en funciones principales
- Type hints en funciones públicas
- Manejo de errores con logging
