import requests
import json
import os
from datetime import datetime
import re

def sanitize_filename(filename):
    """Limpia el nombre del archivo para que sea válido en el sistema de archivos"""
    # Remover caracteres no válidos y reemplazar espacios con guiones bajos
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    filename = filename.replace(' ', '_')
    # Limitar la longitud del nombre
    return filename[:100]

def save_documents():
    """Hace la petición a la API y guarda los documentos organizados por noticia"""
    
    # URL y headers de la API
    url = 'https://evat.oblek.com.mx/notas-api/notas'
    headers = {
        'accept': '*/*',
        'Authorization': 'Bearer xdrqzCwqUd4kMc/5Q5pJtKL6KGPq73dW'
    }
    
    # Parámetros de la consulta
    params = {
        'palabras': 'aduanas, ley, comercio exterior, turismo, aduanas, leyes',
        'fechaInicio': '2025-10-16',
        'fechaFin': '2025-10-17',
        'limit': 500
    }
    
    try:
        print("Haciendo petición a la API...")
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        print(f"Respuesta recibida: {len(data) if isinstance(data, list) else 'Objeto único'}")
        
        # Crear carpeta principal para los documentos
        main_folder = f"documentos_noticias_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(main_folder, exist_ok=True)
        
        # Procesar cada noticia/documento
        if isinstance(data, list):
            for i, item in enumerate(data):
                # Crear nombre único para la carpeta de cada noticia
                if 'titulo' in item:
                    folder_name = f"{i+1:03d}_{sanitize_filename(item['titulo'])}"
                elif 'title' in item:
                    folder_name = f"{i+1:03d}_{sanitize_filename(item['title'])}"
                else:
                    folder_name = f"noticia_{i+1:03d}"
                
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
                    'fecha_publicacion': item.get('fecha', item.get('date', 'No disponible'))
                }
                
                with open(os.path.join(item_folder, 'metadatos.json'), 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, ensure_ascii=False, indent=2)
                
                print(f"Guardada noticia {i+1}: {folder_name}")
        
        else:
            # Si es un solo objeto, guardarlo también
            folder_name = "documento_unico"
            item_folder = os.path.join(main_folder, folder_name)
            os.makedirs(item_folder, exist_ok=True)
            
            with open(os.path.join(item_folder, 'documento_completo.json'), 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"Guardado documento único en: {folder_name}")
        
        print(f"\n✅ Proceso completado. Documentos guardados en: {main_folder}")
        return main_folder
        
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
    print("🚀 Iniciando descarga y organización de documentos...")
    result = save_documents()
    if result:
        print(f"📁 Los documentos se han guardado en la carpeta: {result}")
    else:
        print("❌ No se pudieron guardar los documentos") 