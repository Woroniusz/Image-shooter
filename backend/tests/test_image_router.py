import numpy as np
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from source_app.api.routers.routers_loader import ImageRouter, resize_image
from source_app.utils.Config import Config


@pytest.fixture
def config() -> Config:
	return Config.from_dict({'api': {'title': 'Shooter', 'version': '0.1.0', 'ip': 'localhost', 'port': 5000}})


@pytest.fixture
def client(config: Config) -> TestClient:
	"""
	Fixture to create a FastAPI app with the ImageRouter included.
	"""
	app = FastAPI()
	image_router = ImageRouter(config)
	app.include_router(image_router.router)
	return TestClient(app)


def test_process_image_valid_image(client: TestClient) -> None:
	with open('tests/sample_image/image1.jpg', 'rb') as image_file:
		response = client.post(
			'/process-image',
			files={'file': ('image1.jpg', image_file, 'image/jpeg')},
		)

	assert response.status_code == 200
	assert response.headers['content-type'] == 'image/jpeg'


def test_process_image_invalid_file(client: TestClient) -> None:
	response = client.post(
		'/process-image',
		files={'file': ('sample_text.txt', b'This is not an image', 'text/plain')},
	)

	assert response.status_code == 400  # Unprocessable Entity
	assert 'Uploaded file is not an image' in response.json()['detail']


def test_process_image_missing_content_type(client: TestClient) -> None:
	response = client.post(
		'/process-image',
		files={'file': ('sample_image.jpg', b'fake_image_data')},
	)

	# Sprawdzenie odpowiedzi
	assert response.status_code == 400  # Unprocessable Entity
	assert 'Failed to decode image' in response.json()['detail']
