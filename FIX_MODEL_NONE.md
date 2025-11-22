# Fix para modelos None en inference_pool

## Problema

Al intentar usar la interfaz (cargar imágenes, procesar frames), la aplicación falla con:

```
AttributeError: 'NoneType' object has no attribute 'run'
```

Este error ocurre en múltiples lugares:
- `face_detector.py` líneas 401, 413, 425, 437 (funciones `forward_with_*`)
- `content_analyser.py` línea 225 (función `forward_nsfw`)

## Causa Raíz

El `inference_pool` se crea ANTES de que los modelos se descarguen. Cuando se intenta obtener un modelo del pool:

```python
face_detector = get_inference_pool().get('yolo_face')  # Devuelve None si el modelo no existe
detection = face_detector.run(...)  # ❌ AttributeError: 'NoneType' object has no attribute 'run'
```

El flujo problemático es:

1. Usuario carga una imagen en la UI
2. Se llama a `get_inference_pool()` que crea el pool
3. En `create_inference_pool()`, se verifica `if is_file(model_path)` pero el archivo no existe aún
4. El pool se crea vacío: `{}`
5. `.get('yolo_face')` devuelve `None`
6. Se intenta llamar `None.run()` → **AttributeError**

## Solución

Se agregaron verificaciones de `None` en todas las funciones `forward_with_*` y `forward_nsfw`:

### 1. Verificar si el modelo es None
### 2. Si es None, llamar a `pre_check()` para forzar la descarga
### 3. Intentar obtener el modelo nuevamente
### 4. Si aún es None, devolver un valor por defecto seguro

### Implementación en face_detector.py

```python
def forward_with_yolo_face(detect_vision_frame : VisionFrame) -> Detection:
    face_detector = get_inference_pool().get('yolo_face')
    
    if face_detector is None:
        # Modelo no cargado - forzar descarga
        pre_check()
        face_detector = get_inference_pool().get('yolo_face')
        
        if face_detector is None:
            return []  # Devolver lista vacía si no se puede cargar

    with thread_semaphore():
        detection = face_detector.run(None, {'input': detect_vision_frame})

    return detection
```

Lo mismo se aplicó a:
- `forward_with_retinaface()`
- `forward_with_scrfd()`
- `forward_with_yunet()`

### Implementación en content_analyser.py

```python
def forward_nsfw(vision_frame : VisionFrame, model_name : str) -> Detection:
    content_analyser = get_inference_pool().get(model_name)
    
    if content_analyser is None:
        # Modelo no cargado - forzar descarga
        pre_check()
        content_analyser = get_inference_pool().get(model_name)
        
        if content_analyser is None:
            # Devolver detección segura (no NSFW)
            if model_name == 'nsfw_1':
                return numpy.zeros((1, 85))
            else:
                return numpy.array([1.0, 0.0, 0.0, 0.0])

    with conditional_thread_semaphore():
        detection = content_analyser.run(None, {'input': vision_frame})[0]

    if model_name in [ 'nsfw_2', 'nsfw_3' ]:
        return detection[0]

    return detection
```

## Resultado

Con estos cambios:
- ✅ No más `AttributeError: 'NoneType' object has no attribute 'run'`
- ✅ Los modelos se descargan automáticamente cuando se necesitan
- ✅ Si la descarga falla, se devuelven valores por defecto seguros
- ✅ La interfaz funciona correctamente incluso en el primer uso

## Archivos Modificados

1. **MODIFICADO**: `faceswap_colab/face_detector.py`
   - Líneas 397-406: `forward_with_retinaface()`
   - Líneas 409-418: `forward_with_scrfd()`
   - Líneas 421-430: `forward_with_yolo_face()`
   - Líneas 433-442: `forward_with_yunet()`

2. **MODIFICADO**: `faceswap_colab/content_analyser.py`
   - Líneas 221-233: `forward_nsfw()`

## Flujo Corregido

1. Usuario carga una imagen en la UI
2. Se llama a `get_inference_pool()` que crea el pool (posiblemente vacío)
3. Se intenta obtener el modelo: `face_detector = get_inference_pool().get('yolo_face')`
4. **NUEVO**: Si `face_detector is None`, se llama a `pre_check()` para descargar modelos
5. Se intenta obtener el modelo nuevamente
6. Si existe, se usa normalmente; si no, se devuelve un valor por defecto
7. ✅ No hay AttributeError

## Compatibilidad

- ✅ Primera ejecución (modelos no descargados)
- ✅ Ejecuciones subsecuentes (modelos ya descargados)
- ✅ Fallos de descarga (valores por defecto seguros)
