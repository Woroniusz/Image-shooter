from abc import ABC, abstractmethod

import numpy as np
from supervision.detection.core import Detections

from source_app.Logger.logger import get_logger
from source_app.utils.Config import Config

logger = get_logger(__name__)


class Detector(ABC):
	"""
	Abstract base class for detectors.
	"""

	def __init__(self, cfg: Config):
		"""
		Initialize the detector with configuration and weight files.
		"""
		# Init: check if cfg and weight files exist
		self.cfg: Config = cfg

	@abstractmethod
	def __call__(self, image: np.ndarray) -> Detections:
		"""
		Detect objects in the given image.

		:param image: The input image as a NumPy array BGR format.

		:return: Detections object containing detected objects.
		"""
		pass
