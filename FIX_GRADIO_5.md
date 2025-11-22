# Fix para Gradio 5.x

## Problema

En Gradio 5.x, la API de `launch()` cambió:
- ❌ `favicon_path` ya no existe
- ✅ `share` es el parámetro correcto para enlaces públicos (Colab)
- ✅ `server_name` y `server_port` funcionan igual

## Solución Aplicada

Se actualizaron todos los layouts para usar la API de Gradio 5.x:

### Archivos Modificados:

1. ✅ `uis/layouts/default.py`
2. ✅ `uis/layouts/webcam.py`
3. ✅ `uis/layouts/jobs.py`

### Cambios:

**Antes (Gradio 4.x):**
```python
ui.launch(favicon_path = 'faceswap_colab.ico', inbrowser = False)
```

**Ahora (Gradio 5.x):**
```python
ui.launch(
    inbrowser = state_manager.get_item('open_browser'),
    share = True,  # Para Colab - enlace público
    server_name = '0.0.0.0',
    server_port = 7860
)
```

### Manejo de Errores:

El código incluye fallbacks para compatibilidad:
1. Intenta con parámetros de Gradio 5.x
2. Si falla, intenta solo con `inbrowser`
3. Si falla, lanza sin parámetros

## Resultado

✅ La interfaz ahora funciona correctamente con Gradio 5.x
✅ Se genera un enlace público automáticamente (share=True)
✅ Compatible con versiones anteriores si es necesario

