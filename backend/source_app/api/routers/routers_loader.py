import io

import cv2
import numpy as np
from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from source_app.utils.Config import Config


class ImageRouter:
	"""
	A router class for handling image upload and processing.
	"""

	def __init__(self, config: Config) -> None:
		self.router = APIRouter()
		self.config = config
		self.router.add_api_route('/process-image', self.process_image, methods=['POST'])

	async def process_image(self, file: UploadFile) -> StreamingResponse:
		# Open the uploaded image
		if not file.content_type or file.content_type == '' or not file.content_type.startswith('image/'):
			raise HTTPException(status_code=400, detail='Uploaded file is not an image')
		contents = await file.read()
		if not contents:
			raise HTTPException(status_code=400, detail='No content in the uploaded file')

		image = np.frombuffer(contents, np.uint8)
		image_code = cv2.imdecode(image, cv2.IMREAD_COLOR)
		if image_code is None:
			raise HTTPException(status_code=400, detail='Failed to decode image')

		buf = io.BytesIO(image_code.tobytes())

		# Return the processed image as a StreamingResponse
		return StreamingResponse(buf, media_type='image/jpeg')
