from src.Detectors.Detector import Detector
from src.Detectors.Detectron2 import Detectron2
from src.utils.Config import Config


class FactoryDetector:
	"""
	Factory class for creating detector instances.
	"""

	@staticmethod
	def create_detector(config: Config) -> Detector:
		"""
		Create a detector instance based on the provided name and configuration.

		:param detector_name: Name of the detector to create.
		:param config: Configuration dictionary for the detector.
		:return: An instance of the specified detector.
		"""

		if config.Detectors.name == 'Detectron2':
			return Detectron2(config)
		else:
			raise ValueError(f"Detector '{config.Detectors.name}' is not supported.")
