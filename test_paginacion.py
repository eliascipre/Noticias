import requests
import json
from datetime import datetime, timedelta

def test_api_pagination():
    """Prueba diferentes parámetros de paginación en la API de noticias"""
    
    url = 'https://evat.oblek.com.mx/notas-api/notas'
    headers = {
        'accept': '*/*',
        'Authorization': 'Bearer xdrqzCwqUd4kMc/5Q5pJtKL6KGPq73dW'
    }
    
    # Parámetros base
    base_params = {
        'palabras': 'aduanas, ley, comercio exterior, turismo',
        'fechaInicio': '2025-10-19',
        'fechaFin': '2025-10-20'
    }
    
    # Lista de parámetros de paginación a probar
    pagination_params = [
        {},  # Sin parámetros adicionales
        {'limit': 10},  # Límite pequeño
        {'limit': 100},  # Límite mediano
        {'limit': 500},  # Límite máximo según documentación
        {'limit': 1000},  # Límite mayor al máximo documentado
        {'page': 1},  # Parámetro de página
        {'page': 1, 'limit': 50},  # Página con límite
        {'page': 2, 'limit': 50},  # Segunda página
        {'offset': 0},  # Parámetro de offset
        {'offset': 50, 'limit': 50},  # Offset con límite
        {'skip': 0},  # Parámetro skip
        {'skip': 50, 'limit': 50},  # Skip con límite
        {'start': 0},  # Parámetro start
        {'start': 50, 'limit': 50},  # Start con límite
        {'pageSize': 50},  # Parámetro pageSize
        {'pageSize': 50, 'page': 1},  # pageSize con page
        {'size': 50},  # Parámetro size
        {'size': 50, 'page': 1},  # size con page
    ]
    
    print("🔍 Probando parámetros de paginación en la API de noticias...")
    print("=" * 60)
    
    for i, extra_params in enumerate(pagination_params, 1):
        params = {**base_params, **extra_params}
        
        try:
            print(f"\n{i:2d}. Probando: {extra_params}")
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                count = len(data) if isinstance(data, list) else 1
                print(f"    ✅ Status: {response.status_code} | Resultados: {count}")
                
                # Si hay más de 0 resultados, mostrar algunos detalles
                if count > 0 and isinstance(data, list):
                    first_item = data[0]
                    print(f"    📄 Primer resultado: {first_item.get('titulo', 'Sin título')[:50]}...")
                    
                    # Verificar si hay metadatos de paginación en la respuesta
                    if isinstance(data, dict) and any(key in data for key in ['total', 'totalCount', 'hasMore', 'nextPage', 'page', 'pages']):
                        print(f"    📊 Metadatos de paginación encontrados: {[k for k in data.keys() if k in ['total', 'totalCount', 'hasMore', 'nextPage', 'page', 'pages']]}")
                
            else:
                print(f"    ❌ Status: {response.status_code} | Error: {response.text[:100]}")
                
        except Exception as e:
            print(f"    ❌ Error: {str(e)[:100]}")
    
    print("\n" + "=" * 60)
    print("🏁 Pruebas completadas")

def test_large_limit():
    """Prueba específica para verificar si el límite se ha ampliado"""
    
    url = 'https://evat.oblek.com.mx/notas-api/notas'
    headers = {
        'accept': '*/*',
        'Authorization': 'Bearer xdrqzCwqUd4kMc/5Q5pJtKL6KGPq73dW'
    }
    
    # Probar con diferentes límites grandes
    limits_to_test = [500, 1000, 2000, 5000, 10000]
    
    print("\n🔍 Probando límites ampliados...")
    print("=" * 40)
    
    for limit in limits_to_test:
        params = {
            'palabras': 'aduanas, ley, comercio exterior, turismo',
            'fechaInicio': '2025-10-19',
            'fechaFin': '2025-10-20',
            'limit': limit
        }
        
        try:
            print(f"\nProbando límite: {limit}")
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                count = len(data) if isinstance(data, list) else 1
                print(f"✅ Resultados obtenidos: {count}")
                
                if count >= limit:
                    print(f"🎉 ¡Límite de {limit} funcionando!")
                elif count == 500:
                    print(f"⚠️  Límite parece estar en 500 (máximo anterior)")
                else:
                    print(f"ℹ️  Solo {count} resultados disponibles")
            else:
                print(f"❌ Error {response.status_code}: {response.text[:100]}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_api_pagination()
    test_large_limit()
