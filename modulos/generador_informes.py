"""
Módulo para generación inteligente de informes Survey123
Con procesamiento de lenguaje natural e insights automáticos
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from collections import Counter
import re
from typing import Dict, List, Any, Tuple

class AnalizadorInteligente:
    """Analizador que genera insights automáticos de los datos Survey123"""
    
    def __init__(self, datos: pd.DataFrame):
        self.datos = datos
        self.total_registros = len(datos)
        self.insights = []
        self.recomendaciones = []
        
    def analizar_tendencias_temporales(self) -> Dict[str, Any]:
        """Analiza tendencias temporales en los datos"""
        if 'fecha_dilig' not in self.datos.columns:
            return {}
            
        # Convertir fechas
        fechas = pd.to_datetime(self.datos['fecha_dilig'], errors='coerce')
        fechas_validas = fechas.dropna()
        
        if len(fechas_validas) == 0:
            return {}
            
        rango_dias = (fechas_validas.max() - fechas_validas.min()).days
        
        analisis = {
            'fecha_inicio': fechas_validas.min(),
            'fecha_fin': fechas_validas.max(),
            'rango_dias': rango_dias,
            'registros_por_dia': len(fechas_validas) / max(rango_dias, 1),
            'dias_mas_activos': fechas_validas.dt.day_name().value_counts().head(3).to_dict()
        }
        
        # Generar insights temporales
        if rango_dias > 30:
            self.insights.append(f"Los datos abarcan un período de {rango_dias} días, indicando un proyecto de larga duración.")
        
        registros_diarios = analisis['registros_por_dia']
        if registros_diarios > 3:
            self.insights.append(f"Alta frecuencia de actividades con {registros_diarios:.1f} registros por día en promedio.")
        elif registros_diarios < 1:
            self.insights.append("Baja frecuencia de actividades, sugiere actividades espaciadas o específicas.")
            
        return analisis
    
    def analizar_recursos_humanos(self) -> Dict[str, Any]:
        """Analiza distribución y eficiencia de recursos humanos"""
        rh_data = {}
        
        # Análisis de trabajadores
        if 'num_total_' in self.datos.columns:
            trabajadores = self.datos['num_total_'].fillna(0)
            rh_data['total_trabajadores'] = int(trabajadores.sum())
            rh_data['promedio_por_actividad'] = trabajadores.mean()
            rh_data['max_trabajadores_actividad'] = int(trabajadores.max())
            rh_data['actividades_sin_personal'] = int((trabajadores == 0).sum())
        
        # Análisis de horas
        if 'total_hora' in self.datos.columns:
            horas = self.datos['total_hora'].fillna(0)
            rh_data['total_horas'] = float(horas.sum())
            rh_data['promedio_horas_actividad'] = horas.mean()
            rh_data['eficiencia_hora_trabajador'] = rh_data['total_horas'] / max(rh_data.get('total_trabajadores', 1), 1)
        
        # Generar insights de RH
        if rh_data.get('total_trabajadores', 0) > 0:
            promedio_trabajadores = rh_data['promedio_por_actividad']
            if promedio_trabajadores > 10:
                self.insights.append("Las actividades requieren equipos de trabajo grandes, indicando proyectos de alta complejidad.")
                self.recomendaciones.append("Considerar subdividir actividades grandes para optimizar la gestión de equipos.")
            elif promedio_trabajadores < 3:
                self.insights.append("Predominan actividades con equipos pequeños, sugiere trabajos especializados.")
        
        eficiencia = rh_data.get('eficiencia_hora_trabajador', 0)
        if eficiencia > 8:
            self.insights.append("Alta intensidad de trabajo por persona, indica proyectos demandantes.")
        elif eficiencia < 4:
            self.recomendaciones.append("Revisar la asignación de horas para optimizar la productividad del personal.")
            
        return rh_data
    
    def analizar_distribucion_geografica(self) -> Dict[str, Any]:
        """Analiza distribución geográfica de las intervenciones"""
        geo_data = {}
        
        if 'X' in self.datos.columns and 'Y' in self.datos.columns:
            coords_validas = self.datos.dropna(subset=['X', 'Y'])
            
            if len(coords_validas) > 0:
                geo_data['puntos_unicos'] = len(coords_validas.groupby(['X', 'Y']))
                geo_data['concentracion'] = len(coords_validas) / geo_data['puntos_unicos']
                geo_data['rango_lat'] = coords_validas['Y'].max() - coords_validas['Y'].min()
                geo_data['rango_lon'] = coords_validas['X'].max() - coords_validas['X'].min()
                geo_data['centro_lat'] = coords_validas['Y'].mean()
                geo_data['centro_lon'] = coords_validas['X'].mean()
        
        # Análisis por estado de obra
        if 'estado_obr' in self.datos.columns:
            estados = self.datos['estado_obr'].value_counts()
            geo_data['distribucion_estados'] = estados.to_dict()
            
            # Insights de estados
            estado_predominante = estados.index[0] if len(estados) > 0 else None
            if estado_predominante:
                porcentaje = (estados.iloc[0] / self.total_registros) * 100
                if porcentaje > 70:
                    self.insights.append(f"El {porcentaje:.1f}% de las obras están en estado '{estado_predominante}', indicando una fase concentrada del proyecto.")
                
                if estado_predominante.lower() == 'terminada':
                    self.insights.append("Predominan obras terminadas, sugiere un proyecto en fase de cierre o evaluación.")
                elif estado_predominante.lower() in ['en ejecucion', 'en proceso']:
                    self.insights.append("Mayoría de obras en ejecución, proyecto en fase activa de implementación.")
        
        # Insights geográficos
        concentracion = geo_data.get('concentracion', 1)
        if concentracion > 3:
            self.insights.append("Alta concentración de actividades por punto geográfico, indica intervenciones intensivas.")
        elif concentracion == 1:
            self.insights.append("Una actividad por punto geográfico, sugiere intervenciones distribuidas y específicas.")
            
        return geo_data
    
    def analizar_tipos_actividades(self) -> Dict[str, Any]:
        """Analiza tipos y patrones de actividades"""
        actividades_data = {}
        
        # Buscar columnas relacionadas con actividades
        columnas_actividades = [col for col in self.datos.columns if any(palabra in col.lower() 
                              for palabra in ['actividad', 'trabajo', 'labor', 'tarea', 'tipo'])]
        
        for col in columnas_actividades[:3]:  # Analizar máximo 3 columnas
            if self.datos[col].dtype == 'object':
                valores = self.datos[col].value_counts().head(5)
                actividades_data[col] = valores.to_dict()
        
        # Análisis de maquinaria y equipos
        columnas_maquinaria = [col for col in self.datos.columns if any(palabra in col.lower() 
                              for palabra in ['maquina', 'equipo', 'herramienta', 'vehiculo'])]
        
        maquinaria_total = 0
        for col in columnas_maquinaria:
            if pd.api.types.is_numeric_dtype(self.datos[col]):
                maquinaria_total += self.datos[col].fillna(0).sum()
        
        if maquinaria_total > 0:
            actividades_data['total_maquinaria'] = maquinaria_total
            actividades_data['promedio_maquinaria_actividad'] = maquinaria_total / self.total_registros
            
            # Insights de maquinaria
            if maquinaria_total > self.total_registros * 2:
                self.insights.append("Alto uso de maquinaria y equipos, indica actividades de construcción pesada.")
            elif maquinaria_total < self.total_registros * 0.5:
                self.insights.append("Bajo uso de maquinaria, sugiere actividades manuales o de mantenimiento.")
        
        return actividades_data
    
    def generar_recomendaciones_automaticas(self) -> List[str]:
        """Genera recomendaciones automáticas basadas en el análisis"""
        recomendaciones_adicionales = []
        
        # Recomendaciones basadas en el tamaño del proyecto
        if self.total_registros > 100:
            recomendaciones_adicionales.append("Considerar implementar un sistema de seguimiento automatizado dado el volumen de actividades.")
        elif self.total_registros < 20:
            recomendaciones_adicionales.append("Evaluar la posibilidad de consolidar actividades para optimizar recursos.")
        
        # Recomendaciones de calidad de datos
        columnas_con_nulos = self.datos.isnull().sum()
        columnas_problematicas = columnas_con_nulos[columnas_con_nulos > self.total_registros * 0.3]
        
        if len(columnas_problematicas) > 0:
            recomendaciones_adicionales.append("Mejorar la completitud de datos en el diligenciamiento de formularios.")
        
        return self.recomendaciones + recomendaciones_adicionales
    
    def generar_resumen_ejecutivo(self) -> str:
        """Genera un resumen ejecutivo inteligente"""
        # Realizar todos los análisis
        temporal = self.analizar_tendencias_temporales()
        rh = self.analizar_recursos_humanos()
        geo = self.analizar_distribucion_geografica()
        actividades = self.analizar_tipos_actividades()
        
        # Construir resumen
        resumen_partes = []
        
        # Introducción
        resumen_partes.append(f"Este informe analiza {self.total_registros} registros de actividades del proyecto Survey123.")
        
        # Temporalidad
        if temporal.get('rango_dias', 0) > 0:
            resumen_partes.append(f"Las actividades se desarrollaron durante {temporal['rango_dias']} días, "
                                f"con una frecuencia promedio de {temporal['registros_por_dia']:.1f} actividades por día.")
        
        # Recursos humanos
        if rh.get('total_trabajadores', 0) > 0:
            resumen_partes.append(f"Se movilizaron {rh['total_trabajadores']} trabajadores, "
                                f"registrando {rh['total_horas']:.1f} horas de trabajo total.")
        
        # Distribución geográfica
        if geo.get('puntos_unicos', 0) > 0:
            resumen_partes.append(f"Las intervenciones se distribuyeron en {geo['puntos_unicos']} puntos geográficos únicos.")
        
        # Estados de obra
        if 'distribucion_estados' in geo:
            estado_principal = max(geo['distribucion_estados'].items(), key=lambda x: x[1])
            resumen_partes.append(f"El estado predominante es '{estado_principal[0]}' con {estado_principal[1]} registros.")
        
        return " ".join(resumen_partes)


class GeneradorProsa:
    """Generador de texto en prosa para informes"""
    
    @staticmethod
    def generar_introduccion(tipo_informe: str, total_registros: int) -> str:
        """Genera introducción dinámica según el tipo de informe"""
        introducciones = {
            'estadistico': f"""
            El presente informe estadístico proporciona un análisis cuantitativo exhaustivo de las {total_registros} 
            actividades registradas en el sistema Survey123. A través de métricas clave y indicadores de rendimiento, 
            se evalúa el desempeño general del proyecto, identificando patrones significativos en la ejecución de obras 
            y la asignación de recursos humanos y técnicos.
            """,
            'detallado': f"""
            Este informe detallado examina minuciosamente cada aspecto de las {total_registros} intervenciones registradas, 
            proporcionando un análisis integral que abarca desde la distribución temporal de actividades hasta la 
            caracterización específica de recursos empleados. El documento constituye una herramienta fundamental 
            para la evaluación operativa y la toma de decisiones informadas en la gestión del proyecto.
            """,
            'ejecutivo': f"""
            El presente resumen ejecutivo consolida los hallazgos más relevantes derivados del análisis de {total_registros} 
            registros de actividades, presentando de manera concisa los indicadores críticos de desempeño, las tendencias 
            identificadas y las recomendaciones estratégicas para la optimización de los procesos de ejecución del proyecto.
            """
        }
        
        return introducciones.get(tipo_informe, introducciones['estadistico']).strip()
    
    @staticmethod
    def generar_seccion_recursos_humanos(datos_rh: Dict[str, Any]) -> str:
        """Genera prosa para la sección de recursos humanos"""
        if not datos_rh:
            return "No se encontraron datos suficientes para el análisis de recursos humanos."
        
        total_trabajadores = datos_rh.get('total_trabajadores', 0)
        total_horas = datos_rh.get('total_horas', 0)
        promedio_trabajadores = datos_rh.get('promedio_por_actividad', 0)
        eficiencia = datos_rh.get('eficiencia_hora_trabajador', 0)
        
        prosa = f"""
        La movilización de recursos humanos para el proyecto alcanzó un total de {total_trabajadores:,} trabajadores, 
        quienes contribuyeron con {total_horas:,.1f} horas de trabajo efectivo. La distribución promedio de personal 
        por actividad fue de {promedio_trabajadores:.1f} trabajadores, evidenciando 
        {'equipos de trabajo robustos' if promedio_trabajadores > 5 else 'grupos de trabajo focalizados'}.
        
        El indicador de eficiencia por trabajador registra {eficiencia:.1f} horas promedio por persona, lo que 
        {'sugiere una carga de trabajo intensa y actividades de alta demanda técnica' if eficiencia > 8 
         else 'indica una distribución equilibrada de la carga laboral' if eficiencia > 4 
         else 'podría señalar oportunidades de optimización en la asignación de recursos'}.
        """
        
        return prosa.strip()
    
    @staticmethod
    def generar_seccion_geografica(datos_geo: Dict[str, Any]) -> str:
        """Genera prosa para la sección geográfica"""
        if not datos_geo:
            return "No se encontraron datos geográficos para el análisis."
        
        puntos_unicos = datos_geo.get('puntos_unicos', 0)
        concentracion = datos_geo.get('concentracion', 1)
        distribucion_estados = datos_geo.get('distribucion_estados', {})
        
        prosa = f"""
        La distribución geográfica del proyecto abarca {puntos_unicos} puntos de intervención únicos, 
        con una concentración promedio de {concentracion:.1f} actividades por ubicación. Esta distribución 
        {'revela un enfoque intensivo en sitios específicos' if concentracion > 2 
         else 'muestra una estrategia de intervención distribuida y focalizada'}.
        """
        
        if distribucion_estados:
            estado_principal = max(distribucion_estados.items(), key=lambda x: x[1])
            porcentaje_principal = (estado_principal[1] / sum(distribucion_estados.values())) * 100
            
            prosa += f"""
            
            En términos del estado de ejecución, {porcentaje_principal:.1f}% de las intervenciones se encuentran 
            en estado '{estado_principal[0]}', lo que {'indica un proyecto en fase de cierre' if 'terminada' in estado_principal[0].lower()
                                                       else 'sugiere un proyecto en desarrollo activo' if 'ejecucion' in estado_principal[0].lower()
                                                       else 'refleja el estado actual de implementación'}.
            """
        
        return prosa.strip()
    
    @staticmethod
    def generar_conclusiones(insights: List[str], recomendaciones: List[str]) -> str:
        """Genera conclusiones basadas en insights y recomendaciones"""
        conclusiones = """
        ## CONCLUSIONES Y RECOMENDACIONES
        
        ### Hallazgos Principales:
        """
        
        for i, insight in enumerate(insights[:5], 1):
            conclusiones += f"\n{i}. {insight}"
        
        if recomendaciones:
            conclusiones += "\n\n### Recomendaciones Estratégicas:\n"
            for i, recomendacion in enumerate(recomendaciones[:5], 1):
                conclusiones += f"\n{i}. {recomendacion}"
        
        return conclusiones


def procesar_datos_para_informe(datos: pd.DataFrame) -> Dict[str, Any]:
    """Procesa los datos y genera toda la información necesaria para los informes"""
    analizador = AnalizadorInteligente(datos)
    
    # Realizar análisis completo
    temporal = analizador.analizar_tendencias_temporales()
    rh = analizador.analizar_recursos_humanos()
    geo = analizador.analizar_distribucion_geografica()
    actividades = analizador.analizar_tipos_actividades()
    recomendaciones = analizador.generar_recomendaciones_automaticas()
    resumen_ejecutivo = analizador.generar_resumen_ejecutivo()
    
    return {
        'metadata': {
            'total_registros': len(datos),
            'columnas_analizadas': len(datos.columns),
            'fecha_procesamiento': datetime.now().strftime('%d/%m/%Y %H:%M')
        },
        'temporal': temporal,
        'recursos_humanos': rh,
        'geografico': geo,
        'actividades': actividades,
        'insights': analizador.insights,
        'recomendaciones': recomendaciones,
        'resumen_ejecutivo': resumen_ejecutivo
    }
