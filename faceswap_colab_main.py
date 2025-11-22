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
    """Instala las dependencias necesarias"""
    print("Instalando dependencias...")
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '-q',
            'gradio-rangeslider==0.0.8',
            'gradio==5.44.1',
            'numpy==2.3.4',
            'onnx==1.19.1',
            'onnxruntime-gpu==1.23.2',
            'opencv-python==4.12.0.88',
            'psutil==7.1.2',
            'tqdm==4.67.1',
            'scipy==1.16.3',
            'insightface==0.7.3'
        ])
        print("✓ Dependencias instaladas correctamente")
    except subprocess.CalledProcessError as e:
        print(f"Error instalando dependencias: {e}")
        return False
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

def main():
    """Función principal"""
    print("=" * 60)
    print("FaceSwapColab - Versión completa para Google Colab")
    print("=" * 60)
    
    # Instalar dependencias
    if not install_dependencies():
        print("Error: No se pudieron instalar las dependencias")
        return
    
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



