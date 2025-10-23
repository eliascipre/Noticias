import requests
import json
from datetime import datetime, timedelta

def test_pagination_with_exact_params():
    """Prueba la paginación usando exactamente los mismos parámetros del script original"""
    
    url = 'https://evat.oblek.com.mx/notas-api/notas'
    headers = {
        'accept': '*/*',
        'Authorization': 'Bearer xdrqzCwqUd4kMc/5Q5pJtKL6KGPq73dW'
    }
    
    # Parámetros EXACTOS del script original
    base_params = {
        'palabras': 'aduanas, ley, comercio exterior, turismo, aduanas, leyes',
        'fechaInicio': '2025-10-21',
        'fechaFin': '2025-10-22',
        'limit': 500
    }
    
    print("🔍 Probando paginación con parámetros EXACTOS del script original")
    print("=" * 70)
    print(f"Palabras: {base_params['palabras']}")
    print(f"Fecha inicio: {base_params['fechaInicio']}")
    print(f"Fecha fin: {base_params['fechaFin']}")
    print("=" * 70)
    
    # Primero, probar sin paginación para ver cuántos resultados hay
    print("\n1️⃣ Prueba base (sin paginación):")
    try:
        response = requests.get(url, headers=headers, params=base_params)
        if response.status_code == 200:
            data = response.json()
            count = len(data) if isinstance(data, list) else 1
            print(f"   ✅ Status: {response.status_code} | Resultados: {count}")
            
            if count > 0 and isinstance(data, list):
                print(f"   📄 Primer resultado: {data[0].get('titulo', 'Sin título')[:80]}...")
                print(f"   📅 Fecha: {data[0].get('fecha', 'Sin fecha')}")
                print(f"   🏷️  Fuente: {data[0].get('fuente', 'Sin fuente')}")
                
                # Mostrar el contenido completo del resultado
                print(f"\n   📋 CONTENIDO COMPLETO DEL RESULTADO:")
                print(f"   {'='*60}")
                print(json.dumps(data[0], indent=2, ensure_ascii=False))
                print(f"   {'='*60}")
        else:
            print(f"   ❌ Error {response.status_code}: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    # Probar con diferentes rangos de fechas para obtener más datos
    print("\n2️⃣ Probando con rangos de fechas más amplios:")
    
    date_ranges = [
        ('2025-10-15', '2025-10-20'),  # 5 días
        ('2025-10-10', '2025-10-20'),  # 10 días
        ('2025-10-01', '2025-10-20'),  # 20 días
        ('2025-09-01', '2025-10-20'),  # 50 días
    ]
    
    for fecha_inicio, fecha_fin in date_ranges:
        params = {
            'palabras': 'aduanas, ley, comercio exterior, turismo, aduanas, leyes',
            'fechaInicio': fecha_inicio,
            'fechaFin': fecha_fin,
            'limit': 500
        }
        
        try:
            print(f"\n   📅 Rango: {fecha_inicio} a {fecha_fin}")
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                count = len(data) if isinstance(data, list) else 1
                print(f"      ✅ Resultados: {count}")
                
                if count > 1:
                    print(f"      🎉 ¡Encontramos {count} resultados! Probando paginación...")
                    # Mostrar el contenido completo del primer resultado
                    print(f"\n      📋 CONTENIDO COMPLETO DEL PRIMER RESULTADO:")
                    print(f"      {'='*60}")
                    print(json.dumps(data[0], indent=2, ensure_ascii=False))
                    print(f"      {'='*60}")
                    test_pagination_with_data(params, headers, url, count)
                    break
            else:
                print(f"      ❌ Error {response.status_code}")
        except Exception as e:
            print(f"      ❌ Error: {str(e)}")

def test_pagination_with_data(base_params, headers, url, total_results):
    """Prueba la paginación cuando hay datos disponibles"""
    
    print(f"\n3️⃣ Probando paginación con {total_results} resultados disponibles:")
    print("-" * 50)
    
    # Probar diferentes tamaños de página
    page_sizes = [10, 25, 50, 100]
    
    for page_size in page_sizes:
        print(f"\n   📊 Probando con page_size: {page_size}")
        
        # Probar diferentes parámetros de paginación
        pagination_tests = [
            {'limit': page_size},
            {'limit': page_size, 'page': 1},
            {'limit': page_size, 'offset': 0},
            {'limit': page_size, 'skip': 0},
            {'limit': page_size, 'start': 0},
            {'pageSize': page_size},
            {'pageSize': page_size, 'page': 1},
            {'size': page_size},
            {'size': page_size, 'page': 1},
        ]
        
        for i, extra_params in enumerate(pagination_tests, 1):
            params = {**base_params, **extra_params}
            
            try:
                response = requests.get(url, headers=headers, params=params)
                if response.status_code == 200:
                    data = response.json()
                    count = len(data) if isinstance(data, list) else 1
                    print(f"      {i:2d}. {extra_params} → {count} resultados")
                    
                    # Si obtenemos menos resultados que el total, podría ser paginación
                    if count < total_results and count > 0:
                        print(f"         🎯 Posible paginación funcionando!")
                        print(f"         📄 Primer resultado: {data[0].get('titulo', 'Sin título')[:50]}...")
                else:
                    print(f"      {i:2d}. {extra_params} → Error {response.status_code}")
            except Exception as e:
                print(f"      {i:2d}. {extra_params} → Error: {str(e)[:30]}")

def test_different_keywords():
    """Prueba con diferentes palabras clave para obtener más resultados"""
    
    print("\n4️⃣ Probando con diferentes palabras clave:")
    print("-" * 50)
    
    url = 'https://evat.oblek.com.mx/notas-api/notas'
    headers = {
        'accept': '*/*',
        'Authorization': 'Bearer xdrqzCwqUd4kMc/5Q5pJtKL6KGPq73dW'
    }
    
    keyword_sets = [
        'aduanas',
        'ley',
        'comercio exterior',
        'turismo',
        'aduanas, turismo',
        'ley, comercio exterior',
        'aduanas, ley, comercio exterior, turismo',
        'aduanas, ley, comercio exterior, turismo, aduanas, leyes',  # Original
    ]
    
    for keywords in keyword_sets:
        params = {
            'palabras': keywords,
            'fechaInicio': '2025-10-19',
            'fechaFin': '2025-10-20',
            'limit': 500
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                count = len(data) if isinstance(data, list) else 1
                print(f"   🔍 '{keywords}' → {count} resultados")
                
                if count > 1:
                    print(f"      🎉 ¡Encontramos {count} resultados con estas palabras!")
                    # Mostrar el contenido completo del primer resultado
                    print(f"\n      📋 CONTENIDO COMPLETO DEL PRIMER RESULTADO:")
                    print(f"      {'='*60}")
                    print(json.dumps(data[0], indent=2, ensure_ascii=False))
                    print(f"      {'='*60}")
                    return keywords, count
            else:
                print(f"   ❌ '{keywords}' → Error {response.status_code}")
        except Exception as e:
            print(f"   ❌ '{keywords}' → Error: {str(e)}")
    
    return None, 0

if __name__ == "__main__":
    print("🚀 Iniciando pruebas detalladas de paginación...")
    
    # Probar con parámetros exactos
    test_pagination_with_exact_params()
    
    # Probar con diferentes palabras clave
    best_keywords, best_count = test_different_keywords()
    
    if best_count > 1:
        print(f"\n✅ Mejores resultados encontrados con: '{best_keywords}' ({best_count} resultados)")
        print("   Ahora puedes probar la paginación con estos parámetros.")
    else:
        print("\n⚠️  No se encontraron suficientes resultados para probar la paginación.")
        print("   Considera:")
        print("   - Ampliar el rango de fechas")
        print("   - Usar palabras clave más generales")
        print("   - Verificar que la API tenga datos en esas fechas")
