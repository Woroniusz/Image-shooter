import os

import uvicorn
from fastapi import FastAPI

from source_app.api.routers.routers_loader import ImageRouter
from source_app.Logger.logger import get_logger
from source_app.utils.Config import Config
from fastapi.middleware.cors import CORSMiddleware
from source_app.Detectors.FactoryDetector import FactoryDetector

# from source_app.api.routers.dynamic_router import dynamic_router

logger = get_logger(__name__)


def create_app(config: Config) -> FastAPI:
	app = FastAPI(
		title=config.api.title,
		version=config.api.version,
	)

	print(f'{config.api.cors.allow_origins=}')
	# Ustawienia CORS
	app.add_middleware(
		CORSMiddleware,
		allow_origins=config.api.cors.allow_origins,
		allow_credentials=True,
		allow_methods=['*'],
		allow_headers=['*'],
	)

	# Inicjalizacja detektorów
	detector = FactoryDetector.create_detector(config)

	# Dodajemy ImageRouter
	image_router: ImageRouter = ImageRouter(config, detector=detector)
	app.include_router(image_router.router)

	return app


if __name__ == '__main__':
	my_path = os.path.dirname(os.path.abspath(__file__))
	try:
		config = Config(path=f'{my_path}/../../config.toml')
	except Exception as e:
		logger.error(f'Error while loading configuration: {e}', exc_info=e)
		exit(1)

	app = create_app(config)

	uvicorn.run(app, host=config.api.ip, port=config.api.port, log_level='info')
