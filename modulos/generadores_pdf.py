"""
Generadores de informes PDF con formato profesional y contenido inteligente
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO
import pandas as pd
from datetime import datetime
from typing import Dict, Any, List
import os

from .generador_informes import procesar_datos_para_informe, GeneradorProsa


class InformeEstadistico:
    """Generador de informe estadístico con formato profesional"""
    
    def __init__(self, datos: pd.DataFrame):
        self.datos = datos
        self.analisis = procesar_datos_para_informe(datos)
        self.prosa = GeneradorProsa()
        
    def generar_pdf(self) -> BytesIO:
        """Genera el PDF del informe estadístico"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=A4,
            rightMargin=inch * 0.75,
            leftMargin=inch * 0.75,
            topMargin=inch,
            bottomMargin=inch
        )
        
        # Configurar estilos
        styles = self._configurar_estilos()
        story = []
        
        # Portada
        story.extend(self._generar_portada(styles))
        story.append(PageBreak())
        
        # Contenido principal
        story.extend(self._generar_contenido_principal(styles))
        
        # Construir documento
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def _configurar_estilos(self) -> Dict[str, ParagraphStyle]:
        """Configura estilos personalizados para el documento"""
        styles = getSampleStyleSheet()
        
        # Título principal
        styles.add(ParagraphStyle(
            name='TituloPortada',
            parent=styles['Title'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#1e3a8a')
        ))
        
        # Subtítulo
        styles.add(ParagraphStyle(
            name='Subtitulo',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=20,
            textColor=colors.HexColor('#3b82f6'),
            borderWidth=1,
            borderColor=colors.HexColor('#3b82f6'),
            borderPadding=10
        ))
        
        # Texto justificado
        styles.add(ParagraphStyle(
            name='TextoJustificado',
            parent=styles['Normal'],
            alignment=TA_JUSTIFY,
            spaceAfter=12,
            fontSize=11,
            leading=14
        ))
        
        # Encabezado de sección
        styles.add(ParagraphStyle(
            name='EncabezadoSeccion',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=15,
            spaceBefore=20,
            textColor=colors.HexColor('#1f2937'),
            borderWidth=0,
            borderColor=colors.HexColor('#e5e7eb'),
            borderPadding=5
        ))
        
        return styles
    
    def _generar_portada(self, styles) -> List:
        """Genera la portada del documento"""
        portada = []
        
        # Espacio superior
        portada.append(Spacer(1, 2*inch))
        
        # Título principal
        portada.append(Paragraph("INFORME ESTADÍSTICO", styles['TituloPortada']))
        portada.append(Paragraph("SISTEMA SURVEY123", styles['TituloPortada']))
        
        # Información del proyecto
        portada.append(Spacer(1, 1*inch))
        info_proyecto = f"""
        <b>Secretaría de Infraestructura Física</b><br/>
        <b>Alcaldía de Medellín</b><br/><br/>
        <b>Período de análisis:</b> {self.analisis['metadata']['fecha_procesamiento']}<br/>
        <b>Total de registros:</b> {self.analisis['metadata']['total_registros']:,}<br/>
        <b>Columnas analizadas:</b> {self.analisis['metadata']['columnas_analizadas']}
        """
        portada.append(Paragraph(info_proyecto, styles['TextoJustificado']))
        
        # Pie de portada
        portada.append(Spacer(1, 2*inch))
        fecha_actual = datetime.now().strftime('%d de %B de %Y')
        portada.append(Paragraph(f"Medellín, {fecha_actual}", styles['TextoJustificado']))
        
        return portada
    
    def _generar_contenido_principal(self, styles) -> List:
        """Genera el contenido principal del informe"""
        contenido = []
        
        # Introducción
        contenido.append(Paragraph("1. INTRODUCCIÓN", styles['Subtitulo']))
        intro_texto = self.prosa.generar_introduccion('estadistico', self.analisis['metadata']['total_registros'])
        contenido.append(Paragraph(intro_texto, styles['TextoJustificado']))
        contenido.append(Spacer(1, 20))
        
        # Resumen ejecutivo
        contenido.append(Paragraph("2. RESUMEN EJECUTIVO", styles['Subtitulo']))
        contenido.append(Paragraph(self.analisis['resumen_ejecutivo'], styles['TextoJustificado']))
        contenido.append(Spacer(1, 20))
        
        # Análisis de recursos humanos
        if self.analisis['recursos_humanos']:
            contenido.append(Paragraph("3. ANÁLISIS DE RECURSOS HUMANOS", styles['Subtitulo']))
            
            # Métricas clave
            rh = self.analisis['recursos_humanos']
            metricas_rh = [
                ['Métrica', 'Valor'],
                ['Total de trabajadores', f"{rh.get('total_trabajadores', 0):,}"],
                ['Total de horas trabajadas', f"{rh.get('total_horas', 0):,.1f}"],
                ['Promedio trabajadores/actividad', f"{rh.get('promedio_por_actividad', 0):.1f}"],
                ['Horas promedio/trabajador', f"{rh.get('eficiencia_hora_trabajador', 0):.1f}"]
            ]
            
            tabla_rh = Table(metricas_rh, colWidths=[3*inch, 2*inch])
            tabla_rh.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0'))
            ]))
            
            contenido.append(tabla_rh)
            contenido.append(Spacer(1, 15))
            
            # Análisis textual
            texto_rh = self.prosa.generar_seccion_recursos_humanos(rh)
            contenido.append(Paragraph(texto_rh, styles['TextoJustificado']))
            contenido.append(Spacer(1, 20))
        
        # Análisis geográfico
        if self.analisis['geografico']:
            contenido.append(Paragraph("4. ANÁLISIS GEOGRÁFICO Y TERRITORIAL", styles['Subtitulo']))
            
            geo = self.analisis['geografico']
            
            # Tabla de distribución geográfica
            metricas_geo = [['Aspecto Geográfico', 'Valor']]
            
            if 'puntos_unicos' in geo:
                metricas_geo.append(['Puntos de intervención únicos', f"{geo['puntos_unicos']:,}"])
            if 'concentracion' in geo:
                metricas_geo.append(['Concentración promedio', f"{geo['concentracion']:.1f} actividades/punto"])
            if 'centro_lat' in geo and 'centro_lon' in geo:
                metricas_geo.append(['Centro geográfico', f"{geo['centro_lat']:.6f}, {geo['centro_lon']:.6f}"])
            
            if len(metricas_geo) > 1:
                tabla_geo = Table(metricas_geo, colWidths=[3*inch, 2*inch])
                tabla_geo.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0fdf4')),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bbf7d0'))
                ]))
                contenido.append(tabla_geo)
                contenido.append(Spacer(1, 15))
            
            # Estados de obra
            if 'distribucion_estados' in geo:
                contenido.append(Paragraph("4.1 Distribución por Estado de Obra", styles['EncabezadoSeccion']))
                
                estados_data = [['Estado de Obra', 'Cantidad', 'Porcentaje']]
                total_registros = sum(geo['distribucion_estados'].values())
                
                for estado, cantidad in geo['distribucion_estados'].items():
                    porcentaje = (cantidad / total_registros) * 100
                    estados_data.append([estado, str(cantidad), f"{porcentaje:.1f}%"])
                
                tabla_estados = Table(estados_data, colWidths=[2.5*inch, 1*inch, 1*inch])
                tabla_estados.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8b5cf6')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 11),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#faf5ff')),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#c4b5fd'))
                ]))
                contenido.append(tabla_estados)
                contenido.append(Spacer(1, 15))
            
            # Análisis textual geográfico
            texto_geo = self.prosa.generar_seccion_geografica(geo)
            contenido.append(Paragraph(texto_geo, styles['TextoJustificado']))
            contenido.append(Spacer(1, 20))
        
        # Insights y recomendaciones
        if self.analisis['insights'] or self.analisis['recomendaciones']:
            contenido.append(Paragraph("5. INSIGHTS Y RECOMENDACIONES", styles['Subtitulo']))
            
            if self.analisis['insights']:
                contenido.append(Paragraph("5.1 Hallazgos Principales", styles['EncabezadoSeccion']))
                for i, insight in enumerate(self.analisis['insights'][:5], 1):
                    contenido.append(Paragraph(f"• {insight}", styles['TextoJustificado']))
                contenido.append(Spacer(1, 15))
            
            if self.analisis['recomendaciones']:
                contenido.append(Paragraph("5.2 Recomendaciones Estratégicas", styles['EncabezadoSeccion']))
                for i, recomendacion in enumerate(self.analisis['recomendaciones'][:5], 1):
                    contenido.append(Paragraph(f"• {recomendacion}", styles['TextoJustificado']))
        
        return contenido


class InformeDetallado:
    """Generador de informe detallado con análisis exhaustivo"""
    
    def __init__(self, datos: pd.DataFrame):
        self.datos = datos
        self.analisis = procesar_datos_para_informe(datos)
        self.prosa = GeneradorProsa()
        
    def generar_pdf(self) -> BytesIO:
        """Genera el PDF del informe detallado"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=A4,
            rightMargin=inch * 0.75,
            leftMargin=inch * 0.75,
            topMargin=inch,
            bottomMargin=inch
        )
        
        styles = self._configurar_estilos()
        story = []
        
        # Portada
        story.extend(self._generar_portada(styles))
        story.append(PageBreak())
        
        # Tabla de contenidos
        story.extend(self._generar_tabla_contenidos(styles))
        story.append(PageBreak())
        
        # Contenido detallado
        story.extend(self._generar_contenido_detallado(styles))
        
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def _configurar_estilos(self):
        """Configura estilos para el informe detallado"""
        styles = getSampleStyleSheet()
        
        styles.add(ParagraphStyle(
            name='TituloDetallado',
            parent=styles['Title'],
            fontSize=22,
            spaceAfter=25,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#1f2937')
        ))
        
        styles.add(ParagraphStyle(
            name='SeccionPrincipal',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=15,
            spaceBefore=25,
            textColor=colors.HexColor('#374151'),
            borderWidth=2,
            borderColor=colors.HexColor('#6b7280'),
            borderPadding=8
        ))
        
        styles.add(ParagraphStyle(
            name='SubseccionDetallada',
            parent=styles['Heading2'],
            fontSize=13,
            spaceAfter=10,
            spaceBefore=15,
            textColor=colors.HexColor('#4b5563')
        ))
        
        styles.add(ParagraphStyle(
            name='CuerpoDetallado',
            parent=styles['Normal'],
            alignment=TA_JUSTIFY,
            spaceAfter=10,
            fontSize=10,
            leading=13
        ))
        
        return styles
    
    def _generar_portada(self, styles) -> List:
        """Genera portada del informe detallado"""
        portada = []
        
        portada.append(Spacer(1, 1.5*inch))
        portada.append(Paragraph("INFORME DETALLADO", styles['TituloDetallado']))
        portada.append(Paragraph("ANÁLISIS INTEGRAL SURVEY123", styles['TituloDetallado']))
        
        portada.append(Spacer(1, 0.8*inch))
        
        info_detallada = f"""
        <b>SECRETARÍA DE INFRAESTRUCTURA FÍSICA</b><br/>
        <b>ALCALDÍA DE MEDELLÍN</b><br/><br/>
        
        <b>CARACTERÍSTICAS DEL ANÁLISIS:</b><br/>
        • Total de registros procesados: {self.analisis['metadata']['total_registros']:,}<br/>
        • Variables analizadas: {self.analisis['metadata']['columnas_analizadas']}<br/>
        • Fecha de procesamiento: {self.analisis['metadata']['fecha_procesamiento']}<br/>
        • Tipo de análisis: Exhaustivo y multidimensional<br/><br/>
        
        <b>ALCANCE DEL DOCUMENTO:</b><br/>
        Este informe proporciona un análisis integral y detallado de todas las dimensiones 
        identificadas en los datos del proyecto, incluyendo análisis temporal, distribución 
        de recursos, caracterización geográfica y evaluación de eficiencia operacional.
        """
        
        portada.append(Paragraph(info_detallada, styles['CuerpoDetallado']))
        
        return portada
    
    def _generar_tabla_contenidos(self, styles) -> List:
        """Genera tabla de contenidos"""
        contenidos = []
        
        contenidos.append(Paragraph("TABLA DE CONTENIDOS", styles['SeccionPrincipal']))
        contenidos.append(Spacer(1, 20))
        
        indices = [
            "1. RESUMEN EJECUTIVO DEL PROYECTO",
            "2. METODOLOGÍA DE ANÁLISIS",
            "3. ANÁLISIS TEMPORAL DETALLADO", 
            "4. EVALUACIÓN INTEGRAL DE RECURSOS HUMANOS",
            "5. CARACTERIZACIÓN GEOGRÁFICA Y TERRITORIAL",
            "6. ANÁLISIS DE TIPOS DE ACTIVIDADES",
            "7. INDICADORES DE EFICIENCIA Y PRODUCTIVIDAD",
            "8. INSIGHTS Y HALLAZGOS SIGNIFICATIVOS",
            "9. RECOMENDACIONES ESTRATÉGICAS",
            "10. CONCLUSIONES Y PRÓXIMOS PASOS"
        ]
        
        for indice in indices:
            contenidos.append(Paragraph(indice, styles['CuerpoDetallado']))
            contenidos.append(Spacer(1, 8))
        
        return contenidos
    
    def _generar_contenido_detallado(self, styles) -> List:
        """Genera el contenido detallado completo"""
        contenido = []
        
        # 1. Resumen ejecutivo
        contenido.append(Paragraph("1. RESUMEN EJECUTIVO DEL PROYECTO", styles['SeccionPrincipal']))
        contenido.append(Paragraph(self.analisis['resumen_ejecutivo'], styles['CuerpoDetallado']))
        contenido.append(Spacer(1, 20))
        
        # 2. Metodología
        contenido.append(Paragraph("2. METODOLOGÍA DE ANÁLISIS", styles['SeccionPrincipal']))
        metodologia = f"""
        El presente análisis se fundamenta en el procesamiento sistemático de {self.analisis['metadata']['total_registros']:,} 
        registros de actividades, aplicando técnicas de análisis estadístico descriptivo, identificación de patrones 
        temporales y evaluación de indicadores de eficiencia. La metodología incluye:
        
        • Análisis de completitud y calidad de datos
        • Evaluación de distribuciones estadísticas
        • Identificación de tendencias temporales
        • Cálculo de indicadores de eficiencia operacional
        • Análisis de correlaciones entre variables clave
        • Generación automática de insights mediante algoritmos de procesamiento de lenguaje natural
        """
        contenido.append(Paragraph(metodologia, styles['CuerpoDetallado']))
        contenido.append(Spacer(1, 20))
        
        # 3. Análisis temporal detallado
        if self.analisis['temporal']:
            contenido.append(Paragraph("3. ANÁLISIS TEMPORAL DETALLADO", styles['SeccionPrincipal']))
            temporal = self.analisis['temporal']
            
            if temporal.get('rango_dias', 0) > 0:
                analisis_temporal = f"""
                El proyecto presenta una extensión temporal de {temporal['rango_dias']} días calendario, 
                registrando una frecuencia promedio de {temporal['registros_por_dia']:.2f} actividades por día. 
                Esta distribución temporal evidencia {'un ritmo de trabajo intensivo' if temporal['registros_por_dia'] > 2 
                                                    else 'un desarrollo sistemático y planificado'} en la ejecución 
                de las actividades programadas.
                
                La concentración de actividades por día de la semana muestra patrones operacionales que reflejan 
                la organización del trabajo y la disponibilidad de recursos humanos y técnicos.
                """
                contenido.append(Paragraph(analisis_temporal, styles['CuerpoDetallado']))
            
            contenido.append(Spacer(1, 20))
        
        # 4. Recursos humanos detallado
        if self.analisis['recursos_humanos']:
            contenido.append(Paragraph("4. EVALUACIÓN INTEGRAL DE RECURSOS HUMANOS", styles['SeccionPrincipal']))
            
            rh = self.analisis['recursos_humanos']
            texto_rh_detallado = self.prosa.generar_seccion_recursos_humanos(rh)
            contenido.append(Paragraph(texto_rh_detallado, styles['CuerpoDetallado']))
            
            # Análisis adicional de eficiencia
            eficiencia_adicional = f"""
            
            El análisis de eficiencia revela que la relación horas-trabajador de {rh.get('eficiencia_hora_trabajador', 0):.1f} 
            horas por persona constituye {'un indicador superior al promedio sectorial' if rh.get('eficiencia_hora_trabajador', 0) > 8 
                                         else 'un nivel de eficiencia estándar para este tipo de proyectos'}, 
            lo que {'sugiere la necesidad de evaluar la sostenibilidad de la carga de trabajo' if rh.get('eficiencia_hora_trabajador', 0) > 10
                   else 'indica una gestión equilibrada de los recursos humanos'}.
            """
            contenido.append(Paragraph(eficiencia_adicional, styles['CuerpoDetallado']))
            contenido.append(Spacer(1, 20))
        
        # 5. Análisis geográfico detallado
        if self.analisis['geografico']:
            contenido.append(Paragraph("5. CARACTERIZACIÓN GEOGRÁFICA Y TERRITORIAL", styles['SeccionPrincipal']))
            texto_geo_detallado = self.prosa.generar_seccion_geografica(self.analisis['geografico'])
            contenido.append(Paragraph(texto_geo_detallado, styles['CuerpoDetallado']))
            contenido.append(Spacer(1, 20))
        
        # 6. Actividades detalladas
        if self.analisis['actividades']:
            contenido.append(Paragraph("6. ANÁLISIS DE TIPOS DE ACTIVIDADES", styles['SeccionPrincipal']))
            
            actividades_texto = """
            La caracterización de actividades permite identificar los patrones de intervención y la naturaleza 
            de las obras ejecutadas. El análisis revela la diversidad de acciones implementadas y su distribución 
            relativa dentro del conjunto total de intervenciones.
            """
            contenido.append(Paragraph(actividades_texto, styles['CuerpoDetallado']))
            contenido.append(Spacer(1, 20))
        
        # 7. Indicadores de eficiencia
        contenido.append(Paragraph("7. INDICADORES DE EFICIENCIA Y PRODUCTIVIDAD", styles['SeccionPrincipal']))
        
        indicadores_texto = f"""
        Los indicadores de eficiencia calculados proporcionan una visión integral del desempeño del proyecto:
        
        • Eficiencia de registro: {self.analisis['metadata']['total_registros'] / max(self.analisis['temporal'].get('rango_dias', 1), 1):.2f} actividades/día
        • Densidad de intervención: {self.analisis['geografico'].get('concentracion', 1):.2f} actividades por punto geográfico
        • Intensidad de recursos: {self.analisis['recursos_humanos'].get('promedio_por_actividad', 0):.1f} trabajadores promedio por actividad
        
        Estos indicadores permiten evaluar la eficiencia operacional y identificar oportunidades de optimización 
        en la gestión de recursos y la planificación de actividades futuras.
        """
        contenido.append(Paragraph(indicadores_texto, styles['CuerpoDetallado']))
        contenido.append(Spacer(1, 20))
        
        # 8. Insights
        if self.analisis['insights']:
            contenido.append(Paragraph("8. INSIGHTS Y HALLAZGOS SIGNIFICATIVOS", styles['SeccionPrincipal']))
            
            for i, insight in enumerate(self.analisis['insights'], 1):
                contenido.append(Paragraph(f"{i}. {insight}", styles['CuerpoDetallado']))
                contenido.append(Spacer(1, 8))
            
            contenido.append(Spacer(1, 20))
        
        # 9. Recomendaciones
        if self.analisis['recomendaciones']:
            contenido.append(Paragraph("9. RECOMENDACIONES ESTRATÉGICAS", styles['SeccionPrincipal']))
            
            for i, recomendacion in enumerate(self.analisis['recomendaciones'], 1):
                contenido.append(Paragraph(f"{i}. {recomendacion}", styles['CuerpoDetallado']))
                contenido.append(Spacer(1, 8))
        
        return contenido


class ResumenEjecutivo:
    """Generador de resumen ejecutivo conciso y estratégico"""
    
    def __init__(self, datos: pd.DataFrame):
        self.datos = datos
        self.analisis = procesar_datos_para_informe(datos)
        self.prosa = GeneradorProsa()
        
    def generar_pdf(self) -> BytesIO:
        """Genera el PDF del resumen ejecutivo"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=A4,
            rightMargin=inch * 0.75,
            leftMargin=inch * 0.75,
            topMargin=inch,
            bottomMargin=inch
        )
        
        styles = self._configurar_estilos()
        story = []
        
        # Encabezado ejecutivo
        story.extend(self._generar_encabezado_ejecutivo(styles))
        
        # Contenido ejecutivo
        story.extend(self._generar_contenido_ejecutivo(styles))
        
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def _configurar_estilos(self):
        """Configura estilos para el resumen ejecutivo"""
        styles = getSampleStyleSheet()
        
        styles.add(ParagraphStyle(
            name='TituloEjecutivo',
            parent=styles['Title'],
            fontSize=20,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#dc2626')
        ))
        
        styles.add(ParagraphStyle(
            name='SeccionEjecutiva',
            parent=styles['Heading1'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=18,
            textColor=colors.HexColor('#991b1b'),
            borderWidth=1,
            borderColor=colors.HexColor('#fee2e2'),
            borderPadding=6
        ))
        
        styles.add(ParagraphStyle(
            name='CuerpoEjecutivo',
            parent=styles['Normal'],
            alignment=TA_JUSTIFY,
            spaceAfter=8,
            fontSize=11,
            leading=14
        ))
        
        styles.add(ParagraphStyle(
            name='DestacadoEjecutivo',
            parent=styles['Normal'],
            alignment=TA_CENTER,
            spaceAfter=10,
            fontSize=12,
            textColor=colors.HexColor('#dc2626'),
            fontName='Helvetica-Bold'
        ))
        
        return styles
    
    def _generar_encabezado_ejecutivo(self, styles) -> List:
        """Genera encabezado del resumen ejecutivo"""
        encabezado = []
        
        encabezado.append(Paragraph("RESUMEN EJECUTIVO", styles['TituloEjecutivo']))
        encabezado.append(Paragraph("PROYECTO SURVEY123", styles['TituloEjecutivo']))
        
        # Información clave en formato destacado
        info_clave = f"""
        <b>SECRETARÍA DE INFRAESTRUCTURA FÍSICA - ALCALDÍA DE MEDELLÍN</b><br/>
        Fecha: {self.analisis['metadata']['fecha_procesamiento']} | 
        Registros: {self.analisis['metadata']['total_registros']:,} | 
        Variables: {self.analisis['metadata']['columnas_analizadas']}
        """
        encabezado.append(Paragraph(info_clave, styles['DestacadoEjecutivo']))
        encabezado.append(Spacer(1, 20))
        
        return encabezado
    
    def _generar_contenido_ejecutivo(self, styles) -> List:
        """Genera contenido conciso del resumen ejecutivo"""
        contenido = []
        
        # Síntesis del proyecto
        contenido.append(Paragraph("SÍNTESIS DEL PROYECTO", styles['SeccionEjecutiva']))
        contenido.append(Paragraph(self.analisis['resumen_ejecutivo'], styles['CuerpoEjecutivo']))
        contenido.append(Spacer(1, 15))
        
        # Indicadores clave
        contenido.append(Paragraph("INDICADORES CLAVE DE DESEMPEÑO", styles['SeccionEjecutiva']))
        
        # Crear tabla de indicadores
        indicadores = [['INDICADOR', 'VALOR', 'EVALUACIÓN']]
        
        # Recursos humanos
        if self.analisis['recursos_humanos']:
            rh = self.analisis['recursos_humanos']
            total_trabajadores = rh.get('total_trabajadores', 0)
            total_horas = rh.get('total_horas', 0)
            eficiencia = rh.get('eficiencia_hora_trabajador', 0)
            
            indicadores.extend([
                ['Personal movilizado', f"{total_trabajadores:,} trabajadores", 
                 'Alto' if total_trabajadores > 300 else 'Medio' if total_trabajadores > 100 else 'Estándar'],
                ['Horas de trabajo', f"{total_horas:,.0f} horas",
                 'Intensivo' if total_horas > 1500 else 'Moderado'],
                ['Eficiencia por trabajador', f"{eficiencia:.1f} h/persona",
                 'Alta' if eficiencia > 8 else 'Equilibrada']
            ])
        
        # Distribución geográfica
        if self.analisis['geografico']:
            geo = self.analisis['geografico']
            puntos = geo.get('puntos_unicos', 0)
            concentracion = geo.get('concentracion', 1)
            
            indicadores.extend([
                ['Cobertura geográfica', f"{puntos} puntos únicos",
                 'Amplia' if puntos > 20 else 'Focalizada'],
                ['Concentración', f"{concentracion:.1f} act/punto",
                 'Intensiva' if concentracion > 2 else 'Distribuida']
            ])
        
        tabla_indicadores = Table(indicadores, colWidths=[2.2*inch, 1.8*inch, 1.2*inch])
        tabla_indicadores.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dc2626')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fef2f2')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#fca5a5'))
        ]))
        
        contenido.append(tabla_indicadores)
        contenido.append(Spacer(1, 20))
        
        # Hallazgos principales (máximo 3)
        if self.analisis['insights']:
            contenido.append(Paragraph("HALLAZGOS PRINCIPALES", styles['SeccionEjecutiva']))
            for i, insight in enumerate(self.analisis['insights'][:3], 1):
                contenido.append(Paragraph(f"<b>{i}.</b> {insight}", styles['CuerpoEjecutivo']))
                contenido.append(Spacer(1, 6))
            contenido.append(Spacer(1, 15))
        
        # Recomendaciones estratégicas (máximo 3)
        if self.analisis['recomendaciones']:
            contenido.append(Paragraph("RECOMENDACIONES ESTRATÉGICAS PRIORITARIAS", styles['SeccionEjecutiva']))
            for i, recomendacion in enumerate(self.analisis['recomendaciones'][:3], 1):
                contenido.append(Paragraph(f"<b>{i}.</b> {recomendacion}", styles['CuerpoEjecutivo']))
                contenido.append(Spacer(1, 6))
        
        # Conclusión ejecutiva
        contenido.append(Spacer(1, 20))
        contenido.append(Paragraph("CONCLUSIÓN EJECUTIVA", styles['SeccionEjecutiva']))
        
        conclusion = f"""
        El análisis de {self.analisis['metadata']['total_registros']:,} registros evidencia un proyecto 
        {'de gran envergadura' if self.analisis['metadata']['total_registros'] > 50 else 'focalizado'} 
        con {'alta movilización de recursos' if self.analisis['recursos_humanos'].get('total_trabajadores', 0) > 200 else 'gestión eficiente de recursos'} 
        y {'amplia distribución territorial' if self.analisis['geografico'].get('puntos_unicos', 0) > 10 else 'intervención focalizada'}. 
        
        Los indicadores de eficiencia {'superan los estándares sectoriales' if self.analisis['recursos_humanos'].get('eficiencia_hora_trabajador', 0) > 8 else 'se mantienen en niveles óptimos'}, 
        lo que {'requiere atención en la sostenibilidad de la operación' if self.analisis['recursos_humanos'].get('eficiencia_hora_trabajador', 0) > 10 else 'confirma la viabilidad operacional del proyecto'}.
        """
        
        contenido.append(Paragraph(conclusion, styles['CuerpoEjecutivo']))
        
        return contenido
