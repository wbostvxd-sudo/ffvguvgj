"""
Compatibilidad entre NumPy 1.x y 2.x
Proporciona funciones de compatibilidad para trabajar con ambas versiones
"""
import numpy as np
import sys

# Detectar versión de numpy
NUMPY_VERSION = tuple(map(int, np.__version__.split('.')[:2]))
NUMPY_2_PLUS = NUMPY_VERSION >= (2, 0)

# Importar broadcast_to según la versión
if NUMPY_2_PLUS:
    # En numpy 2.x, broadcast_to está directamente en numpy
    try:
        from numpy import broadcast_to
    except ImportError:
        # Fallback: usar la implementación manual
        def broadcast_to(array, shape):
            return np.broadcast_to(array, shape)
    
    # PARCHAR numpy.lib.stride_tricks para compatibilidad con código antiguo
    # Esto permite que scipy y otros módulos que importan desde ahí funcionen
    try:
        import numpy.lib.stride_tricks as stride_tricks_module
        if not hasattr(stride_tricks_module, 'broadcast_to'):
            stride_tricks_module.broadcast_to = broadcast_to
    except:
        pass
else:
    # En numpy 1.x, está en numpy.lib.stride_tricks
    try:
        from numpy.lib.stride_tricks import broadcast_to
    except ImportError:
        # Fallback: usar la función directa de numpy
        from numpy import broadcast_to

# Exportar para uso en otros módulos
__all__ = ['broadcast_to', 'NUMPY_2_PLUS', 'NUMPY_VERSION']

