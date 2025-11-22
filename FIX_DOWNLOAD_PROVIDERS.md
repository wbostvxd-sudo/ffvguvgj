# Fix para download_providers None

## Problema

Al intentar ejecutar un trabajo (run), la aplicación falla con:

```
TypeError: 'NoneType' object is not iterable
```

Este error ocurre en `download.py` línea 159:

```python
for download_provider in download_providers:  # ❌ TypeError si download_providers es None
```

## Causa Raíz

El problema es un **orden de inicialización incorrecto**:

1. Durante la importación de módulos, se llama a `create_static_model_set('full')` en `content_analyser.py`
2. Esta función usa `@lru_cache()`, por lo que se ejecuta inmediatamente
3. Dentro de `create_static_model_set()`, se llama a `resolve_download_url('models-3.3.0', 'nsfw_1.hash')`
4. `resolve_download_url()` intenta obtener `download_providers` del `state_manager`
5. **PERO** en este punto, `init_default_state()` aún no se ha llamado
6. Por lo tanto, `state_manager.get_item('download_providers')` devuelve `None`
7. Intentar iterar sobre `None` causa el `TypeError`

### Flujo Problemático

```
Importación de módulos
  ↓
content_analyser.py importado
  ↓
create_static_model_set() llamado (por @lru_cache)
  ↓
resolve_download_url() llamado
  ↓
state_manager.get_item('download_providers') → None ❌
  ↓
for download_provider in None → TypeError
```

## Solución

Se modificó `faceswap_colab/download.py` para usar un valor por defecto cuando `download_providers` es `None`:

```python
def resolve_download_url(base_name : str, file_name : str) -> Optional[str]:
    download_providers = state_manager.get_item('download_providers')
    
    # Si download_providers es None (no inicializado aún), usar valor por defecto
    if download_providers is None:
        download_providers = ['github']

    for download_provider in download_providers:
        download_url = resolve_download_url_by_provider(download_provider, base_name, file_name)
        if download_url:
            return download_url

    return None
```

### ¿Por qué 'github'?

En `init_defaults.py` línea 82, el valor por defecto de `download_providers` es `['github']`:

```python
'download_providers': ['github'],
```

Por lo tanto, usar `['github']` como fallback es consistente con la configuración por defecto.

## Resultado

Con este cambio:
- ✅ `resolve_download_url()` funciona incluso si se llama antes de `init_default_state()`
- ✅ No más `TypeError: 'NoneType' object is not iterable`
- ✅ Los modelos se pueden descargar correctamente
- ✅ La aplicación puede ejecutar trabajos sin errores

## Archivos Modificados

1. **MODIFICADO**: `faceswap_colab/download.py`
   - Líneas 156-164: Agregada verificación de `None` en `resolve_download_url()`

## Compatibilidad

- ✅ Llamadas antes de `init_default_state()` (durante importación de módulos)
- ✅ Llamadas después de `init_default_state()` (funcionamiento normal)
- ✅ Configuraciones personalizadas de `download_providers`

## Flujo Corregido

```
Importación de módulos
  ↓
content_analyser.py importado
  ↓
create_static_model_set() llamado (por @lru_cache)
  ↓
resolve_download_url() llamado
  ↓
state_manager.get_item('download_providers') → None
  ↓
✅ Usar ['github'] como fallback
  ↓
for download_provider in ['github'] → Funciona correctamente
```
