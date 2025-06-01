import os
from abc import ABC, abstractmethod

import numpy as np
from supervision.detection.core import Detections

from src.logger.logger import get_logger

logger = get_logger(__name__)


class Detector(ABC):
	"""
	Abstract base class for detectors.
	"""

	def __init__(self, cfg: str):
		"""
		Initialize the detector with configuration and weight files.
		"""
		# Init: check if cfg and weight files exist
		if not os.path.exists(cfg):
			logger.error(f'Configuration file {cfg} does not exist.')
			raise FileNotFoundError(f'Configuration file {cfg} does not exist.')

		self.cfg = cfg
		self.weight = weight

	@abstractmethod
	def __call__(self, image: np.ndarray) -> Detections:
		"""
		Detect objects in the given image.

		:param image: The input image as a NumPy array BGR format.

		:return: Detections object containing detected objects.
		"""
		pass
