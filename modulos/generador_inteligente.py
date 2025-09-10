"""
Generador de Informes Inteligentes con Motor de IA y NLP
Utiliza el AnalizadorInteligenteSurvey123 para crear reportes dinámicos
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from io import BytesIO
import tempfile
from .inteligencia_nlp import AnalizadorInteligenteSurvey123

class GeneradorInformeInteligente:
    """
    Generador que crea informes dinámicos usando IA y procesamiento de lenguaje natural
    """
    
    def __init__(self, datos):
        self.datos = datos
        self.analizador_ia = AnalizadorInteligenteSurvey123(datos)
        self.analisis_completo = None
        self.styles = getSampleStyleSheet()
        self._configurar_estilos()
        
    def _configurar_estilos(self):
        """Configura estilos personalizados para el documento"""
        
        # Estilo para títulos principales
        self.styles.add(ParagraphStyle(
            name='TituloInteligente',
            parent=self.styles['Title'],
            fontSize=18,
            spaceAfter=20,
            textColor=colors.HexColor('#2E86AB'),
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Estilo para subtítulos
        self.styles.add(ParagraphStyle(
            name='SubtituloInteligente',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceBefore=15,
            spaceAfter=10,
            textColor=colors.HexColor('#A23B72'),
            fontName='Helvetica-Bold'
        ))
        
        # Estilo para insights importantes
        self.styles.add(ParagraphStyle(
            name='InsightDestacado',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceBefore=8,
            spaceAfter=8,
            leftIndent=20,
            borderColor=colors.HexColor('#F18F01'),
            borderWidth=0.5,
            borderPadding=8,
            backColor=colors.HexColor('#FFF8E1'),
            fontName='Helvetica',
            alignment=TA_JUSTIFY
        ))
        
        # Estilo para texto narrativo
        self.styles.add(ParagraphStyle(
            name='NarrativaIA',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceBefore=6,
            spaceAfter=6,
            alignment=TA_JUSTIFY,
            fontName='Helvetica'
        ))
        
        # Estilo para métricas clave
        self.styles.add(ParagraphStyle(
            name='MetricaClave',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceBefore=5,
            spaceAfter=5,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#2E86AB'),
            fontName='Helvetica-Bold'
        ))
        
        # Estilo para recomendaciones
        self.styles.add(ParagraphStyle(
            name='Recomendacion',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceBefore=8,
            spaceAfter=8,
            leftIndent=15,
            bulletIndent=10,
            fontName='Helvetica'
        ))
    
    def generar_informe_estadistico_inteligente(self, nombre_archivo):
        """
        Genera un informe estadístico con análisis inteligente
        """
        # Ejecutar análisis de IA
        self.analisis_completo = self.analizador_ia.generar_informe_textual('estadistico')
        
        # Crear documento PDF
        doc = SimpleDocTemplate(nombre_archivo, pagesize=A4)
        story = []
        
        # Agregar encabezado
        story.extend(self._crear_encabezado_inteligente("Informe Estadístico Inteligente"))
        
        # Agregar resumen ejecutivo con IA
        story.extend(self._crear_seccion_resumen_ejecutivo())
        
        # Agregar análisis de insights
        story.extend(self._crear_seccion_insights())
        
        # Agregar métricas avanzadas
        story.extend(self._crear_seccion_metricas_avanzadas())
        
        # Agregar análisis temporal inteligente
        story.extend(self._crear_seccion_analisis_temporal())
        
        # Agregar análisis de recursos humanos
        story.extend(self._crear_seccion_recursos_humanos())
        
        # Agregar distribución geográfica
        story.extend(self._crear_seccion_distribucion_geografica())
        
        # Agregar patrones detectados
        story.extend(self._crear_seccion_patrones())
        
        # Agregar recomendaciones inteligentes
        story.extend(self._crear_seccion_recomendaciones())
        
        # Generar PDF
        doc.build(story)
        return nombre_archivo
    
    def generar_informe_detallado_inteligente(self, nombre_archivo):
        """
        Genera un informe detallado con análisis profundo de IA
        """
        # Ejecutar análisis de IA
        self.analisis_completo = self.analizador_ia.generar_informe_textual('detallado')
        
        # Crear documento PDF
        doc = SimpleDocTemplate(nombre_archivo, pagesize=A4)
        story = []
        
        # Agregar encabezado
        story.extend(self._crear_encabezado_inteligente("Informe Detallado con Análisis de IA"))
        
        # Agregar resumen ejecutivo
        story.extend(self._crear_seccion_resumen_ejecutivo())
        
        # Agregar análisis completo de todas las categorías
        story.extend(self._crear_analisis_completo_categorias())
        
        # Agregar correlaciones y patrones avanzados
        story.extend(self._crear_seccion_correlaciones_avanzadas())
        
        # Agregar análisis semántico de actividades
        story.extend(self._crear_seccion_analisis_semantico())
        
        # Agregar proyecciones y tendencias
        story.extend(self._crear_seccion_proyecciones())
        
        # Agregar plan de acción detallado
        story.extend(self._crear_seccion_plan_accion())
        
        # Generar PDF
        doc.build(story)
        return nombre_archivo
    
    def generar_informe_ejecutivo_inteligente(self, nombre_archivo):
        """
        Genera un informe ejecutivo conciso con insights de alto nivel
        """
        # Ejecutar análisis de IA
        self.analisis_completo = self.analizador_ia.generar_informe_textual('ejecutivo')
        
        # Crear documento PDF
        doc = SimpleDocTemplate(nombre_archivo, pagesize=A4)
        story = []
        
        # Agregar encabezado
        story.extend(self._crear_encabezado_inteligente("Informe Ejecutivo - Dashboard Inteligente"))
        
        # Agregar dashboard de métricas clave
        story.extend(self._crear_dashboard_ejecutivo())
        
        # Agregar insights estratégicos
        story.extend(self._crear_insights_estrategicos())
        
        # Agregar indicadores de desempeño
        story.extend(self._crear_indicadores_desempeno())
        
        # Agregar recomendaciones estratégicas
        story.extend(self._crear_recomendaciones_estrategicas())
        
        # Agregar próximos pasos
        story.extend(self._crear_seccion_proximos_pasos())
        
        # Generar PDF
        doc.build(story)
        return nombre_archivo
    
    def _crear_encabezado_inteligente(self, titulo):
        """Crea un encabezado dinámico con información contextual"""
        elements = []
        
        # Logo (si existe)
        logo_path = "static/images/logo_alcaldia.jpg"
        if os.path.exists(logo_path):
            logo = Image(logo_path, width=1*inch, height=0.8*inch)
            elements.append(logo)
            elements.append(Spacer(1, 10))
        
        # Título principal
        elements.append(Paragraph(titulo, self.styles['TituloInteligente']))
        elements.append(Spacer(1, 10))
        
        # Información contextual dinámica
        metadata = self.analisis_completo['metadata']
        info_contextual = f"""
        <b>Análisis Generado por Sistema de Inteligencia Artificial</b><br/>
        Fecha del Análisis: {metadata['fecha_analisis']}<br/>
        Total de Registros Procesados: {metadata['total_registros']}<br/>
        Variables Analizadas: {metadata['total_columnas']}<br/>
        Período de Datos: {metadata['periodo_datos']}
        """
        
        elements.append(Paragraph(info_contextual, self.styles['Normal']))
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _crear_seccion_resumen_ejecutivo(self):
        """Crea la sección de resumen ejecutivo con narrativa de IA"""
        elements = []
        
        elements.append(Paragraph("Resumen Ejecutivo Inteligente", self.styles['SubtituloInteligente']))
        
        # Obtener narrativa principal de IA
        narrativa = self.analisis_completo['narrativa_principal']
        
        # Introducción
        elements.append(Paragraph(narrativa['introduccion'], self.styles['NarrativaIA']))
        elements.append(Spacer(1, 10))
        
        # Resumen ejecutivo
        if 'resumen_ejecutivo' in narrativa:
            elements.append(Paragraph(narrativa['resumen_ejecutivo'], self.styles['InsightDestacado']))
        
        elements.append(Spacer(1, 15))
        
        return elements
    
    def _crear_seccion_insights(self):
        """Crea la sección de insights clave generados por IA"""
        elements = []
        
        elements.append(Paragraph("Insights Clave Identificados por IA", self.styles['SubtituloInteligente']))
        
        insights_clave = self.analisis_completo['insights_clave']
        
        for i, insight in enumerate(insights_clave[:5], 1):  # Top 5 insights
            insight_text = f"""
            <b>Insight {i} - {insight['tipo'].replace('_', ' ').title()}</b><br/>
            {insight['descripcion']}<br/>
            <i>Dato Clave: {insight['dato_clave']}</i>
            """
            elements.append(Paragraph(insight_text, self.styles['InsightDestacado']))
            elements.append(Spacer(1, 8))
        
        return elements
    
    def _crear_seccion_metricas_avanzadas(self):
        """Crea tabla con métricas avanzadas calculadas por IA"""
        elements = []
        
        elements.append(Paragraph("Métricas Avanzadas Calculadas", self.styles['SubtituloInteligente']))
        
        metricas = self.analisis_completo['metricas_calculadas']
        
        if metricas:
            # Crear tabla de métricas
            data = [['Métrica', 'Valor', 'Interpretación']]
            
            for metrica, valor in metricas.items():
                interpretacion = self._interpretar_metrica(metrica, valor)
                data.append([
                    metrica.replace('_', ' ').title(),
                    str(valor),
                    interpretacion
                ])
            
            table = Table(data, colWidths=[2.5*inch, 1*inch, 2.5*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(table)
        
        elements.append(Spacer(1, 15))
        
        return elements
    
    def _interpretar_metrica(self, metrica, valor):
        """Interpreta dinámicamente las métricas"""
        interpretaciones = {
            'productividad_global': f"{'Alta' if valor > 8 else 'Media' if valor > 6 else 'Baja'} productividad",
            'indice_diversidad_actividades': f"{'Alta' if valor > 0.5 else 'Media' if valor > 0.3 else 'Baja'} diversidad",
            'cobertura_territorial': f"Abarca {valor} comuna{'s' if valor != 1 else ''}",
            'intensidad_uso_maquinaria': f"{'Alto' if valor > 10 else 'Moderado' if valor > 5 else 'Bajo'} uso de equipos"
        }
        
        return interpretaciones.get(metrica, "Métrica calculada")
    
    def _crear_seccion_analisis_temporal(self):
        """Análisis temporal inteligente"""
        elements = []
        
        elements.append(Paragraph("Análisis Temporal Inteligente", self.styles['SubtituloInteligente']))
        
        # Buscar patrones temporales en los insights
        insights_temporales = [i for i in self.analisis_completo['insights_clave'] 
                             if i['categoria'] == 'temporal']
        
        if insights_temporales:
            for insight in insights_temporales:
                elements.append(Paragraph(insight['descripcion'], self.styles['NarrativaIA']))
                elements.append(Spacer(1, 8))
        else:
            elements.append(Paragraph(
                "Los datos analizados muestran una distribución temporal estable sin patrones significativos que requieran atención especial.",
                self.styles['NarrativaIA']
            ))
        
        elements.append(Spacer(1, 15))
        
        return elements
    
    def _crear_seccion_recursos_humanos(self):
        """Análisis inteligente de recursos humanos"""
        elements = []
        
        elements.append(Paragraph("Análisis de Recursos Humanos", self.styles['SubtituloInteligente']))
        
        # Buscar insights de recursos humanos
        insights_rh = [i for i in self.analisis_completo['insights_clave'] 
                      if i['categoria'] in ['recursos_humanos', 'productividad']]
        
        for insight in insights_rh:
            elements.append(Paragraph(insight['descripcion'], self.styles['NarrativaIA']))
            elements.append(Spacer(1, 8))
        
        elements.append(Spacer(1, 15))
        
        return elements
    
    def _crear_seccion_distribucion_geografica(self):
        """Análisis de distribución geográfica"""
        elements = []
        
        elements.append(Paragraph("Distribución Geográfica", self.styles['SubtituloInteligente']))
        
        # Buscar insights geográficos
        insights_geo = [i for i in self.analisis_completo['insights_clave'] 
                       if i['categoria'] == 'geografia']
        
        for insight in insights_geo:
            elements.append(Paragraph(insight['descripcion'], self.styles['NarrativaIA']))
            elements.append(Spacer(1, 8))
        
        # Agregar información de patrones geográficos si existe
        patrones = self.analisis_completo['patrones_detectados']
        if 'distribucion_geografica' in patrones:
            dist_geo = patrones['distribucion_geografica']
            comunas_text = f"""
            <b>Distribución Detallada:</b><br/>
            • Total de comunas atendidas: {dist_geo['num_comunas']}<br/>
            • Comuna principal: {dist_geo['comuna_principal']}<br/>
            • Concentración: {dist_geo['concentracion']:.1f}%
            """
            elements.append(Paragraph(comunas_text, self.styles['NarrativaIA']))
        
        elements.append(Spacer(1, 15))
        
        return elements
    
    def _crear_seccion_patrones(self):
        """Sección de patrones detectados por IA"""
        elements = []
        
        elements.append(Paragraph("Patrones Detectados por IA", self.styles['SubtituloInteligente']))
        
        patrones = self.analisis_completo['patrones_detectados']
        
        # Mostrar correlaciones significativas
        if 'correlaciones_significativas' in patrones:
            elements.append(Paragraph("<b>Correlaciones Estadísticamente Significativas:</b>", self.styles['Normal']))
            
            for corr in patrones['correlaciones_significativas'][:3]:  # Top 3
                corr_text = f"• {corr['variable1']} y {corr['variable2']}: Correlación {corr['interpretacion']} ({corr['correlacion']:.3f})"
                elements.append(Paragraph(corr_text, self.styles['NarrativaIA']))
        
        # Mostrar otros patrones
        for patron_key, patron_data in patrones.items():
            if patron_key != 'correlaciones_significativas' and isinstance(patron_data, dict):
                if 'interpretacion' in patron_data:
                    elements.append(Paragraph(f"<b>{patron_key.replace('_', ' ').title()}:</b> {patron_data['interpretacion']}", self.styles['NarrativaIA']))
                    elements.append(Spacer(1, 5))
        
        elements.append(Spacer(1, 15))
        
        return elements
    
    def _crear_seccion_recomendaciones(self):
        """Sección de recomendaciones generadas por IA"""
        elements = []
        
        elements.append(Paragraph("Recomendaciones Inteligentes", self.styles['SubtituloInteligente']))
        
        recomendaciones = self.analisis_completo['recomendaciones_estrategicas']
        
        for i, rec in enumerate(recomendaciones, 1):
            rec_text = f"""
            <b>{i}. {rec['titulo']}</b> (Prioridad: {rec['prioridad']})<br/>
            {rec['descripcion']}<br/>
            <i>Beneficio Esperado: {rec['beneficio_esperado']}</i>
            """
            elements.append(Paragraph(rec_text, self.styles['Recomendacion']))
            elements.append(Spacer(1, 10))
        
        return elements
    
    def _crear_analisis_completo_categorias(self):
        """Análisis completo de todas las categorías para informe detallado"""
        elements = []
        
        elements.append(Paragraph("Análisis Completo por Categorías", self.styles['SubtituloInteligente']))
        
        # Agrupar insights por categoría
        insights_por_categoria = {}
        for insight in self.analisis_completo['insights_clave']:
            categoria = insight['categoria']
            if categoria not in insights_por_categoria:
                insights_por_categoria[categoria] = []
            insights_por_categoria[categoria].append(insight)
        
        # Crear sección por cada categoría
        for categoria, insights in insights_por_categoria.items():
            elements.append(Paragraph(f"Categoría: {categoria.replace('_', ' ').title()}", self.styles['Heading3']))
            
            for insight in insights:
                elements.append(Paragraph(f"• {insight['descripcion']}", self.styles['NarrativaIA']))
                elements.append(Spacer(1, 5))
            
            elements.append(Spacer(1, 10))
        
        return elements
    
    def _crear_seccion_correlaciones_avanzadas(self):
        """Análisis avanzado de correlaciones"""
        elements = []
        
        elements.append(Paragraph("Análisis de Correlaciones Avanzadas", self.styles['SubtituloInteligente']))
        
        patrones = self.analisis_completo['patrones_detectados']
        
        if 'correlaciones_significativas' in patrones:
            correlaciones = patrones['correlaciones_significativas']
            
            # Crear tabla detallada de correlaciones
            data = [['Variable 1', 'Variable 2', 'Coeficiente', 'Interpretación', 'Significancia']]
            
            for corr in correlaciones:
                significancia = 'Muy Alta' if abs(corr['correlacion']) > 0.8 else 'Alta'
                data.append([
                    corr['variable1'],
                    corr['variable2'],
                    f"{corr['correlacion']:.3f}",
                    corr['interpretacion'],
                    significancia
                ])
            
            table = Table(data, colWidths=[1.5*inch, 1.5*inch, 1*inch, 1.5*inch, 1*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#A23B72')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(table)
        
        elements.append(Spacer(1, 15))
        
        return elements
    
    def _crear_seccion_analisis_semantico(self):
        """Análisis semántico de actividades"""
        elements = []
        
        elements.append(Paragraph("Análisis Semántico de Actividades", self.styles['SubtituloInteligente']))
        
        patrones = self.analisis_completo['patrones_detectados']
        
        if 'temas_actividades' in patrones:
            temas = patrones['temas_actividades']
            
            elements.append(Paragraph("<b>Palabras Clave Identificadas:</b>", self.styles['Normal']))
            
            for palabra, frecuencia in temas['palabras_clave']:
                elements.append(Paragraph(f"• {palabra}: {frecuencia} ocurrencias", self.styles['NarrativaIA']))
            
            elements.append(Spacer(1, 10))
            elements.append(Paragraph(f"<b>Interpretación:</b> {temas['interpretacion']}", self.styles['NarrativaIA']))
        
        elements.append(Spacer(1, 15))
        
        return elements
    
    def _crear_seccion_proyecciones(self):
        """Sección de proyecciones y tendencias"""
        elements = []
        
        elements.append(Paragraph("Proyecciones y Tendencias", self.styles['SubtituloInteligente']))
        
        # Análisis predictivo basado en patrones actuales
        total_registros = self.analisis_completo['metadata']['total_registros']
        
        proyeccion_text = f"""
        <b>Análisis Predictivo:</b><br/>
        Basado en los {total_registros} registros analizados y los patrones identificados, 
        se proyecta un comportamiento estable en las operaciones con oportunidades de 
        optimización en las áreas identificadas por el análisis de correlaciones.
        """
        
        elements.append(Paragraph(proyeccion_text, self.styles['NarrativaIA']))
        elements.append(Spacer(1, 15))
        
        return elements
    
    def _crear_seccion_plan_accion(self):
        """Plan de acción detallado"""
        elements = []
        
        elements.append(Paragraph("Plan de Acción Detallado", self.styles['SubtituloInteligente']))
        
        recomendaciones = self.analisis_completo['recomendaciones_estrategicas']
        
        # Agrupar por prioridad
        alta_prioridad = [r for r in recomendaciones if r['prioridad'] == 'alta']
        media_prioridad = [r for r in recomendaciones if r['prioridad'] == 'media']
        
        if alta_prioridad:
            elements.append(Paragraph("<b>Acciones de Alta Prioridad (Implementación Inmediata):</b>", self.styles['Normal']))
            for i, rec in enumerate(alta_prioridad, 1):
                elements.append(Paragraph(f"{i}. {rec['titulo']}: {rec['descripcion']}", self.styles['Recomendacion']))
        
        if media_prioridad:
            elements.append(Paragraph("<b>Acciones de Media Prioridad (Implementación a 3-6 meses):</b>", self.styles['Normal']))
            for i, rec in enumerate(media_prioridad, 1):
                elements.append(Paragraph(f"{i}. {rec['titulo']}: {rec['descripcion']}", self.styles['Recomendacion']))
        
        elements.append(Spacer(1, 15))
        
        return elements
    
    def _crear_dashboard_ejecutivo(self):
        """Dashboard de métricas para informe ejecutivo"""
        elements = []
        
        elements.append(Paragraph("Dashboard de Métricas Ejecutivas", self.styles['SubtituloInteligente']))
        
        metadata = self.analisis_completo['metadata']
        metricas = self.analisis_completo['metricas_calculadas']
        
        # Crear grid de métricas clave
        metricas_texto = f"""
        <table>
        <tr>
            <td><b>Total Registros:</b> {metadata['total_registros']}</td>
            <td><b>Variables Analizadas:</b> {metadata['total_columnas']}</td>
        </tr>
        <tr>
            <td><b>Período:</b> {metadata['periodo_datos']}</td>
            <td><b>Fecha Análisis:</b> {metadata['fecha_analisis']}</td>
        </tr>
        </table>
        """
        
        elements.append(Paragraph(metricas_texto, self.styles['Normal']))
        elements.append(Spacer(1, 15))
        
        return elements
    
    def _crear_insights_estrategicos(self):
        """Insights estratégicos para ejecutivos"""
        elements = []
        
        elements.append(Paragraph("Insights Estratégicos", self.styles['SubtituloInteligente']))
        
        # Filtrar solo insights de alto impacto estratégico
        insights_estrategicos = [i for i in self.analisis_completo['insights_clave'] 
                               if i['impacto'] in ['alto', 'estrategico']]
        
        for insight in insights_estrategicos[:3]:  # Top 3 para ejecutivos
            elements.append(Paragraph(f"• {insight['descripcion']}", self.styles['InsightDestacado']))
            elements.append(Spacer(1, 8))
        
        return elements
    
    def _crear_indicadores_desempeno(self):
        """Indicadores de desempeño clave"""
        elements = []
        
        elements.append(Paragraph("Indicadores de Desempeño Clave (KPIs)", self.styles['SubtituloInteligente']))
        
        metricas = self.analisis_completo['metricas_calculadas']
        
        # Crear tabla de KPIs
        data = [['Indicador', 'Valor Actual', 'Estado']]
        
        for metrica, valor in metricas.items():
            estado = self._evaluar_estado_kpi(metrica, valor)
            data.append([
                metrica.replace('_', ' ').title(),
                str(valor),
                estado
            ])
        
        if len(data) > 1:
            table = Table(data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(table)
        
        elements.append(Spacer(1, 15))
        
        return elements
    
    def _evaluar_estado_kpi(self, metrica, valor):
        """Evalúa el estado de un KPI"""
        if 'productividad' in metrica:
            return '🟢 Óptimo' if valor > 8 else '🟡 Bueno' if valor > 6 else '🔴 Requiere Atención'
        elif 'diversidad' in metrica:
            return '🟢 Alta' if valor > 0.5 else '🟡 Media' if valor > 0.3 else '🔴 Baja'
        elif 'cobertura' in metrica:
            return f'🟢 {valor} Comunas'
        else:
            return '🟡 Monitoreando'
    
    def _crear_recomendaciones_estrategicas(self):
        """Recomendaciones para nivel ejecutivo"""
        elements = []
        
        elements.append(Paragraph("Recomendaciones Estratégicas", self.styles['SubtituloInteligente']))
        
        recomendaciones = self.analisis_completo['recomendaciones_estrategicas']
        
        # Solo mostrar recomendaciones de alta prioridad para ejecutivos
        alta_prioridad = [r for r in recomendaciones if r['prioridad'] == 'alta']
        
        for i, rec in enumerate(alta_prioridad, 1):
            rec_text = f"""
            <b>{i}. {rec['titulo']}</b><br/>
            {rec['descripcion']}<br/>
            <i>ROI Esperado: {rec['beneficio_esperado']}</i>
            """
            elements.append(Paragraph(rec_text, self.styles['Recomendacion']))
            elements.append(Spacer(1, 10))
        
        return elements
    
    def _crear_seccion_proximos_pasos(self):
        """Sección de próximos pasos"""
        elements = []
        
        elements.append(Paragraph("Próximos Pasos Recomendados", self.styles['SubtituloInteligente']))
        
        pasos_text = """
        <b>Cronograma Sugerido de Implementación:</b><br/>
        • Semana 1-2: Revisión de recomendaciones de alta prioridad<br/>
        • Semana 3-4: Implementación de mejoras operativas inmediatas<br/>
        • Mes 2-3: Monitoreo de indicadores de desempeño<br/>
        • Mes 4-6: Evaluación de impacto y ajustes estratégicos<br/><br/>
        
        <b>Seguimiento:</b><br/>
        Se recomienda ejecutar este análisis mensualmente para mantener 
        la optimización continua basada en datos actualizados.
        """
        
        elements.append(Paragraph(pasos_text, self.styles['NarrativaIA']))
        
        return elements
