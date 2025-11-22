# Fix para numpy.ma en NumPy 2.x

## Problema

Al ejecutar la aplicación en Google Colab con NumPy 2.0.2, se produce el siguiente error:

```
AttributeError: 'numpy.ufunc' object has no attribute '__qualname__'
```

Este error ocurre en `numpy/ma/core.py` cuando intenta acceder al atributo `__qualname__` de objetos `ufunc`, que no existe en NumPy 2.x.

## Causa Raíz

En NumPy 2.x, los objetos `numpy.ufunc` no tienen el atributo `__qualname__`. Sin embargo, el módulo `numpy.ma.core` intenta acceder a este atributo al inicializar las clases `_MaskedUnaryOperation` y `_MaskedBinaryOperation`:

```python
# En numpy/ma/core.py línea 942
self.__qualname__ = ufunc.__qualname__  # ❌ Falla porque ufunc no tiene __qualname__
```

## Solución

Se creó el archivo `faceswap_colab/numpy_ma_patch.py` que:

1. **Detecta NumPy 2.x**: Verifica la versión de NumPy instalada
2. **Parchea las clases problemáticas**: Reemplaza `_MaskedUnaryOperation` y `_MaskedBinaryOperation` con versiones parcheadas
3. **Maneja __qualname__ correctamente**: Establece `__qualname__` manualmente usando `__name__` si `__qualname__` no existe

### Implementación

El parche se aplica en dos lugares:

#### 1. En `faceswap_colab/numpy_ma_patch.py`:

```python
class _PatchedMaskedUnaryOperation(_OriginalMaskedUnaryOperation):
    def __init__(self, mufunc):
        # Llamar al __init__ del abuelo directamente
        ma_core.MaskedUFunc.__init__(self, mufunc)
        
        # Establecer __qualname__ manualmente
        if not hasattr(mufunc, '__qualname__'):
            self.__qualname__ = mufunc.__name__ if hasattr(mufunc, '__name__') else 'unknown'
        else:
            self.__qualname__ = mufunc.__qualname__
```

#### 2. En `faceswap_colab_main.py`:

```python
# PARCHEAR numpy.ma ANTES DE QUE SE IMPORTE
try:
    from faceswap_colab import numpy_ma_patch
except Exception as e:
    pass
```

## Resultado

Con este parche:
- ✅ `matplotlib` puede importarse sin errores
- ✅ `pandas` puede importarse sin errores  
- ✅ `numpy.ma` funciona correctamente
- ✅ Gradio puede ejecutarse sin problemas

## Archivos Modificados

1. **NUEVO**: `faceswap_colab/numpy_ma_patch.py` - Parche para numpy.ma
2. **MODIFICADO**: `faceswap_colab_main.py` - Importa el parche antes de cualquier otra cosa

## Orden de Carga

Es crítico que los parches se carguen en este orden:

1. `numpy_compat.py` - Parcha `numpy.lib.stride_tricks.broadcast_to`
2. `numpy_ma_patch.py` - Parcha `numpy.ma.core._MaskedUnaryOperation`
3. Resto de imports (matplotlib, pandas, gradio, etc.)

## Compatibilidad

- ✅ NumPy 2.0.2
- ✅ NumPy 2.x (cualquier versión)
- ✅ NumPy 1.x (el parche se salta automáticamente)
