# 📰 Sistema de Descarga y Análisis de Noticias

Este proyecto contiene scripts en Python para consultar, descargar y analizar noticias desde la API de EVAT (oblek.com.mx), con funcionalidades para procesar, organizar y analizar datos de noticias relacionadas con aduanas, comercio exterior y turismo.

## 📋 Tabla de Contenidos

- [Descripción General](#descripción-general)
- [Requisitos](#requisitos)
- [API de Noticias](#api-de-noticias)
- [Scripts Disponibles](#scripts-disponibles)
- [Guía de Uso](#guía-de-uso)
- [Estructura de Datos](#estructura-de-datos)
- [Ejemplos de Uso](#ejemplos-de-uso)

---

## 📖 Descripción General

Este sistema permite:

- ✅ Consultar noticias desde la API de EVAT
- 📥 Descargar noticias con paginación automática
- 📁 Organizar noticias en carpetas estructuradas
- 📊 Analizar noticias descargadas (contar, detectar duplicados, etc.)
- 🔍 Probar y validar el funcionamiento de la API

### Tipos de Búsqueda Permitidas

Las siguientes palabras clave están permitidas en la API:
- `leyes`
- `ley`
- `comercio exterior`
- `aduanas`
- `aduana`
- `turismo`

---

## 🔧 Requisitos

### Dependencias

```bash
pip install requests
```

### Variables de Configuración

Todos los scripts requieren un token de autorización para acceder a la API:

```python
headers = {
    'accept': '*/*',
    'Authorization': 'Bearer xdrqzCwqUd4kMc/5Q5pJtKL6KGPq73dW'
}
```

⚠️ **Nota**: En un entorno de producción, considera usar variables de entorno para almacenar el token de forma segura.

---

## 🌐 API de Noticias

### Endpoint Base

```
https://evat.oblek.com.mx/notas-api
```

### Endpoint de Noticias

```
GET /notas
```

### Parámetros de Consulta

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `palabras` | string | ✅ Sí | Palabras de búsqueda separadas por comas |
| `fechaInicio` | string (YYYY-MM-DD) | ❌ No | Fecha de inicio del rango |
| `fechaFin` | string (YYYY-MM-DD) | ❌ No | Fecha de fin del rango |
| `limit` | integer | ❌ No | Número máximo de resultados (default: 50, max: 500) |

### Respuesta de la API

La API retorna un objeto JSON con la siguiente estructura:

```json
{
  "success": true,
  "total": 1234,
  "limit": 500,
  "filtros": {
    "fechaInicio": "2025-10-19",
    "fechaFin": "2025-10-20",
    "palabrasBuscadas": ["aduanas", "ley", "comercio exterior"]
  },
  "metadata": {
    "baseDatos": {
      "actual": "...",
      "historica": "..."
    },
    "resultados": {
      "actual": 1000,
      "historica": 234
    }
  },
  "notas": [
    {
      "id": "nota_123",
      "titulo": "Título de la noticia",
      "contenido": "Contenido completo...",
      "resumen": "Resumen de la noticia",
      "fecha": "2025-10-19T10:30:00Z",
      "fuente": "Nombre de la fuente",
      "nombre_programa": "Programa al que pertenece"
    }
  ]
}
```

---

## 📜 Scripts Disponibles

### 1. `prueba.py` - Descarga Básica

Script básico para descargar noticias y organizarlas en carpetas individuales.

**Características:**
- ✅ Descarga noticias con parámetros configurables
- 📁 Organiza cada noticia en su propia carpeta
- 💾 Guarda JSON completo, contenido, resumen y metadatos
- 🧹 Sanitiza nombres de archivos automáticamente

**Estructura de salida:**
```
documentos_noticias_YYYYMMDD_HHMMSS/
├── 001_Titulo_Noticia/
│   ├── noticia_completa.json
│   ├── contenido.txt
│   ├── resumen.txt
│   └── metadatos.json
├── 002_Otra_Noticia/
│   └── ...
└── ...
```

### 2. `descargar_noticias_paginadas.py` - Descarga con Paginación

Descarga todas las noticias usando paginación automática y las guarda en un solo archivo JSON.

**Características:**
- 🔄 Soporte para paginación automática
- 📦 Guarda todas las noticias en un solo archivo
- 📊 Incluye metadatos de descarga y parámetros de búsqueda
- ✅ Maneja grandes volúmenes de datos (500+ noticias)

**Estructura de salida:**
```
todas_las_noticias_YYYYMMDD_HHMMSS.json
```

### 3. `test_paginacion_con_descarga.py` - Descarga Paginada Organizada

Combina paginación con descarga organizada, creando tanto el archivo consolidado como carpetas individuales.

**Características:**
- 🔄 Paginación automática
- 📦 Archivo JSON consolidado
- 📁 Carpetas individuales por noticia
- 📊 Muestra progreso cada 50 noticias

**Estructura de salida:**
```
documentos_noticias_YYYYMMDD_HHMMSS/
├── todas_las_noticias.json
├── 0001_Titulo_Noticia_1/
│   ├── noticia_completa.json
│   ├── contenido.txt
│   ├── resumen.txt
│   └── metadatos.json
├── 0002_Titulo_Noticia_2/
│   └── ...
└── ...
```

### 4. `test_simple.py` - Pruebas de API

Script de prueba para validar el funcionamiento de la API con diferentes configuraciones.

**Características:**
- 🔍 Pruebas básicas de la API
- 📅 Pruebas con diferentes rangos de fechas
- 📊 Muestra información detallada de la respuesta
- ✅ Útil para debugging y validación

### 5. `contar_noticias.py` - Análisis de Noticias

Analiza archivos JSON descargados y proporciona estadísticas detalladas.

**Características:**
- 📊 Conteo total de noticias
- 📅 Análisis por fechas (rango, noticias por día)
- 🔍 Detección de duplicados
- 📋 Información detallada sobre filtros y metadatos

**Salida de ejemplo:**
```
📊 INFORMACIÓN GENERAL:
✅ Éxito: true
📈 Total reportado: 1234
🔢 Límite: 500

📅 PERÍODO CONSULTADO:
   Fecha inicio: 2025-10-19
   Fecha fin: 2025-10-20
   Palabras buscadas: aduanas, ley, comercio exterior

🔍 CONTEO REAL DE NOTICIAS:
   Número de noticias en el array: 500

📅 NOTICIAS POR DÍA:
   2025-10-19: 250 noticias
   2025-10-20: 250 noticias

🔍 ANÁLISIS DE DUPLICADOS:
   Total títulos: 500
   Títulos únicos: 495
   Duplicados: 5
```

---

## 🚀 Guía de Uso

### Uso Básico

1. **Descargar noticias de un rango específico:**

```bash
python prueba.py
```

2. **Descargar con paginación:**

```bash
python descargar_noticias_paginadas.py
```

3. **Analizar noticias descargadas:**

```bash
python contar_noticias.py
```

4. **Probar la API:**

```bash
python test_simple.py
```

### Configuración de Parámetros

Todos los scripts permiten modificar los parámetros de búsqueda. Edita los siguientes valores en cada script:

```python
params = {
    'palabras': 'aduanas, ley, comercio exterior, turismo, aduanas, leyes',
    'fechaInicio': '2025-10-19',  # Modifica estas fechas
    'fechaFin': '2025-10-20',      # según tus necesidades
    'limit': 500
}
```

---

## 📊 Estructura de Datos

### Estructura de una Noticia

```json
{
  "id": "identificador_unico",
  "titulo": "Título de la noticia",
  "contenido": "Contenido completo de la noticia...",
  "resumen": "Resumen breve de la noticia",
  "fecha": "2025-10-19T10:30:00Z",
  "fuente": "Nombre de la fuente",
  "nombre_programa": "Programa al que pertenece"
}
```

### Metadatos Guardados

```json
{
  "fecha_creacion": "2025-10-20T15:30:00",
  "id_noticia": "nota_123",
  "fuente": "Nombre de la fuente",
  "fecha_publicacion": "2025-10-19T10:30:00Z",
  "numero_noticia": 1
}
```

---

## 💡 Ejemplos de Uso

### Ejemplo 1: Descargar Noticias de un Día Específico

```python
# En prueba.py, modifica los parámetros:
params = {
    'palabras': 'aduanas, turismo',
    'fechaInicio': '2025-10-19',
    'fechaFin': '2025-10-19',  # Mismo día
    'limit': 500
}
```

### Ejemplo 2: Descargar Todas las Noticias Disponibles

```python
# En descargar_noticias_paginadas.py:
base_params = {
    'palabras': 'aduanas, ley, comercio exterior, turismo',
    'fechaInicio': '2025-01-01',  # Rango amplio
    'fechaFin': '2025-10-22',
    'limit': 500
}
```

### Ejemplo 3: Buscar por Palabras Específicas

```python
params = {
    'palabras': 'comercio exterior, aduanas',  # Solo estas palabras
    'fechaInicio': '2025-10-01',
    'fechaFin': '2025-10-31',
    'limit': 500
}
```

---

## 🔍 Funcionalidades Especiales

### Sanitización de Nombres de Archivo

El script `sanitize_filename()` limpia automáticamente los nombres de archivo para evitar problemas en el sistema de archivos:

```python
def sanitize_filename(filename):
    """Limpia el nombre del archivo para que sea válido"""
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    filename = filename.replace(' ', '_')
    return filename[:100]
```

### Paginación Automática

Los scripts de paginación automáticamente:
- Detectan cuando hay más de 500 noticias
- Realizan múltiples consultas si es necesario
- Consolidan todos los resultados en un solo conjunto de datos

### Manejo de Errores

Todos los scripts incluyen manejo de errores robusto:

```python
try:
    # Código de descarga
except requests.exceptions.RequestException as e:
    print(f"❌ Error en la petición: {e}")
except json.JSONDecodeError as e:
    print(f"❌ Error al decodificar JSON: {e}")
except Exception as e:
    print(f"❌ Error inesperado: {e}")
```

---

## 📝 Notas Importantes

1. **Token de Autorización**: El token actual en los scripts es funcional pero es recomendable almacenarlo de forma segura (variables de entorno).

2. **Límite de la API**: El límite máximo permitido es 500 resultados por consulta. Para obtener más resultados, usa los scripts con paginación.

3. **Formato de Fechas**: Las fechas deben estar en formato `YYYY-MM-DD`.

4. **Palabras Permtidas**: Solo puedes usar las palabras específicas mencionadas en la especificación de la API.

5. **Codificación UTF-8**: Todos los archivos se guardan con codificación UTF-8 para soportar caracteres especiales.

---

## 🤝 Contribución

Para contribuir a este proyecto:

1. Agrega nuevos scripts según las necesidades
2. Mejora el manejo de errores
3. Documenta cambios en este README
4. Mantén el estilo de código consistente

---

## 📄 Licencia

Este proyecto es para uso interno y educativo.

---

## 📧 Contacto

Para consultas sobre la API o este proyecto, contacta al equipo de EVAT.

---

**Última actualización**: Octubre 2025

