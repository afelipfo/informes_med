"""
Módulos principales del sistema de informes Survey123
Secretaría de Infraestructura Física de Medellín
"""

__version__ = "1.0.0"
__author__ = "Equipo de Desarrollo"
__email__ = "soporte@medellin.gov.co"

# Importaciones principales
from .ingesta import ProcesadorSurvey123
from .modelos import Intervencion, KPI, EstadoObra, RepositorioIntervenciones
from .analisis import AnalisisSurvey123, AnalizadorDatos
from .reportes import GeneradorReportes

# Importar georreferenciación si está disponible
try:
    from .georreferenciacion import GeorreferenciadeSurvey123
    GEORREFERENCIACION_DISPONIBLE = True
except ImportError:
    GeorreferenciadeSurvey123 = None
    GEORREFERENCIACION_DISPONIBLE = False

__all__ = [
    'ProcesadorSurvey123',
    'Intervencion',
    'KPI',
    'EstadoObra',
    'RepositorioIntervenciones',
    'AnalisisSurvey123',
    'AnalizadorDatos',
    'GeneradorReportes',
]

if GEORREFERENCIACION_DISPONIBLE:
    __all__.append('GeorreferenciadeSurvey123')