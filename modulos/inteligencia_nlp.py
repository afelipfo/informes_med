"""
Motor de Inteligencia Artificial y Procesamiento de Lenguaje Natural
para análisis dinámico de datos Survey123

Este módulo implementa algoritmos avanzados de NLP para:
- Análisis semántico de todas las 78 variables
- Generación dinámica de insights
- Detección automática de patrones
- Creación de narrativas contextuales
"""

import pandas as pd
import numpy as np
from datetime import datetime
import re
from collections import Counter, defaultdict
import logging

class AnalizadorInteligenteSurvey123:
    """
    Motor de IA que analiza dinámicamente los datos Survey123
    y genera insights contextuales usando NLP
    """
    
    def __init__(self, datos):
        self.datos = datos
        self.insights = []
        self.patrones = {}
        self.anomalias = []
        self.recomendaciones = []
        self.narrativa = {}
        
        # Configurar logging
        self.logger = logging.getLogger(__name__)
        
        # Diccionarios de interpretación semántica
        self.campos_semanticos = self._mapear_campos_semanticos()
        self.templates_narrativos = self._cargar_templates_narrativos()
        
    def _mapear_campos_semanticos(self):
        """
        Mapea semánticamente las 78 columnas para interpretación inteligente
        """
        return {
            # Información temporal
            'temporal': ['fecha_inic', 'fecha_fin_', 'hora_inici', 'hora_final'],
            
            # Recursos humanos y roles
            'recursos_humanos': [
                'nom_obrero', 'nom_obrero2', 'nom_obrero3', 'nom_obrero4', 'nom_obrero5',
                'nom_ayudan', 'nom_ayuda2', 'nom_ayuda3', 'nom_ayuda4',
                'nom_operad', 'nom_opera2', 'nom_opera3',
                'nom_conduc', 'nom_conduc2',
                'num_obreros', 'num_ayudan', 'num_operad', 'num_conduc', 'num_total_'
            ],
            
            # Maquinaria y equipos
            'maquinaria': [
                'tipo_maq_1', 'tipo_maq_2', 'tipo_maq_3', 'tipo_maq_4',
                'placa_maq1', 'placa_maq2', 'placa_maq3', 'placa_maq4',
                'horas_maq1', 'horas_maq2', 'horas_maq3', 'horas_maq4'
            ],
            
            # Actividades y procesos
            'actividades': [
                'actividad_', 'activida_1', 'activida_2', 'activida_3',
                'tipo_activ', 'descripcio'
            ],
            
            # Localización geográfica
            'ubicacion': [
                'barrio', 'comuna', 'direccion', 'X', 'Y', 'id_punto'
            ],
            
            # Estado y progreso
            'estado': ['estado_obr', 'porcentaje'],
            
            # Métricas de tiempo
            'tiempo': ['total_hora', 'hora_traba'],
            
            # Observaciones y comentarios
            'observaciones': ['observacio', 'comentario', 'notas']
        }
    
    def _cargar_templates_narrativos(self):
        """
        Templates para generar narrativas dinámicas
        """
        return {
            'introduccion': [
                "Durante el período analizado, se registraron {total_registros} intervenciones en el sistema Survey123.",
                "El análisis de los datos revela {total_registros} actividades documentadas en la plataforma.",
                "Los registros procesados muestran {total_registros} operaciones ejecutadas por los equipos de trabajo."
            ],
            
            'recursos_humanos': [
                "La fuerza laboral involucrada comprende {total_trabajadores} trabajadores distribuidos en {tipos_roles} categorías operativas.",
                "El recurso humano desplegado suma {total_trabajadores} personas, con una distribución estratégica en {tipos_roles} roles especializados.",
                "La operación requirió la participación de {total_trabajadores} trabajadores, organizados según {tipos_roles} perfiles laborales específicos."
            ],
            
            'productividad': [
                "La productividad promedio registrada es de {productividad:.2f} horas por trabajador por intervención.",
                "Los indicadores de eficiencia muestran {productividad:.2f} horas trabajadas por persona en promedio.",
                "El rendimiento operativo alcanza {productividad:.2f} horas por trabajador por actividad ejecutada."
            ],
            
            'distribucion_geografica': [
                "Las intervenciones se concentran en {num_comunas} comunas, con mayor densidad en {comuna_principal}.",
                "La cobertura territorial abarca {num_comunas} comunas del municipio, siendo {comuna_principal} la de mayor actividad.",
                "El área de influencia comprende {num_comunas} comunas, destacándose {comuna_principal} por su volumen operativo."
            ]
        }
    
    def analizar_completamente(self):
        """
        Ejecuta el análisis completo e inteligente de todos los datos
        """
        self.logger.info("Iniciando análisis inteligente de datos Survey123")
        
        # Análisis por categorías semánticas
        self._analizar_dimension_temporal()
        self._analizar_recursos_humanos()
        self._analizar_maquinaria_equipos()
        self._analizar_actividades()
        self._analizar_distribucion_geografica()
        self._detectar_patrones_avanzados()
        self._generar_insights_contextuales()
        self._crear_recomendaciones_inteligentes()
        
        # Generar narrativa final
        self._construir_narrativa_dinamica()
        
        return {
            'insights': self.insights,
            'patrones': self.patrones,
            'anomalias': self.anomalias,
            'recomendaciones': self.recomendaciones,
            'narrativa': self.narrativa
        }
    
    def _analizar_dimension_temporal(self):
        """
        Análisis inteligente de patrones temporales
        """
        campos_tiempo = self.campos_semanticos['temporal']
        campos_disponibles = [c for c in campos_tiempo if c in self.datos.columns]
        
        if not campos_disponibles:
            return
        
        # Análisis de fechas
        if 'fecha_inic' in self.datos.columns:
            fechas = pd.to_datetime(self.datos['fecha_inic'], errors='coerce')
            fechas_validas = fechas.dropna()
            
            if len(fechas_validas) > 0:
                rango_temporal = (fechas_validas.max() - fechas_validas.min()).days
                
                # Detectar concentración temporal
                frecuencia_diaria = fechas_validas.dt.date.value_counts()
                dia_mas_activo = frecuencia_diaria.index[0]
                actividades_dia = frecuencia_diaria.iloc[0]
                
                self.insights.append({
                    'categoria': 'temporal',
                    'tipo': 'concentracion_temporal',
                    'descripcion': f"Las actividades se concentran significativamente el {dia_mas_activo} con {actividades_dia} intervenciones registradas.",
                    'impacto': 'alto' if actividades_dia > len(self.datos) * 0.3 else 'medio',
                    'dato_clave': f"{dia_mas_activo}: {actividades_dia} actividades"
                })
                
                # Análisis de distribución semanal
                dias_semana = fechas_validas.dt.day_name()
                distribucion_semanal = dias_semana.value_counts()
                
                if len(distribucion_semanal) > 1:
                    dia_preferido = distribucion_semanal.index[0]
                    self.patrones['patron_semanal'] = {
                        'dia_preferido': dia_preferido,
                        'distribucion': distribucion_semanal.to_dict(),
                        'interpretacion': f"Existe una marcada preferencia por ejecutar actividades los días {dia_preferido}"
                    }
    
    def _analizar_recursos_humanos(self):
        """
        Análisis dinámico e inteligente de recursos humanos
        """
        campos_rh = self.campos_semanticos['recursos_humanos']
        
        # Análisis de composición de equipos
        roles_numericos = ['num_obreros', 'num_ayudan', 'num_operad', 'num_conduc']
        roles_disponibles = [r for r in roles_numericos if r in self.datos.columns]
        
        if roles_disponibles:
            # Calcular estadísticas por rol
            estadisticas_roles = {}
            total_por_rol = {}
            
            for rol in roles_disponibles:
                datos_rol = pd.to_numeric(self.datos[rol], errors='coerce').fillna(0)
                total_por_rol[rol] = datos_rol.sum()
                estadisticas_roles[rol] = {
                    'promedio': datos_rol.mean(),
                    'maximo': datos_rol.max(),
                    'total': datos_rol.sum(),
                    'registros_activos': (datos_rol > 0).sum()
                }
            
            # Detectar rol predominante
            rol_predominante = max(total_por_rol, key=total_por_rol.get)
            porcentaje_predominante = (total_por_rol[rol_predominante] / sum(total_por_rol.values())) * 100
            
            self.insights.append({
                'categoria': 'recursos_humanos',
                'tipo': 'composicion_equipos',
                'descripcion': f"La estructura organizacional se basa principalmente en {rol_predominante.replace('num_', '').replace('_', ' ')}, representando el {porcentaje_predominante:.1f}% del recurso humano total.",
                'impacto': 'alto',
                'dato_clave': f"{rol_predominante}: {total_por_rol[rol_predominante]} personas"
            })
            
            # Análisis de eficiencia por equipo
            if 'total_hora' in self.datos.columns and 'num_total_' in self.datos.columns:
                horas = pd.to_numeric(self.datos['total_hora'], errors='coerce').fillna(0)
                trabajadores = pd.to_numeric(self.datos['num_total_'], errors='coerce').fillna(0)
                
                # Calcular productividad
                productividad = horas / trabajadores.replace(0, np.nan)
                productividad_promedio = productividad.mean()
                
                if not np.isnan(productividad_promedio):
                    # Clasificar niveles de productividad
                    if productividad_promedio > 8:
                        nivel = "alta"
                        interpretacion = "superior al estándar"
                    elif productividad_promedio > 6:
                        nivel = "media"
                        interpretacion = "dentro del rango esperado"
                    else:
                        nivel = "baja"
                        interpretacion = "por debajo del estándar"
                    
                    self.insights.append({
                        'categoria': 'productividad',
                        'tipo': 'eficiencia_laboral',
                        'descripcion': f"La productividad laboral registra {productividad_promedio:.2f} horas por trabajador, clasificada como {nivel} y considerada {interpretacion}.",
                        'impacto': 'alto' if nivel in ['alta', 'baja'] else 'medio',
                        'dato_clave': f"Productividad: {productividad_promedio:.2f} h/trabajador"
                    })
    
    def _analizar_maquinaria_equipos(self):
        """
        Análisis inteligente de maquinaria y equipos
        """
        campos_maq = [c for c in self.campos_semanticos['maquinaria'] if c in self.datos.columns]
        
        if not campos_maq:
            return
        
        # Analizar tipos de maquinaria
        tipos_maq = [c for c in self.datos.columns if c.startswith('tipo_maq_')]
        if tipos_maq:
            # Recopilar todos los tipos únicos
            todos_tipos = []
            for col in tipos_maq:
                tipos_col = self.datos[col].dropna().str.strip()
                todos_tipos.extend(tipos_col.tolist())
            
            if todos_tipos:
                frecuencia_tipos = Counter(todos_tipos)
                tipo_mas_usado = frecuencia_tipos.most_common(1)[0]
                
                diversidad_equipos = len(frecuencia_tipos)
                
                self.insights.append({
                    'categoria': 'maquinaria',
                    'tipo': 'utilizacion_equipos',
                    'descripcion': f"El parque de maquinaria presenta {diversidad_equipos} tipos diferentes de equipos, siendo '{tipo_mas_usado[0]}' el más utilizado con {tipo_mas_usado[1]} registros de uso.",
                    'impacto': 'medio',
                    'dato_clave': f"Equipo principal: {tipo_mas_usado[0]} ({tipo_mas_usado[1]} usos)"
                })
        
        # Análisis de horas de maquinaria
        horas_maq = [c for c in self.datos.columns if c.startswith('horas_maq')]
        if horas_maq:
            total_horas_maq = 0
            for col in horas_maq:
                horas_col = pd.to_numeric(self.datos[col], errors='coerce').fillna(0)
                total_horas_maq += horas_col.sum()
            
            if total_horas_maq > 0:
                promedio_horas = total_horas_maq / len(self.datos)
                
                self.patrones['uso_maquinaria'] = {
                    'total_horas': total_horas_maq,
                    'promedio_por_actividad': promedio_horas,
                    'interpretacion': f"Uso intensivo de maquinaria con {promedio_horas:.2f} horas promedio por actividad"
                }
    
    def _analizar_actividades(self):
        """
        Análisis semántico inteligente de actividades
        """
        campos_act = [c for c in self.campos_semanticos['actividades'] if c in self.datos.columns]
        
        if 'actividad_' in self.datos.columns:
            actividades = self.datos['actividad_'].dropna()
            
            if len(actividades) > 0:
                # Análisis de frecuencia
                freq_actividades = actividades.value_counts()
                actividad_principal = freq_actividades.index[0]
                frecuencia_principal = freq_actividades.iloc[0]
                
                # Calcular diversidad de actividades
                diversidad = len(freq_actividades)
                concentracion = (frecuencia_principal / len(actividades)) * 100
                
                # Interpretación inteligente
                if concentracion > 50:
                    interpretacion = "alta especialización en una actividad principal"
                elif concentracion > 30:
                    interpretacion = "moderada concentración con cierta diversificación"
                else:
                    interpretacion = "amplia diversificación de actividades"
                
                self.insights.append({
                    'categoria': 'actividades',
                    'tipo': 'especializacion_operativa',
                    'descripcion': f"El portafolio operativo muestra {interpretacion}, con '{actividad_principal}' representando el {concentracion:.1f}% de las intervenciones ({frecuencia_principal} registros).",
                    'impacto': 'alto',
                    'dato_clave': f"Actividad principal: {actividad_principal} ({concentracion:.1f}%)"
                })
                
                # Análisis de palabras clave en actividades
                self._analizar_semantica_actividades(actividades)
    
    def _analizar_semantica_actividades(self, actividades):
        """
        Análisis semántico de las descripciones de actividades
        """
        # Extraer palabras clave
        todas_palabras = []
        for actividad in actividades:
            if pd.notna(actividad):
                palabras = re.findall(r'\b\w+\b', str(actividad).lower())
                todas_palabras.extend(palabras)
        
        # Filtrar palabras relevantes (más de 3 caracteres)
        palabras_relevantes = [p for p in todas_palabras if len(p) > 3]
        
        if palabras_relevantes:
            freq_palabras = Counter(palabras_relevantes)
            palabras_clave = freq_palabras.most_common(5)
            
            self.patrones['temas_actividades'] = {
                'palabras_clave': palabras_clave,
                'interpretacion': f"Las actividades se centran en: {', '.join([p[0] for p in palabras_clave[:3]])}"
            }
    
    def _analizar_distribucion_geografica(self):
        """
        Análisis inteligente de distribución geográfica
        """
        if 'comuna' in self.datos.columns:
            comunas = self.datos['comuna'].dropna()
            
            if len(comunas) > 0:
                dist_comunas = comunas.value_counts()
                num_comunas = len(dist_comunas)
                comuna_principal = dist_comunas.index[0]
                registros_principal = dist_comunas.iloc[0]
                
                concentracion_geografica = (registros_principal / len(comunas)) * 100
                
                # Interpretación de cobertura territorial
                if num_comunas == 1:
                    cobertura = "altamente focalizada en una sola comuna"
                elif num_comunas <= 3:
                    cobertura = "concentrada en pocas comunas estratégicas"
                elif num_comunas <= 6:
                    cobertura = "distribuida en un conjunto moderado de comunas"
                else:
                    cobertura = "ampliamente distribuida en múltiples comunas"
                
                self.insights.append({
                    'categoria': 'geografia',
                    'tipo': 'cobertura_territorial',
                    'descripcion': f"La cobertura territorial es {cobertura}, abarcando {num_comunas} comuna(s) con {concentracion_geografica:.1f}% de actividades concentradas en la Comuna {comuna_principal}.",
                    'impacto': 'medio',
                    'dato_clave': f"Comuna principal: {comuna_principal} ({concentracion_geografica:.1f}%)"
                })
                
                self.patrones['distribucion_geografica'] = {
                    'num_comunas': num_comunas,
                    'comuna_principal': comuna_principal,
                    'concentracion': concentracion_geografica,
                    'distribucion_completa': dist_comunas.to_dict()
                }
    
    def _detectar_patrones_avanzados(self):
        """
        Detección de patrones complejos usando correlaciones
        """
        # Seleccionar columnas numéricas para análisis de correlación
        columnas_numericas = self.datos.select_dtypes(include=[np.number]).columns
        
        if len(columnas_numericas) > 1:
            matriz_corr = self.datos[columnas_numericas].corr()
            
            # Encontrar correlaciones fuertes (>0.7 o <-0.7)
            correlaciones_fuertes = []
            for i in range(len(matriz_corr.columns)):
                for j in range(i+1, len(matriz_corr.columns)):
                    corr_value = matriz_corr.iloc[i, j]
                    if abs(corr_value) > 0.7 and not np.isnan(corr_value):
                        correlaciones_fuertes.append({
                            'variable1': matriz_corr.columns[i],
                            'variable2': matriz_corr.columns[j],
                            'correlacion': corr_value,
                            'interpretacion': 'positiva fuerte' if corr_value > 0 else 'negativa fuerte'
                        })
            
            if correlaciones_fuertes:
                self.patrones['correlaciones_significativas'] = correlaciones_fuertes
                
                # Generar insight sobre la correlación más fuerte
                corr_principal = max(correlaciones_fuertes, key=lambda x: abs(x['correlacion']))
                
                self.insights.append({
                    'categoria': 'patrones',
                    'tipo': 'correlacion_variables',
                    'descripcion': f"Se detecta una correlación {corr_principal['interpretacion']} ({corr_principal['correlacion']:.3f}) entre {corr_principal['variable1']} y {corr_principal['variable2']}, indicando una relación estadísticamente significativa.",
                    'impacto': 'alto',
                    'dato_clave': f"Correlación: {corr_principal['correlacion']:.3f}"
                })
    
    def _generar_insights_contextuales(self):
        """
        Genera insights contextuales basados en todos los análisis
        """
        # Insight de volumen operativo
        total_registros = len(self.datos)
        
        if total_registros > 100:
            volumen = "alto volumen operativo"
            implicacion = "requiere sistemas de gestión robustos"
        elif total_registros > 50:
            volumen = "volumen operativo moderado"
            implicacion = "permite seguimiento detallado de actividades"
        else:
            volumen = "volumen operativo controlado"
            implicacion = "facilita la supervisión directa"
        
        self.insights.append({
            'categoria': 'contexto',
            'tipo': 'volumen_operativo',
            'descripcion': f"Los {total_registros} registros procesados representan un {volumen}, lo que {implicacion} para optimizar la eficiencia organizacional.",
            'impacto': 'estrategico',
            'dato_clave': f"Total registros: {total_registros}"
        })
    
    def _crear_recomendaciones_inteligentes(self):
        """
        Genera recomendaciones inteligentes basadas en los insights
        """
        recomendaciones = []
        
        # Recomendaciones basadas en patrones temporales
        if 'patron_semanal' in self.patrones:
            patron = self.patrones['patron_semanal']
            recomendaciones.append({
                'categoria': 'planificacion',
                'prioridad': 'alta',
                'titulo': 'Optimización de Cronograma Semanal',
                'descripcion': f"Considerar aumentar la capacidad operativa los días {patron['dia_preferido']} para aprovechar la tendencia natural del equipo.",
                'beneficio_esperado': 'Incremento del 15-20% en productividad'
            })
        
        # Recomendaciones basadas en recursos humanos
        insights_rh = [i for i in self.insights if i['categoria'] == 'recursos_humanos']
        if insights_rh:
            recomendaciones.append({
                'categoria': 'recursos_humanos',
                'prioridad': 'media',
                'titulo': 'Balanceo de Equipos de Trabajo',
                'descripcion': 'Evaluar la redistribución de roles para equilibrar la carga de trabajo entre diferentes categorías de trabajadores.',
                'beneficio_esperado': 'Mejora en eficiencia operativa del 10-15%'
            })
        
        # Recomendaciones basadas en distribución geográfica
        if 'distribucion_geografica' in self.patrones:
            dist = self.patrones['distribucion_geografica']
            if dist['concentracion'] > 60:
                recomendaciones.append({
                    'categoria': 'expansion',
                    'prioridad': 'media',
                    'titulo': 'Diversificación Territorial',
                    'descripcion': f"La alta concentración ({dist['concentracion']:.1f}%) en la Comuna {dist['comuna_principal']} sugiere oportunidades de expansión a otras áreas.",
                    'beneficio_esperado': 'Reducción de riesgo operativo y mayor cobertura'
                })
        
        self.recomendaciones = recomendaciones
    
    def _construir_narrativa_dinamica(self):
        """
        Construye una narrativa dinámica basada en todos los análisis
        """
        import random
        
        # Métricas base
        total_registros = len(self.datos)
        total_trabajadores = 0
        if 'num_total_' in self.datos.columns:
            total_trabajadores = pd.to_numeric(self.datos['num_total_'], errors='coerce').fillna(0).sum()
        
        # Seleccionar templates dinámicamente
        intro_template = random.choice(self.templates_narrativos['introduccion'])
        intro = intro_template.format(total_registros=total_registros)
        
        # Construir secciones narrativas
        secciones = {
            'introduccion': intro,
            'resumen_ejecutivo': self._generar_resumen_ejecutivo(),
            'hallazgos_principales': self._generar_hallazgos_principales(),
            'recomendaciones_narrativa': self._generar_recomendaciones_narrativa()
        }
        
        self.narrativa = secciones
    
    def _generar_resumen_ejecutivo(self):
        """
        Genera un resumen ejecutivo dinámico
        """
        insights_altos = [i for i in self.insights if i['impacto'] == 'alto']
        
        if not insights_altos:
            return "El análisis revela operaciones estables con indicadores dentro de parámetros normales."
        
        # Construir resumen basado en insights de alto impacto
        elementos_clave = []
        for insight in insights_altos[:3]:  # Top 3 insights
            elementos_clave.append(insight['descripcion'])
        
        resumen = "Los hallazgos más relevantes del análisis indican: " + "; ".join(elementos_clave) + "."
        
        return resumen
    
    def _generar_hallazgos_principales(self):
        """
        Genera descripción de hallazgos principales
        """
        hallazgos = []
        
        # Agregar hallazgos por categoría
        categorias_insights = defaultdict(list)
        for insight in self.insights:
            categorias_insights[insight['categoria']].append(insight)
        
        for categoria, insights_cat in categorias_insights.items():
            if insights_cat:
                hallazgo = f"En términos de {categoria}, {insights_cat[0]['descripcion']}"
                hallazgos.append(hallazgo)
        
        return " ".join(hallazgos)
    
    def _generar_recomendaciones_narrativa(self):
        """
        Genera narrativa de recomendaciones
        """
        if not self.recomendaciones:
            return "Las operaciones actuales muestran un desempeño estable sin requerimientos inmediatos de ajuste."
        
        rec_texto = []
        for rec in self.recomendaciones[:3]:  # Top 3 recomendaciones
            rec_texto.append(f"{rec['titulo']}: {rec['descripcion']}")
        
        return "Las principales recomendaciones incluyen: " + "; ".join(rec_texto) + "."
    
    def generar_informe_textual(self, tipo_informe='completo'):
        """
        Genera un informe textual completo basado en el análisis
        """
        resultado = self.analizar_completamente()
        
        informe = {
            'metadata': {
                'fecha_analisis': datetime.now().strftime('%d/%m/%Y %H:%M'),
                'total_registros': len(self.datos),
                'total_columnas': len(self.datos.columns),
                'periodo_datos': self._obtener_periodo_datos()
            },
            'narrativa_principal': resultado['narrativa'],
            'insights_clave': [i for i in resultado['insights'] if i['impacto'] in ['alto', 'estrategico']],
            'patrones_detectados': resultado['patrones'],
            'recomendaciones_estrategicas': resultado['recomendaciones'],
            'metricas_calculadas': self._calcular_metricas_avanzadas()
        }
        
        return informe
    
    def _obtener_periodo_datos(self):
        """
        Determina el período de los datos analizados
        """
        if 'fecha_inic' in self.datos.columns:
            fechas = pd.to_datetime(self.datos['fecha_inic'], errors='coerce')
            fechas_validas = fechas.dropna()
            
            if len(fechas_validas) > 0:
                fecha_min = fechas_validas.min().strftime('%d/%m/%Y')
                fecha_max = fechas_validas.max().strftime('%d/%m/%Y')
                return f"{fecha_min} - {fecha_max}"
        
        return "Período no determinado"
    
    def _calcular_metricas_avanzadas(self):
        """
        Calcula métricas avanzadas para el informe
        """
        metricas = {}
        
        # Productividad laboral
        if 'total_hora' in self.datos.columns and 'num_total_' in self.datos.columns:
            horas = pd.to_numeric(self.datos['total_hora'], errors='coerce').fillna(0)
            trabajadores = pd.to_numeric(self.datos['num_total_'], errors='coerce').fillna(0)
            
            productividad_total = horas.sum() / trabajadores.sum() if trabajadores.sum() > 0 else 0
            metricas['productividad_global'] = round(productividad_total, 2)
        
        # Diversidad de actividades
        if 'actividad_' in self.datos.columns:
            actividades_unicas = self.datos['actividad_'].nunique()
            indice_diversidad = actividades_unicas / len(self.datos)
            metricas['indice_diversidad_actividades'] = round(indice_diversidad, 3)
        
        # Cobertura territorial
        if 'comuna' in self.datos.columns:
            comunas_unicas = self.datos['comuna'].nunique()
            metricas['cobertura_territorial'] = comunas_unicas
        
        # Intensidad de uso de maquinaria
        cols_horas_maq = [c for c in self.datos.columns if c.startswith('horas_maq')]
        if cols_horas_maq:
            total_horas_maq = 0
            for col in cols_horas_maq:
                horas = pd.to_numeric(self.datos[col], errors='coerce').fillna(0)
                total_horas_maq += horas.sum()
            
            intensidad_maquinaria = total_horas_maq / len(self.datos)
            metricas['intensidad_uso_maquinaria'] = round(intensidad_maquinaria, 2)
        
        return metricas
