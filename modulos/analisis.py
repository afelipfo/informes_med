"""
Módulo de análisis de datos para Survey123
Secretaría de Infraestructura Física de Medellín

Este módulo proporciona funcionalidades para analizar los datos
procesados de Survey123 y generar estadísticas e insights.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
from typing import Dict, Any
import os

warnings.filterwarnings('ignore')


class AnalizadorDatos:
    """
    Clase para análisis básico de datos de Survey123
    """
    
    def __init__(self):
        """Inicializa el analizador"""
        pass
    
    def calcular_estadisticas_basicas(self, datos: pd.DataFrame) -> Dict[str, Any]:
        """
        Calcula estadísticas básicas de los datos
        
        Args:
            datos: DataFrame con los datos
            
        Returns:
            Dict con estadísticas básicas
        """
        try:
            estadisticas = {
                'total_intervenciones': len(datos),
                'trabajadores_unicos': datos['trabajador'].nunique() if 'trabajador' in datos.columns else 0,
                'intervenciones_por_estado': {},
                'promedio_horas': 0
            }
            
            if 'estado_obr' in datos.columns:
                estadisticas['intervenciones_por_estado'] = datos['estado_obr'].value_counts().to_dict()
            
            if 'total_hora' in datos.columns:
                estadisticas['promedio_horas'] = datos['total_hora'].mean()
            
            return estadisticas
        except Exception as e:
            return {
                'total_intervenciones': 0,
                'trabajadores_unicos': 0,
                'intervenciones_por_estado': {},
                'promedio_horas': 0,
                'error': str(e)
            }
    
    def analizar_productividad(self, datos: pd.DataFrame) -> Dict[str, Any]:
        """
        Analiza la productividad de los trabajadores
        
        Args:
            datos: DataFrame con los datos
            
        Returns:
            Dict con análisis de productividad
        """
        try:
            productividad = {
                'horas_promedio': 0,
                'trabajador_mas_productivo': 'N/A',
                'cuadrilla_mas_activa': 'N/A'
            }
            
            if 'total_hora' in datos.columns:
                productividad['horas_promedio'] = datos['total_hora'].mean()
            
            if 'trabajador' in datos.columns and 'total_hora' in datos.columns:
                horas_por_trabajador = datos.groupby('trabajador')['total_hora'].sum()
                if len(horas_por_trabajador) > 0:
                    productividad['trabajador_mas_productivo'] = horas_por_trabajador.idxmax()
            
            if 'num_cuadri' in datos.columns:
                intervenciones_por_cuadrilla = datos['num_cuadri'].value_counts()
                if len(intervenciones_por_cuadrilla) > 0:
                    productividad['cuadrilla_mas_activa'] = intervenciones_por_cuadrilla.idxmax()
            
            return productividad
        except Exception as e:
            return {
                'horas_promedio': 0,
                'trabajador_mas_productivo': 'N/A',
                'cuadrilla_mas_activa': 'N/A',
                'error': str(e)
            }
    
    def generar_tendencias(self, datos: pd.DataFrame) -> Dict[str, Any]:
        """
        Genera análisis de tendencias temporales
        
        Args:
            datos: DataFrame con los datos
            
        Returns:
            Dict con tendencias
        """
        try:
            tendencias = {
                'intervenciones_por_dia': pd.Series(dtype='int64'),
                'tendencia_semanal': {}
            }
            
            if 'fecha_dilig' in datos.columns:
                # Convertir fechas si no están en formato datetime
                if not pd.api.types.is_datetime64_any_dtype(datos['fecha_dilig']):
                    datos['fecha_dilig'] = pd.to_datetime(datos['fecha_dilig'], errors='coerce')
                
                datos_con_fecha = datos.dropna(subset=['fecha_dilig'])
                if len(datos_con_fecha) > 0:
                    tendencias['intervenciones_por_dia'] = datos_con_fecha.groupby(
                        datos_con_fecha['fecha_dilig'].dt.date
                    ).size()
                    
                    # Tendencia semanal
                    datos_con_fecha['dia_semana'] = datos_con_fecha['fecha_dilig'].dt.day_name()
                    tendencias['tendencia_semanal'] = datos_con_fecha['dia_semana'].value_counts().to_dict()
            
            return tendencias
        except Exception as e:
            return {
                'intervenciones_por_dia': pd.Series(dtype='int64'),
                'tendencia_semanal': {},
                'error': str(e)
            }

class AnalisisSurvey123:
    """
    Clase principal para análisis de datos de Survey123
    """
    
    def __init__(self, datos: pd.DataFrame):
        """
        Inicializa el analizador con los datos procesados
        
        Args:
            datos: DataFrame con los datos de Survey123 procesados
        """
        self.datos = datos.copy()
        self.metricas = {}
        self.configurar_estilos()
    
    def configurar_estilos(self):
        """Configura estilos para las visualizaciones"""
        plt.style.use('default')
        sns.set_palette("husl")
        
        # Configuración para matplotlib
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.titlesize'] = 14
        plt.rcParams['axes.labelsize'] = 12
        plt.rcParams['xtick.labelsize'] = 10
        plt.rcParams['ytick.labelsize'] = 10
        plt.rcParams['legend.fontsize'] = 10
    
    def calcular_metricas_generales(self) -> Dict[str, Any]:
        """
        Calcula métricas generales del proyecto
        
        Returns:
            Dict con métricas generales
        """
        metricas = {
            'total_registros': len(self.datos),
            'fecha_inicio': self.datos['fecha_dilig'].min() if 'fecha_dilig' in self.datos.columns else None,
            'fecha_fin': self.datos['fecha_dilig'].max() if 'fecha_dilig' in self.datos.columns else None,
            'estados_obra': self.datos['estado_obr'].value_counts().to_dict() if 'estado_obr' in self.datos.columns else {},
            'total_puntos_unicos': self.datos['id_punto'].nunique() if 'id_punto' in self.datos.columns else 0,
            'cobertura_geografica': {
                'lat_min': self.datos['Y'].min() if 'Y' in self.datos.columns else 0,
                'lat_max': self.datos['Y'].max() if 'Y' in self.datos.columns else 0,
                'lon_min': self.datos['X'].min() if 'X' in self.datos.columns else 0,
                'lon_max': self.datos['X'].max() if 'X' in self.datos.columns else 0
            }
        }
        
        if 'fecha_dilig' in self.datos.columns and metricas['fecha_inicio'] and metricas['fecha_fin']:
            metricas['duracion_proyecto'] = (metricas['fecha_fin'] - metricas['fecha_inicio']).days
        else:
            metricas['duracion_proyecto'] = 0
        
        self.metricas['generales'] = metricas
        return metricas
    
    def analizar_recursos_humanos(self) -> Dict[str, Any]:
        """
        Analiza los recursos humanos utilizados
        
        Returns:
            Dict con análisis de recursos humanos
        """
        columnas_rrhh = ['cant_ayuda', 'cant_ofici', 'cant_opera', 'cant_auxil', 'cant_otros', 'num_total_', 'total_hora']
        
        # Verificar que las columnas existen
        columnas_existentes = [col for col in columnas_rrhh if col in self.datos.columns]
        
        if not columnas_existentes:
            return {'error': 'No se encontraron columnas de recursos humanos'}
        
        analisis = {
            'total_ayudantes': self.datos['cant_ayuda'].sum() if 'cant_ayuda' in self.datos.columns else 0,
            'total_oficiales': self.datos['cant_ofici'].sum() if 'cant_ofici' in self.datos.columns else 0,
            'total_operadores': self.datos['cant_opera'].sum() if 'cant_opera' in self.datos.columns else 0,
            'total_auxiliares': self.datos['cant_auxil'].sum() if 'cant_auxil' in self.datos.columns else 0,
            'total_otros': self.datos['cant_otros'].sum() if 'cant_otros' in self.datos.columns else 0,
            'total_trabajadores': self.datos['num_total_'].sum() if 'num_total_' in self.datos.columns else 0,
            'total_horas_trabajadas': self.datos['total_hora'].sum() if 'total_hora' in self.datos.columns else 0,
            'promedio_trabajadores_por_obra': self.datos['num_total_'].mean() if 'num_total_' in self.datos.columns else 0,
            'promedio_horas_por_obra': self.datos['total_hora'].mean() if 'total_hora' in self.datos.columns else 0,
            'distribucion_personal': {
                'Ayudantes': self.datos['cant_ayuda'].sum() if 'cant_ayuda' in self.datos.columns else 0,
                'Oficiales': self.datos['cant_ofici'].sum() if 'cant_ofici' in self.datos.columns else 0,
                'Operadores': self.datos['cant_opera'].sum() if 'cant_opera' in self.datos.columns else 0,
                'Auxiliares': self.datos['cant_auxil'].sum() if 'cant_auxil' in self.datos.columns else 0,
                'Otros': self.datos['cant_otros'].sum() if 'cant_otros' in self.datos.columns else 0
            }
        }
        
        # Distribución por obra
        if 'num_total_' in self.datos.columns:
            analisis['estadisticas_trabajadores'] = self.datos['num_total_'].describe().to_dict()
        
        if 'total_hora' in self.datos.columns:
            analisis['estadisticas_horas'] = self.datos['total_hora'].describe().to_dict()
        
        self.metricas['recursos_humanos'] = analisis
        return analisis
    
    def analizar_maquinaria(self) -> Dict[str, Any]:
        """
        Analiza el uso de maquinaria y equipos
        
        Returns:
            Dict con análisis de maquinaria
        """
        # Columnas específicas de maquinaria según el archivo
        columnas_maquinaria = ['horas_retr', 'horas_mini', 'horas_volq', 'horas_comp', 'horas_otra', 'maquinaria', 'nombre_otr']
        
        analisis = {
            'total_horas_retroexcavadora': self.datos['horas_retr'].sum() if 'horas_retr' in self.datos.columns else 0,
            'total_horas_minicargador': self.datos['horas_mini'].sum() if 'horas_mini' in self.datos.columns else 0,
            'total_horas_volqueta': self.datos['horas_volq'].sum() if 'horas_volq' in self.datos.columns else 0,
            'total_horas_compactadora': self.datos['horas_comp'].sum() if 'horas_comp' in self.datos.columns else 0,
            'total_horas_otra': self.datos['horas_otra'].sum() if 'horas_otra' in self.datos.columns else 0,
            'distribucion_horas_maquinaria': {
                'Retroexcavadora': self.datos['horas_retr'].sum() if 'horas_retr' in self.datos.columns else 0,
                'Minicargador': self.datos['horas_mini'].sum() if 'horas_mini' in self.datos.columns else 0,
                'Volqueta': self.datos['horas_volq'].sum() if 'horas_volq' in self.datos.columns else 0,
                'Compactadora': self.datos['horas_comp'].sum() if 'horas_comp' in self.datos.columns else 0,
                'Otra': self.datos['horas_otra'].sum() if 'horas_otra' in self.datos.columns else 0
            },
            'tipos_maquinaria_usada': {}
        }
        
        # Analizar tipos de maquinaria
        if 'maquinaria' in self.datos.columns:
            analisis['tipos_maquinaria_usada'] = self.datos['maquinaria'].value_counts().to_dict()
        
        if 'nombre_otr' in self.datos.columns:
            otras_maquinarias = self.datos['nombre_otr'].dropna().value_counts()
            if len(otras_maquinarias) > 0:
                analisis['otras_maquinarias'] = otras_maquinarias.to_dict()
        
        total_horas_maquinaria = sum([
            analisis['total_horas_retroexcavadora'],
            analisis['total_horas_minicargador'],
            analisis['total_horas_volqueta'],
            analisis['total_horas_compactadora'],
            analisis['total_horas_otra']
        ])
        
        analisis['total_horas_maquinaria'] = total_horas_maquinaria
        analisis['promedio_horas_por_obra'] = total_horas_maquinaria / len(self.datos) if len(self.datos) > 0 else 0
        
        self.metricas['maquinaria'] = analisis
        return analisis
    
    def analizar_actividades_construccion(self) -> Dict[str, Any]:
        """
        Analiza todas las actividades de construcción específicas del Survey123
        
        Returns:
            Dict con análisis completo de actividades
        """
        # Grupos de actividades según las columnas del Survey123
        grupos_actividades = {
            'preparacion_terreno': ['descapote', 'a_mano', 'a_maquina', 'Tala_poda', 'roceria_li'],
            'cerramientos_proteccion': ['cerramient', 'tela_verde', 'malla_nara', 'teja_ondul', 'cubierta_p', 'pasarela_p', 'proteccion', 'protecci_vehicular'],
            'limpieza_mantenimiento': ['limpieza_e', 'limpieza_s'],
            'infraestructura_hidrica': ['malla_esla', 'canoas_rua', 'bajantes', 'tuberia_en'],
            'estructuras_seguridad': ['cerco_made', 'pintura_ba', 'pasamanos_', 'barrera_me', 'pintura_pa'],
            'elementos_servicio': ['aparatos_s', 'puertas', 'senal_vert', 'reparacion', 'ventanas', 'teja_barro'],
            'pavimentacion': ['piso_adoqu', 'piso_ado_1', 'cordones_c'],
            'drenajes': ['carcamos_c', 'Cunetas_co', 'drenaje_pe'],
            'excavaciones': ['excav_manu', 'excav_ma_1', 'excav_meca', 'excav_me_1', 'excav_me_2', 'excav_me_3', 'explanacio', 'explanac_1', 'excav_terrazas'],
            'trabajos_roca': ['roca_cielo_cuña', 'roca_cielo_martillo', 'roca_pila_'],
            'concreto': ['e_concreto'],
            'cortes_taludes': ['corte_talu', 'corte_ta_1', 'corte_ta_2'],
            'transporte': ['transpor_1']
        }
        
        analisis_completo = {
            'resumen_por_grupo': {},
            'totales_generales': {},
            'actividades_mas_comunes': {},
            'cobertura_actividades': {}
        }
        
        # Analizar cada grupo de actividades
        for grupo, columnas in grupos_actividades.items():
            columnas_existentes = [col for col in columnas if col in self.datos.columns]
            
            if columnas_existentes:
                grupo_stats = {
                    'columnas_analizadas': columnas_existentes,
                    'totales_por_actividad': {},
                    'total_grupo': 0,
                    'obras_con_actividad': 0,
                    'promedio_por_obra': 0
                }
                
                total_grupo = 0
                obras_con_actividad = 0
                
                for col in columnas_existentes:
                    if col in self.datos.columns:
                        total_col = self.datos[col].sum()
                        obras_con_col = (self.datos[col] > 0).sum()
                        
                        grupo_stats['totales_por_actividad'][col] = {
                            'total': total_col,
                            'obras_con_actividad': obras_con_col,
                            'promedio': self.datos[col].mean(),
                            'maximo': self.datos[col].max()
                        }
                        
                        total_grupo += total_col
                        if obras_con_col > 0:
                            obras_con_actividad += 1
                
                grupo_stats['total_grupo'] = total_grupo
                grupo_stats['obras_con_actividad'] = obras_con_actividad
                grupo_stats['promedio_por_obra'] = total_grupo / len(self.datos) if len(self.datos) > 0 else 0
                
                analisis_completo['resumen_por_grupo'][grupo] = grupo_stats
        
        # Calcular totales generales
        total_todas_actividades = 0
        actividades_con_mayor_volumen = {}
        
        for grupo, stats in analisis_completo['resumen_por_grupo'].items():
            total_todas_actividades += stats['total_grupo']
            for actividad, valores in stats['totales_por_actividad'].items():
                actividades_con_mayor_volumen[actividad] = valores['total']
        
        # Ordenar actividades por volumen
        actividades_ordenadas = sorted(actividades_con_mayor_volumen.items(), 
                                     key=lambda x: x[1], reverse=True)
        
        analisis_completo['totales_generales'] = {
            'total_todas_actividades': total_todas_actividades,
            'promedio_actividades_por_obra': total_todas_actividades / len(self.datos) if len(self.datos) > 0 else 0
        }
        
        analisis_completo['actividades_mas_comunes'] = dict(actividades_ordenadas[:10])  # Top 10
        
        # Calcular cobertura de actividades
        total_columnas_actividades = sum(len(cols) for cols in grupos_actividades.values())
        columnas_con_datos = sum(1 for grupo, stats in analisis_completo['resumen_por_grupo'].items() 
                               for col in stats['totales_por_actividad'].keys() 
                               if stats['totales_por_actividad'][col]['total'] > 0)
        
        analisis_completo['cobertura_actividades'] = {
            'columnas_totales': total_columnas_actividades,
            'columnas_con_datos': columnas_con_datos,
            'porcentaje_cobertura': (columnas_con_datos / total_columnas_actividades * 100) if total_columnas_actividades > 0 else 0
        }
        
        self.metricas['actividades_construccion'] = analisis_completo
        return analisis_completo
    
    def generar_analisis_completo(self) -> Dict[str, Any]:
        """
        Genera un análisis completo de todos los aspectos del proyecto
        
        Returns:
            Dict con análisis completo
        """
        analisis_completo = {
            'metadata': {
                'fecha_analisis': datetime.now().isoformat(),
                'total_registros': len(self.datos),
                'columnas_analizadas': list(self.datos.columns)
            },
            'metricas_generales': self.calcular_metricas_generales(),
            'recursos_humanos': self.analizar_recursos_humanos(),
            'maquinaria': self.analizar_maquinaria(),
            'actividades_construccion': self.analizar_actividades_construccion()
        }
        
        # Agregar análisis de localización si hay coordenadas
        if 'X' in self.datos.columns and 'Y' in self.datos.columns:
            analisis_completo['analisis_geografico'] = {
                'rango_coordenadas': {
                    'min_x': self.datos['X'].min(),
                    'max_x': self.datos['X'].max(),
                    'min_y': self.datos['Y'].min(),
                    'max_y': self.datos['Y'].max()
                },
                'centroide': {
                    'x': self.datos['X'].mean(),
                    'y': self.datos['Y'].mean()
                },
                'puntos_unicos': self.datos[['X', 'Y']].drop_duplicates().shape[0]
            }
        
        # Agregar análisis temporal si hay fechas
        if 'fecha_dilig' in self.datos.columns:
            fechas_validas = self.datos['fecha_dilig'].dropna()
            if len(fechas_validas) > 0:
                analisis_completo['analisis_temporal'] = {
                    'fecha_inicio': fechas_validas.min().isoformat(),
                    'fecha_fin': fechas_validas.max().isoformat(),
                    'duracion_dias': (fechas_validas.max() - fechas_validas.min()).days,
                    'registros_por_mes': fechas_validas.dt.to_period('M').value_counts().to_dict()
                }
        
        return analisis_completo
