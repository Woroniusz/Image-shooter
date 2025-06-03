import cv2
import numpy as np
from supervision.annotators.core import BoxAnnotator
from supervision.detection.core import Detections


def draw_detections_with_count(image: np.ndarray, detections: Detections) -> np.ndarray:
	"""
	args:
		image (np.ndarray): The input image on which to draw the detections.
		detections (Detections): The detections to be drawn on the image.
	returns:
		np.ndarray: The image with detections drawn and the count of detections displayed.
	"""
	# check if the input image is a valid numpy array
	if not isinstance(image, np.ndarray):
		raise ValueError('Input image must be a numpy array')

	# copy the image to avoid modifying the original
	annotated = image.copy()

	# draw the detections on the image
	box_annotator = BoxAnnotator(thickness=2)
	annotated = box_annotator.annotate(scene=annotated, detections=detections)

	# count the number of detections
	count = len(detections)

	text = f'number of detections {count}'
	font = cv2.FONT_HERSHEY_SIMPLEX
	font_scale = 1.0
	font_thickness = 2

	(text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, font_thickness)
	margin = 10

	x = annotated.shape[1] - text_width - margin
	y = text_height + margin

	bg_x1 = x - margin // 2
	bg_y1 = margin // 2
	bg_x2 = x + text_width + margin // 2
	bg_y2 = margin // 2 + text_height + margin // 2 + 4

	# draw a filled rectangle behind the text for better visibility
	cv2.rectangle(annotated, (bg_x1, bg_y1), (bg_x2, bg_y2), (0, 0, 0), thickness=-1)

	cv2.putText(annotated, text, (x, y), font, font_scale, (255, 255, 255), font_thickness, lineType=cv2.LINE_AA)

	return annotated  # type: ignore
