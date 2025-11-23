"""
Inicialización de valores por defecto para state_manager
Asegura que todos los valores necesarios estén inicializados antes de usar la UI
"""
from typing import List, Tuple
import tempfile

def init_default_state():
    """Inicializa todos los valores por defecto necesarios para la UI"""
    from faceswap_colab import state_manager
    
    # Valores básicos
    defaults = {
        'processors': ['face_swapper'],  # Procesador principal para intercambio de rostros
        'source_paths': [],
        'target_path': '',
        'output_path': '',
        'temp_path': tempfile.gettempdir(),
        'jobs_path': '.jobs',
        'config_path': 'faceswap_colab.ini',
        'log_level': 'info',
        'open_browser': False,
        'ui_layouts': ['default'],
        'ui_workflow': 'instant_runner',
        'command': 'run',
        
        # Face detector defaults
        'face_detector_model': 'yolo_face',
        'face_detector_size': '640x640',
        'face_detector_margin': (0, 0, 0, 0),
        'face_detector_angles': [0],
        'face_detector_score': 0.5,
        
        # Face landmarker defaults
        'face_landmarker_model': 'many',
        'face_landmarker_score': 0.0,
        
        # Face selector defaults
        'face_selector_mode': 'many',
        'face_selector_order': 'left-right',
        'face_selector_gender': None,
        'face_selector_race': None,
        'face_selector_age_start': 0,
        'face_selector_age_end': 100,
        'reference_face_position': 0,
        'reference_face_distance': 0.6,
        'reference_frame_number': 0,
        
        # Face mask defaults
        'face_occluder_model': 'many',
        'face_parser_model': 'bisenet_resnet_18',
        'face_mask_types': [],
        'face_mask_areas': [],
        'face_mask_regions': [],
        'face_mask_blur': 0.3,
        'face_mask_padding': (0, 0, 0, 0),
        
        # Output defaults
        'output_image_quality': 80,
        'output_image_scale': 1.0,
        'output_video_encoder': 'libx264',
        'output_video_preset': 'medium',
        'output_video_quality': 80,
        'output_video_scale': 1.0,
        'output_video_fps': 25.0,
        'output_audio_encoder': 'aac',
        'output_audio_quality': 80,
        'output_audio_volume': 100,
        
        # Execution defaults
        'execution_providers': ['cpu'],
        'execution_device_ids': [0],  # Usar device 0 por defecto (GPU en Colab, CPU si no hay GPU)
        'execution_thread_count': 4,
        'video_memory_strategy': 'moderate',
        'system_memory_limit': 0,
        
        # Other defaults
        'temp_frame_format': 'jpeg',
        'keep_temp': False,
        'trim_frame_start': None,
        'trim_frame_end': None,
        'voice_extractor_model': 'kim_vocal_1',
        'download_providers': ['github'],
        'download_scope': 'lite',
        'halt_on_error': False,
        
        # Background remover defaults
        'background_remover_model': 'ben_2',
        'background_remover_color': (0, 0, 0, 0),  # RGBA - transparente por defecto
        
        # Face swapper defaults
        'face_swapper_model': 'inswapper_128',  # Modelo por defecto para intercambio de rostros
        'face_swapper_pixel_boost': '128x128',  # Resolución de procesamiento
        'face_swapper_weight': 0.5,  # Balance entre rostro fuente y objetivo
        
        # Job defaults
        'job_id': '',
        'job_status': 'drafted',
        'step_index': 0,
    }
    
    # Inicializar solo los que no existen
    for key, value in defaults.items():
        if state_manager.get_item(key) is None:
            state_manager.init_item(key, value)
    
    # Detectar y configurar GPU/CUDA automáticamente
    try:
        from onnxruntime import get_available_providers
        available_providers = get_available_providers()
        
        # Verificar si CUDA está disponible en onnxruntime
        if 'CUDAExecutionProvider' in available_providers:
            # GPU disponible - usar CUDA
            state_manager.set_item('execution_providers', ['cuda'])
            print("  ✓ GPU detectada - usando CUDA (onnxruntime)")
        elif 'TensorrtExecutionProvider' in available_providers:
            # TensorRT disponible
            state_manager.set_item('execution_providers', ['tensorrt'])
            print("  ✓ GPU detectada - usando TensorRT")
        else:
            # Solo CPU disponible
            print("  ℹ GPU no detectada - usando CPU")
    except Exception as e:
        # Si falla la detección, usar CPU (ya está configurado)
        print(f"  ⚠ Error detectando GPU: {e}")
        print("  ℹ Usando CPU por defecto")

