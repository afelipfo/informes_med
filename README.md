# Sistema de Análisis Survey123

## Secretaría de Infraestructura Física de Medellín

### 🏛️ Descripción del Proyecto

Sistema web desarrollado en Python/Flask para el procesamiento automatizado de datos Survey123 de obras de infraestructura física en Medellín. Proporciona análisis estadístico, visualización geográfica, generación de reportes y capacidades de inteligencia artificial para optimizar la gestión de proyectos de infraestructura municipal.

### Características Principales

- **Ingesta Automática**: Procesamiento de archivos Excel de Survey123
- **Validación de Datos**: Verificación de integridad y consistencia
- **Cálculos Automáticos**: KPIs y totales calculados automáticamente
- **Georreferenciación**: Mapas interactivos de intervenciones
- **Informes Automáticos**: Generación en PDF, Word y Excel
- **Inteligencia Artificial**: Análisis de textos y predicciones
- **Interfaz Web**: Panel intuitivo en español

### Estructura del Proyecto

```
aplicacion-web/
│
├── app.py                      # Aplicación principal Flask
├── config.py                   # Configuraciones
├── requirements.txt            # Dependencias
├── README.md                   # Documentación
│
├── modulos/                    # Módulos principales
│   ├── __init__.py
│   ├── ingesta.py             # Carga y validación de datos
│   ├── modelos.py             # Modelos de datos
│   ├── analisis.py            # Procesamiento y análisis
│   ├── reportes.py            # Generación de informes
│   ├── georreferenciacion.py  # Mapas y coordenadas
│   └── inteligencia_artificial.py # Módulos de IA
│
├── templates/                  # Plantillas HTML
│   ├── base.html
│   ├── index.html
│   ├── cargar_datos.html
│   ├── ver_analisis.html
│   ├── generar_informe.html
│   └── mapa_intervenciones.html
│
├── static/                     # Archivos estáticos
│   ├── css/
│   ├── js/
│   └── img/
│
├── plantillas_informes/        # Plantillas de informes
│   ├── informe_base.html
│   ├── informe_template.docx
│   └── estilos_pdf.css
│
├── datos/                      # Datos procesados
│   ├── procesados/
│   ├── reportes_generados/
│   └── mapas/
│
├── tests/                      # Pruebas unitarias
│   ├── test_ingesta.py
│   ├── test_modelos.py
│   ├── test_analisis.py
│   └── test_reportes.py
│
└── docs/                       # Documentación
    ├── instalacion.md
    ├── uso.md
    └── api.md
```

### Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone <url-repositorio>
   cd aplicacion-web
   ```

2. **Crear entorno virtual**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar la aplicación**:
   ```bash
   cp config.py.example config.py
   # Editar config.py con tus configuraciones
   ```

5. **Ejecutar la aplicación**:
   ```bash
   python app.py
   ```

### Uso

1. **Acceder a la aplicación**: http://localhost:5000
2. **Cargar archivo Survey123**: Seleccionar archivo Excel en formato Survey123
3. **Revisar análisis**: Ver dashboard con KPIs y estadísticas
4. **Generar informes**: Descargar en PDF, Word o Excel
5. **Visualizar mapas**: Ver distribución geográfica de intervenciones

### Tecnologías Utilizadas

- **Backend**: Python 3.8+, Flask
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **Análisis de Datos**: Pandas, NumPy, SciPy
- **Visualización**: Matplotlib, Plotly, Folium
- **Georreferenciación**: Folium, GeoPandas
- **Generación de Informes**: ReportLab (PDF), python-docx (Word), openpyxl (Excel)
- **Inteligencia Artificial**: scikit-learn, NLTK, spaCy
- **Base de Datos**: SQLite (desarrollo), PostgreSQL (producción)

### Contribución

1. Fork el proyecto
2. Crear rama para feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

### Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

### Contacto

- **Desarrollador**: Equipo de Desarrollo
- **Organización**: Secretaría de Infraestructura Física de Medellín
- **Email**: soporte@medellin.gov.co

### Changelog

#### v1.0.0 (2025-01-XX)
- Versión inicial
- Ingesta de datos Survey123
- Generación básica de informes
- Mapas interactivos
- Dashboard de análisis

#### Funcionalidades Planificadas

- [ ] Integración con API de Survey123
- [ ] Notificaciones automáticas
- [ ] Exportación a sistemas externos
- [ ] App móvil para visualización
- [ ] Dashboard ejecutivo avanzado
- [ ] Análisis predictivo con ML
