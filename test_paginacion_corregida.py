import requests
import json
from datetime import datetime, timedelta

def test_pagination_corrected():
    """Prueba la paginación entendiendo la estructura real de la respuesta"""
    
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
        'limit': 500
    }
    
    print("🔍 Probando paginación con estructura de datos corregida...")
    print("=" * 70)
    
    # Primero, obtener el total de noticias disponibles
    print("\n1️⃣ Obteniendo total de noticias disponibles...")
    try:
        response = requests.get(url, headers=headers, params=base_params)
        if response.status_code == 200:
            data = response.json()
            
            if isinstance(data, dict) and 'notas' in data:
                notas = data['notas']
                total_disponible = len(notas)
                total_reportado = data.get('total', total_disponible)
                
                print(f"   ✅ Noticias en respuesta: {total_disponible}")
                print(f"   📊 Total reportado por API: {total_reportado}")
                print(f"   🎯 Límite solicitado: {base_params['limit']}")
                
                if total_disponible > 1:
                    print(f"\n2️⃣ Probando paginación con {total_disponible} noticias disponibles...")
                    test_pagination_parameters(base_params, headers, url, total_disponible)
                else:
                    print(f"\n⚠️  Solo hay {total_disponible} noticia disponible. Probando con fechas más amplias...")
                    test_with_broader_dates(headers, url)
            else:
                print(f"   ❌ Estructura de datos inesperada: {list(data.keys()) if isinstance(data, dict) else type(data)}")
        else:
            print(f"   ❌ Error {response.status_code}: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

def test_pagination_parameters(base_params, headers, url, total_available):
    """Prueba diferentes parámetros de paginación"""
    
    # Probar diferentes tamaños de página
    page_sizes = [10, 25, 50, 100]
    
    for page_size in page_sizes:
        print(f"\n   📊 Probando con page_size: {page_size}")
        
        # Probar diferentes combinaciones de parámetros de paginación
        pagination_tests = [
            {'limit': page_size},
            {'limit': page_size, 'page': 1},
            {'limit': page_size, 'page': 2},
            {'limit': page_size, 'offset': 0},
            {'limit': page_size, 'offset': page_size},
            {'limit': page_size, 'skip': 0},
            {'limit': page_size, 'skip': page_size},
            {'pageSize': page_size},
            {'pageSize': page_size, 'page': 1},
            {'pageSize': page_size, 'page': 2},
            {'size': page_size},
            {'size': page_size, 'page': 1},
        ]
        
        for i, extra_params in enumerate(pagination_tests, 1):
            params = {**base_params, **extra_params}
            
            try:
                response = requests.get(url, headers=headers, params=params)
                if response.status_code == 200:
                    data = response.json()
                    
                    if isinstance(data, dict) and 'notas' in data:
                        notas = data['notas']
                        count = len(notas)
                        total_api = data.get('total', count)
                        
                        print(f"      {i:2d}. {extra_params}")
                        print(f"          → Noticias: {count} | Total API: {total_api}")
                        
                        # Verificar si la paginación está funcionando
                        if count < total_available and count > 0:
                            print(f"          🎯 ¡Posible paginación funcionando!")
                            print(f"          📄 Primera: {notas[0].get('titulo', 'Sin título')[:50]}...")
                            
                            # Verificar si hay metadatos de paginación
                            if 'metadata' in data:
                                metadata = data['metadata']
                                print(f"          📊 Metadatos: {metadata}")
                    else:
                        print(f"      {i:2d}. {extra_params} → Estructura inesperada")
                else:
                    print(f"      {i:2d}. {extra_params} → Error {response.status_code}")
            except Exception as e:
                print(f"      {i:2d}. {extra_params} → Error: {str(e)[:50]}")

def test_with_broader_dates(headers, url):
    """Prueba con rangos de fechas más amplios para obtener más datos"""
    
    date_ranges = [
        ('2025-10-15', '2025-10-22'),  # 7 días
        ('2025-10-10', '2025-10-22'),  # 12 días
        ('2025-10-01', '2025-10-22'),  # 21 días
        ('2025-09-01', '2025-10-22'),  # 51 días
    ]
    
    for fecha_inicio, fecha_fin in date_ranges:
        params = {
            'palabras': 'aduanas, ley, comercio exterior, turismo, aduanas, leyes',
            'fechaInicio': fecha_inicio,
            'fechaFin': fecha_fin,
            'limit': 500
        }
        
        try:
            print(f"\n   📅 Probando: {fecha_inicio} a {fecha_fin}")
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                if isinstance(data, dict) and 'notas' in data:
                    notas = data['notas']
                    count = len(notas)
                    total_api = data.get('total', count)
                    
                    print(f"      ✅ Noticias: {count} | Total API: {total_api}")
                    
                    if count > 1:
                        print(f"      🎉 ¡Encontramos {count} noticias! Probando paginación...")
                        test_pagination_parameters(params, headers, url, count)
                        return
                else:
                    print(f"      ❌ Estructura inesperada")
            else:
                print(f"      ❌ Error {response.status_code}")
        except Exception as e:
            print(f"      ❌ Error: {str(e)}")

def test_large_limits():
    """Prueba si el límite se ha ampliado más allá de 500"""
    
    url = 'https://evat.oblek.com.mx/notas-api/notas'
    headers = {
        'accept': '*/*',
        'Authorization': 'Bearer xdrqzCwqUd4kMc/5Q5pJtKL6KGPq73dW'
    }
    
    # Probar con diferentes límites grandes
    limits_to_test = [500, 1000, 2000, 5000]
    
    print("\n3️⃣ Probando límites ampliados...")
    print("=" * 50)
    
    for limit in limits_to_test:
        params = {
            'palabras': 'aduanas, ley, comercio exterior, turismo, aduanas, leyes',
            'fechaInicio': '2025-10-19',
            'fechaFin': '2025-10-20',
            'limit': limit
        }
        
        try:
            print(f"\n   🔢 Probando límite: {limit}")
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                if isinstance(data, dict) and 'notas' in data:
                    notas = data['notas']
                    count = len(notas)
                    total_api = data.get('total', count)
                    
                    print(f"      ✅ Noticias obtenidas: {count}")
                    print(f"      📊 Total reportado por API: {total_api}")
                    
                    if count >= limit:
                        print(f"      🎉 ¡Límite de {limit} funcionando!")
                    elif count == 500:
                        print(f"      ⚠️  Límite parece estar en 500 (máximo anterior)")
                    else:
                        print(f"      ℹ️  Solo {count} noticias disponibles en este rango")
                else:
                    print(f"      ❌ Estructura inesperada")
            else:
                print(f"      ❌ Error {response.status_code}: {response.text[:100]}")
        except Exception as e:
            print(f"      ❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🚀 Iniciando pruebas de paginación con estructura corregida...")
    
    # Probar paginación
    test_pagination_corrected()
    
    # Probar límites ampliados
    test_large_limits()
    
    print("\n🏁 Pruebas completadas")
