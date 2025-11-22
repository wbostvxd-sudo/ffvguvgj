# Solución para Error de NumPy en Colab

## Problema

Colab tiene numpy 2.2.6 preinstalado, pero opencv-python fue compilado con numpy 1.x, causando:
```
AttributeError: _ARRAY_API not found
ImportError: numpy.core.multiarray failed to import
```

## Solución Automática

El script ahora maneja esto automáticamente, pero si necesitas hacerlo manualmente:

### Opción 1: Script Mejorado (Recomendado)

El script `faceswap_colab_main.py` ahora:
1. ✅ Desinstala numpy 2.x
2. ✅ Instala numpy 1.26.4 explícitamente
3. ✅ Reinstala opencv-python con numpy 1.x
4. ✅ Verifica al final que numpy 1.x esté activo

### Opción 2: Manual (Si el script falla)

```python
# 1. Desinstalar numpy 2.x
!pip uninstall -y numpy

# 2. Instalar numpy 1.x
!pip install numpy==1.26.4

# 3. Reinstalar opencv-python
!pip uninstall -y opencv-python opencv-contrib-python
!pip install opencv-python==4.9.0.80

# 4. Verificar
import numpy
print(f"NumPy version: {numpy.__version__}")  # Debe ser 1.26.4

# 5. Verificar opencv
import cv2
print(f"OpenCV version: {cv2.__version__}")  # Debe funcionar sin errores
```

### Opción 3: Forzar Reinstalación Completa

```python
# Desinstalar todo
!pip uninstall -y numpy opencv-python opencv-contrib-python scipy

# Instalar en orden correcto
!pip install numpy==1.26.4
!pip install opencv-python==4.9.0.80
!pip install scipy==1.11.4

# Verificar
import numpy
import cv2
import scipy
print("✓ Todas las dependencias funcionan")
```

## Verificación

Después de instalar, verifica:

```python
import numpy
import cv2

print(f"NumPy: {numpy.__version__}")
print(f"OpenCV: {cv2.__version__}")

# Debe mostrar:
# NumPy: 1.26.4
# OpenCV: 4.9.0
# Sin errores
```

## Si Aún Hay Problemas

### Error: "numpy 2.x sigue instalado"

```python
# Forzar reinstalación
!pip install --force-reinstall --no-deps numpy==1.26.4
!pip install --force-reinstall opencv-python==4.9.0.80
```

### Error: "opencv no funciona"

```python
# Reinstalar opencv desde cero
!pip uninstall -y opencv-python opencv-contrib-python opencv-python-headless
!pip install opencv-python==4.9.0.80
```

### Error: "scipy no funciona"

```python
# Reinstalar scipy
!pip uninstall -y scipy
!pip install scipy==1.11.4
```

## Notas Importantes

1. **Orden de instalación es crítico**: numpy 1.x DEBE instalarse ANTES que opencv-python
2. **Verificar siempre**: Después de instalar, verifica que numpy sea 1.x
3. **Reiniciar kernel**: Si hay problemas persistentes, reinicia el kernel de Colab
4. **No mezclar versiones**: No instales numpy 2.x después de instalar numpy 1.x

## Comando Completo de Verificación

```python
import sys
import subprocess

# Verificar versiones instaladas
packages = ['numpy', 'opencv-python', 'scipy', 'gradio', 'onnx', 'onnxruntime']
for pkg in packages:
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', 'show', pkg], 
                              capture_output=True, text=True)
        version_line = [line for line in result.stdout.split('\n') if 'Version:' in line]
        if version_line:
            print(f"{pkg}: {version_line[0].split(':')[1].strip()}")
    except:
        print(f"{pkg}: No encontrado")
```

