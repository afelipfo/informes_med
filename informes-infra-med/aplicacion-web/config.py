# Configuración de la aplicación Flask
import os
from datetime import timedelta

class Config:
    """Configuración base de la aplicación"""
    
    # Configuración básica de Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Configuración de archivos
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'datos', 'uploads')
    PROCESSED_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'datos', 'procesados')
    REPORTS_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'datos', 'reportes_generados')
    MAPS_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'datos', 'mapas')
    
    # Tamaño máximo de archivo (16MB)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    
    # Extensiones permitidas
    ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
    
    # Configuración de base de datos
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///survey123_app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración de sesiones
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    
    # Configuración de logs
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs', 'app.log')
    
    # Configuración de georreferenciación
    DEFAULT_MAP_CENTER = [6.2442, -75.5812]  # Medellín, Colombia
    DEFAULT_ZOOM = 11
    
    # Configuración de reportes
    REPORT_FORMATS = ['pdf', 'docx', 'xlsx']
    
    # Columnas esenciales del Survey123
    REQUIRED_COLUMNS = [
        'Shape', 'X', 'Y', 'start', 'id_punto', 'estado_obr', 
        'fecha_dilig', 'nombre_int', 'num_cuadri', 'trabajador'
    ]
    
    # Columnas de recursos humanos
    RRHH_COLUMNS = [
        'num_cuadri', 'trabajador', 'cant_ayuda', 'cant_ofici', 
        'cant_opera', 'cant_auxil', 'cant_otros', 'num_total_', 'total_hora'
    ]
    
    # Columnas de maquinaria
    MAQUINARIA_COLUMNS = [
        'maquinaria', 'horas_retr', 'horas_mini', 'horas_volq', 
        'horas_comp', 'nombre_otr', 'horas_otra'
    ]
    
    # Columnas de actividades preliminares
    PRELIMINARES_COLUMNS = [
        'localizaci', 'descapote', 'a_mano', 'a_maquina', 'Tala_poda',
        'roceria_li', 'cerramient', 'tela_verde', 'malla_nara',
        'teja_ondul', 'cubierta_p', 'pasarela_p'
    ]

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///survey123_dev.db'

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///survey123_prod.db'

class TestingConfig(Config):
    """Configuración para pruebas"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///survey123_test.db'
    WTF_CSRF_ENABLED = False

# Diccionario de configuraciones
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
