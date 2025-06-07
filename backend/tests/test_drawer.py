import cv2
import numpy as np
import pytest
from supervision.detection.core import Detections

from source_app.Detectors.Detector import Detector
from source_app.Detectors.FactoryDetector import FactoryDetector
from source_app.utils.Config import Config
from source_app.utils.Drawer import draw_detections_with_count


@pytest.fixture
def detections() -> Detections:
	"""
	Fixture to create a sample Detections object for testing.
	"""
	# Create a sample Detections object with dummy data
	boxes = np.array([[10, 10, 50, 50], [60, 60, 100, 100]])
	scores = np.array([0.9, 0.8])
	class_ids = np.array([1, 2])
	return Detections(xyxy=boxes, confidence=scores, class_id=class_ids)


@pytest.fixture
def detector() -> Detector:
	"""
	Fixture to create a FactoryDetector instance for testing.
	"""
	return FactoryDetector.create_detector(
		Config.from_dict(
			{
				'Detectors': {
					'name': 'Detectron2',
					'device': 'cpu',
					'Detectron2': {
						'cfg': 'source_app/zoo/detectron2/faster_rcnn_R_50_FPN_3x.yaml',
						'weights': 'source_app/zoo/detectron2/model.pt',
						'filters': [2],  # Only detect cars
					},
				}
			}
		)
	)


@pytest.mark.manual
def test_draw_detections_with_count(detections: Detections) -> None:
	"""
	Test the draw_detections_with_count function with a sample image and detections.
	"""
	# Create a dummy image
	image = np.zeros((200, 200, 3), dtype=np.uint8)

	# Draw detections on the image
	annotated_image = draw_detections_with_count(image, detections)

	# Check if the annotated image is not None
	assert annotated_image is not None

	# save image to file for manual inspection
	cv2.imwrite('tests/drawer/test_image_1.jpg', annotated_image)


@pytest.mark.manual
def test_real_draw_detections_with_count(detector: Detector) -> None:
	"""
	Real test to verify the draw_detections_with_count function with actual image and detections.
	"""
	# Load a real image
	image = cv2.imread('tests/sample_image/image1.jpg')
	if image is None:
		raise FileNotFoundError('Test image not found')

	detections = detector(image)

	# Draw detections on the real image
	annotated_image = draw_detections_with_count(image, detections)

	# Save the annotated image for manual inspection
	cv2.imwrite('tests/drawer/test_image_2.jpg', annotated_image)
