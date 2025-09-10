"""
Aplicación principal Flask para el Sistema de Informes Survey123
Secretaría de Infraestructura Física de Medellín
"""

from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
import pandas as pd
import numpy as np
import os
import logging
import time
from datetime import datetime
from werkzeug.utils import secure_filename
import json

# Importar módulos locales
from config import Config
from modulos.ingesta import ProcesadorSurvey123
from modulos.modelos import RepositorioIntervenciones

def convertir_tipos_numpy(obj):
    """Convertir tipos numpy a tipos Python para serialización JSON"""
    if isinstance(obj, dict):
        return {key: convertir_tipos_numpy(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convertir_tipos_numpy(item) for item in obj]
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, (np.bool_, bool)):
        return bool(obj)
    elif hasattr(obj, 'dtype') and 'bool' in str(obj.dtype):
        return bool(obj)
    elif hasattr(obj, 'item'):  # Para tipos escalares de numpy/pandas
        try:
            return obj.item()
        except (ValueError, AttributeError):
            return str(obj)
    elif pd.isna(obj):
        return None
    else:
        return obj

def crear_aplicacion():
    """Factory pattern para crear la aplicación Flask"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Marcar tiempo de inicio para uptime
    app.start_time = time.time()
    
    # Configurar logging - mostrar solo mensajes esenciales
    if not app.debug:
        # Configurar logging para mostrar solo el mensaje de inicio del servidor
        logging.basicConfig(
            level=logging.INFO,
            format=' * %(message)s',
            handlers=[logging.StreamHandler()]
        )
        # Configurar Werkzeug para mostrar solo el mensaje de inicio
        werkzeug_logger = logging.getLogger('werkzeug')
        werkzeug_logger.setLevel(logging.INFO)
        werkzeug_logger.handlers = []
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(' * %(message)s'))
        werkzeug_logger.addHandler(handler)
    
    # Variables globales de la aplicación
    app.datos_cargados = None
    app.procesador = ProcesadorSurvey123(Config)
    app.repositorio = RepositorioIntervenciones()
    
    def cargar_ultimo_archivo_procesado():
        """Cargar automáticamente el último archivo procesado"""
        try:
            upload_dir = os.path.join(app.config['UPLOAD_FOLDER'])
            if os.path.exists(upload_dir):
                archivos_procesados = [f for f in os.listdir(upload_dir) if f.endswith('_procesado.xlsx')]
                if archivos_procesados:
                    # Obtener el archivo más reciente
                    archivo_mas_reciente = max(archivos_procesados, 
                                             key=lambda x: os.path.getmtime(os.path.join(upload_dir, x)))
                    ruta_archivo = os.path.join(upload_dir, archivo_mas_reciente)
                    
                    # Cargar los datos
                    app.datos_cargados = pd.read_excel(ruta_archivo)
                    app.repositorio.desde_dataframe(app.datos_cargados)
                    
                    app.logger.info(f"Datos cargados automáticamente desde: {archivo_mas_reciente}")
                    app.logger.info(f"Registros cargados: {len(app.datos_cargados)}")
        except Exception as e:
            app.logger.warning(f"No se pudo cargar automáticamente los datos: {str(e)}")
    
    # Intentar cargar el último archivo procesado al iniciar
    cargar_ultimo_archivo_procesado()
    
    @app.route('/')
    def index():
        """Página de inicio"""
        return render_template('index.html')

    @app.route('/cargar_datos')
    def cargar_datos():
        """Página para cargar datos"""
        return render_template('cargar_datos.html')

    @app.route('/procesar_archivo', methods=['POST'])
    def procesar_archivo():
        """Procesar archivo cargado"""
        try:
            if 'archivo' not in request.files:
                return jsonify({'error': 'No se seleccionó archivo'}), 400
            
            archivo = request.files['archivo']
            
            if archivo.filename == '':
                return jsonify({'error': 'Archivo vacío'}), 400
            
            if archivo and archivo.filename.lower().endswith(('.xlsx', '.xls')):
                # Guardar archivo temporalmente
                filename = secure_filename(archivo.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename_procesado = f"{timestamp}_{filename}"
                
                # Asegurar que existe el directorio de uploads
                upload_dir = os.path.join(app.config['UPLOAD_FOLDER'])
                os.makedirs(upload_dir, exist_ok=True)
                
                archivo_temporal = os.path.join(upload_dir, filename_procesado)
                archivo.save(archivo_temporal)
                
                # Procesar archivo
                exito, resumen = app.procesador.procesar_archivo_completo(archivo_temporal)
                
                if exito:
                    # Guardar datos procesados
                    app.datos_cargados = app.procesador.obtener_datos_procesados()
                    
                    # Actualizar repositorio
                    app.repositorio.desde_dataframe(app.datos_cargados)
                    
                    archivo_procesado = archivo_temporal.replace('.xlsx', '_procesado.xlsx')
                    app.datos_cargados.to_excel(archivo_procesado, index=False)
                    
                    return jsonify({
                        'exito': True,
                        'mensaje': 'Archivo procesado exitosamente',
                        'resumen': convertir_tipos_numpy(resumen),
                        'archivo_original': filename,
                        'archivo_procesado': os.path.basename(archivo_procesado)
                    })
                else:
                    return jsonify({'error': 'Error procesando archivo', 'detalles': resumen}), 400
            else:
                return jsonify({'error': 'Tipo de archivo no permitido. Use archivos .xlsx o .xls'}), 400
                
        except Exception as e:
            app.logger.error(f"Error procesando archivo: {str(e)}")
            return jsonify({'error': 'Error interno del servidor', 'detalles': str(e)}), 500

    @app.route('/ver_analisis')
    def ver_analisis():
        """Página de análisis y dashboard"""
        if app.datos_cargados is None:
            flash('No hay datos cargados. Por favor, cargue un archivo primero.', 'warning')
            return redirect(url_for('cargar_datos'))
        
        try:
            # Usar el análisis completo de Survey123
            from modulos.analisis import AnalisisSurvey123
            analizador = AnalisisSurvey123(app.datos_cargados)
            estadisticas = analizador.generar_analisis_completo()
            
            # Convertir tipos numpy para evitar errores de serialización en templates
            estadisticas = convertir_tipos_numpy(estadisticas)
            
            return render_template('ver_analisis.html', estadisticas=estadisticas)
        except Exception as e:
            app.logger.error(f"Error generando análisis: {str(e)}")
            flash(f'Error generando análisis: {str(e)}', 'error')
            return redirect(url_for('cargar_datos'))

    @app.route('/api/estadisticas')
    def api_estadisticas():
        """API para obtener estadísticas en formato JSON"""
        if app.datos_cargados is None:
            return jsonify({'error': 'No hay datos cargados'}), 400
        
        try:
            from modulos.analisis import AnalizadorDatos
            analizador = AnalizadorDatos()
            estadisticas = analizador.calcular_estadisticas_basicas(app.datos_cargados)
            return jsonify(convertir_tipos_numpy(estadisticas))
        except Exception as e:
            app.logger.error(f"Error obteniendo estadísticas: {str(e)}")
            return jsonify({'error': 'Error obteniendo estadísticas', 'detalles': str(e)}), 500

    @app.route('/api/productividad')
    def api_productividad():
        """API para obtener análisis de productividad"""
        if app.datos_cargados is None:
            return jsonify({'error': 'No hay datos cargados'}), 400
        
        try:
            from modulos.analisis import AnalizadorDatos
            analizador = AnalizadorDatos()
            productividad = analizador.analizar_productividad(app.datos_cargados)
            return jsonify(convertir_tipos_numpy(productividad))
        except Exception as e:
            app.logger.error(f"Error obteniendo productividad: {str(e)}")
            return jsonify({'error': 'Error obteniendo productividad', 'detalles': str(e)}), 500

    @app.route('/api/tendencias')
    def api_tendencias():
        """API para obtener análisis de tendencias"""
        if app.datos_cargados is None:
            return jsonify({'error': 'No hay datos cargados'}), 400
        
        try:
            from modulos.analisis import AnalizadorDatos
            analizador = AnalizadorDatos()
            tendencias = analizador.generar_tendencias(app.datos_cargados)
            return jsonify(convertir_tipos_numpy(tendencias))
        except Exception as e:
            app.logger.error(f"Error obteniendo tendencias: {str(e)}")
            return jsonify({'error': 'Error obteniendo tendencias', 'detalles': str(e)}), 500

    @app.route('/api/aplicar_filtros', methods=['POST'])
    def api_aplicar_filtros():
        """API para aplicar filtros a los datos"""
        if app.datos_cargados is None:
            return jsonify({'error': 'No hay datos cargados'}), 400
        
        try:
            filtros = request.get_json()
            
            # Obtener los datos base
            datos_filtrados = app.datos_cargados.copy()
            
            # Aplicar filtro por estado
            if filtros.get('estados') and len(filtros['estados']) > 0:
                if 'estado_obr' in datos_filtrados.columns:
                    datos_filtrados = datos_filtrados[datos_filtrados['estado_obr'].isin(filtros['estados'])]
            
            # Aplicar filtro por fechas
            if filtros.get('fechaInicio') or filtros.get('fechaFin'):
                if 'fecha_dilig' in datos_filtrados.columns:
                    # Convertir la columna a datetime si no lo está
                    datos_filtrados['fecha_dilig'] = pd.to_datetime(datos_filtrados['fecha_dilig'], errors='coerce')
                    
                    if filtros.get('fechaInicio'):
                        fecha_inicio = pd.to_datetime(filtros['fechaInicio'])
                        datos_filtrados = datos_filtrados[datos_filtrados['fecha_dilig'] >= fecha_inicio]
                    
                    if filtros.get('fechaFin'):
                        fecha_fin = pd.to_datetime(filtros['fechaFin'])
                        datos_filtrados = datos_filtrados[datos_filtrados['fecha_dilig'] <= fecha_fin]
            
            # Generar análisis con datos filtrados
            from modulos.analisis import AnalisisSurvey123
            analizador = AnalisisSurvey123(datos_filtrados)
            estadisticas = analizador.generar_analisis_completo()
            
            # Convertir tipos numpy
            estadisticas = convertir_tipos_numpy(estadisticas)
            
            # Agregar información de filtros aplicados
            estadisticas['filtros_aplicados'] = {
                'total_registros_originales': len(app.datos_cargados),
                'total_registros_filtrados': len(datos_filtrados),
                'filtros': filtros
            }
            
            return jsonify(estadisticas)
            
        except Exception as e:
            app.logger.error(f"Error aplicando filtros: {str(e)}")
            return jsonify({'error': 'Error aplicando filtros', 'detalles': str(e)}), 500

    @app.route('/api/datos_grafico/<tipo>')
    def api_datos_grafico(tipo):
        """API para obtener datos específicos para gráficos"""
        if app.datos_cargados is None:
            return jsonify({'error': 'No hay datos cargados'}), 400
        
        try:
            if tipo == 'estados_obra':
                datos = app.datos_cargados['estado_obr'].value_counts().to_dict()
            elif tipo == 'recursos_humanos':
                datos = {
                    'total_trabajadores': app.datos_cargados['num_total_'].sum(),
                    'total_horas': app.datos_cargados['total_hora'].sum(),
                    'promedio_trabajadores': app.datos_cargados['num_total_'].mean()
                }
            elif tipo == 'maquinaria':
                datos = {
                    'horas_retroexcavadora': app.datos_cargados['horas_retr'].sum(),
                    'horas_minicargador': app.datos_cargados['horas_mini'].sum(),
                    'horas_volqueta': app.datos_cargados['horas_volq'].sum(),
                    'horas_compactadora': app.datos_cargados['horas_comp'].sum()
                }
            else:
                return jsonify({'error': 'Tipo de gráfico no soportado'}), 400
            
            return jsonify(convertir_tipos_numpy(datos))
            
        except Exception as e:
            app.logger.error(f"Error obteniendo datos para gráfico {tipo}: {str(e)}")
            return jsonify({'error': 'Error obteniendo datos', 'detalles': str(e)}), 500

    @app.route('/generar_informe')
    def generar_informe():
        """Página de generación de informes"""
        if app.datos_cargados is None:
            flash('No hay datos cargados. Por favor, cargue un archivo primero.', 'warning')
            return redirect(url_for('cargar_datos'))
        
        return render_template('generar_informe.html')

    @app.route('/api/generar_informe_estadistico')
    def api_generar_informe_estadistico():
        """Generar informe estadístico con análisis inteligente en formato PDF"""
        if app.datos_cargados is None:
            return jsonify({'error': 'No hay datos cargados'}), 400
        
        try:
            from modulos.generador_inteligente import GeneradorInformeInteligente
            
            # Generar informe con AI avanzada
            generador = GeneradorInformeInteligente(app.datos_cargados)
            
            # Crear nombre de archivo temporal
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f'datos/reportes_generados/informe_estadistico_inteligente_{timestamp}.pdf'
            
            # Asegurar que el directorio existe
            os.makedirs('datos/reportes_generados', exist_ok=True)
            
            # Generar informe inteligente
            archivo_generado = generador.generar_informe_estadistico_inteligente(nombre_archivo)
            
            return send_file(
                archivo_generado,
                as_attachment=True,
                download_name=f'informe_estadistico_inteligente_{timestamp}.pdf',
                mimetype='application/pdf'
            )
            
        except Exception as e:
            app.logger.error(f"Error generando informe estadístico inteligente: {str(e)}")
            return jsonify({'error': 'Error generando informe', 'detalles': str(e)}), 500

    @app.route('/api/generar_informe_detallado/<formato>')
    def api_generar_informe_detallado(formato):
        """Generar informe detallado con análisis exhaustivo usando IA"""
        if app.datos_cargados is None:
            return jsonify({'error': 'No hay datos cargados'}), 400
        
        try:
            if formato.lower() == 'pdf':
                from modulos.generador_inteligente import GeneradorInformeInteligente
                
                # Generar informe detallado con AI avanzada
                generador = GeneradorInformeInteligente(app.datos_cargados)
                
                # Crear nombre de archivo temporal
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                nombre_archivo = f'datos/reportes_generados/informe_detallado_inteligente_{timestamp}.pdf'
                
                # Asegurar que el directorio existe
                os.makedirs('datos/reportes_generados', exist_ok=True)
                
                # Generar informe inteligente
                archivo_generado = generador.generar_informe_detallado_inteligente(nombre_archivo)
                
                return send_file(
                    archivo_generado,
                    as_attachment=True,
                    download_name=f'informe_detallado_inteligente_{timestamp}.pdf',
                    mimetype='application/pdf'
                )
            else:
                return jsonify({'error': 'Solo se soporta formato PDF para informe detallado'}), 400
                
        except Exception as e:
            app.logger.error(f"Error generando informe detallado inteligente: {str(e)}")
            return jsonify({'error': 'Error generando informe', 'detalles': str(e)}), 500

    @app.route('/api/generar_informe_geografico')
    def api_generar_informe_geografico():
        """Generar informe geográfico con mapas"""
        if app.datos_cargados is None:
            return jsonify({'error': 'No hay datos cargados'}), 400
        
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            from io import BytesIO
            
            # Crear PDF en memoria
            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)
            width, height = letter
            
            # Título
            p.setFont("Helvetica-Bold", 16)
            p.drawString(50, height - 50, "Informe Geográfico - Survey123")
            
            # Información geográfica básica
            y_position = height - 100
            p.setFont("Helvetica", 12)
            
            total_puntos = len(app.datos_cargados)
            lat_min, lat_max = app.datos_cargados['Y'].min(), app.datos_cargados['Y'].max()
            lon_min, lon_max = app.datos_cargados['X'].min(), app.datos_cargados['X'].max()
            lat_centro = app.datos_cargados['Y'].mean()
            lon_centro = app.datos_cargados['X'].mean()
            
            p.drawString(50, y_position, f"Total de puntos analizados: {total_puntos}")
            y_position -= 20
            p.drawString(50, y_position, f"Coordenadas centro: {lat_centro:.6f}, {lon_centro:.6f}")
            y_position -= 20
            p.drawString(50, y_position, f"Rango Latitud: {lat_min:.6f} - {lat_max:.6f}")
            y_position -= 20
            p.drawString(50, y_position, f"Rango Longitud: {lon_min:.6f} - {lon_max:.6f}")
            y_position -= 40
            
            # Estadísticas por estado
            if 'estado_obr' in app.datos_cargados.columns:
                estados = app.datos_cargados['estado_obr'].value_counts()
                p.drawString(50, y_position, "Distribución por Estado:")
                y_position -= 20
                for estado, cantidad in estados.items():
                    p.drawString(70, y_position, f"• {estado}: {cantidad}")
                    y_position -= 15
            
            # Agregar fecha de generación
            p.drawString(50, y_position - 40, f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            
            p.showPage()
            p.save()
            
            buffer.seek(0)
            
            return send_file(
                buffer,
                as_attachment=True,
                download_name=f'informe_geografico_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf',
                mimetype='application/pdf'
            )
            
        except Exception as e:
            app.logger.error(f"Error generando informe geográfico: {str(e)}")
            return jsonify({'error': 'Error generando informe', 'detalles': str(e)}), 500

    @app.route('/api/generar_informe_ejecutivo')
    def api_generar_informe_ejecutivo():
        """Generar resumen ejecutivo estratégico con IA en formato PDF"""
        if app.datos_cargados is None:
            return jsonify({'error': 'No hay datos cargados'}), 400
        
        try:
            from modulos.generador_inteligente import GeneradorInformeInteligente
            
            # Generar resumen ejecutivo con AI avanzada
            generador = GeneradorInformeInteligente(app.datos_cargados)
            
            # Crear nombre de archivo temporal
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f'datos/reportes_generados/resumen_ejecutivo_inteligente_{timestamp}.pdf'
            
            # Asegurar que el directorio existe
            os.makedirs('datos/reportes_generados', exist_ok=True)
            
            # Generar informe inteligente
            archivo_generado = generador.generar_informe_ejecutivo_inteligente(nombre_archivo)
            
            return send_file(
                archivo_generado,
                as_attachment=True,
                download_name=f'resumen_ejecutivo_inteligente_{timestamp}.pdf',
                mimetype='application/pdf'
            )
            
        except Exception as e:
            app.logger.error(f"Error generando resumen ejecutivo inteligente: {str(e)}")
            return jsonify({'error': 'Error generando informe', 'detalles': str(e)}), 500

    # ==================== RUTAS PARA INFORMES TRADICIONALES ====================
    
    @app.route('/api/generar_informe_tradicional_estadistico')
    def api_generar_informe_tradicional_estadistico():
        """Generar informe estadístico tradicional (sin IA) en formato PDF"""
        if app.datos_cargados is None:
            return jsonify({'error': 'No hay datos cargados'}), 400
        
        try:
            from modulos.generadores_pdf import InformeEstadistico
            
            # Generar informe tradicional
            generador = InformeEstadistico(app.datos_cargados)
            buffer = generador.generar_pdf()
            
            return send_file(
                buffer,
                as_attachment=True,
                download_name=f'informe_estadistico_tradicional_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf',
                mimetype='application/pdf'
            )
            
        except Exception as e:
            app.logger.error(f"Error generando informe estadístico tradicional: {str(e)}")
            return jsonify({'error': 'Error generando informe tradicional', 'detalles': str(e)}), 500
    
    @app.route('/api/generar_informe_tradicional_detallado')
    def api_generar_informe_tradicional_detallado():
        """Generar informe detallado tradicional (sin IA) en formato PDF"""
        if app.datos_cargados is None:
            return jsonify({'error': 'No hay datos cargados'}), 400
        
        try:
            from modulos.generadores_pdf import InformeDetallado
            
            # Generar informe detallado tradicional
            generador = InformeDetallado(app.datos_cargados)
            buffer = generador.generar_pdf()
            
            return send_file(
                buffer,
                as_attachment=True,
                download_name=f'informe_detallado_tradicional_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf',
                mimetype='application/pdf'
            )
            
        except Exception as e:
            app.logger.error(f"Error generando informe detallado tradicional: {str(e)}")
            return jsonify({'error': 'Error generando informe tradicional', 'detalles': str(e)}), 500
    
    @app.route('/api/generar_informe_tradicional_ejecutivo')
    def api_generar_informe_tradicional_ejecutivo():
        """Generar resumen ejecutivo tradicional (sin IA) en formato PDF"""
        if app.datos_cargados is None:
            return jsonify({'error': 'No hay datos cargados'}), 400
        
        try:
            from modulos.generadores_pdf import ResumenEjecutivo
            
            # Generar resumen ejecutivo tradicional
            generador = ResumenEjecutivo(app.datos_cargados)
            buffer = generador.generar_pdf()
            
            return send_file(
                buffer,
                as_attachment=True,
                download_name=f'resumen_ejecutivo_tradicional_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf',
                mimetype='application/pdf'
            )
            
        except Exception as e:
            app.logger.error(f"Error generando resumen ejecutivo tradicional: {str(e)}")
            return jsonify({'error': 'Error generando informe tradicional', 'detalles': str(e)}), 500

    @app.route('/mapa_intervenciones')
    def mapa_intervenciones():
        """Página del mapa de intervenciones"""
        if app.datos_cargados is None:
            flash('No hay datos cargados. Por favor, cargue un archivo primero.', 'warning')
            return redirect(url_for('cargar_datos'))
        
        try:
            # Calcular estadísticas para el template
            df = app.datos_cargados
            
            # Contar por estado
            total_intervenciones = len(df)
            terminadas = len(df[df['estado_obr'].str.contains('Terminada', case=False, na=False)])
            en_ejecucion = len(df[df['estado_obr'].str.contains('ejecucion|proceso', case=False, na=False)])
            pendientes = len(df[df['estado_obr'].str.contains('Pendiente', case=False, na=False)])
            
            return render_template('mapa_intervenciones.html',
                                 total_intervenciones=total_intervenciones,
                                 terminadas=terminadas,
                                 en_ejecucion=en_ejecucion,
                                 pendientes=pendientes)
        except Exception as e:
            app.logger.error(f"Error calculando estadísticas: {str(e)}")
            return render_template('mapa_intervenciones.html',
                                 total_intervenciones=0,
                                 terminadas=0,
                                 en_ejecucion=0,
                                 pendientes=0)

    @app.route('/api/datos_mapa')
    def api_datos_mapa():
        """API para obtener datos del mapa"""
        if app.datos_cargados is None:
            return jsonify({'error': 'No hay datos cargados'}), 400
        
        try:
            # Preparar datos para el mapa
            datos_mapa = []
            for _, fila in app.datos_cargados.iterrows():
                # Verificar que las coordenadas sean válidas
                try:
                    lat = float(fila.get('Y', 0))
                    lng = float(fila.get('X', 0))
                    
                    # Filtrar coordenadas inválidas (0,0 o fuera de Colombia)
                    if lat == 0 or lng == 0 or lat < -5 or lat > 15 or lng < -85 or lng > -65:
                        continue
                        
                except (ValueError, TypeError):
                    continue
                
                punto = {
                    'id_punto': str(fila.get('id_punto', '')),
                    'lat': lat,
                    'lng': lng,
                    'estado_obra': str(fila.get('estado_obr', '')),
                    'nombre_interventor': str(fila.get('nombre_int', '')),
                    'fecha_diligenciamiento': str(fila.get('fecha_dilig', '')),
                    'total_trabajadores': int(fila.get('num_total_', 0)) if pd.notna(fila.get('num_total_', 0)) else 0,
                    'total_horas': float(fila.get('total_hora', 0)) if pd.notna(fila.get('total_hora', 0)) else 0
                }
                datos_mapa.append(punto)
            
            return jsonify(convertir_tipos_numpy(datos_mapa))
            
        except Exception as e:
            app.logger.error(f"Error obteniendo datos del mapa: {str(e)}")
            return jsonify({'error': 'Error obteniendo datos del mapa', 'detalles': str(e)}), 500

    @app.route('/favicon.ico')
    def favicon():
        """Ruta para el favicon"""
        return '', 204
    
    @app.route('/health')
    def health_check():
        """Endpoint de health check para monitoreo"""
        try:
            import psutil
            
            # Verificar estado de la aplicación
            health_status = {
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'version': '1.0.0',
                'uptime_seconds': time.time() - app.start_time if hasattr(app, 'start_time') else 0
            }
            
            # Verificar memoria
            memoria = psutil.virtual_memory()
            health_status['memory'] = {
                'used_percent': round(memoria.percent, 2),
                'available_gb': round(memoria.available / (1024**3), 2)
            }
            
            # Verificar espacio en disco
            upload_folder = app.config.get('UPLOAD_FOLDER', '.')
            if os.path.exists(upload_folder):
                if os.name == 'nt':  # Windows
                    import shutil
                    free_space_gb = shutil.disk_usage(upload_folder).free / (1024**3)
                else:  # Unix/Linux
                    stats = os.statvfs(upload_folder)
                    free_space_gb = (stats.f_bavail * stats.f_frsize) / (1024**3)
                
                health_status['disk'] = {
                    'free_space_gb': round(free_space_gb, 2)
                }
            
            # Verificar directorios críticos
            directorios_criticos = [
                app.config.get('UPLOAD_FOLDER'),
                app.config.get('PROCESSED_FOLDER'),
                app.config.get('REPORTS_FOLDER')
            ]
            
            health_status['directories'] = {}
            for directorio in directorios_criticos:
                if directorio:
                    health_status['directories'][os.path.basename(directorio)] = {
                        'exists': os.path.exists(directorio),
                        'writable': os.access(directorio, os.W_OK) if os.path.exists(directorio) else False
                    }
            
            # Verificar si hay datos cargados
            health_status['data'] = {
                'loaded': app.datos_cargados is not None,
                'records_count': len(app.datos_cargados) if app.datos_cargados is not None else 0
            }
            
            # Determinar estado general
            memoria_ok = memoria.percent < 90
            disco_ok = health_status.get('disk', {}).get('free_space_gb', 0) > 0.5
            directorios_ok = all(
                dir_info.get('exists', False) and dir_info.get('writable', False)
                for dir_info in health_status['directories'].values()
            )
            
            if memoria_ok and disco_ok and directorios_ok:
                health_status['status'] = 'healthy'
                status_code = 200
            else:
                health_status['status'] = 'degraded'
                health_status['issues'] = []
                if not memoria_ok:
                    health_status['issues'].append('High memory usage')
                if not disco_ok:
                    health_status['issues'].append('Low disk space')
                if not directorios_ok:
                    health_status['issues'].append('Directory access issues')
                status_code = 200  # Mantenemos 200 pero marcamos como degraded
            
            return jsonify(health_status), status_code
            
        except Exception as e:
            app.logger.error(f"Error en health check: {str(e)}")
            return jsonify({
                'status': 'unhealthy',
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }), 503
    
    @app.route('/metrics')
    def metrics():
        """Endpoint de métricas para monitoreo avanzado"""
        try:
            import psutil
            
            proceso = psutil.Process()
            
            metrics_data = {
                'timestamp': datetime.now().isoformat(),
                'system': {
                    'cpu_percent': psutil.cpu_percent(interval=1),
                    'memory_percent': psutil.virtual_memory().percent,
                    'disk_usage_percent': psutil.disk_usage('/').percent if os.name == 'posix' else psutil.disk_usage('C:\\').percent
                },
                'process': {
                    'memory_mb': round(proceso.memory_info().rss / 1024 / 1024, 2),
                    'cpu_percent': proceso.cpu_percent(),
                    'threads': proceso.num_threads(),
                    'open_files': len(proceso.open_files())
                },
                'application': {
                    'data_loaded': app.datos_cargados is not None,
                    'records_count': len(app.datos_cargados) if app.datos_cargados is not None else 0,
                    'config_valid': all([
                        app.config.get('SECRET_KEY'),
                        app.config.get('UPLOAD_FOLDER'),
                        app.config.get('REQUIRED_COLUMNS')
                    ])
                }
            }
            
            return jsonify(metrics_data)
            
        except Exception as e:
            app.logger.error(f"Error obteniendo métricas: {str(e)}")
            return jsonify({'error': 'Error obteniendo métricas', 'details': str(e)}), 500

    @app.errorhandler(404)
    def not_found_error(error):
        """Manejador de errores 404"""
        return jsonify({'error': 'Página no encontrada'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        """Manejador de errores 500"""
        app.logger.error(f'Error interno del servidor: {error}')
        return jsonify({'error': 'Error interno del servidor'}), 500

    return app

if __name__ == '__main__':
    print("🚀 INICIANDO SISTEMA DE INFORMES SURVEY123")
    print("🏛️  Secretaría de Infraestructura Física de Medellín")
    
    app = crear_aplicacion()
    
    app.run(host='127.0.0.1', port=5000, debug=False)
else:
    # Para importación directa
    app = crear_aplicacion()
