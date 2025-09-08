"""
Módulos principales del sistema de informes Survey123
Secretaría de Infraestructura Física de Medellín
"""

__version__ = "1.0.0"
__author__ = "Equipo de Desarrollo"
__email__ = "soporte@medellin.gov.co"

# Importaciones principales
from .ingesta import ProcesadorSurvey123
from .modelos import Intervencion, KPI, EstadoObra
from .analisis import AnalisisSurvey123
from .reportes import GeneradorReportes
# from .georreferenciacion import GeorreferenciadeSurvey123  # Comentado hasta instalar geopandas

__all__ = [
    'ProcesadorSurvey123',
    'Intervencion',
    'KPI', 
    'EstadoObra',
    'AnalisisSurvey123',
    'GeneradorReportes',
    # 'GeorreferenciadeSurvey123'
]