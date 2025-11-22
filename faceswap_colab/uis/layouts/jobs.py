import gradio

from faceswap_colab import state_manager
from faceswap_colab.uis.components import about, job_list, job_list_options


def pre_check() -> bool:
	return True


def render() -> gradio.Blocks:
	with gradio.Blocks() as layout:
		with gradio.Row():
			with gradio.Column(scale = 4):
				with gradio.Blocks():
					about.render()
				with gradio.Blocks():
					job_list_options.render()
			with gradio.Column(scale = 11):
				with gradio.Blocks():
					job_list.render()
	return layout


def listen() -> None:
	job_list_options.listen()
	job_list.listen()


def run(ui : gradio.Blocks) -> None:
	# En Gradio 5.x, favicon_path ya no existe, usar share para Colab
	try:
		ui.launch(
			inbrowser = state_manager.get_item('open_browser'),
			share = True,
			server_name = '0.0.0.0',
			server_port = 7860
		)
	except TypeError:
		try:
			ui.launch(inbrowser = state_manager.get_item('open_browser'))
		except:
			ui.launch()
