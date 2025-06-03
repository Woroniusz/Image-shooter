import os

import uvicorn
from fastapi import FastAPI

from source_app.api.routers.routers_loader import ImageRouter
from source_app.Logger.logger import get_logger
from source_app.utils.Config import Config

# from source_app.api.routers.dynamic_router import dynamic_router

logger = get_logger(__name__)


def create_app(config: Config) -> FastAPI:
	app = FastAPI(
		title=config.api.title,
		version=config.api.version,
	)

	# Dodajemy ImageRouter
	image_router: ImageRouter = ImageRouter(config)
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
