# Instalación en Google Colab

## Método 1: Instalación Automática (Recomendado)

Simplemente ejecuta el archivo principal:

```python
!python faceswap_colab_main.py
```

El script instalará automáticamente todas las dependencias con versiones compatibles.

## Método 2: Instalación Manual

Si prefieres instalar manualmente:

```python
# 1. Actualizar pip
!pip install --upgrade pip setuptools wheel

# 2. Instalar dependencias base
!pip install "numpy>=1.24.0,<2.0.0" opencv-python psutil tqdm scipy

# 3. Instalar paquetes de ML
!pip install "onnx>=1.15.0" "onnxruntime-gpu>=1.16.0"

# 4. Instalar Gradio
!pip install "gradio>=4.0.0" gradio-rangeslider

# 5. Instalar InsightFace
!pip install insightface

# 6. Ejecutar
!python faceswap_colab_main.py
```

## Método 3: Desde requirements.txt

```python
!pip install -r requirements.txt
!python faceswap_colab_main.py
```

## Solución de Problemas

### Error: "Cannot install gradio==5.44.1"

**Solución:** El script ahora usa versiones flexibles que se adaptan automáticamente. Si aún tienes problemas:

```python
# Instalar versiones específicas compatibles
!pip install numpy==1.26.4
!pip install gradio==4.44.0
!pip install onnx==1.16.0
!pip install onnxruntime-gpu==1.16.3
```

### Error: "numpy version conflict"

**Solución:** Usar numpy 1.x en lugar de 2.x:

```python
!pip install "numpy>=1.24.0,<2.0.0"
```

### Error: "onnxruntime-gpu not found"

**Solución alternativa:** Usar onnxruntime (CPU) si no hay GPU:

```python
!pip install onnxruntime
```

Luego modifica el código para usar CPU en lugar de GPU.

## Notas

- Las versiones ahora son flexibles (>=) para evitar conflictos
- El script intenta instalar todas las dependencias incluso si algunas fallan
- Si una dependencia falla, el script continúa con las demás

