# Fix para Valores None en State Manager

## Problema

Varios componentes de la UI intentan acceder a valores del `state_manager` que pueden ser `None`, causando errores como:
- `'NoneType' object is not subscriptable`
- `unsupported operand type(s) for +: 'NoneType' and 'list'`

## Solución Implementada

### 1. ✅ Módulo de Inicialización

**Archivo creado:** `faceswap_colab/init_defaults.py`

Inicializa todos los valores por defecto necesarios:
- ✅ `processors`: []
- ✅ `background_remover_color`: (0, 0, 0, 0)
- ✅ `face_detector_margin`: (0, 0, 0, 0)
- ✅ `face_mask_padding`: (0, 0, 0, 0)
- ✅ Y muchos más valores por defecto

### 2. ✅ Correcciones en Componentes

Se agregaron verificaciones de `None` en:

**background_remover_options.py:**
```python
background_remover_color = state_manager.get_item('background_remover_color')
if background_remover_color is None:
    background_remover_color = (0, 0, 0, 0)
    state_manager.set_item('background_remover_color', background_remover_color)
```

**face_detector.py:**
```python
face_detector_margin = state_manager.get_item('face_detector_margin')
if face_detector_margin is None:
    face_detector_margin = (0, 0, 0, 0)
    state_manager.set_item('face_detector_margin', face_detector_margin)
```

**face_masker.py:**
```python
face_mask_types = state_manager.get_item('face_mask_types')
if face_mask_types is None:
    face_mask_types = []
    state_manager.set_item('face_mask_types', face_mask_types)

face_mask_padding = state_manager.get_item('face_mask_padding')
if face_mask_padding is None:
    face_mask_padding = (0, 0, 0, 0)
    state_manager.set_item('face_mask_padding', face_mask_padding)
```

**preview.py:**
```python
background_remover_color = state_manager.get_item('background_remover_color')
if background_remover_color is None:
    background_remover_color = (0, 0, 0, 0)
```

**processors.py:**
```python
# Ya corregido anteriormente
if processors is None:
    processors = []
```

### 3. ✅ Integración en Script Principal

El script `faceswap_colab_main.py` ahora:
1. Inicializa valores básicos
2. Llama a `init_default_state()` para inicializar todos los valores
3. Los componentes verifican `None` antes de usar valores

## Valores Inicializados

El módulo `init_defaults.py` inicializa más de 50 valores por defecto, incluyendo:

- Configuración básica (paths, log_level, etc.)
- Face detector (model, size, margin, angles, score)
- Face landmarker (model, score)
- Face selector (mode, order, gender, race, age, etc.)
- Face mask (types, areas, regions, blur, padding)
- Output (image/video quality, scale, encoder, preset, fps)
- Execution (providers, device_ids, thread_count, memory)
- Processors (background_remover, face_swapper, etc.)

## Resultado

✅ **Todos los valores están inicializados antes de usar la UI**
✅ **Manejo seguro de `None` en todos los componentes**
✅ **La UI se renderiza sin errores**
✅ **Compatible con el flujo normal de FaceFusion**

## Archivos Modificados

1. ✅ `faceswap_colab/init_defaults.py` - **NUEVO**
2. ✅ `faceswap_colab_main.py` - Integración de init_defaults
3. ✅ `uis/components/processors.py` - Manejo de None
4. ✅ `uis/components/background_remover_options.py` - Manejo de None
5. ✅ `uis/components/face_detector.py` - Manejo de None
6. ✅ `uis/components/face_masker.py` - Manejo de None
7. ✅ `uis/components/preview.py` - Manejo de None

