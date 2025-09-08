"""
Modelos de datos para el sistema de informes Survey123
Secretaría de Infraestructura Física de Medellín
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Union
from enum import Enum
import pandas as pd

class EstadoObra(Enum):
    """Estados posibles de una obra"""
    SIN_INICIAR = "Sin iniciar"
    EN_EJECUCION = "En ejecución"
    EN_EJECUCION_ALT = "En ejecucion"  # Variante sin tilde
    FINALIZADA = "Finalizada"
    
    @classmethod
    def from_string(cls, valor: str):
        """Crear EstadoObra desde string con flexibilidad"""
        # Manejar valores None o float
        if valor is None or pd.isna(valor):
            return cls.SIN_INICIAR
        
        # Convertir a string si es necesario
        if not isinstance(valor, str):
            valor = str(valor)
        
        valor_normalizado = valor.strip().lower()
        
        # Mapeo de valores
        mapeo = {
            'sin iniciar': cls.SIN_INICIAR,
            'en ejecución': cls.EN_EJECUCION,
            'en ejecucion': cls.EN_EJECUCION,  # Maneja ambas variantes
            'finalizada': cls.FINALIZADA,
            'finalizado': cls.FINALIZADA
        }
        
        return mapeo.get(valor_normalizado, cls.SIN_INICIAR)

class TipoMaquinaria(Enum):
    """Tipos de maquinaria disponibles"""
    RETROEXCAVADORA = "Retroexcavadora"
    MINICARGADOR = "Minicargador"
    VOLQUETA = "Volqueta"
    COMPACTADORA = "Compactadora"
    OTRA = "Otra"

@dataclass
class DatosGenerales:
    """Datos generales de una intervención"""
    id_punto: str
    estado_obra: EstadoObra
    fecha_diligenciamiento: datetime
    nombre_interventor: str
    coordenada_x: float
    coordenada_y: float
    fecha_inicio: Optional[datetime] = None
    shape: Optional[str] = None

@dataclass
class RecursosHumanos:
    """Recursos humanos asignados a una intervención"""
    num_cuadrillas: int = 0
    trabajadores_por_cuadrilla: int = 0
    cant_ayudantes: int = 0
    cant_oficiales: int = 0
    cant_operadores: int = 0
    cant_auxiliares_transito: int = 0
    cant_otros: int = 0
    total_trabajadores: int = 0
    total_horas_trabajadas: float = 0.0
    
    def __post_init__(self):
        """Calcular total de trabajadores automáticamente"""
        if self.total_trabajadores == 0:
            self.total_trabajadores = (
                self.cant_ayudantes + self.cant_oficiales + 
                self.cant_operadores + self.cant_auxiliares_transito + 
                self.cant_otros
            )
    
    def validar_consistencia(self) -> bool:
        """Validar que el total reportado coincida con la suma"""
        total_calculado = (
            self.cant_ayudantes + self.cant_oficiales + 
            self.cant_operadores + self.cant_auxiliares_transito + 
            self.cant_otros
        )
        return self.total_trabajadores == total_calculado
    
    def obtener_distribucion(self) -> Dict[str, int]:
        """Obtener distribución de trabajadores por tipo"""
        return {
            "Ayudantes": self.cant_ayudantes,
            "Oficiales": self.cant_oficiales,
            "Operadores": self.cant_operadores,
            "Auxiliares de Tránsito": self.cant_auxiliares_transito,
            "Otros": self.cant_otros
        }

@dataclass
class Maquinaria:
    """Maquinaria utilizada en una intervención"""
    tipo_principal: Optional[TipoMaquinaria] = None
    horas_retroexcavadora: float = 0.0
    horas_minicargador: float = 0.0
    horas_volqueta: float = 0.0
    horas_compactadora: float = 0.0
    nombre_otra_maquinaria: Optional[str] = None
    horas_otra_maquinaria: float = 0.0
    
    def calcular_total_horas(self) -> float:
        """Calcular total de horas de maquinaria"""
        return (
            self.horas_retroexcavadora + self.horas_minicargador +
            self.horas_volqueta + self.horas_compactadora +
            self.horas_otra_maquinaria
        )
    
    def obtener_distribucion_horas(self) -> Dict[str, float]:
        """Obtener distribución de horas por tipo de maquinaria"""
        return {
            "Retroexcavadora": self.horas_retroexcavadora,
            "Minicargador": self.horas_minicargador,
            "Volqueta": self.horas_volqueta,
            "Compactadora": self.horas_compactadora,
            "Otra": self.horas_otra_maquinaria
        }

@dataclass
class ActividadesPreliminares:
    """Actividades preliminares de una intervención"""
    localizacion_replanteo: float = 0.0
    descapote_total: float = 0.0
    descapote_manual: float = 0.0
    descapote_mecanico: float = 0.0
    tala_poda: float = 0.0
    roceria_limpieza: float = 0.0
    cerramiento_total: float = 0.0
    tela_verde: float = 0.0
    malla_naranja: float = 0.0
    teja_ondulada: float = 0.0
    cubierta_plastica: float = 0.0
    pasarela_peatonal: float = 0.0
    
    def calcular_total_descapote(self) -> float:
        """Calcular total de descapote"""
        return self.descapote_manual + self.descapote_mecanico

@dataclass
class ActividadesPrincipales:
    """Actividades principales de construcción"""
    retiros: Dict[str, float] = field(default_factory=dict)
    demoliciones: Dict[str, float] = field(default_factory=dict)
    excavaciones: Dict[str, float] = field(default_factory=dict)
    rellenos: Dict[str, float] = field(default_factory=dict)
    concretos: Dict[str, float] = field(default_factory=dict)
    senalizacion: Dict[str, float] = field(default_factory=dict)
    paisajismo: Dict[str, float] = field(default_factory=dict)
    otros: Dict[str, float] = field(default_factory=dict)

@dataclass
class Intervencion:
    """
    Modelo principal que representa una intervención completa
    """
    datos_generales: DatosGenerales
    recursos_humanos: RecursosHumanos
    maquinaria: Maquinaria
    actividades_preliminares: ActividadesPreliminares
    actividades_principales: ActividadesPrincipales
    datos_originales: Dict = field(default_factory=dict)  # Agregar datos originales completos
    
    def __post_init__(self):
        """Validaciones post-inicialización"""
        self.validar_datos()
    
    def validar_datos(self) -> List[str]:
        """
        Validar todos los datos de la intervención
        
        Returns:
            List[str]: Lista de errores encontrados
        """
        errores = []
        
        # Validar coordenadas
        if not (-76 <= self.datos_generales.coordenada_x <= -75):
            errores.append("Coordenada X fuera del rango de Medellín")
        
        if not (6 <= self.datos_generales.coordenada_y <= 7):
            errores.append("Coordenada Y fuera del rango de Medellín")
        
        # Validar recursos humanos
        if not self.recursos_humanos.validar_consistencia():
            errores.append("Inconsistencia en total de trabajadores")
        
        # Validar fechas
        if self.datos_generales.fecha_inicio and self.datos_generales.fecha_diligenciamiento:
            if self.datos_generales.fecha_inicio > self.datos_generales.fecha_diligenciamiento:
                errores.append("Fecha de inicio posterior a fecha de diligenciamiento")
        
        return errores
    
    def calcular_kpis(self) -> 'KPI':
        """Calcular KPIs de la intervención"""
        return KPI(
            total_trabajadores=self.recursos_humanos.total_trabajadores,
            total_horas_humanas=self.recursos_humanos.total_horas_trabajadas,
            total_horas_maquinaria=self.maquinaria.calcular_total_horas(),
            total_descapote=self.actividades_preliminares.calcular_total_descapote(),
            eficiencia_horas_trabajador=(
                self.recursos_humanos.total_horas_trabajadas / 
                max(self.recursos_humanos.total_trabajadores, 1)
            ),
            estado_obra=self.datos_generales.estado_obra
        )
    
    @classmethod
    def desde_dataframe_fila(cls, fila: pd.Series) -> 'Intervencion':
        """
        Crear una instancia de Intervención desde una fila de DataFrame
        
        Args:
            fila: Fila del DataFrame con datos de Survey123
            
        Returns:
            Intervencion: Instancia creada
        """
        # Convertir la fila completa a diccionario para preservar TODOS los datos originales
        datos_originales = fila.to_dict()
        
        # Datos generales
        datos_generales = DatosGenerales(
            id_punto=str(fila.get('id_punto', '')),
            estado_obra=EstadoObra.from_string(str(fila.get('estado_obr', 'Sin iniciar'))),
            fecha_diligenciamiento=pd.to_datetime(fila.get('fecha_dilig')),
            nombre_interventor=str(fila.get('nombre_int', '')),
            coordenada_x=float(fila.get('X', 0)),
            coordenada_y=float(fila.get('Y', 0)),
            fecha_inicio=pd.to_datetime(fila.get('start')) if pd.notna(fila.get('start')) else None,
            shape=str(fila.get('Shape', ''))
        )
        
        # Recursos humanos
        recursos_humanos = RecursosHumanos(
            num_cuadrillas=int(fila.get('num_cuadri', 0)),
            trabajadores_por_cuadrilla=int(fila.get('trabajador', 0)),
            cant_ayudantes=int(fila.get('cant_ayuda', 0)),
            cant_oficiales=int(fila.get('cant_ofici', 0)),
            cant_operadores=int(fila.get('cant_opera', 0)),
            cant_auxiliares_transito=int(fila.get('cant_auxil', 0)),
            cant_otros=int(fila.get('cant_otros', 0)),
            total_trabajadores=int(fila.get('num_total_', 0)),
            total_horas_trabajadas=float(fila.get('total_hora', 0))
        )
        
        # Maquinaria
        tipo_maq = fila.get('maquinaria')
        tipo_principal = None
        if tipo_maq and str(tipo_maq).strip():
            # Convertir a string y normalizar para comparación
            tipo_maq_str = str(tipo_maq)
            for tipo in TipoMaquinaria:
                if tipo_maq_str.lower() in tipo.value.lower():
                    tipo_principal = tipo
                    break
        
        maquinaria = Maquinaria(
            tipo_principal=tipo_principal,
            horas_retroexcavadora=float(fila.get('horas_retr', 0)),
            horas_minicargador=float(fila.get('horas_mini', 0)),
            horas_volqueta=float(fila.get('horas_volq', 0)),
            horas_compactadora=float(fila.get('horas_comp', 0)),
            nombre_otra_maquinaria=str(fila.get('nombre_otr', '')),
            horas_otra_maquinaria=float(fila.get('horas_otra', 0))
        )
        
        # Actividades preliminares
        actividades_preliminares = ActividadesPreliminares(
            localizacion_replanteo=float(fila.get('localizaci', 0)),
            descapote_total=float(fila.get('descapote', 0)),
            descapote_manual=float(fila.get('a_mano', 0)),
            descapote_mecanico=float(fila.get('a_maquina', 0)),
            tala_poda=float(fila.get('Tala_poda', 0)),
            roceria_limpieza=float(fila.get('roceria_li', 0)),
            cerramiento_total=float(fila.get('cerramient', 0)),
            tela_verde=float(fila.get('tela_verde', 0)),
            malla_naranja=float(fila.get('malla_nara', 0)),
            teja_ondulada=float(fila.get('teja_ondul', 0)),
            cubierta_plastica=float(fila.get('cubierta_p', 0)),
            pasarela_peatonal=float(fila.get('pasarela_p', 0))
        )
        
        # Actividades principales (simplificado por ahora)
        actividades_principales = ActividadesPrincipales()
        
        return cls(
            datos_generales=datos_generales,
            recursos_humanos=recursos_humanos,
            maquinaria=maquinaria,
            actividades_preliminares=actividades_preliminares,
            actividades_principales=actividades_principales,
            datos_originales=datos_originales  # Incluir TODOS los datos originales
        )

@dataclass
class KPI:
    """Indicadores clave de desempeño"""
    total_trabajadores: int = 0
    total_horas_humanas: float = 0.0
    total_horas_maquinaria: float = 0.0
    total_descapote: float = 0.0
    eficiencia_horas_trabajador: float = 0.0
    estado_obra: EstadoObra = EstadoObra.SIN_INICIAR
    
    def generar_resumen(self) -> Dict[str, Union[int, float, str]]:
        """Generar resumen de KPIs"""
        return {
            "Total de Trabajadores": self.total_trabajadores,
            "Total de Horas Humanas": round(self.total_horas_humanas, 2),
            "Total de Horas de Maquinaria": round(self.total_horas_maquinaria, 2),
            "Total de Descapote (m²)": round(self.total_descapote, 2),
            "Eficiencia (horas/trabajador)": round(self.eficiencia_horas_trabajador, 2),
            "Estado de la Obra": self.estado_obra.value
        }

class RepositorioIntervenciones:
    """Repositorio para gestionar múltiples intervenciones"""
    
    def __init__(self):
        self.intervenciones: List[Intervencion] = []
    
    def agregar_intervencion(self, intervencion: Intervencion):
        """Agregar una intervención al repositorio"""
        self.intervenciones.append(intervencion)
    
    def desde_dataframe(self, df: pd.DataFrame) -> List[Intervencion]:
        """
        Crear intervenciones desde un DataFrame completo
        
        Args:
            df: DataFrame con datos de Survey123
            
        Returns:
            List[Intervencion]: Lista de intervenciones creadas
        """
        self.intervenciones = []
        
        for _, fila in df.iterrows():
            try:
                intervencion = Intervencion.desde_dataframe_fila(fila)
                self.agregar_intervencion(intervencion)
            except Exception as e:
                print(f"Error procesando fila {fila.get('id_punto', 'unknown')}: {e}")
        
        return self.intervenciones
    
    def calcular_kpis_agregados(self) -> KPI:
        """Calcular KPIs agregados de todas las intervenciones"""
        if not self.intervenciones:
            return KPI()
        
        total_trabajadores = sum(i.recursos_humanos.total_trabajadores for i in self.intervenciones)
        total_horas_humanas = sum(i.recursos_humanos.total_horas_trabajadas for i in self.intervenciones)
        total_horas_maquinaria = sum(i.maquinaria.calcular_total_horas() for i in self.intervenciones)
        total_descapote = sum(i.actividades_preliminares.calcular_total_descapote() for i in self.intervenciones)
        
        eficiencia = total_horas_humanas / max(total_trabajadores, 1)
        
        return KPI(
            total_trabajadores=total_trabajadores,
            total_horas_humanas=total_horas_humanas,
            total_horas_maquinaria=total_horas_maquinaria,
            total_descapote=total_descapote,
            eficiencia_horas_trabajador=eficiencia
        )
    
    def filtrar_por_estado(self, estado: EstadoObra) -> List[Intervencion]:
        """Filtrar intervenciones por estado"""
        return [i for i in self.intervenciones if i.datos_generales.estado_obra == estado]
    
    def obtener_estadisticas(self) -> Dict:
        """Obtener estadísticas generales del repositorio"""
        if not self.intervenciones:
            return {}
        
        # Crear DataFrame para análisis completo con TODAS las 78 variables
        datos_para_analisis = []
        for interv in self.intervenciones:
            # Obtener datos originales completos desde el procesador
            datos_originales = interv.datos_originales if hasattr(interv, 'datos_originales') else {}
            
            # Mapear TODAS las 78 variables del Survey123
            registro_completo = {
                # Variables básicas de geometría y identificación
                'Shape': datos_originales.get('Shape', None),
                'X': interv.datos_generales.coordenada_x,
                'Y': interv.datos_generales.coordenada_y,
                'start': datos_originales.get('start', None),
                'id_punto': interv.datos_generales.id_punto,
                'estado_obr': interv.datos_generales.estado_obra.value,
                'fecha_dilig': interv.datos_generales.fecha_diligenciamiento,
                'nombre_int': datos_originales.get('nombre_int', None),
                'num_cuadri': datos_originales.get('num_cuadri', None),
                
                # Recursos humanos (trabajadores)
                'trabajador': datos_originales.get('trabajador', None),
                'cant_ayuda': interv.recursos_humanos.cant_ayudantes,
                'cant_ofici': interv.recursos_humanos.cant_oficiales,
                'cant_opera': interv.recursos_humanos.cant_operadores,
                'cant_auxil': interv.recursos_humanos.cant_auxiliares_transito,
                'cant_otros': interv.recursos_humanos.cant_otros,
                'num_total_': interv.recursos_humanos.total_trabajadores,
                'total_hora': interv.recursos_humanos.total_horas_trabajadas,
                
                # Maquinaria
                'maquinaria': datos_originales.get('maquinaria', None),
                'horas_retr': interv.maquinaria.horas_retroexcavadora,
                'horas_mini': interv.maquinaria.horas_minicargador,
                'horas_volq': interv.maquinaria.horas_volqueta,
                'horas_comp': interv.maquinaria.horas_compactadora,
                'nombre_otr': datos_originales.get('nombre_otr', None),
                'horas_otra': interv.maquinaria.horas_otra_maquinaria,
                
                # Localización y preparación del terreno
                'localizaci': datos_originales.get('localizaci', None),
                'descapote': datos_originales.get('descapote', None),
                'a_mano': datos_originales.get('a_mano', None),
                'a_maquina': datos_originales.get('a_maquina', None),
                'Tala_poda': datos_originales.get('Tala_poda', None),
                'roceria_li': datos_originales.get('roceria_li', None),
                
                # Cerramientos y protección
                'cerramient': datos_originales.get('cerramient', None),
                'tela_verde': datos_originales.get('tela_verde', None),
                'malla_nara': datos_originales.get('malla_nara', None),
                'teja_ondul': datos_originales.get('teja_ondul', None),
                'cubierta_p': datos_originales.get('cubierta_p', None),
                'pasarela_p': datos_originales.get('pasarela_p', None),
                'proteccion': datos_originales.get('proteccion', None),
                'protecci_vehicular': datos_originales.get('protecci_vehicular', None),
                
                # Limpieza y mantenimiento
                'limpieza_e': datos_originales.get('limpieza_e', None),
                'limpieza_s': datos_originales.get('limpieza_s', None),
                'malla_esla': datos_originales.get('malla_esla', None),
                
                # Infraestructura hídrica
                'canoas_rua': datos_originales.get('canoas_rua', None),
                'bajantes': datos_originales.get('bajantes', None),
                'tuberia_en': datos_originales.get('tuberia_en', None),
                
                # Estructuras de seguridad
                'cerco_made': datos_originales.get('cerco_made', None),
                'pintura_ba': datos_originales.get('pintura_ba', None),
                'pasamanos_': datos_originales.get('pasamanos_', None),
                'barrera_me': datos_originales.get('barrera_me', None),
                'pintura_pa': datos_originales.get('pintura_pa', None),
                
                # Elementos de servicio
                'aparatos_s': datos_originales.get('aparatos_s', None),
                'puertas': datos_originales.get('puertas', None),
                'senal_vert': datos_originales.get('senal_vert', None),
                'reparacion': datos_originales.get('reparacion', None),
                'ventanas': datos_originales.get('ventanas', None),
                
                # Pavimentación
                'teja_barro': datos_originales.get('teja_barro', None),
                'piso_adoqu': datos_originales.get('piso_adoqu', None),
                'piso_ado_1': datos_originales.get('piso_ado_1', None),
                
                # Drenajes
                'cordones_c': datos_originales.get('cordones_c', None),
                'carcamos_c': datos_originales.get('carcamos_c', None),
                'Cunetas_co': datos_originales.get('Cunetas_co', None),
                
                # Trabajos en roca
                'roca_cielo_cuña': datos_originales.get('roca_cielo_cuña', None),
                'roca_cielo_martillo': datos_originales.get('roca_cielo_martillo', None),
                'roca_pila_': datos_originales.get('roca_pila_', None),
                
                # Concreto
                'e_concreto': datos_originales.get('e_concreto', None),
                
                # Excavaciones
                'excav_manu': datos_originales.get('excav_manu', None),
                'excav_ma_1': datos_originales.get('excav_ma_1', None),
                'excav_meca': datos_originales.get('excav_meca', None),
                'excav_me_1': datos_originales.get('excav_me_1', None),
                'excav_me_2': datos_originales.get('excav_me_2', None),
                'excav_me_3': datos_originales.get('excav_me_3', None),
                'explanacio': datos_originales.get('explanacio', None),
                'explanac_1': datos_originales.get('explanac_1', None),
                
                # Cortes y taludes
                'corte_talu': datos_originales.get('corte_talu', None),
                'corte_ta_1': datos_originales.get('corte_ta_1', None),
                'corte_ta_2': datos_originales.get('corte_ta_2', None),
                'excav_terrazas': datos_originales.get('excav_terrazas', None),
                
                # Drenaje perimetral y transporte
                'drenaje_pe': datos_originales.get('drenaje_pe', None),
                'transpor_1': datos_originales.get('transpor_1', None)
            }
            
            datos_para_analisis.append(registro_completo)
        
        df_analisis = pd.DataFrame(datos_para_analisis)
        
        # Importar y usar el analizador
        from .analisis import AnalisisSurvey123
        analizador = AnalisisSurvey123(df_analisis)
        
        # Generar análisis completo
        estadisticas_completas = analizador.generar_analisis_completo()
        
        # Agregar estadísticas básicas del repositorio
        estados = {}
        for estado in EstadoObra:
            count = len(self.filtrar_por_estado(estado))
            estados[estado.value] = count
        
        estadisticas_completas.update({
            "total_intervenciones": len(self.intervenciones),
            "distribucion_estados": estados,
            "kpis_agregados": self.calcular_kpis_agregados().generar_resumen()
        })
        
        return estadisticas_completas
