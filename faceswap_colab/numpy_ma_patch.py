"""
Parche para numpy.ma (masked arrays) en NumPy 2.x
Soluciona el error: AttributeError: 'numpy.ufunc' object has no attribute '__qualname__'
"""

import sys

def patch_numpy_ma():
    """Parchea numpy.ma para que funcione con NumPy 2.x"""
    try:
        import numpy as np
        
        # Solo aplicar el parche si es NumPy 2.x
        numpy_version = tuple(map(int, np.__version__.split('.')[:2]))
        if numpy_version[0] < 2:
            return  # No es necesario en NumPy 1.x
        
        # Parchear numpy.ma.core antes de que se importe
        import numpy.ma.core as ma_core
        
        # Guardar la clase original
        _OriginalMaskedUnaryOperation = ma_core._MaskedUnaryOperation
        
        # Crear una versión parcheada
        class _PatchedMaskedUnaryOperation(_OriginalMaskedUnaryOperation):
            def __init__(self, mufunc):
                # Llamar al __init__ del abuelo (MaskedUFunc) directamente
                # para evitar el problema con __qualname__
                ma_core.MaskedUFunc.__init__(self, mufunc)
                
                # Establecer __qualname__ manualmente si no existe
                if not hasattr(mufunc, '__qualname__'):
                    self.__qualname__ = mufunc.__name__ if hasattr(mufunc, '__name__') else 'unknown'
                else:
                    self.__qualname__ = mufunc.__qualname__
        
        # Reemplazar la clase en el módulo
        ma_core._MaskedUnaryOperation = _PatchedMaskedUnaryOperation
        
        # También parchear _MaskedBinaryOperation si existe
        if hasattr(ma_core, '_MaskedBinaryOperation'):
            _OriginalMaskedBinaryOperation = ma_core._MaskedBinaryOperation
            
            class _PatchedMaskedBinaryOperation(_OriginalMaskedBinaryOperation):
                def __init__(self, mbfunc):
                    ma_core.MaskedUFunc.__init__(self, mbfunc)
                    if not hasattr(mbfunc, '__qualname__'):
                        self.__qualname__ = mbfunc.__name__ if hasattr(mbfunc, '__name__') else 'unknown'
                    else:
                        self.__qualname__ = mbfunc.__qualname__
            
            ma_core._MaskedBinaryOperation = _PatchedMaskedBinaryOperation
        
        return True
        
    except Exception as e:
        # Si falla el parche, intentar una solución alternativa
        try:
            import numpy as np
            
            # Agregar __qualname__ a todos los ufuncs si no lo tienen
            import numpy.core.umath as umath
            for name in dir(umath):
                obj = getattr(umath, name)
                if isinstance(obj, np.ufunc) and not hasattr(obj, '__qualname__'):
                    try:
                        object.__setattr__(obj, '__qualname__', name)
                    except:
                        pass
            
            return True
        except:
            return False

# Aplicar el parche inmediatamente al importar
patch_numpy_ma()
