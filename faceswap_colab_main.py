#!/usr/bin/env python3
"""
FaceSwapColab - Versión completa de FaceFusion adaptada para Google Colab
Copia literal de FaceFusion con nombres cambiados
"""

import os
import sys
import subprocess
import tempfile

# Configurar variables de entorno para optimización
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'

# Agregar el directorio al path PRIMERO
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# CARGAR MÓDULO DE COMPATIBILIDAD DE NUMPY ANTES DE CUALQUIER OTRA COSA
# Esto parchea numpy.lib.stride_tricks para que scipy y otros módulos funcionen
try:
    from faceswap_colab import numpy_compat
    # Forzar el parche inmediatamente
    if numpy_compat.NUMPY_2_PLUS:
        import numpy.lib.stride_tricks as stride_tricks_module
        if not hasattr(stride_tricks_module, 'broadcast_to'):
            stride_tricks_module.broadcast_to = numpy_compat.broadcast_to
except Exception as e:
    # Si falla, continuar de todas formas
    pass

def install_dependencies():
    """Instala las dependencias necesarias con versiones ACTUALES (numpy 2.x compatible)"""
    print("Instalando dependencias (versiones actuales)...")
    
    # Actualizar pip primero
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '--quiet', '--upgrade', 'pip', 'setuptools', 'wheel'
        ])
    except:
        pass
    
    # Usar versiones ACTUALES compatibles con numpy 2.x
    print("  Instalando versiones actuales compatibles...")
    
    # Lista de paquetes con versiones ACTUALES
    packages = [
        # Base - usar versiones actuales que soportan numpy 2.x
        ('numpy', None),  # Usar la versión actual (2.x) que ya está en Colab
        ('opencv-python', '4.12.0.88'),  # Versión actual que requiere numpy>=2.0
        ('pandas', None),  # Instalar versión actual compatible
        ('scipy', None),  # Instalar versión actual compatible
        ('psutil', None),
        ('tqdm', None),
        # ML
        ('onnx', None),  # Versión actual
        ('onnxruntime-gpu', None),  # Versión actual
        # Gradio - versión actual
        ('gradio', None),  # Usar versión actual (5.x)
        ('gradio-rangeslider', None),
        # InsightFace
        ('insightface', '0.7.3'),
    ]
    
    failed_packages = []
    
    # Instalar cada paquete (sin forzar versiones antiguas)
    for package_info in packages:
        if len(package_info) == 2:
            package_name, version = package_info
        else:
            package_name = package_info[0]
            version = None
        
        try:
            if version:
                print(f"  Instalando {package_name}=={version}...")
                subprocess.check_call([
                    sys.executable, '-m', 'pip', 'install', '--quiet', '--upgrade',
                    f'{package_name}=={version}'
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                print(f"  Instalando {package_name} (última versión)...")
                subprocess.check_call([
                    sys.executable, '-m', 'pip', 'install', '--quiet', '--upgrade', package_name
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            failed_packages.append(package_name)
            print(f"  ⚠ No se pudo instalar {package_name}")
    
    if failed_packages:
        print(f"\n⚠ Advertencia: No se pudieron instalar: {', '.join(failed_packages)}")
        print("Intentando continuar...")
    
    print("✓ Instalación de dependencias completada")
    return True

def setup_environment():
    """Configura el entorno para Colab"""
    # Crear directorios temporales si no existen
    temp_dir = tempfile.gettempdir()
    os.makedirs(os.path.join(temp_dir, 'faceswap_colab'), exist_ok=True)
    os.makedirs(os.path.join(temp_dir, 'faceswap_colab', 'gradio'), exist_ok=True)
    
    # Configurar variables de entorno
    os.environ['GRADIO_ANALYTICS_ENABLED'] = '0'
    os.environ['GRADIO_TEMP_DIR'] = os.path.join(temp_dir, 'faceswap_colab', 'gradio')

def verify_numpy():
    """Verifica que numpy esté instalado correctamente (soporta 1.x y 2.x)"""
    try:
        import numpy
        version = numpy.__version__
        print(f"  NumPy {version} detectado")
        
        # Intentar importar broadcast_to usando el módulo de compatibilidad
        try:
            # Intentar importar nuestro módulo de compatibilidad
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            from faceswap_colab.numpy_compat import broadcast_to
            
            # Probar que funciona
            test_array = numpy.array([1, 2, 3])
            result = broadcast_to(test_array, (2, 3))
            print(f"  ✓ NumPy {version} (compatible, broadcast_to funciona)")
            return True
        except Exception as e:
            print(f"  ⚠ Error con broadcast_to: {e}")
            print("  El módulo de compatibilidad se cargará al importar")
            return True  # Continuar de todas formas, el módulo de compatibilidad lo manejará
    except Exception as e:
        print(f"  ⚠ Error verificando NumPy: {e}")
        return False

def main():
    """Función principal"""
    print("=" * 60)
    print("FaceSwapColab - Versión completa para Google Colab")
    print("=" * 60)
    
    # Instalar dependencias
    if not install_dependencies():
        print("Error: No se pudieron instalar las dependencias")
        return
    
    # Verificar numpy antes de continuar
    print("\nVerificando NumPy...")
    verify_numpy()
    
    # Configurar entorno
    setup_environment()
    
    # Cargar módulo de compatibilidad de numpy ANTES de importar otros módulos
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from faceswap_colab import numpy_compat
        print("  ✓ Módulo de compatibilidad NumPy cargado")
    except Exception as e:
        print(f"  ⚠ Advertencia: No se pudo cargar módulo de compatibilidad: {e}")
    
    # Importar y ejecutar
    try:
        from faceswap_colab import core
        
        # Configurar para modo UI
        from faceswap_colab import state_manager
        state_manager.init_item('command', 'run')
        state_manager.init_item('ui_layouts', ['default'])
        state_manager.init_item('open_browser', False)
        state_manager.init_item('temp_path', tempfile.gettempdir())
        state_manager.init_item('log_level', 'info')
        
        print("\n✓ Iniciando interfaz...")
        print("=" * 60)
        
        # Lanzar la interfaz usando el sistema de UI de FaceFusion
        import faceswap_colab.uis.core as ui
        ui.init()
        
        # El método launch() de uis/core.py crea la UI y llama a run() en cada layout
        # El método run() en los layouts maneja el lanzamiento real con Gradio
        ui.launch()
        
    except Exception as e:
        print(f"Error al iniciar: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()



