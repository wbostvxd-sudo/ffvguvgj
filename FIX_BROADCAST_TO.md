# Solución para Error de broadcast_to

## Problema

Error: `cannot import name 'broadcast_to' from 'numpy.lib.stride_tricks'`

Esto ocurre cuando:
- Hay una versión incorrecta de numpy instalada
- pandas/gradio fueron instalados antes que numpy
- Hay versiones mixtas de numpy en el sistema

## Solución Automática

El script ahora:
1. ✅ Desinstala numpy, pandas, scipy juntos
2. ✅ Instala numpy 1.26.4 primero
3. ✅ Reinstala pandas y scipy después de numpy
4. ✅ Reinstala gradio después de pandas
5. ✅ Verifica que `broadcast_to` funcione

## Solución Manual (Si el script falla)

### Paso 1: Limpiar todo
```python
!pip uninstall -y numpy pandas scipy gradio opencv-python
```

### Paso 2: Instalar en orden correcto
```python
# 1. NumPy primero (versión que tiene broadcast_to)
!pip install --no-cache-dir numpy==1.26.4

# 2. Verificar que broadcast_to funciona
import numpy
from numpy.lib.stride_tricks import broadcast_to
print(f"NumPy {numpy.__version__} - broadcast_to OK")

# 3. Pandas después de numpy
!pip install --no-cache-dir pandas

# 4. Scipy
!pip install --no-cache-dir scipy==1.11.4

# 5. Gradio después de pandas
!pip install --no-cache-dir gradio==4.44.0 gradio-rangeslider==0.0.8

# 6. OpenCV
!pip install --no-cache-dir opencv-python==4.9.0.80

# 7. Resto de dependencias
!pip install --no-cache-dir psutil==5.9.8 tqdm==4.66.1 onnx==1.16.0 onnxruntime-gpu==1.16.3 insightface==0.7.3
```

### Paso 3: Verificar
```python
import numpy
from numpy.lib.stride_tricks import broadcast_to
import pandas
import gradio
import cv2

print(f"✓ NumPy: {numpy.__version__}")
print(f"✓ Pandas: {pandas.__version__}")
print(f"✓ Gradio: {gradio.__version__}")
print(f"✓ OpenCV: {cv2.__version__}")

# Probar broadcast_to
test = numpy.array([1, 2, 3])
result = broadcast_to(test, (2, 3))
print(f"✓ broadcast_to funciona: {result.shape}")
```

## Comando Completo de Reinstalación

```python
# Limpiar
!pip uninstall -y numpy pandas scipy gradio gradio-rangeslider opencv-python

# Instalar en orden
!pip install --no-cache-dir numpy==1.26.4
!pip install --no-cache-dir pandas scipy==1.11.4
!pip install --no-cache-dir gradio==4.44.0 gradio-rangeslider==0.0.8
!pip install --no-cache-dir opencv-python==4.9.0.80
!pip install --no-cache-dir psutil==5.9.8 tqdm==4.66.1
!pip install --no-cache-dir onnx==1.16.0 onnxruntime-gpu==1.16.3
!pip install --no-cache-dir insightface==0.7.3

# Verificar
import numpy
from numpy.lib.stride_tricks import broadcast_to
print("✓ Todo instalado correctamente")
```

## Notas Importantes

1. **Orden es crítico**: numpy → pandas → gradio
2. **Usar --no-cache-dir**: Evita problemas con caché corrupto
3. **Verificar broadcast_to**: Asegúrate de que funciona antes de continuar
4. **Reiniciar kernel**: Si hay problemas persistentes, reinicia el kernel de Colab

## Verificación Rápida

```python
try:
    import numpy
    from numpy.lib.stride_tricks import broadcast_to
    import pandas
    import gradio
    
    # Test broadcast_to
    test = numpy.array([1, 2, 3])
    broadcast_to(test, (2, 3))
    
    print("✓ Todas las dependencias funcionan correctamente")
except Exception as e:
    print(f"✗ Error: {e}")
    print("Ejecuta la reinstalación manual")
```

