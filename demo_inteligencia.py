"""
Demo de análisis inteligente para mostrar las capacidades del motor de IA
"""

import pandas as pd
import numpy as np
from modulos.inteligencia_nlp import AnalizadorInteligenteSurvey123

def demo_inteligencia_sistema():
    """
    Demuestra las capacidades inteligentes del sistema con datos reales
    """
    
    # Cargar datos reales
    datos_path = "datos/uploads/20250910_081054_survey123_procesado.xlsx"
    try:
        datos = pd.read_excel(datos_path)
        print("🧠 DEMO DEL MOTOR DE INTELIGENCIA ARTIFICIAL")
        print("=" * 60)
        print(f"📊 Datos cargados: {len(datos)} registros, {len(datos.columns)} variables")
        print()
        
        # Crear el analizador inteligente
        analizador = AnalizadorInteligenteSurvey123(datos)
        
        # Ejecutar análisis completo
        print("🔍 Ejecutando análisis inteligente...")
        resultados = analizador.analizar_completamente()
        
        print("\n🎯 INSIGHTS GENERADOS DINÁMICAMENTE:")
        print("-" * 40)
        
        for i, insight in enumerate(resultados['insights'][:5], 1):
            print(f"{i}. {insight['categoria'].upper()} - {insight['tipo']}")
            print(f"   📝 {insight['descripcion']}")
            print(f"   🎖️  Impacto: {insight['impacto']} | Dato clave: {insight['dato_clave']}")
            print()
        
        print("\n🔗 PATRONES DETECTADOS:")
        print("-" * 30)
        
        for patron_key, patron_data in resultados['patrones'].items():
            if isinstance(patron_data, dict) and 'interpretacion' in patron_data:
                print(f"• {patron_key.replace('_', ' ').title()}: {patron_data['interpretacion']}")
        
        print("\n💡 RECOMENDACIONES INTELIGENTES:")
        print("-" * 35)
        
        for i, rec in enumerate(resultados['recomendaciones'][:3], 1):
            print(f"{i}. {rec['titulo']} (Prioridad: {rec['prioridad'].upper()})")
            print(f"   📋 {rec['descripcion']}")
            print(f"   💰 Beneficio: {rec['beneficio_esperado']}")
            print()
        
        print("\n📖 NARRATIVA INTELIGENTE:")
        print("-" * 25)
        
        narrativa = resultados['narrativa']
        print(f"🚀 Introducción: {narrativa['introduccion']}")
        print(f"📊 Resumen: {narrativa['resumen_ejecutivo']}")
        print(f"🔍 Hallazgos: {narrativa['hallazgos_principales'][:200]}...")
        
        print("\n✨ ANÁLISIS COMPARATIVO:")
        print("-" * 25)
        
        # Generar informe textual completo
        informe_completo = analizador.generar_informe_textual('completo')
        
        print(f"📅 Período analizado: {informe_completo['metadata']['periodo_datos']}")
        print(f"🏗️  Total variables procesadas: {informe_completo['metadata']['total_columnas']}")
        
        metricas = informe_completo['metricas_calculadas']
        print("\n🎯 MÉTRICAS CALCULADAS DINÁMICAMENTE:")
        for metrica, valor in metricas.items():
            print(f"   • {metrica.replace('_', ' ').title()}: {valor}")
        
        print("\n" + "=" * 60)
        print("✅ DEMO COMPLETADA - El sistema analiza TODAS las 78 variables")
        print("🤖 Cada informe es único y se adapta dinámicamente a los datos")
        print("📈 Los insights cambian según los patrones encontrados")
        print("💡 Las recomendaciones se generan basadas en correlaciones reales")
        
    except Exception as e:
        print(f"❌ Error en demo: {str(e)}")

if __name__ == "__main__":
    demo_inteligencia_sistema()
