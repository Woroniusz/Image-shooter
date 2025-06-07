import cv2
import numpy as np
import pytest
import torch
from detectron2.engine import DefaultPredictor
from detectron2.structures import Boxes, Instances
from supervision.detection.core import Detections

from source_app.Detectors.Detector import Detector
from source_app.Detectors.Detectron2 import Detectron2, detectron2_to_supervision, filter_detections
from source_app.Detectors.FactoryDetector import FactoryDetector
from source_app.utils.Config import Config


@pytest.fixture
def mock_config() -> Config:
	"""
	Fixture to provide a mock Config object for testing.
	"""

	return Config.from_dict(
		{
			'Detectors': {
				'name': 'Detectron2',
				'device': 'cpu',
				'Detectron2': {
					'cfg': 'source_app/zoo/detectron2/faster_rcnn_R_50_FPN_3x.yaml',
					'weights': 'source_app/zoo/detectron2/model.pt',
					'filters': [2],
				},
			},
		}
	)


def test_detectron2_to_supervision() -> None:
	"""
	Test the _detectron2_to_supervision method of the Detectron2 class.
	"""

	# Create a mock output from Detectron2
	instances = Instances((1, 1))
	instances.pred_boxes = Boxes(torch.tensor([[10, 20, 30, 40]]))  # xyxy format
	instances.scores = torch.tensor([0.9])
	instances.pred_classes = torch.tensor([1])

	outputs = {'instances': instances}
	detections = detectron2_to_supervision(outputs)

	assert detections.xyxy is not None
	assert detections.xyxy.shape == (1, 4)
	assert detections.confidence is not None
	assert detections.confidence.shape == (1,)
	assert detections.class_id is not None
	assert detections.class_id.shape == (1,)


def test_filter_detections() -> None:
	"""
	Test the filter_detections function.
	"""

	# Create mock detections
	detections = Detections(
		xyxy=np.array([[10, 20, 30, 40], [50, 60, 70, 80]]), confidence=np.array([0.9, 0.8]), class_id=np.array([1, 2])
	)

	# Filter for class_id 2
	filtered_detections = filter_detections(detections, [2])

	assert filtered_detections.xyxy.shape == (1, 4)
	assert filtered_detections.confidence is not None
	assert filtered_detections.confidence.shape == (1,)
	assert filtered_detections.class_id is not None
	assert filtered_detections.class_id.shape == (1,)
	assert filtered_detections.class_id[0] == 2


def test_filter_empty() -> None:
	"""
	Test the filter_detections function with empty detections.
	"""

	# Create empty detections
	detections = Detections.empty()

	# Filter for class_id 2
	filtered_detections = filter_detections(detections, [2])

	assert filtered_detections.is_empty()

	# filter class 1

	detections2 = Detections(xyxy=np.array([[10, 20, 30, 40]]), confidence=np.array([0.9]), class_id=np.array([1]))

	filtered_detections = filter_detections(detections2, [1])

	assert not detections2.is_empty()


def test_detectron2(mock_config: Config) -> None:
	"""
	Test the Detectron2 detector initialization and configuration.
	"""

	detector = Detectron2(mock_config)

	# Check if the predictor is initialized correctly
	assert isinstance(detector.model, DefaultPredictor)
	assert detector.model.model is not None

	# detect test
	image = np.zeros((640, 640, 3), dtype=np.uint8)  # Mock image
	outputs: Detections = detector(image)
	assert isinstance(outputs, Detections)
	assert outputs.is_empty()


def test_factory_detector(mock_config: Config) -> None:
	"""
	Test the FactoryDetector with Detectron2.
	"""

	detector: Detector = FactoryDetector.create_detector(mock_config)

	# detect test
	image = np.zeros((640, 640, 3), dtype=np.uint8)  # Mock image
	outputs: Detections = detector(image)
	assert isinstance(outputs, Detections)
	assert outputs.is_empty()


def test_factory_detector_invalid() -> None:
	"""
	Test the FactoryDetector with an invalid detector name.
	"""

	with pytest.raises(ValueError, match="Detector 'InvalidDetector' is not supported."):
		mock_config = Config.from_dict(
			{
				'Detectors': {
					'name': 'InvalidDetector',
				},
			}
		)
		FactoryDetector.create_detector(mock_config)


@pytest.mark.manul
def test_detection(mock_config: Config) -> None:
	"""
	Test the detection process with Detectron2.
	"""

	detector: Detector = FactoryDetector.create_detector(mock_config)

	# Create a mock image
	image = cv2.imread('tests/sample_image/image1.jpg')

	# Perform detection
	outputs: Detections = detector(image)

	assert isinstance(outputs, Detections)
	assert not outputs.is_empty()
	assert len(outputs.xyxy) > 0
