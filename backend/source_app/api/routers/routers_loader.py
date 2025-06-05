import io

import cv2
import numpy as np
from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from supervision.detection.core import Detections
from source_app.Detectors.Detector import Detector
from source_app.utils.Drawer import draw_detections_with_count

from source_app.utils.Config import Config


def resize_image(img: np.ndarray, max_dim: int = 65500) -> np.ndarray:
	"""
	Resize the image if its dimensions exceed the maximum allowed size.
	"""
	h, w = img.shape[:2]
	if max(h, w) > max_dim:
		scale = max_dim / max(h, w)
		new_w = int(w * scale)
		new_h = int(h * scale)
		img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
	return img


class ImageRouter:
	"""
	A router class for handling image upload and processing.
	"""

	def __init__(self, config: Config, detector: Detector | None = None) -> None:
		self.router = APIRouter()
		self.config: Config = config
		self.detector: Detector | None = detector
		self.router.add_api_route('/process-image', self.process_image, methods=['POST'])

	async def process_image(self, file: UploadFile) -> StreamingResponse:
		if not file.content_type or not file.content_type.startswith('image/'):
			raise HTTPException(status_code=400, detail='Uploaded file is not an image')

		contents = await file.read()
		if not contents:
			raise HTTPException(status_code=400, detail='No content in the uploaded file')

		nparr = np.frombuffer(contents, np.uint8)
		img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
		if img is None:
			raise HTTPException(status_code=400, detail='Failed to decode image')

		img = resize_image(img)

		if self.detector:
			try:
				result: Detections = self.detector(img)
				img = draw_detections_with_count(img, result)
			except Exception as e:
				raise HTTPException(status_code=500, detail=f'Error during detection: {e}')

		try:
			success, encoded = cv2.imencode('.jpg', img)
		except cv2.error as e:
			raise HTTPException(status_code=500, detail=f'Failed to encode image: {e}')  # noqa: E261

		if not success:
			raise HTTPException(status_code=500, detail='Failed to encode image as JPEG')

		buf = io.BytesIO(encoded.tobytes())
		buf.seek(0)
		return StreamingResponse(buf, media_type='image/jpeg')
