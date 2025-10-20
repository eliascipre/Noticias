import json
import os
from datetime import datetime

def contar_noticias():
    """Cuenta las noticias en el archivo JSON descargado"""
    
    # Buscar el archivo JSON más reciente
    json_file = None
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file == 'documento_completo.json':
                json_file = os.path.join(root, file)
                break
        if json_file:
            break
    
    if not json_file:
        print("❌ No se encontró el archivo documento_completo.json")
        return
    
    print(f"📁 Analizando archivo: {json_file}")
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("\n📊 INFORMACIÓN GENERAL:")
        print(f"✅ Éxito: {data.get('success', 'No disponible')}")
        print(f"📈 Total reportado: {data.get('total', 'No disponible')}")
        print(f"🔢 Límite: {data.get('limit', 'No disponible')}")
        
        # Información de filtros
        if 'filtros' in data:
            filtros = data['filtros']
            print(f"\n📅 PERÍODO CONSULTADO:")
            print(f"   Fecha inicio: {filtros.get('fechaInicio', 'No disponible')}")
            print(f"   Fecha fin: {filtros.get('fechaFin', 'No disponible')}")
            print(f"   Palabras buscadas: {', '.join(filtros.get('palabrasBuscadas', []))}")
        
        # Información de metadata
        if 'metadata' in data:
            metadata = data['metadata']
            print(f"\n📋 METADATOS:")
            print(f"   Base de datos actual: {metadata.get('baseDatos', {}).get('actual', 'No disponible')}")
            print(f"   Resultados actuales: {metadata.get('resultados', {}).get('actual', 'No disponible')}")
            print(f"   Resultados históricos: {metadata.get('resultados', {}).get('historica', 'No disponible')}")
        
        # Contar noticias reales
        if 'notas' in data and isinstance(data['notas'], list):
            total_noticias = len(data['notas'])
            print(f"\n🔍 CONTEO REAL DE NOTICIAS:")
            print(f"   Número de noticias en el array: {total_noticias}")
            
            # Analizar fechas de las noticias
            fechas = []
            for nota in data['notas']:
                if 'fecha' in nota:
                    fecha_str = nota['fecha']
                    try:
                        # Convertir a datetime para análisis
                        fecha = datetime.fromisoformat(fecha_str.replace('Z', '+00:00'))
                        fechas.append(fecha)
                    except:
                        fechas.append(fecha_str)
            
            if fechas:
                fechas_ordenadas = sorted(fechas)
                print(f"   Fecha más antigua: {fechas_ordenadas[0]}")
                print(f"   Fecha más reciente: {fechas_ordenadas[-1]}")
                
                # Contar por día
                fechas_por_dia = {}
                for fecha in fechas:
                    if isinstance(fecha, datetime):
                        dia = fecha.strftime('%Y-%m-%d')
                    else:
                        dia = str(fecha)[:10]  # Tomar solo la parte de la fecha
                    
                    fechas_por_dia[dia] = fechas_por_dia.get(dia, 0) + 1
                
                print(f"\n📅 NOTICIAS POR DÍA:")
                for dia, cantidad in sorted(fechas_por_dia.items()):
                    print(f"   {dia}: {cantidad} noticias")
            
            # Verificar si hay duplicados por título
            titulos = [nota.get('titulo', '') for nota in data['notas'] if 'titulo' in nota]
            titulos_unicos = set(titulos)
            print(f"\n🔍 ANÁLISIS DE DUPLICADOS:")
            print(f"   Total títulos: {len(titulos)}")
            print(f"   Títulos únicos: {len(titulos_unicos)}")
            print(f"   Duplicados: {len(titulos) - len(titulos_unicos)}")
            
            # Identificar duplicados específicos
            from collections import Counter
            contador_titulos = Counter(titulos)
            duplicados = {titulo: count for titulo, count in contador_titulos.items() if count > 1}
            
            if duplicados:
                print(f"\n📋 NOTICIAS DUPLICADAS DETALLADAS:")
                for i, (titulo, cantidad) in enumerate(sorted(duplicados.items(), key=lambda x: x[1], reverse=True), 1):
                    print(f"\n   {i}. Título: '{titulo[:80]}{'...' if len(titulo) > 80 else ''}'")
                    print(f"      Cantidad: {cantidad} veces")
                    
                    # Buscar las posiciones de este título duplicado
                    posiciones = []
                    for idx, nota in enumerate(data['notas']):
                        if nota.get('titulo', '') == titulo:
                            fecha = nota.get('fecha', 'Sin fecha')
                            programa = nota.get('nombre_programa', 'Sin programa')
                            posiciones.append(f"Posición {idx+1} - {fecha} - {programa}")
                    
                    print(f"      Ubicaciones:")
                    for pos in posiciones[:5]:  # Mostrar máximo 5 ubicaciones
                        print(f"        • {pos}")
                    if len(posiciones) > 5:
                        print(f"        • ... y {len(posiciones) - 5} más")
            else:
                print(f"\n✅ No se encontraron duplicados por título")
            
        else:
            print("❌ No se encontró el array 'notas' en el JSON")
            
    except json.JSONDecodeError as e:
        print(f"❌ Error al decodificar JSON: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    print("🔍 Analizando noticias descargadas...")
    contar_noticias()
