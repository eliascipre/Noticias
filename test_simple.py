import requests
import json

def test_api_simple():
    """Prueba simple de la API replicando exactamente el comportamiento de curl"""
    
    url = 'https://evat.oblek.com.mx/notas-api/notas'
    headers = {
        'accept': '*/*',
        'Authorization': 'Bearer xdrqzCwqUd4kMc/5Q5pJtKL6KGPq73dW'
    }
    
    # Parámetros exactos del script original
    params = {
        'palabras': 'aduanas, ley, comercio exterior, turismo, aduanas, leyes',
        'fechaInicio': '2025-10-19',
        'fechaFin': '2025-10-20',
        'limit': 500
    }
    
    print("🔍 Probando API con parámetros exactos...")
    print(f"URL: {url}")
    print(f"Headers: {headers}")
    print(f"Params: {params}")
    print("=" * 60)
    
    try:
        # Hacer la petición
        response = requests.get(url, headers=headers, params=params)
        
        print(f"Status Code: {response.status_code}")
        print(f"Headers de respuesta: {dict(response.headers)}")
        print(f"URL final: {response.url}")
        print("=" * 60)
        
        if response.status_code == 200:
            # Intentar parsear como JSON
            try:
                data = response.json()
                print(f"Tipo de datos: {type(data)}")
                
                if isinstance(data, dict):
                    print(f"✅ Objeto con claves: {list(data.keys())}")
                    
                    # Verificar si tiene el campo 'notas' como en contar_noticias.py
                    if 'notas' in data and isinstance(data['notas'], list):
                        notas = data['notas']
                        print(f"📰 NOTICIAS ENCONTRADAS: {len(notas)}")
                        print(f"📊 Total reportado: {data.get('total', 'No disponible')}")
                        print(f"✅ Éxito: {data.get('success', 'No disponible')}")
                        
                        # Mostrar las primeras noticias
                        for i, nota in enumerate(notas[:3]):
                            print(f"\n--- Noticia {i+1} ---")
                            print(f"Título: {nota.get('titulo', 'Sin título')}")
                            print(f"Fecha: {nota.get('fecha', 'Sin fecha')}")
                            print(f"Fuente: {nota.get('fuente', 'Sin fuente')}")
                            print(f"Programa: {nota.get('nombre_programa', 'Sin programa')}")
                        
                        if len(notas) > 3:
                            print(f"\n... y {len(notas)-3} noticias más")
                        
                        return len(notas)  # Retornar el número real de noticias
                    else:
                        print("❌ No se encontró el campo 'notas' o no es una lista")
                        print(json.dumps(data, indent=2, ensure_ascii=False))
                        
                elif isinstance(data, list):
                    print(f"✅ Lista con {len(data)} elementos")
                    for i, item in enumerate(data):
                        print(f"\n--- Elemento {i+1} ---")
                        print(json.dumps(item, indent=2, ensure_ascii=False))
                        if i >= 2:  # Solo mostrar los primeros 3
                            print(f"... y {len(data)-3} elementos más")
                            break
                else:
                    print(f"❌ Tipo de datos inesperado: {type(data)}")
                    print(f"Contenido: {data}")
                    
            except json.JSONDecodeError as e:
                print(f"❌ Error al parsear JSON: {e}")
                print(f"Contenido de respuesta: {response.text[:500]}")
        else:
            print(f"❌ Error HTTP {response.status_code}")
            print(f"Contenido: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error en la petición: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

def test_with_different_dates():
    """Prueba con diferentes rangos de fechas para obtener más datos"""
    
    url = 'https://evat.oblek.com.mx/notas-api/notas'
    headers = {
        'accept': '*/*',
        'Authorization': 'Bearer xdrqzCwqUd4kMc/5Q5pJtKL6KGPq73dW'
    }
    
    # Probar con rangos de fechas más amplios
    date_ranges = [
        ('2025-10-15', '2025-10-22'),  # 7 días
        ('2025-10-10', '2025-10-22'),  # 12 días
        ('2025-10-01', '2025-10-22'),  # 21 días
        ('2025-09-01', '2025-10-22'),  # 51 días
    ]
    
    print("\n🔍 Probando con diferentes rangos de fechas...")
    print("=" * 60)
    
    for fecha_inicio, fecha_fin in date_ranges:
        params = {
            'palabras': 'aduanas, ley, comercio exterior, turismo, aduanas, leyes',
            'fechaInicio': fecha_inicio,
            'fechaFin': fecha_fin,
            'limit': 500
        }
        
        try:
            print(f"\n📅 Probando: {fecha_inicio} a {fecha_fin}")
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                # Verificar la estructura correcta
                if isinstance(data, dict) and 'notas' in data and isinstance(data['notas'], list):
                    notas = data['notas']
                    count = len(notas)
                    print(f"   ✅ Noticias encontradas: {count}")
                    print(f"   📊 Total reportado: {data.get('total', 'No disponible')}")
                    
                    if count > 0:
                        print(f"   🎉 ¡Encontramos {count} noticias!")
                        print(f"   📄 Primera noticia: {notas[0].get('titulo', 'Sin título')[:80]}...")
                        return data  # Retornar los datos encontrados
                else:
                    print(f"   ❌ Estructura de datos inesperada")
                    print(f"   Claves disponibles: {list(data.keys()) if isinstance(data, dict) else 'No es un objeto'}")
            else:
                print(f"   ❌ Error {response.status_code}: {response.text[:100]}")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    return None

if __name__ == "__main__":
    print("🚀 Iniciando pruebas simples de la API...")
    
    # Prueba básica
    test_api_simple()
    
    # Prueba con diferentes fechas
    data = test_with_different_dates()
    
    if data:
        print(f"\n✅ ¡Datos encontrados! Total: {len(data) if isinstance(data, list) else 1}")
    else:
        print("\n⚠️  No se encontraron datos suficientes para probar la paginación")
