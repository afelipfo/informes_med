"""
Módulo de ingesta y validación de datos Survey123
Secretaría de Infraestructura Física de Medellín
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging
from datetime import datetime
import os

class ProcesadorSurvey123:
    """
    Clase principal para procesar archivos de Survey123
    
    Funcionalidades:
    - Carga y validación de archivos Excel
    - Limpieza y conversión de tipos de datos
    - Validación de columnas esenciales
    - Cálculos automáticos de totales
    """
    
    def __init__(self, config=None):
        """Inicializar el procesador con configuración"""
        self.config = config
        self.logger = self._configurar_logger()
        self.df_original = None
        self.df_procesado = None
        self.errores_validacion = []
        
    def _configurar_logger(self):
        """Configurar logger para el módulo"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
    
    def cargar_archivo(self, ruta_archivo: str) -> bool:
        """
        Cargar archivo Excel de Survey123
        
        Args:
            ruta_archivo: Ruta al archivo Excel
            
        Returns:
            bool: True si la carga fue exitosa
        """
        try:
            self.logger.info(f"Cargando archivo: {ruta_archivo}")
            
            # Verificar que el archivo existe
            if not os.path.exists(ruta_archivo):
                raise FileNotFoundError(f"Archivo no encontrado: {ruta_archivo}")
            
            # Cargar archivo Excel
            self.df_original = pd.read_excel(ruta_archivo)
            
            self.logger.info(f"Archivo cargado exitosamente: {self.df_original.shape[0]} filas, {self.df_original.shape[1]} columnas")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error cargando archivo: {str(e)}")
            return False
    
    def validar_estructura(self) -> bool:
        """
        Validar que el archivo tenga la estructura esperada de Survey123
        
        Returns:
            bool: True si la estructura es válida
        """
        if self.df_original is None:
            self.errores_validacion.append("No hay archivo cargado")
            return False
        
        # Validar columnas esenciales
        columnas_requeridas = getattr(self.config, 'REQUIRED_COLUMNS', [
            'Shape', 'X', 'Y', 'start', 'id_punto', 'estado_obr', 
            'fecha_dilig', 'nombre_int', 'num_cuadri', 'trabajador'
        ])
        
        columnas_faltantes = []
        for col in columnas_requeridas:
            if col not in self.df_original.columns:
                columnas_faltantes.append(col)
        
        if columnas_faltantes:
            self.errores_validacion.append(f"Columnas faltantes: {columnas_faltantes}")
            return False
        
        # Validar que hay datos
        if self.df_original.empty:
            self.errores_validacion.append("El archivo está vacío")
            return False
        
        # Validar coordenadas
        if not self._validar_coordenadas():
            return False
        
        self.logger.info("Estructura del archivo validada correctamente")
        return True
    
    def _validar_coordenadas(self) -> bool:
        """Validar que las coordenadas X, Y sean válidas"""
        try:
            # Verificar que X, Y sean numéricos
            if not pd.api.types.is_numeric_dtype(self.df_original['X']):
                self.errores_validacion.append("Columna X no es numérica")
                return False
                
            if not pd.api.types.is_numeric_dtype(self.df_original['Y']):
                self.errores_validacion.append("Columna Y no es numérica")
                return False
            
            # Verificar rangos aproximados para Medellín
            x_min, x_max = -75.7, -75.4
            y_min, y_max = 6.1, 6.4
            
            x_validas = self.df_original['X'].between(x_min, x_max)
            y_validas = self.df_original['Y'].between(y_min, y_max)
            
            if not x_validas.all() or not y_validas.all():
                self.logger.warning("Algunas coordenadas están fuera del rango esperado para Medellín")
            
            return True
            
        except Exception as e:
            self.errores_validacion.append(f"Error validando coordenadas: {str(e)}")
            return False
    
    def limpiar_datos(self) -> bool:
        """
        Limpiar y convertir tipos de datos
        
        Returns:
            bool: True si la limpieza fue exitosa
        """
        try:
            # Crear copia para procesamiento
            self.df_procesado = self.df_original.copy()
            
            # Convertir fechas
            if 'fecha_dilig' in self.df_procesado.columns:
                self.df_procesado['fecha_dilig'] = pd.to_datetime(
                    self.df_procesado['fecha_dilig'], errors='coerce'
                )
            
            if 'start' in self.df_procesado.columns:
                self.df_procesado['start'] = pd.to_datetime(
                    self.df_procesado['start'], errors='coerce'
                )
            
            # Convertir columnas numéricas
            columnas_numericas = [
                'num_cuadri', 'trabajador', 'cant_ayuda', 'cant_ofici', 
                'cant_opera', 'cant_auxil', 'cant_otros', 'num_total_', 
                'total_hora', 'horas_retr', 'horas_mini', 'horas_volq', 
                'horas_comp', 'horas_otra'
            ]
            
            for col in columnas_numericas:
                if col in self.df_procesado.columns:
                    self.df_procesado[col] = pd.to_numeric(
                        self.df_procesado[col], errors='coerce'
                    ).fillna(0)
            
            # Limpiar textos
            columnas_texto = ['id_punto', 'nombre_int', 'maquinaria']
            for col in columnas_texto:
                if col in self.df_procesado.columns:
                    self.df_procesado[col] = self.df_procesado[col].astype(str).str.strip()
            
            self.logger.info("Datos limpiados exitosamente")
            return True
            
        except Exception as e:
            self.logger.error(f"Error limpiando datos: {str(e)}")
            return False
    
    def calcular_totales(self) -> bool:
        """
        Calcular totales automáticos y validar consistencia
        
        Returns:
            bool: True si los cálculos fueron exitosos
        """
        try:
            # Calcular total de trabajadores
            columnas_trabajadores = ['cant_ayuda', 'cant_ofici', 'cant_opera', 'cant_auxil', 'cant_otros']
            columnas_existentes = [col for col in columnas_trabajadores if col in self.df_procesado.columns]
            
            if columnas_existentes:
                self.df_procesado['total_calculado_trabajadores'] = self.df_procesado[columnas_existentes].sum(axis=1)
            
            # Calcular total de horas de maquinaria
            columnas_horas_maq = ['horas_retr', 'horas_mini', 'horas_volq', 'horas_comp', 'horas_otra']
            columnas_maq_existentes = [col for col in columnas_horas_maq if col in self.df_procesado.columns]
            
            if columnas_maq_existentes:
                self.df_procesado['total_horas_maquinaria'] = self.df_procesado[columnas_maq_existentes].sum(axis=1)
            
            # Validar consistencia
            self._validar_consistencia()
            
            self.logger.info("Totales calculados exitosamente")
            return True
            
        except Exception as e:
            self.logger.error(f"Error calculando totales: {str(e)}")
            return False
    
    def _validar_consistencia(self):
        """Validar consistencia entre totales reportados y calculados"""
        # Validar total de trabajadores
        if 'num_total_' in self.df_procesado.columns and 'total_calculado_trabajadores' in self.df_procesado.columns:
            diferencias = abs(self.df_procesado['num_total_'] - self.df_procesado['total_calculado_trabajadores'])
            registros_con_diferencias = (diferencias > 0).sum()
            
            if registros_con_diferencias > 0:
                self.logger.warning(f"{registros_con_diferencias} registros tienen diferencias en total de trabajadores")
    
    def obtener_resumen(self) -> Dict:
        """
        Obtener resumen del procesamiento
        
        Returns:
            Dict: Resumen con estadísticas del procesamiento
        """
        if self.df_procesado is None:
            return {"error": "No hay datos procesados"}
        
        resumen = {
            "archivo_original": {
                "filas": self.df_original.shape[0] if self.df_original is not None else 0,
                "columnas": self.df_original.shape[1] if self.df_original is not None else 0
            },
            "archivo_procesado": {
                "filas": self.df_procesado.shape[0],
                "columnas": self.df_procesado.shape[1]
            },
            "validacion": {
                "errores": self.errores_validacion,
                "es_valido": len(self.errores_validacion) == 0
            },
            "estadisticas": {
                "total_intervenciones": len(self.df_procesado),
                "total_trabajadores": self.df_procesado.get('num_total_', pd.Series([0])).sum(),
                "total_horas": self.df_procesado.get('total_hora', pd.Series([0])).sum(),
                "estados_obra": self.df_procesado.get('estado_obr', pd.Series()).value_counts().to_dict()
            }
        }
        
        return resumen
    
    def obtener_datos_procesados(self) -> Optional[pd.DataFrame]:
        """
        Obtener el DataFrame procesado
        
        Returns:
            pd.DataFrame: Datos procesados o None si no hay datos
        """
        return self.df_procesado
    
    def procesar_archivo_completo(self, ruta_archivo: str) -> Tuple[bool, Dict]:
        """
        Procesar archivo completo en un solo método
        
        Args:
            ruta_archivo: Ruta al archivo Excel
            
        Returns:
            Tuple[bool, Dict]: (éxito, resumen)
        """
        # Cargar archivo
        if not self.cargar_archivo(ruta_archivo):
            return False, {"error": "No se pudo cargar el archivo"}
        
        # Validar estructura
        if not self.validar_estructura():
            return False, {"error": "Estructura de archivo inválida", "errores": self.errores_validacion}
        
        # Limpiar datos
        if not self.limpiar_datos():
            return False, {"error": "Error limpiando datos"}
        
        # Calcular totales
        if not self.calcular_totales():
            return False, {"error": "Error calculando totales"}
        
        # Obtener resumen
        resumen = self.obtener_resumen()
        
        self.logger.info("Archivo procesado exitosamente")
        return True, resumen
