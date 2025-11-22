from typing import Optional

METADATA =\
{
	'name': 'FaceSwapColab',
	'description': 'Industry leading face manipulation platform',
	'version': '3.5.1',
	'license': 'OpenRAIL-AS',
	'author': 'Henry Ruhs',
	'url': 'https://faceswap_colab.io'
}


def get(key : str) -> Optional[str]:
	return METADATA.get(key)



