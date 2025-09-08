"""
Aplicación principal Flask para el Sistema de Informes Survey123
Secretaría de Infraestructura Física de Medellín
"""

from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
import pandas as pd
import numpy as np
import os
import logging
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
    elif pd.isna(obj):
        return None
    else:
        return obj

def crear_aplicacion():
    """Factory pattern para crear la aplicación Flask"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configurar logging
    if not app.debug:
        logging.basicConfig(level=logging.INFO)
    
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
        
        # Calcular estadísticas para el dashboard
        estadisticas = app.repositorio.obtener_estadisticas()
        
        # Convertir tipos numpy para evitar errores de serialización en templates
        estadisticas = convertir_tipos_numpy(estadisticas)
        
        return render_template('ver_analisis.html', estadisticas=estadisticas)

    @app.route('/api/estadisticas')
    def api_estadisticas():
        """API para obtener estadísticas en formato JSON"""
        if app.datos_cargados is None:
            return jsonify({'error': 'No hay datos cargados'}), 400
        
        estadisticas = app.repositorio.obtener_estadisticas()
        return jsonify(convertir_tipos_numpy(estadisticas))

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
        """Generar informe estadístico en formato PDF"""
        if app.datos_cargados is None:
            return jsonify({'error': 'No hay datos cargados'}), 400
        
        try:
            from modulos.analisis import AnalisisSurvey123
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            from io import BytesIO
            
            analizador = AnalisisSurvey123(app.datos_cargados)
            analisis = analizador.generar_analisis_completo()
            
            # Crear PDF en memoria
            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)
            width, height = letter
            
            # Título
            p.setFont("Helvetica-Bold", 16)
            p.drawString(50, height - 50, "Informe Estadístico - Survey123")
            
            # Información básica
            y_position = height - 100
            p.setFont("Helvetica", 12)
            
            if 'metadata' in analisis:
                metadata = analisis['metadata']
                p.drawString(50, y_position, f"Total de registros: {metadata.get('total_registros', 0)}")
                y_position -= 20
                p.drawString(50, y_position, f"Columnas analizadas: {metadata.get('columnas_analizadas', 0)}")
                y_position -= 20
            
            if 'recursos_humanos' in analisis:
                rh = analisis['recursos_humanos']
                y_position -= 20
                p.drawString(50, y_position, f"Total trabajadores: {rh.get('total_trabajadores', 0)}")
                y_position -= 20
                p.drawString(50, y_position, f"Total horas trabajadas: {rh.get('total_horas_trabajadas', 0):.1f}")
                y_position -= 20
            
            # Agregar fecha de generación
            p.drawString(50, y_position - 40, f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            
            p.showPage()
            p.save()
            
            buffer.seek(0)
            
            return send_file(
                buffer,
                as_attachment=True,
                download_name=f'informe_estadistico_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf',
                mimetype='application/pdf'
            )
            
        except Exception as e:
            app.logger.error(f"Error generando informe estadístico: {str(e)}")
            return jsonify({'error': 'Error generando informe', 'detalles': str(e)}), 500

    @app.route('/api/generar_informe_detallado/<formato>')
    def api_generar_informe_detallado(formato):
        """Generar informe detallado en PDF o Excel"""
        if app.datos_cargados is None:
            return jsonify({'error': 'No hay datos cargados'}), 400
        
        try:
            if formato.lower() == 'excel':
                # Crear archivo Excel con múltiples hojas
                from io import BytesIO
                output = BytesIO()
                
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    # Hoja principal con datos
                    app.datos_cargados.to_excel(writer, sheet_name='Datos', index=False)
                    
                    # Hoja de resumen
                    estadisticas = app.repositorio.obtener_estadisticas()
                    resumen_df = pd.DataFrame([
                        {'Métrica': 'Total de Registros', 'Valor': len(app.datos_cargados)},
                        {'Métrica': 'Total de Puntos Únicos', 'Valor': app.datos_cargados['id_punto'].nunique()},
                        {'Métrica': 'Total de Trabajadores', 'Valor': app.datos_cargados['num_total_'].sum()},
                        {'Métrica': 'Total de Horas Trabajadas', 'Valor': app.datos_cargados['total_hora'].sum()}
                    ])
                    resumen_df.to_excel(writer, sheet_name='Resumen', index=False)
                
                output.seek(0)
                
                return send_file(
                    output,
                    as_attachment=True,
                    download_name=f'informe_survey123_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx',
                    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
            
            elif formato.lower() == 'pdf':
                return jsonify({'mensaje': 'Generación de PDF en desarrollo', 'formato': formato})
            
            else:
                return jsonify({'error': 'Formato no soportado. Use "excel" o "pdf"'}), 400
                
        except Exception as e:
            app.logger.error(f"Error generando informe detallado: {str(e)}")
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

    @app.route('/mapa_intervenciones')
    def mapa_intervenciones():
        """Página del mapa de intervenciones"""
        if app.datos_cargados is None:
            flash('No hay datos cargados. Por favor, cargue un archivo primero.', 'warning')
            return redirect(url_for('cargar_datos'))
        
        return render_template('mapa_intervenciones.html')

    @app.route('/api/datos_mapa')
    def api_datos_mapa():
        """API para obtener datos del mapa"""
        if app.datos_cargados is None:
            return jsonify({'error': 'No hay datos cargados'}), 400
        
        try:
            # Preparar datos para el mapa
            datos_mapa = []
            for _, fila in app.datos_cargados.iterrows():
                punto = {
                    'id_punto': str(fila.get('id_punto', '')),
                    'lat': float(fila.get('Y', 0)),
                    'lng': float(fila.get('X', 0)),
                    'estado_obra': str(fila.get('estado_obr', '')),
                    'nombre_interventor': str(fila.get('nombre_int', '')),
                    'fecha_diligenciamiento': str(fila.get('fecha_dilig', '')),
                    'total_trabajadores': int(fila.get('num_total_', 0)),
                    'total_horas': float(fila.get('total_hora', 0))
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
    print("=" * 60)
    print("🚀 INICIANDO SISTEMA DE INFORMES SURVEY123")
    print("🏛️  Secretaría de Infraestructura Física de Medellín")
    print("=" * 60)
    
    app = crear_aplicacion()
    
    print(f"📱 Aplicación disponible en: http://localhost:5000")
    print(f"🔧 Modo debug: {app.debug}")
    print(f"📁 Directorio de trabajo: {os.getcwd()}")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=False)
