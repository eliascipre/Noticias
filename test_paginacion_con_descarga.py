import requests
import json
import os
from datetime import datetime
import re

def sanitize_filename(filename):
    """Limpia el nombre del archivo para que sea válido en el sistema de archivos"""
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    filename = filename.replace(' ', '_')
    return filename[:100]

def descargar_noticias_paginadas():
    """Descarga todas las noticias usando paginación y las guarda organizadas"""
    
    url = 'https://evat.oblek.com.mx/notas-api/notas'
    headers = {
        'accept': '*/*',
        'Authorization': 'Bearer xdrqzCwqUd4kMc/5Q5pJtKL6KGPq73dW'
    }
    
    # Parámetros base
    base_params = {
        'palabras': 'aduanas, ley, comercio exterior, turismo, aduanas, leyes',
        'fechaInicio': '2025-10-19',
        'fechaFin': '2025-10-20',
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
        
        # Paso 2: Guardar las noticias descargadas
        if noticias_a_guardar:
            print(f"\n2️⃣ Guardando {len(noticias_a_guardar)} noticias...")
            
            # Crear carpeta principal para los documentos
            main_folder = f"documentos_noticias_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.makedirs(main_folder, exist_ok=True)
            
            # Guardar el JSON completo con todas las noticias
            with open(os.path.join(main_folder, 'todas_las_noticias.json'), 'w', encoding='utf-8') as f:
                json.dump({
                    'total': len(noticias_a_guardar),
                    'fecha_descarga': datetime.now().isoformat(),
                    'parametros_busqueda': base_params,
                    'noticias': noticias_a_guardar
                }, f, ensure_ascii=False, indent=2)
            
            print(f"   ✅ Archivo JSON creado: todas_las_noticias.json")
            
            # Guardar cada noticia individualmente
            for i, item in enumerate(noticias_a_guardar):
                # Crear nombre único para la carpeta de cada noticia
                if 'titulo' in item:
                    folder_name = f"{i+1:04d}_{sanitize_filename(item['titulo'])}"
                elif 'title' in item:
                    folder_name = f"{i+1:04d}_{sanitize_filename(item['title'])}"
                else:
                    folder_name = f"noticia_{i+1:04d}"
                
                # Crear carpeta para esta noticia
                item_folder = os.path.join(main_folder, folder_name)
                os.makedirs(item_folder, exist_ok=True)
                
                # Guardar el JSON completo de la noticia
                with open(os.path.join(item_folder, 'noticia_completa.json'), 'w', encoding='utf-8') as f:
                    json.dump(item, f, ensure_ascii=False, indent=2)
                
                # Guardar campos específicos si existen
                if 'contenido' in item or 'content' in item:
                    content = item.get('contenido', item.get('content', ''))
                    with open(os.path.join(item_folder, 'contenido.txt'), 'w', encoding='utf-8') as f:
                        f.write(content)
                
                if 'resumen' in item or 'summary' in item:
                    summary = item.get('resumen', item.get('summary', ''))
                    with open(os.path.join(item_folder, 'resumen.txt'), 'w', encoding='utf-8') as f:
                        f.write(summary)
                
                # Guardar metadatos
                metadata = {
                    'fecha_creacion': datetime.now().isoformat(),
                    'id_noticia': item.get('id', f'noticia_{i+1}'),
                    'fuente': item.get('fuente', item.get('source', 'Desconocida')),
                    'fecha_publicacion': item.get('fecha', item.get('date', 'No disponible')),
                    'numero_noticia': i + 1
                }
                
                with open(os.path.join(item_folder, 'metadatos.json'), 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, ensure_ascii=False, indent=2)
                
                # Mostrar progreso cada 50 noticias
                if (i + 1) % 50 == 0:
                    print(f"   📝 Guardadas {i+1}/{len(noticias_a_guardar)} noticias...")
            
            print(f"\n✅ Proceso completado exitosamente!")
            print(f"📁 Total de noticias descargadas: {len(noticias_a_guardar)}")
            print(f"📂 Carpeta de destino: {main_folder}")
            
            return main_folder
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
        return None


if __name__ == "__main__":
    result = descargar_noticias_paginadas()
    if result:
        print(f"\n🎉 ¡Descarga completada! Archivos guardados en: {result}")
    else:
        print("\n❌ La descarga falló")
