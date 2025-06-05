import os
from typing import Any

import numpy as np
import torch
from detectron2 import model_zoo
from detectron2.config import CfgNode, get_cfg
from detectron2.engine import DefaultPredictor
from detectron2.structures import Instances
from supervision.detection.core import Detections

from source_app.Detectors.Detector import Detector
from source_app.Logger.logger import get_logger
from source_app.utils.Config import Config

logger = get_logger(__name__)


def detectron2_to_supervision(outputs: dict[str, Any]) -> Detections:
	instances: Instances = outputs['instances']

	# move to cpu
	instances = instances.to('cpu')

	# get bounding boxes in xyxy format
	boxes_tensor: torch.Tensor = instances.pred_boxes.tensor  # torch.Tensor (N,4)
	boxes_xyxy: np.ndarray = boxes_tensor.numpy()

	# get scores and class ids
	scores: np.ndarray = instances.scores.numpy()  # numpy array (N,)
	class_ids: np.ndarray = instances.pred_classes.numpy()  # numpy array (N,)
	if boxes_xyxy.shape[0] == 0:
		return Detections.empty()

	# convert to Detections object
	detections: Detections = Detections(xyxy=boxes_xyxy, confidence=scores, class_id=class_ids)

	return detections


def filter_detections(detections: Detections, filters: list[int]) -> Detections:
	if (
		not detections.is_empty()
		and detections.class_id is not None
		and len(filters) > 0
		and detections.confidence is not None
	):
		mask = np.isin(detections.class_id, filters)
		if not mask.any():
			return Detections.empty()

		detections = Detections(
			xyxy=detections.xyxy[mask], confidence=detections.confidence[mask], class_id=detections.class_id[mask]
		)
	return detections


class Detectron2(Detector):
	"""
	Detectron2 detector implementation.
	"""

	def __init__(self, cfg: Config):
		"""
		Initialize the Detectron2 detector with configuration and weight files.
		"""
		super().__init__(cfg)
		conf: CfgNode = get_cfg()
		conf.merge_from_file(self.cfg.Detectors.Detectron2.cfg)
		conf.MODEL.WEIGHTS = self.cfg.Detectors.Detectron2.weights  # its work when it will be github LFS
		if not os.path.exists(self.cfg.Detectors.Detectron2.weights):
			logger.error('Model weights not found. Please download the model weights.')
			conf.MODEL.WEIGHTS = model_zoo.get_checkpoint_url('COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml')
		conf.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
		conf.MODEL.DEVICE = cfg.Detectors.device

		self.model = DefaultPredictor(conf)

	def __call__(self, image: np.ndarray) -> Detections:
		"""
		Detect objects in the given image using Detectron2.

		:param image: The input image as a NumPy array in BGR format.
		:return: Detections object containing detected objects.
		"""

		if image.ndim != 3 or image.shape[2] != 3:
			raise ValueError('Input image must be a 3-channel BGR image.')

		outputs: dict[str, Any] = self.model(image)

		# convert outputs to Detections object
		detections: Detections = detectron2_to_supervision(outputs)
		# filter
		detections_filtred: Detections = filter_detections(detections, self.cfg.Detectors.Detectron2.filters)

		return detections_filtred
