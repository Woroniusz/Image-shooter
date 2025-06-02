from source_app.Detectors.Detector import Detector
from source_app.Detectors.Detectron2 import Detectron2
from source_app.utils.Config import Config


class FactoryDetector:
	"""
	Factory class for creating detector instances.
	"""

	@staticmethod
	def create_detector(config: Config) -> Detector:
		"""
		Create a detector instance based on the provided name and configuration.

		:param config: Configuration dictionary for the detector.
		:return: An instance of the specified detector.
		"""

		if config.Detectors.name == 'Detectron2':
			return Detectron2(config)
		else:
			raise ValueError(f"Detector '{config.Detectors.name}' is not supported.")
