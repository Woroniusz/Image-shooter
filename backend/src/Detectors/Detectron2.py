import numpy as np
from supervision.detection.core import Detections

from src.Detectors.Detector import Detector
from src.logger.logger import get_logger

from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from detectron2 import model_zoo


logger = get_logger(__name__)


class Detectron2(Detector):
	"""
	Detectron2 detector implementation.
	"""

	def __init__(self, cfg: str):
		"""
		Initialize the Detectron2 detector with configuration and weight files.

		:param cfg: Path to the configuration file.
		:param weight: Path to the weight file.
		"""
		super().__init__(cfg, weight)

	def __call__(self, image: np.ndarray) -> Detections:
		"""
		Detect objects in the given image using Detectron2.

		:param image: The input image as a NumPy array in BGR format.
		:return: Detections object containing detected objects.
		"""
		# Implement the detection logic using Detectron2 here
		pass
