from typing import List, Optional

import gradio

from faceswap_colab import state_manager, translator
from faceswap_colab.filesystem import get_file_name, resolve_file_paths, resolve_relative_path
from faceswap_colab.processors.core import get_processors_modules
from faceswap_colab.uis.core import register_ui_component

PROCESSORS_CHECKBOX_GROUP : Optional[gradio.CheckboxGroup] = None


def render() -> None:
	global PROCESSORS_CHECKBOX_GROUP
	
	# Asegurar que processors no sea None
	processors = state_manager.get_item('processors')
	if processors is None:
		processors = []
		state_manager.set_item('processors', processors)

	PROCESSORS_CHECKBOX_GROUP = gradio.CheckboxGroup(
		label = translator.get('uis.processors_checkbox_group'),
		choices = sort_processors(processors),
		value = processors
	)
	register_ui_component('processors_checkbox_group', PROCESSORS_CHECKBOX_GROUP)


def listen() -> None:
	PROCESSORS_CHECKBOX_GROUP.change(update_processors, inputs = PROCESSORS_CHECKBOX_GROUP, outputs = PROCESSORS_CHECKBOX_GROUP)


def update_processors(processors : List[str]) -> gradio.CheckboxGroup:
	# Manejar None
	if processors is None:
		processors = []
	
	# Limpiar procesadores anteriores
	old_processors = state_manager.get_item('processors')
	if old_processors is not None:
		for processor_module in get_processors_modules(old_processors):
			if hasattr(processor_module, 'clear_inference_pool'):
				processor_module.clear_inference_pool()

	# Verificar nuevos procesadores
	if processors:
		for processor_module in get_processors_modules(processors):
			if not processor_module.pre_check():
				return gradio.CheckboxGroup()

	state_manager.set_item('processors', processors)
	return gradio.CheckboxGroup(value = processors, choices = sort_processors(processors))


def sort_processors(processors : List[str]) -> List[str]:
	available_processors = [ get_file_name(file_path) for file_path in resolve_file_paths(resolve_relative_path('processors/modules')) ]
	current_processors = []
	
	# Manejar caso cuando processors es None
	if processors is None:
		processors = []

	for processor in processors + available_processors:
		if processor in available_processors and processor not in current_processors:
			current_processors.append(processor)

	return current_processors
