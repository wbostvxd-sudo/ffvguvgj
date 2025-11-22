# Fix para execution_device_ids vacío

## Problema

Al intentar procesar imágenes o videos, la aplicación falla con el siguiente error:

```
IndexError: Cannot choose from an empty sequence
```

Este error ocurre en `inference_manager.py` línea 41:

```python
random.choice(execution_device_ids)  # ❌ Falla si execution_device_ids está vacío
```

## Causa Raíz

En `init_defaults.py`, el valor por defecto de `execution_device_ids` estaba configurado como una lista vacía:

```python
'execution_device_ids': [],  # ❌ Lista vacía causa el error
```

Cuando el código intenta seleccionar un dispositivo aleatoriamente de esta lista vacía, Python lanza un `IndexError`.

## Solución

Se modificó `faceswap_colab/init_defaults.py` para:

1. **Establecer device 0 por defecto**: Cambiar `execution_device_ids` de `[]` a `[0]`
2. **Detectar GPU automáticamente**: Verificar si hay GPU disponible y configurar los execution providers apropiadamente

### Cambios Implementados

#### 1. Device ID por defecto

```python
'execution_device_ids': [0],  # ✅ Usar device 0 por defecto
```

En Google Colab:
- Si hay GPU: device 0 = GPU
- Si no hay GPU: device 0 = CPU

#### 2. Detección automática de GPU

```python
# Detectar y configurar GPU si está disponible
try:
    import torch
    if torch.cuda.is_available():
        # GPU disponible - usar CUDA
        if state_manager.get_item('execution_providers') == ['cpu']:
            state_manager.set_item('execution_providers', ['cuda'])
            print("  ✓ GPU detectada - usando CUDA")
except:
    # Si no hay torch o no hay GPU, usar CPU (ya está configurado)
    pass
```

## Resultado

Con estos cambios:
- ✅ `execution_device_ids` siempre tiene al menos un dispositivo (`[0]`)
- ✅ `random.choice(execution_device_ids)` funciona correctamente
- ✅ La GPU se detecta y usa automáticamente si está disponible
- ✅ Funciona tanto en entornos con GPU como sin GPU

## Archivos Modificados

1. **MODIFICADO**: `faceswap_colab/init_defaults.py`
   - Línea 71: Cambio de `[]` a `[0]`
   - Líneas 100-111: Detección automática de GPU

## Compatibilidad

- ✅ Google Colab con GPU (T4, A100, etc.)
- ✅ Google Colab sin GPU (CPU only)
- ✅ Entornos locales con CUDA
- ✅ Entornos locales sin CUDA

## Ejecución

Ahora cuando se ejecuta la aplicación:

```
Verificando NumPy...
  NumPy 2.0.2 detectado
  ✓ NumPy 2.0.2 (compatible, broadcast_to funciona)
  ✓ Módulo de compatibilidad NumPy cargado
  Inicializando valores por defecto...
  ✓ GPU detectada - usando CUDA  ← Nuevo mensaje
  ✓ Valores por defecto inicializados
```
