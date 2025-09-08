"""
Módulo de georreferenciación para Survey123
Secretaría de Infraestructura Física de Medellín

Este módulo proporciona funcionalidades para procesar, validar y visualizar
datos geográficos de las obras de infraestructura física.
"""

import pandas as pd
import numpy as np
import folium
from folium import plugins
import geopandas as gpd
from shapely.geometry import Point, Polygon
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional
import warnings

warnings.filterwarnings('ignore')

class GeorreferenciadeSurvey123:
    """
    Clase principal para manejo de datos georreferenciados de Survey123
    """
    
    def __init__(self, datos: pd.DataFrame):
        """
        Inicializa el procesador de datos geográficos
        
        Args:
            datos: DataFrame con datos de Survey123 que incluye coordenadas X, Y
        """
        self.datos = datos.copy()
        self.validar_columnas_geograficas()
        self.configurar_parametros_medellin()
    
    def configurar_parametros_medellin(self):
        """Configura parámetros específicos para Medellín"""
        # Límites geográficos aproximados de Medellín
        self.limites_medellin = {
            'lat_min': 6.1,
            'lat_max': 6.4,
            'lon_min': -75.7,
            'lon_max': -75.5
        }
        
        # Centro de Medellín para mapas
        self.centro_medellin = {
            'lat': 6.2442,
            'lon': -75.5812
        }
        
        # Configuración de zoom por defecto
        self.zoom_default = 11
        
        # Colores para diferentes estados de obra
        self.colores_estados = {
            'En ejecución': '#FF6B35',  # Naranja
            'Terminada': '#28A745',     # Verde
            'Suspendida': '#DC3545',    # Rojo
            'Programada': '#007BFF',    # Azul
            'default': '#6C757D'        # Gris
        }
    
    def validar_columnas_geograficas(self):
        """Valida que existan las columnas necesarias para georreferenciación"""
        columnas_requeridas = ['X', 'Y']
        columnas_faltantes = [col for col in columnas_requeridas if col not in self.datos.columns]
        
        if columnas_faltantes:
            raise ValueError(f"Faltan columnas geográficas: {columnas_faltantes}")
        
        # Verificar que las coordenadas sean numéricas
        for col in ['X', 'Y']:
            if not pd.api.types.is_numeric_dtype(self.datos[col]):
                try:
                    self.datos[col] = pd.to_numeric(self.datos[col], errors='coerce')
                except:
                    raise ValueError(f"No se pudo convertir la columna {col} a numérica")
    
    def validar_coordenadas(self) -> Dict[str, Any]:
        """
        Valida las coordenadas geográficas
        
        Returns:
            Dict con estadísticas de validación
        """
        validacion = {
            'total_registros': len(self.datos),
            'coordenadas_validas': 0,
            'coordenadas_invalidas': 0,
            'fuera_de_medellin': 0,
            'estadisticas': {},
            'registros_problematicos': []
        }
        
        # Identificar coordenadas válidas (no nulas y numéricas)
        coordenadas_validas = ~(self.datos['X'].isna() | self.datos['Y'].isna())
        validacion['coordenadas_validas'] = coordenadas_validas.sum()
        validacion['coordenadas_invalidas'] = (~coordenadas_validas).sum()
        
        # Verificar coordenadas dentro de los límites de Medellín
        if validacion['coordenadas_validas'] > 0:
            datos_validos = self.datos[coordenadas_validas]
            
            dentro_limites = (
                (datos_validos['Y'] >= self.limites_medellin['lat_min']) &
                (datos_validos['Y'] <= self.limites_medellin['lat_max']) &
                (datos_validos['X'] >= self.limites_medellin['lon_min']) &
                (datos_validos['X'] <= self.limites_medellin['lon_max'])
            )
            
            validacion['fuera_de_medellin'] = (~dentro_limites).sum()
            
            # Estadísticas de coordenadas
            validacion['estadisticas'] = {
                'lat_min': datos_validos['Y'].min(),
                'lat_max': datos_validos['Y'].max(),
                'lat_promedio': datos_validos['Y'].mean(),
                'lon_min': datos_validos['X'].min(),
                'lon_max': datos_validos['X'].max(),
                'lon_promedio': datos_validos['X'].mean()
            }
            
            # Registros problemáticos
            if validacion['fuera_de_medellin'] > 0:
                problematicos = datos_validos[~dentro_limites]
                validacion['registros_problematicos'] = problematicos[['X', 'Y', 'id_punto']].to_dict('records') if 'id_punto' in self.datos.columns else problematicos[['X', 'Y']].to_dict('records')
        
        return validacion
    
    def crear_geodataframe(self) -> gpd.GeoDataFrame:
        """
        Convierte el DataFrame a GeoDataFrame
        
        Returns:
            GeoDataFrame con geometrías Point
        """
        # Filtrar registros con coordenadas válidas
        datos_validos = self.datos.dropna(subset=['X', 'Y'])
        
        if len(datos_validos) == 0:
            raise ValueError("No hay registros con coordenadas válidas")
        
        # Crear geometrías Point
        geometry = [Point(lon, lat) for lon, lat in zip(datos_validos['X'], datos_validos['Y'])]
        
        # Crear GeoDataFrame
        gdf = gpd.GeoDataFrame(datos_validos, geometry=geometry, crs='EPSG:4326')
        
        return gdf
    
    def generar_mapa_interactivo(self, titulo: str = "Obras de Infraestructura - Medellín",
                                incluir_cluster: bool = True,
                                incluir_heatmap: bool = False) -> folium.Map:
        """
        Genera un mapa interactivo con las obras georreferenciadas
        
        Args:
            titulo: Título del mapa
            incluir_cluster: Si incluir clustering de marcadores
            incluir_heatmap: Si incluir mapa de calor
            
        Returns:
            Objeto folium.Map
        """
        # Crear mapa base centrado en Medellín
        mapa = folium.Map(
            location=[self.centro_medellin['lat'], self.centro_medellin['lon']],
            zoom_start=self.zoom_default,
            tiles='OpenStreetMap'
        )
        
        # Agregar título
        title_html = f'''
        <h3 align="center" style="font-size:20px"><b>{titulo}</b></h3>
        '''
        mapa.get_root().html.add_child(folium.Element(title_html))
        
        # Filtrar datos válidos
        datos_validos = self.datos.dropna(subset=['X', 'Y'])
        
        if len(datos_validos) == 0:
            return mapa
        
        # Preparar datos para marcadores
        if incluir_cluster:
            marker_cluster = plugins.MarkerCluster().add_to(mapa)
        
        # Agregar marcadores
        for idx, row in datos_validos.iterrows():
            # Determinar color según estado
            color = self.colores_estados.get(
                row.get('estado_obr', 'default'), 
                self.colores_estados['default']
            )
            
            # Crear popup con información
            popup_content = self.crear_popup_info(row)
            
            # Crear marcador
            marcador = folium.CircleMarker(
                location=[row['Y'], row['X']],
                radius=8,
                popup=folium.Popup(popup_content, max_width=300),
                color='white',
                weight=2,
                fillColor=color,
                fillOpacity=0.7
            )
            
            if incluir_cluster:
                marcador.add_to(marker_cluster)
            else:
                marcador.add_to(mapa)
        
        # Agregar mapa de calor si se solicita
        if incluir_heatmap and len(datos_validos) > 0:
            heat_data = [[row['Y'], row['X']] for idx, row in datos_validos.iterrows()]
            heatmap = plugins.HeatMap(heat_data, radius=15, blur=15, max_zoom=1)
            
            # Crear feature group para el heatmap
            heat_fg = folium.FeatureGroup(name='Mapa de Calor')
            heat_fg.add_child(heatmap)
            mapa.add_child(heat_fg)
        
        # Agregar control de capas
        folium.LayerControl().add_to(mapa)
        
        # Agregar leyenda
        self.agregar_leyenda(mapa)
        
        # Agregar medidas
        plugins.MeasureControl().add_to(mapa)
        
        # Agregar pantalla completa
        plugins.Fullscreen().add_to(mapa)
        
        return mapa
    
    def crear_popup_info(self, row: pd.Series) -> str:
        """
        Crea el contenido HTML para el popup de información
        
        Args:
            row: Fila del DataFrame con información de la obra
            
        Returns:
            String con HTML del popup
        """
        # Información básica
        info_basica = f"""
        <div style="font-family: Arial, sans-serif; font-size: 12px;">
            <h4 style="margin: 0; color: #003366;">Obra de Infraestructura</h4>
            <hr style="margin: 5px 0;">
        """
        
        # ID del punto
        if 'id_punto' in row and pd.notna(row['id_punto']):
            info_basica += f"<b>ID:</b> {row['id_punto']}<br>"
        
        # Estado de la obra
        if 'estado_obr' in row and pd.notna(row['estado_obr']):
            info_basica += f"<b>Estado:</b> {row['estado_obr']}<br>"
        
        # Fecha de diligenciamiento
        if 'fecha_dilig' in row and pd.notna(row['fecha_dilig']):
            fecha = row['fecha_dilig'].strftime('%d/%m/%Y') if hasattr(row['fecha_dilig'], 'strftime') else str(row['fecha_dilig'])
            info_basica += f"<b>Fecha:</b> {fecha}<br>"
        
        # Coordenadas
        info_basica += f"<b>Coordenadas:</b> {row['Y']:.6f}, {row['X']:.6f}<br>"
        
        # Recursos humanos si están disponibles
        if 'cant_ayuda' in row and 'cant_ofici' in row:
            if pd.notna(row['cant_ayuda']) and pd.notna(row['cant_ofici']):
                total_personal = row['cant_ayuda'] + row['cant_ofici']
                info_basica += f"<b>Personal:</b> {total_personal} ({row['cant_ofici']} oficiales, {row['cant_ayuda']} ayudantes)<br>"
        
        # Horas de retraso si están disponibles
        if 'horas_retr' in row and pd.notna(row['horas_retr']) and row['horas_retr'] > 0:
            info_basica += f"<b>Horas de retraso:</b> {row['horas_retr']}<br>"
        
        info_basica += "</div>"
        return info_basica
    
    def agregar_leyenda(self, mapa: folium.Map):
        """
        Agrega una leyenda al mapa
        
        Args:
            mapa: Objeto folium.Map al que agregar la leyenda
        """
        leyenda_html = '''
        <div style="position: fixed; 
                    bottom: 50px; left: 50px; width: 200px; height: 120px; 
                    background-color: white; border:2px solid grey; z-index:9999; 
                    font-size:14px; padding: 10px">
            <h4 style="margin: 0; color: #003366;">Estados de Obra</h4>
            <hr style="margin: 5px 0;">
        '''
        
        for estado, color in self.colores_estados.items():
            if estado != 'default':
                leyenda_html += f'''
                <div>
                    <i class="fa fa-circle" style="color:{color}"></i>
                    <span style="margin-left: 5px;">{estado}</span>
                </div>
                '''
        
        leyenda_html += '</div>'
        mapa.get_root().html.add_child(folium.Element(leyenda_html))
    
    def generar_mapas_por_estado(self) -> Dict[str, folium.Map]:
        """
        Genera mapas separados por estado de obra
        
        Returns:
            Dict con mapas por cada estado
        """
        mapas = {}
        
        if 'estado_obr' not in self.datos.columns:
            return mapas
        
        estados = self.datos['estado_obr'].unique()
        
        for estado in estados:
            if pd.notna(estado):
                # Filtrar datos por estado
                datos_estado = self.datos[self.datos['estado_obr'] == estado]
                
                # Crear instancia temporal para este estado
                geo_temp = GeorreferenciadeSurvey123(datos_estado)
                
                # Generar mapa
                mapa = geo_temp.generar_mapa_interactivo(
                    titulo=f"Obras {estado} - Medellín",
                    incluir_cluster=False
                )
                
                mapas[estado] = mapa
        
        return mapas
    
    def analizar_densidad_geografica(self, grid_size: float = 0.01) -> pd.DataFrame:
        """
        Analiza la densidad geográfica de las obras
        
        Args:
            grid_size: Tamaño de la grilla en grados decimales
            
        Returns:
            DataFrame con análisis de densidad
        """
        datos_validos = self.datos.dropna(subset=['X', 'Y'])
        
        if len(datos_validos) == 0:
            return pd.DataFrame()
        
        # Crear grilla
        lat_bins = np.arange(
            datos_validos['Y'].min() - grid_size,
            datos_validos['Y'].max() + grid_size,
            grid_size
        )
        lon_bins = np.arange(
            datos_validos['X'].min() - grid_size,
            datos_validos['X'].max() + grid_size,
            grid_size
        )
        
        # Asignar puntos a celdas de la grilla
        datos_validos['lat_bin'] = pd.cut(datos_validos['Y'], lat_bins, include_lowest=True)
        datos_validos['lon_bin'] = pd.cut(datos_validos['X'], lon_bins, include_lowest=True)
        
        # Calcular densidad por celda
        densidad = datos_validos.groupby(['lat_bin', 'lon_bin']).agg({
            'X': ['count', 'mean'],
            'Y': 'mean'
        }).round(6)
        
        densidad.columns = ['cantidad_obras', 'lon_centro', 'lat_centro']
        densidad = densidad.reset_index()
        
        return densidad
    
    def exportar_datos_geograficos(self, ruta_salida: str = 'datos/mapas/', formato: str = 'todos'):
        """
        Exporta los datos geográficos en diferentes formatos
        
        Args:
            ruta_salida: Ruta donde guardar los archivos
            formato: 'geojson', 'shapefile', 'kml', 'todos'
        """
        os.makedirs(ruta_salida, exist_ok=True)
        
        try:
            gdf = self.crear_geodataframe()
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            archivos_generados = {}
            
            # GeoJSON
            if formato in ['geojson', 'todos']:
                archivo_geojson = f'{ruta_salida}obras_medellin_{timestamp}.geojson'
                gdf.to_file(archivo_geojson, driver='GeoJSON')
                archivos_generados['geojson'] = archivo_geojson
            
            # Shapefile
            if formato in ['shapefile', 'todos']:
                archivo_shp = f'{ruta_salida}obras_medellin_{timestamp}.shp'
                # Truncar nombres de columnas para shapefile (máximo 10 caracteres)
                gdf_shp = gdf.copy()
                gdf_shp.columns = [col[:10] for col in gdf_shp.columns]
                gdf_shp.to_file(archivo_shp, driver='ESRI Shapefile')
                archivos_generados['shapefile'] = archivo_shp
            
            # KML
            if formato in ['kml', 'todos']:
                archivo_kml = f'{ruta_salida}obras_medellin_{timestamp}.kml'
                gdf.to_file(archivo_kml, driver='KML')
                archivos_generados['kml'] = archivo_kml
            
            return archivos_generados
            
        except Exception as e:
            print(f"Error exportando datos geográficos: {e}")
            return {}
    
    def guardar_mapas(self, ruta_salida: str = 'datos/mapas/'):
        """
        Guarda los mapas generados como archivos HTML
        
        Args:
            ruta_salida: Ruta donde guardar los mapas
            
        Returns:
            Dict con las rutas de los mapas guardados
        """
        os.makedirs(ruta_salida, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        mapas_guardados = {}
        
        # Mapa principal
        mapa_principal = self.generar_mapa_interactivo()
        archivo_principal = f'{ruta_salida}mapa_obras_medellin_{timestamp}.html'
        mapa_principal.save(archivo_principal)
        mapas_guardados['principal'] = archivo_principal
        
        # Mapas por estado
        mapas_estados = self.generar_mapas_por_estado()
        for estado, mapa in mapas_estados.items():
            archivo_estado = f'{ruta_salida}mapa_{estado.lower().replace(" ", "_")}_{timestamp}.html'
            mapa.save(archivo_estado)
            mapas_guardados[f'estado_{estado}'] = archivo_estado
        
        return mapas_guardados

def procesar_georreferenciacion_completa(datos: pd.DataFrame) -> Dict[str, Any]:
    """
    Función principal para procesamiento completo de georreferenciación
    
    Args:
        datos: DataFrame con datos de Survey123
        
    Returns:
        Dict con todos los resultados del procesamiento
    """
    try:
        # Crear instancia del procesador
        geo_processor = GeorreferenciadeSurvey123(datos)
        
        # Validar coordenadas
        validacion = geo_processor.validar_coordenadas()
        
        # Generar mapas
        mapas_guardados = geo_processor.guardar_mapas()
        
        # Exportar datos geográficos
        archivos_geograficos = geo_processor.exportar_datos_geograficos()
        
        # Analizar densidad
        densidad = geo_processor.analizar_densidad_geografica()
        
        return {
            'validacion_coordenadas': validacion,
            'mapas_generados': mapas_guardados,
            'archivos_geograficos': archivos_geograficos,
            'analisis_densidad': densidad.to_dict('records') if not densidad.empty else [],
            'total_puntos_validos': validacion['coordenadas_validas'],
            'centro_geografico': {
                'lat': validacion['estadisticas'].get('lat_promedio', 0),
                'lon': validacion['estadisticas'].get('lon_promedio', 0)
            } if validacion['estadisticas'] else None
        }
        
    except Exception as e:
        return {
            'error': str(e),
            'validacion_coordenadas': None,
            'mapas_generados': {},
            'archivos_geograficos': {},
            'analisis_densidad': [],
            'total_puntos_validos': 0,
            'centro_geografico': None
        }

if __name__ == "__main__":
    print("Módulo de georreferenciación Survey123 - Secretaría de Infraestructura Física de Medellín")
    print("Para usar este módulo, importe la clase GeorreferenciadeSurvey123 y pase sus datos con coordenadas X, Y.")
