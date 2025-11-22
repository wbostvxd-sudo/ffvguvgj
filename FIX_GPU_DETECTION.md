# Fix para detección de GPU y uso de CUDA

## Problema

La aplicación no utiliza la GPU para procesar imágenes:
- Se cargan las imágenes pero no se intercambian los rostros
- No usa GPU ni CPU para el procesamiento
- Consumo de RAM aumenta de 1GB a 1.7GB pero no hace nada
- La GPU no se detecta correctamente

## Causa Raíz

El problema estaba en la detección de GPU en `init_defaults.py`:

### Código Anterior (Problemático)
```python
try:
    import torch
    if torch.cuda.is_available():
        if state_manager.get_item('execution_providers') == ['cpu']:
            state_manager.set_item('execution_providers', ['cuda'])
except:
    pass
```

**Problemas**:
1. Dependía de PyTorch (`torch.cuda.is_available()`)
2. Solo cambiaba si el valor era exactamente `['cpu']`
3. No verificaba si CUDA estaba disponible en **onnxruntime** (que es lo que realmente importa)

## Solución

Se modificó `faceswap_colab/init_defaults.py` para usar la detección de providers de onnxruntime:

```python
try:
    from onnxruntime import get_available_providers
    available_providers = get_available_providers()
    
    # Verificar si CUDA está disponible en onnxruntime
    if 'CUDAExecutionProvider' in available_providers:
        # GPU disponible - usar CUDA
        state_manager.set_item('execution_providers', ['cuda'])
        print("  ✓ GPU detectada - usando CUDA (onnxruntime)")
    elif 'TensorrtExecutionProvider' in available_providers:
        # TensorRT disponible
        state_manager.set_item('execution_providers', ['tensorrt'])
        print("  ✓ GPU detectada - usando TensorRT")
    else:
        # Solo CPU disponible
        print("  ℹ GPU no detectada - usando CPU")
except Exception as e:
    # Si falla la detección, usar CPU (ya está configurado)
    print(f"  ⚠ Error detectando GPU: {e}")
    print("  ℹ Usando CPU por defecto")
```

## Ventajas de la Nueva Implementación

### 1. Usa onnxruntime directamente
- Verifica los providers disponibles en onnxruntime
- No depende de PyTorch
- Más preciso para detectar qué puede usar realmente

### 2. Soporta múltiples backends
- **CUDAExecutionProvider**: NVIDIA CUDA
- **TensorrtExecutionProvider**: NVIDIA TensorRT (más rápido)
- **CPUExecutionProvider**: Fallback a CPU

### 3. Logging mejorado
- Muestra claramente qué provider se está usando
- Ayuda a diagnosticar problemas de detección
- Muestra errores si la detección falla

## Verificación

Cuando la aplicación se inicia correctamente, deberías ver uno de estos mensajes:

### Con GPU CUDA
```
Inicializando valores por defecto...
  ✓ GPU detectada - usando CUDA (onnxruntime)
  ✓ Valores por defecto inicializados
```

### Con GPU TensorRT
```
Inicializando valores por defecto...
  ✓ GPU detectada - usando TensorRT
  ✓ Valores por defecto inicializados
```

### Sin GPU (CPU)
```
Inicializando valores por defecto...
  ℹ GPU no detectada - usando CPU
  ✓ Valores por defecto inicializados
```

## Verificar Providers Disponibles en Colab

Para verificar qué providers están disponibles en tu entorno de Google Colab:

```python
from onnxruntime import get_available_providers
print("Providers disponibles:", get_available_providers())
```

**Salida esperada en Colab con GPU**:
```
Providers disponibles: ['TensorrtExecutionProvider', 'CUDAExecutionProvider', 'CPUExecutionProvider']
```

**Salida en Colab sin GPU**:
```
Providers disponibles: ['CPUExecutionProvider']
```

## Instalación de onnxruntime-gpu

Si CUDA no está disponible, asegúrate de que `onnxruntime-gpu` esté instalado:

```bash
pip install onnxruntime-gpu
```

En Google Colab, esto debería instalarse automáticamente por el script `faceswap_colab_main.py`.

## Archivos Modificados

1. **MODIFICADO**: `faceswap_colab/init_defaults.py`
   - Líneas 101-121: Nueva detección de GPU usando onnxruntime

## Resultado Esperado

Con este fix:
- ✅ La GPU se detecta correctamente usando onnxruntime
- ✅ Los modelos usan CUDA para inferencia
- ✅ El procesamiento de imágenes usa la GPU
- ✅ Mensajes claros sobre qué provider se está usando

## Troubleshooting

### Si aún no usa la GPU:

1. **Verificar que onnxruntime-gpu esté instalado**:
   ```python
   import onnxruntime
   print(onnxruntime.__version__)
   print(onnxruntime.get_available_providers())
   ```

2. **Verificar que CUDA esté disponible en el sistema**:
   ```bash
   nvidia-smi
   ```

3. **Verificar logs de inicio**:
   - Buscar el mensaje "✓ GPU detectada - usando CUDA"
   - Si dice "GPU no detectada", verificar instalación de onnxruntime-gpu

4. **Reinstalar onnxruntime-gpu**:
   ```bash
   pip uninstall onnxruntime onnxruntime-gpu
   pip install onnxruntime-gpu
   ```

## Compatibilidad

- ✅ Google Colab con GPU T4
- ✅ Google Colab con GPU A100
- ✅ Google Colab con GPU V100
- ✅ Google Colab sin GPU (CPU fallback)
- ✅ Entornos locales con CUDA
- ✅ Entornos locales sin CUDA
