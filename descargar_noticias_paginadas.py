import requests
import json
import os
from datetime import datetime

def descargar_noticias_paginadas():
    """Descarga todas las noticias usando paginación y las guarda en un solo archivo JSON"""
    
    url = 'https://evat.oblek.com.mx/notas-api/notas'
    headers = {
        'accept': '*/*',
        'Authorization': 'Bearer xdrqzCwqUd4kMc/5Q5pJtKL6KGPq73dW'
    }
    
    # Parámetros base - Rango ampliado para obtener más de 500 noticias
    base_params = {
        'palabras': 'aduanas, ley, comercio exterior, turismo, aduanas, leyes',
        'fechaInicio': '2025-10-01',  # Desde 1 de octubre
        'fechaFin': '2025-10-22',      # Hasta 22 de octubre
        'limit': 500  # Primero obtener el total disponible
    }
    
    print("🚀 Iniciando descarga de noticias con paginación...")
    print("=" * 70)
    
    # Paso 1: Obtener el total de noticias disponibles
    print("\n1️⃣ Obteniendo total de noticias disponibles...")
    
    try:
        response = requests.get(url, headers=headers, params=base_params)
        response.raise_for_status()
        
        data = response.json()
        
        # Verificar estructura de datos
        if isinstance(data, dict) and 'notas' in data:
            total_noticias = len(data['notas'])
            total_disponibles = data.get('total', total_noticias)
            
            print(f"   ✅ Noticias en primera consulta: {total_noticias}")
            print(f"   📊 Total disponibles (según API): {total_disponibles}")
            
            # Si la API tiene un campo 'total' mayor que las noticias obtenidas,
            # necesitamos hacer consultas paginadas
            if total_disponibles > total_noticias:
                print(f"\n   ⚠️  Hay {total_disponibles} noticias pero solo se obtuvieron {total_noticias}")
                print(f"   🔄 Usando paginación para descargar todas las noticias...")
                
                # Descargar todas las páginas
                todas_las_noticias = []
                page = 1
                limit = 500  # Máximo permitido
                
                while True:
                    params = {**base_params, 'limit': limit, 'page': page}
                    
                    print(f"\n   📄 Descargando página {page}...")
                    page_response = requests.get(url, headers=headers, params=params)
                    page_response.raise_for_status()
                    
                    page_data = page_response.json()
                    
                    if isinstance(page_data, dict) and 'notas' in page_data:
                        notas_pagina = page_data['notas']
                        if not notas_pagina:  # No hay más noticias
                            break
                        
                        todas_las_noticias.extend(notas_pagina)
                        print(f"      ✅ Obtenidas {len(notas_pagina)} noticias (Total acumulado: {len(todas_las_noticias)})")
                        
                        # Si obtuvimos menos noticias de las esperadas, probablemente es la última página
                        if len(notas_pagina) < limit:
                            break
                        
                        # Si llegamos al total disponible, detener
                        if len(todas_las_noticias) >= total_disponibles:
                            break
                        
                        page += 1
                    else:
                        print(f"      ❌ Estructura inesperada en la página {page}")
                        break
                
                print(f"\n   🎉 Total de noticias descargadas: {len(todas_las_noticias)}")
                noticias_a_guardar = todas_las_noticias
                
            else:
                # No necesitamos paginación, usar las noticias obtenidas
                print(f"\n   ✅ Todas las noticias obtenidas en una sola consulta")
                noticias_a_guardar = data['notas']
        
        elif isinstance(data, list):
            # Si la respuesta es una lista directa
            print(f"   ✅ Lista con {len(data)} noticias")
            noticias_a_guardar = data
            
        else:
            print(f"   ❌ Estructura de datos inesperada")
            print(f"   Tipo: {type(data)}")
            print(f"   Claves: {list(data.keys()) if isinstance(data, dict) else 'N/A'}")
            return None
        
        # Paso 2: Guardar las noticias en un solo archivo JSON
        if noticias_a_guardar:
            print(f"\n2️⃣ Guardando {len(noticias_a_guardar)} noticias en un solo archivo JSON...")
            
            # Crear el nombre del archivo con timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"todas_las_noticias_{timestamp}.json"
            
            # Preparar los datos a guardar
            datos_completos = {
                'total': len(noticias_a_guardar),
                'fecha_descarga': datetime.now().isoformat(),
                'parametros_busqueda': base_params,
                'noticias': noticias_a_guardar
            }
            
            # Guardar el archivo JSON
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(datos_completos, f, ensure_ascii=False, indent=2)
            
            print(f"   ✅ Archivo creado: {filename}")
            print(f"   📊 Total de noticias guardadas: {len(noticias_a_guardar)}")
            
            # Mostrar un resumen de las primeras noticias
            if noticias_a_guardar:
                print(f"\n   📰 Primeras noticias:")
                for i, noticia in enumerate(noticias_a_guardar[:3], 1):
                    titulo = noticia.get('titulo', 'Sin título')
                    fecha = noticia.get('fecha', 'Sin fecha')
                    print(f"      {i}. {titulo[:60]}...")
                    print(f"         Fecha: {fecha}")
                
                if len(noticias_a_guardar) > 3:
                    print(f"      ... y {len(noticias_a_guardar) - 3} noticias más")
            
            print(f"\n✅ Proceso completado exitosamente!")
            print(f"📁 Archivo: {filename}")
            
            return filename
        else:
            print("\n⚠️  No se encontraron noticias para descargar")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error en la petición: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Error al decodificar JSON: {e}")
        return None
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    result = descargar_noticias_paginadas()
    if result:
        print(f"\n🎉 ¡Descarga completada! Archivo: {result}")
    else:
        print("\n❌ La descarga falló")
