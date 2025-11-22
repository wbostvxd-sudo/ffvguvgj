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

# Agregar el directorio al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def install_dependencies():
    """Instala las dependencias necesarias con versiones compatibles"""
    print("Instalando dependencias...")
    
    # Actualizar pip primero
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '--quiet', '--upgrade', 'pip', 'setuptools', 'wheel'
        ])
    except:
        pass
    
    # CRÍTICO: Forzar numpy 1.x primero (Colab puede tener numpy 2.x preinstalado)
    print("  Forzando numpy 1.x (compatible)...")
    try:
        # Desinstalar cualquier numpy 2.x y paquetes dependientes
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'uninstall', '-y', 'numpy', 'pandas', 'scipy'
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        pass
    
    # Instalar numpy 1.x explícitamente (versión que tiene broadcast_to)
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '--quiet', '--no-cache-dir', 'numpy==1.26.4'
        ])
        print("  ✓ numpy 1.26.4 instalado")
    except:
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', '--quiet', '--no-cache-dir', 'numpy==1.26.4'
            ])
        except:
            print("  ⚠ Error instalando numpy, intentando continuar...")
    
    # Reinstalar pandas y scipy DESPUÉS de numpy (para compatibilidad)
    print("  Reinstalando pandas y scipy (compatible con numpy 1.x)...")
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '--quiet', '--no-cache-dir', 
            'pandas>=2.0.0', 'scipy==1.11.4'
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        pass
    
    # Desinstalar opencv-python si existe (necesita recompilarse con numpy 1.x)
    print("  Reinstalando opencv-python (compatible con numpy 1.x)...")
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'uninstall', '-y', 'opencv-python', 'opencv-contrib-python'
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        pass
    
    # Lista de paquetes con versiones compatibles probadas
    packages = [
        # Base - numpy ya instalado arriba
        ('opencv-python', '4.9.0.80'),
        ('psutil', '5.9.8'),
        ('tqdm', '4.66.1'),
        ('scipy', '1.11.4'),
        # ML
        ('onnx', '1.16.0'),
        ('onnxruntime-gpu', '1.16.3'),
        # Gradio - versión estable (reinstalar después de numpy/pandas)
        ('gradio', '4.44.0'),
        ('gradio-rangeslider', '0.0.8'),
        # InsightFace
        ('insightface', '0.7.3'),
    ]
    
    failed_packages = []
    
    # Instalar cada paquete individualmente
    for package_name, version in packages:
        try:
            print(f"  Instalando {package_name}=={version}...")
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', '--quiet', 
                f'{package_name}=={version}'
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            # Si falla con versión exacta, intentar sin versión
            try:
                print(f"  Intentando {package_name} (última versión)...")
                subprocess.check_call([
                    sys.executable, '-m', 'pip', 'install', '--quiet', package_name
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except:
                failed_packages.append(package_name)
                print(f"  ⚠ No se pudo instalar {package_name}")
    
    # Verificar numpy y reinstalar dependencias si es necesario
    try:
        import numpy
        if numpy.__version__.startswith('2.'):
            print("  ⚠ ADVERTENCIA: numpy 2.x detectado, forzando downgrade...")
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', '--force-reinstall', '--no-deps', 
                '--no-cache-dir', 'numpy==1.26.4'
            ])
            # Reinstalar dependencias que necesitan numpy
            print("  Reinstalando dependencias compatibles...")
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', '--force-reinstall', '--no-cache-dir',
                'pandas', 'scipy==1.11.4', 'opencv-python==4.9.0.80'
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"  ⚠ Error en verificación: {e}")
    
    # Reinstalar gradio después de asegurar numpy/pandas correctos
    print("  Reinstalando Gradio (compatible)...")
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '--force-reinstall', '--no-cache-dir',
            'gradio==4.44.0', 'gradio-rangeslider==0.0.8'
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        pass
    
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
    """Verifica que numpy 1.x esté instalado correctamente y que broadcast_to funcione"""
    try:
        import numpy
        from numpy.lib.stride_tricks import broadcast_to
        version = numpy.__version__
        if version.startswith('2.'):
            print(f"⚠ ADVERTENCIA: NumPy {version} detectado (incompatible)")
            print("  Forzando downgrade a NumPy 1.26.4...")
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', '--force-reinstall', 
                '--no-deps', '--no-cache-dir', 'numpy==1.26.4'
            ])
            # Reinstalar pandas y gradio
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', '--force-reinstall', '--no-cache-dir',
                'pandas', 'gradio==4.44.0'
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            # Recargar numpy
            import importlib
            import numpy
            importlib.reload(numpy)
            print(f"  ✓ NumPy {numpy.__version__} ahora activo")
        else:
            # Verificar que broadcast_to funciona
            try:
                from numpy.lib.stride_tricks import broadcast_to
                test_array = numpy.array([1, 2, 3])
                broadcast_to(test_array, (2, 3))
                print(f"  ✓ NumPy {version} (compatible, broadcast_to funciona)")
            except ImportError:
                print(f"  ⚠ NumPy {version} no tiene broadcast_to, reinstalando...")
                subprocess.check_call([
                    sys.executable, '-m', 'pip', 'install', '--force-reinstall', 
                    '--no-cache-dir', 'numpy==1.26.4'
                ])
                subprocess.check_call([
                    sys.executable, '-m', 'pip', 'install', '--force-reinstall', '--no-cache-dir',
                    'pandas', 'gradio==4.44.0'
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception as e:
        print(f"  ⚠ Error verificando NumPy: {e}")
        print("  Intentando reinstalar numpy y dependencias...")
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', '--force-reinstall', '--no-cache-dir',
                'numpy==1.26.4', 'pandas', 'gradio==4.44.0'
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            pass
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
    if not verify_numpy():
        print("⚠ Advertencia: Problema con NumPy, intentando continuar...")
    
    # Configurar entorno
    setup_environment()
    
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
        
        # Lanzar la interfaz
        import faceswap_colab.uis.core as ui
        ui.init()
        ui.launch(share=True, server_name='0.0.0.0', server_port=7860)
        
    except Exception as e:
        print(f"Error al iniciar: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()



